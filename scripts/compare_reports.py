#!/usr/bin/env python3
"""Review two verified sector snapshots using comparable explicit contracts."""
import argparse
from datetime import datetime,timezone
import json
from pathlib import Path
import uuid

from bundle_integrity import verify,digest
from market_io import timestamp
from price_setups import STATE_LABELS

REASONS={None:'—','added_or_removed_product':'样本新增或移除','contract_or_quote_identity_changed':'合约或报价口径改变',
         'missing_snapshot_endpoint':'缺少端点价格','stale_endpoint':'端点过旧','nonpositive_start_price':'起点价格非正',
         'window_anchor_changed':'窗口起点变化','sector_members_changed':'板块样本变化','contract_identity_changed':'合约变化',
         'coverage_policy_changed':'覆盖门槛变化','incomplete_samples':'样本不完整','staleness_policy_missing':'缺少陈旧判断口径'}


def compare(before,after):
    if before['data_kind']!=after['data_kind']:
        raise ValueError('do not mix synthetic and imported snapshots in one review')
    if before['catalog_sha256']!=after['catalog_sha256']:
        raise ValueError('catalog taxonomy changed; reconcile it before comparison')
    if timestamp(before['as_of_utc'])>=timestamp(after['as_of_utc']) or before['trade_date']>=after['trade_date']:
        raise ValueError('review requires a later cutoff and a later trading date')
    old={item['symbol']:item for item in before['products']}
    new={item['symbol']:item for item in after['products']}
    products=[]
    for symbol in sorted(set(old)|set(new)):
        a,b=old.get(symbol),new.get(symbol)
        reason=None
        if a is None or b is None:
            reason='added_or_removed_product'
        elif any(a[key]!=b[key] for key in ('contract','currency','unit','exchange','sector')):
            reason='contract_or_quote_identity_changed'
        elif a['latest_close'] is None or b['latest_close'] is None:
            reason='missing_snapshot_endpoint'
        elif 'max_bar_age_hours' not in before or 'max_bar_age_hours' not in after:
            reason='staleness_policy_missing'
        elif a['quote_age_hours']>before['max_bar_age_hours'] or b['quote_age_hours']>after['max_bar_age_hours']:
            reason='stale_endpoint'
        elif a['latest_close']<=0:
            reason='nonpositive_start_price'
        products.append({'symbol':symbol,'sector':(b or a)['sector'],'before_contract':None if a is None else a['contract'],
                         'after_contract':None if b is None else b['contract'],'before_close':None if a is None else a['latest_close'],
                         'after_close':None if b is None else b['latest_close'],
                         'matched_price_change':None if reason else b['latest_close']/a['latest_close']-1,
                         'unavailable_reason':reason,'before_attention':[] if a is None else a['attention'],'after_attention':[] if b is None else b['attention']})
        products[-1]['before_setups']=[] if a is None else a.get('setups',[])
        products[-1]['after_setups']=[] if b is None else b.get('setups',[])
        earlier={plan['name']:plan for plan in products[-1]['before_setups']}
        later={plan['name']:plan for plan in products[-1]['after_setups']}
        parameters=('timeframe','side','declared_at','anchor_time','level','invalidation_level','retest_tolerance','validation_bars')
        products[-1]['rule_changes']=[{'name':name,'change':'added_or_removed_rule' if name not in earlier or name not in later else 'rule_parameters_changed'}
                                     for name in sorted(set(earlier)|set(later))
                                     if name not in earlier or name not in later or any(earlier[name][key]!=later[name][key] for key in parameters)]
    old_boards={board['id']:board for board in before['sectors']}
    windows=[]
    for board in after['sectors']:
        previous=old_boards.get(board['id'])
        for key,window in after['windows'].items():
            reason=None
            if key not in before['windows'] or before['windows'][key]['start_date']!=window['start_date']:
                reason='window_anchor_changed'
            elif previous is None or sorted(previous['symbols'])!=sorted(board['symbols']):
                reason='sector_members_changed'
            elif any(item['unavailable_reason']=='contract_or_quote_identity_changed' for item in products if item['symbol'] in board['symbols']):
                reason='contract_identity_changed'
            elif before['minimum_sector_coverage']!=after['minimum_sector_coverage']:
                reason='coverage_policy_changed'
            else:
                a,b=previous['windows'][key],board['windows'][key]
                if a['coverage']!=1 or b['coverage']!=1:
                    reason='incomplete_samples'
            windows.append({'sector':board['id'],'window':key,'unavailable_reason':reason,
                            'before_rank':None if reason else previous['windows'][key]['rank'],
                            'after_rank':None if reason else board['windows'][key]['rank'],
                            'interpretation':'same anchored window with a later endpoint; price observation, not predictive performance'})
    return {'schema_version':1,'data_kind':after['data_kind'],'before_trade_date':before['trade_date'],'after_trade_date':after['trade_date'],
            'before_as_of':before['as_of_utc'],'after_as_of':after['as_of_utc'],'products':products,'anchored_rank_comparisons':windows,
            'scope':'Matched-contract snapshot review only; not traded P&L, strategy backtest or causal attribution.'}


def run(before_dir,after_dir,output):
    before_dir,after_dir=Path(before_dir),Path(after_dir)
    verify(before_dir)
    verify(after_dir)
    snapshots=[]
    input_hashes={}
    for label,directory in [('before',before_dir),('after',after_dir)]:
        raw=(directory/'bundle.json').read_bytes()
        data=json.loads(raw)
        config=json.loads((directory/'config.snapshot.json').read_text(encoding='utf-8'))
        data.setdefault('max_bar_age_hours',config['max_bar_age_hours'])
        snapshots.append(data)
        input_hashes[label]=digest(raw)
    result=compare(*snapshots)
    result['input_bundle_sha256']=input_hashes
    result['generated_at_utc']=datetime.now(timezone.utc).isoformat()
    root=Path(output)/('review-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')+'-'+uuid.uuid4().hex[:8])
    root.mkdir(parents=True,exist_ok=False)
    lines=['# 两次期货研究记录对照','',f"{result['data_kind']}；{result['before_trade_date']} → {result['after_trade_date']}",'',
           '| 品种 | 前次合约 | 本次合约 | 固定合约价格变化 | 不可比较原因 |','|---|---|---|---:|---|']
    for item in result['products']:
        value=item['matched_price_change']
        label='—' if value is None else f'{value*100:+.4f}%'
        cells=[item['symbol'],item['before_contract'] or '—',item['after_contract'] or '—',label,REASONS[item['unavailable_reason']]]
        lines.append('| '+' | '.join(str(value).replace('|','\\|').replace('\n',' ') for value in cells)+' |')
    lines += ['','## 固定锚点区间的观察排名','','| 板块 / 窗口 | 前次 | 本次 | 不可比较原因 |','|---|---:|---:|---|']
    # Names are presentation only; stable identifiers remain in the JSON.
    names={board['id']:board['name'] for board in snapshots[1]['sectors']}
    for item in result['anchored_rank_comparisons']:
        lines.append('| '+names.get(item['sector'],item['sector'])+' / '+item['window']+' | '+str(item['before_rank'] or '—')+' | '+str(item['after_rank'] or '—')+' | '+REASONS[item['unavailable_reason']]+' |')
    lines += ['','## 事先声明的结构条件','']
    for item in result['products']:
        if item['before_setups'] or item['after_setups']:
            lines.append('### '+item['symbol'])
            for change in item['rule_changes']:
                lines.append('- 条件变更：'+change['name']+'。新增、移除或修改过条件，分别解释两次观察，不把它们当同一套原计划。')
            for label,plans in [('前次',item['before_setups']),('本次',item['after_setups'])]:
                for plan in plans:
                    lines.append('- '+label+'：'+plan['name']+'；'+STATE_LABELS[plan['state']]+'；声明 '+plan['declared_at']+'；参照 '+plan['anchor_time'])
    lines += ['','窗口起点、样本或合约变化时，不直接比较旧排名。具体原因见 JSON。这里比较价格快照；实际执行、费用和盈亏需用成交记录另算。','']
    (root/'REVIEW.md').write_text('\n'.join(lines),encoding='utf-8',newline='\n')
    (root/'review.json').write_text(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8',newline='\n')
    return root


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--before',type=Path,required=True)
    parser.add_argument('--after',type=Path,required=True)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    try:
        root=run(args.before,args.after,args.out)
    except (ValueError,OSError,KeyError,TypeError) as exc:
        parser.exit(2,f'ERROR: {exc}\n')
    print(f'PASS / snapshot review -> {root / "REVIEW.md"}')


if __name__=='__main__':
    main()
