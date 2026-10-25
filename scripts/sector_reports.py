"""Readable sector report exports, with no external browser resources."""
from html import escape
import json
from price_setups import STATE_LABELS


def percent(value):
    return '缺数据' if value is None else f'{value*100:+.2f}%'


def numeric(value):
    return '—' if value is None else f'{value:,.4f}'.rstrip('0').rstrip('.')


def tag(result):
    return '模拟练习数据' if result['data_kind']=='synthetic' else '导入观测，来源与版本由使用者核对'


def text(value):
    return escape(str(value),quote=True)


STYLE='''*{box-sizing:border-box}body{margin:0;background:#0a111b;color:#dfe8f5;font:15px/1.7 system-ui,"Microsoft YaHei",sans-serif}main{max-width:1260px;margin:auto;padding:30px 20px}h1{font-size:clamp(28px,5vw,40px);margin:12px 0}h2{font-size:22px}a{color:#79dfc6}p,.muted{color:#a8b7ca}.tag{font:12px monospace;color:#79dfc6;letter-spacing:2px}.summary{display:flex;gap:16px;flex-wrap:wrap;margin:22px 0}.summary article,section,details{padding:20px;background:#121e2d;border:1px solid #2b3c53;border-radius:10px;margin-bottom:18px}.summary article{flex:1;min-width:180px}.summary strong{display:block;font-size:30px}.scroll{overflow:auto}table{border-collapse:collapse;width:100%;white-space:nowrap}th,td{padding:11px 12px;border-bottom:1px solid #29394e;text-align:left}th{color:#a8b7ca;font-size:13px}tbody tr:hover{background:#192b3c}.positive{color:#79dfc6}.negative{color:#ef9b97}.thin{color:#a8b7ca}.bar{display:inline-block;vertical-align:middle;height:7px;border-radius:4px;margin-right:8px}.up{background:#79dfc6}.down{background:#ef9b97}input,select{background:#101c2b;border:1px solid #40556e;border-radius:7px;color:#e6eef8;padding:10px;margin:4px 10px 12px 0;max-width:100%}pre{white-space:pre-wrap;overflow-wrap:anywhere;font-size:12px;max-height:600px;overflow:auto}li{margin:7px 0}.pill{display:inline-block;margin:4px;padding:6px 12px;border:1px solid #39516d;border-radius:6px}footer{color:#a8b7ca;margin:22px 0;font-size:13px}[hidden]{display:none!important}@media print{body{background:white;color:#111}main{max-width:none}section,.summary article,details{background:white;border:1px solid #bbb}a,p,.muted,th,footer{color:#333}input,select,details{display:none}.scroll{overflow:visible}table{white-space:normal;font-size:10px}}'''

MA_LABELS={'ascending':'向上排列','descending':'向下排列','mixed_or_flat':'交织或走平','insufficient_history':'历史不足'}
BOUNDARY_LABELS={'closed_below_support':'收盘跌破支撑','reclaimed_after_closed_break':'跌破后的收盘已收回支撑',
                 'wick_below_then_close_at_or_above':'影线穿过支撑，收盘未破','above_support_no_reclaim_pattern':'位于支撑上方，未出现本规则的收回形态',
                 'closed_above_resistance':'收盘突破压力','rejected_after_closed_break':'突破后收盘跌回压力下方',
                 'wick_above_then_close_at_or_below':'影线穿过压力，收盘未突破','below_resistance_no_rejection_pattern':'位于压力下方，未出现本规则的跌回形态'}
CURVE_LABELS={'contango':'远月逐段高于近月','backwardation':'近月逐段高于远月','flat':'各月价格相同','mixed':'曲线有拐点'}


def page(title,body,result,nav=''):
    policy=result.get('sources',{}).get('panel',{}).get('vintage_policy')
    note='<p>使用本次取数时可见的历史版本，逐行可用时间记录为取数时间；不能据此还原过去当时知道的信息。</p>' if policy=='retrieval_snapshot' else ''
    return f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{text(title)}</title><style>{STYLE}</style><main><header><div class="tag">涛涛的期货研究 / 板块分析</div><h1>{text(title)}</h1><p>{text(tag(result))} · 交易日 {text(result['trade_date'])} · 截止 {text(result['as_of_utc'])}</p>{note}{nav}</header>{body}<footer>各板块采用本次配置的代表品种；表内涨跌幅是同一合约的价格变化。产业数据按公布时间筛选，原始文件与哈希随报告保存。</footer></main></html>'''


def overview_html(result):
    contracts={item['symbol']:item['contract'] for item in result['products']}
    options=''.join(f'<option value="{text(key)}">{text(value["label"])}：{text(value["start_date"])} → {text(result["trade_date"])}</option>' for key,value in result['windows'].items())
    nav='<a href="REPORT.md">文字报告</a> · <a href="bundle.json">计算明细</a> · <a href="sector_returns.csv">板块 CSV</a>'
    body=f'''<div class="summary"><article><span>本次选定板块</span><strong>{result['configured_sector_count']}</strong></article><article><span>配置的代表品种</span><strong>{result['configured_product_count']}</strong></article><article><span>产业数据记录</span><strong>{sum(len(board['evidence']) for board in result['sectors'])}</strong></article></div><section><h2>板块比较</h2><p>区间相同，品种和权重按配置选取。覆盖率达到 {result['minimum_sector_coverage']*100:g}% 才列排名。即便样本齐全，也不代表覆盖了板块内所有合约。</p><label for="window">比较区间</label> <select id="window">{options}</select><label for="search">筛选板块或代码</label> <input id="search" type="search" placeholder="例如：黑色、AU、EC">'''
    for index,(key,window) in enumerate(result['windows'].items()):
        boards=sorted([board for board in result['sectors'] if board['symbols']],key=lambda board:(board['windows'][key]['rank'] is None,board['windows'][key]['rank'] or 0,board['id']))
        max_value=max([abs(board['windows'][key]['sample_equal_weight_price_return'] or 0) for board in boards]+[.00001])
        rows=[]
        for board in boards:
            value=board['windows'][key]
            change=value['sample_equal_weight_price_return']
            css='thin' if change is None else 'positive' if change>=0 else 'negative'
            width=0 if change is None else 75*abs(change)/max_value
            bar=f'<span class="bar {"up" if (change or 0)>=0 else "down"}" style="width:{width:.1f}px"></span>'
            rank='未排名' if value['rank'] is None else str(value['rank'])
            selected=', '.join(symbol+' ('+contracts[symbol]+')' for symbol in board['symbols'])
            rows.append(f'<tr class="board"><td>{text(rank)}</td><td><a href="sectors/{text(board["id"])}.html">{text(board["name"])}</a></td><td class="{css}">{bar}{percent(change)}</td><td>{value["observed_products"]}/{value["expected_products"]} ({value["coverage"]*100:.0f}%)</td><td>{value["advancing"]}/{value["declining"]}/{value["unchanged"]}</td><td>{text(selected)}</td></tr>')
        body+=f'<div class="scroll" data-window="{text(key)}"'+(' hidden' if index else '')+'><table><thead><tr><th>区间排名</th><th>板块</th><th>样本等权价格变化</th><th>覆盖</th><th>涨/跌/平</th><th>代表品种与合约</th></tr></thead><tbody>'+''.join(rows)+'</tbody></table></div>'
    body+='</section><section><h2>先查数据缺口</h2><ul>'
    warnings=[f"{item['symbol']}：{alert}" for item in result['products'] for alert in item['attention']]
    unverified=sum(item.get('bars_without_available_at',0) for item in result['products'])
    if result['data_kind']=='imported_observations' and unverified:
        warnings.append(f'{unverified} 根价格观测未提供 available_at；仅按收盘时刻筛选，历史版本需另核对。')
    if not warnings:
        warnings=['本次未触发日线陈旧或缺失检查。来源真实性、交易日历与交割规则仍按目标市场核对。']
    body+=''.join('<li>'+text(value)+'</li>' for value in warnings)+'</ul></section>'
    body+='''<script>const selector=document.getElementById('window'),search=document.getElementById('search');function refresh(){document.querySelectorAll('[data-window]').forEach(table=>{table.hidden=table.dataset.window!==selector.value;table.querySelectorAll('tr.board').forEach(row=>{row.hidden=!row.textContent.toLowerCase().includes(search.value.toLowerCase())})})}selector.addEventListener('change',refresh);search.addEventListener('input',refresh);</script>'''
    return page('按板块看期货',body,result,nav)


def sector_html(board,result):
    members=[item for item in result['products'] if item['sector']==board['id']]
    body='<section><h2>先查这些资料</h2><ul>'+''.join('<li>'+text(item)+'</li>' for item in board['drivers'])+'</ul><h2>下一次检查</h2><ul>'+''.join('<li>'+text(item)+'</li>' for item in board['next_checks'])+'</ul></section>'
    window_names=list(result['windows'])
    body+='<section><h2>品种比较</h2><div class="scroll"><table><thead><tr><th>品种 / 固定合约</th><th>收盘 / 单位</th>'+''.join('<th>'+text(result['windows'][key]['label'])+'</th>' for key in window_names)+'<th>ATR14</th><th>较前次观测增仓</th><th>前次观测日</th><th>量/前5根均量</th></tr></thead><tbody>'
    for item in members:
        body+=f'<tr><td>{text(item["symbol"])} / {text(item["contract"])}</td><td>{numeric(item["latest_close"])} / {text(item["unit"])}</td>'+''.join('<td>'+percent(item['windows'][key]['price_return'])+'</td>' for key in window_names)+f'<td>{numeric(item["atr14_simple"])}</td><td>{numeric(item["flow"]["open_interest_change"])}</td><td>{text(item["flow"].get("previous_observation_trade_date") or "—")}</td><td>{numeric(item["flow"]["volume_vs_prior5_mean"])}</td></tr>'
    body+='</tbody></table></div><p>增仓与前一条有效日线比较，表中保留其交易日；缺日线时，差值可能跨多日。量比采用之前5条观测。量仓是手数，不据此确定谁在加多或加空。</p></section>'
    body+='<section><h2>截止时刻已公布的产业数据</h2>'
    if not board['evidence']:
        body+='<p>本次没有导入这个板块的产业数据。价格表现之外的解释需要补资料。</p>'
    else:
        for item in board['evidence']:
            body+=f'<p><strong>{text(item["metric"])}</strong>：{numeric(item["value"])} {text(item["unit"])}<br>观测 {text(item["observed_at"])}；公布 {text(item["published_at"])}<br>来源：{text(item["source"])}</p>'
    body+='</section><section><h2>多周期与关键位</h2>'
    for item in members:
        body+='<h3>'+text(item['symbol'])+'</h3>'
        if not item['structures']:
            body+='<p>未提供价格结构数据。</p>'
        for frame,value in sorted(item['structures'].items()):
            macd=value['macd']
            momentum=({'positive':'正柱','negative':'负柱','zero':'零柱'}[macd['sign']]+' / '+{'expanding':'绝对值扩张','shrinking':'绝对值缩小','unchanged':'绝对值未变'}[macd['absolute_magnitude']]) if macd['ready'] else '历史不足'
            body+=f'<p>{text(frame)}：均线{text(MA_LABELS[value["ma_ordering"]])}；MACD {text(momentum)}；末根 {text(value["latest_completed_bar"]["close_time"])}</p>'
            for boundary,observation in value['boundary_observations'].items():
                body+='<p>'+('支撑' if boundary=='support' else '压力')+' '+numeric(observation['level'])+'：'+text(BOUNDARY_LABELS[observation['observation']])+'。</p>'
            if value['reference_window']:
                reference=value['reference_window']
                state={None:'未设置验证期限','expired':'已过期','due_now':'正好到期','within_window':'窗口内'}[reference['window_state']]
                window='未设置' if reference['window_bars'] is None else str(reference['window_bars'])+' 根'
                body+='<p>参照后已收盘 '+str(reference['completed_bars_after_reference'])+' 根；窗口 '+window+'；'+state+'。</p>'
    body+='</section>'
    events={'boundary_reclaimed':'收盘回到边界内','later_retest_held':'后续测试守住边界','structure_invalidated':'结构触及失效位'}
    for item in members:
        for setup in item.get('setups',[]):
            body+='<section><h2>'+text(item['symbol'])+'：'+text(setup['name'])+'</h2><p>'+text(STATE_LABELS[setup['state']])+'</p>'
            body+='<p>声明 '+text(setup['declared_at'])+'；参照 '+text(setup['anchor_time'])+'；验证 '+str(setup['validation_bars'])+' 根 '+text(setup['timeframe'])+'。边界 '+numeric(setup['level'])+'，失效位 '+numeric(setup['invalidation_level'])+'。</p><ul>'
            body+=''.join('<li>'+text(events[event['event']])+'：'+text(event['close_time'])+'，参照后第 '+str(event['bars_after_anchor'])+' 根。</li>' for event in setup['observed_events'])+'</ul><p>这些是按预先填写条件得到的观察，不代表已验证的交易优势或保证止损成交。</p></section>'
    for curve in result['curves']:
        if any(item['symbol']==curve['symbol'] for item in members):
            body+='<section><h2>'+text(curve['symbol'])+' 跨月快照</h2><p>'+text(CURVE_LABELS[curve['shape']])+'；近月−远月 '+numeric(curve['near_minus_far'])+' '+text(curve['unit'])+'；报价跨度 '+numeric(curve['quote_span_seconds'])+' 秒；最旧报价距截止 '+numeric(curve['oldest_quote_age_hours'])+' 小时</p><pre>'+text(json.dumps(curve['quotes'],ensure_ascii=False,indent=2))+'</pre></section>'
    body+='<details><summary>本板块的完整计算</summary><pre>'+text(json.dumps({'sector':board,'products':members},ensure_ascii=False,indent=2))+'</pre></details>'
    return page(board['name'],body,result,'<a href="../index.html">← 返回板块总览</a> · <a href="../bundle.json">JSON</a>')


def markdown(result):
    lines=['# 涛涛的期货研究：板块报告','',f"{tag(result)}。交易日 {result['trade_date']}，截止 {result['as_of_utc']}。",'',
           f"本次配置 {result['configured_product_count']} 个代表品种；板块排名覆盖率门槛 {result['minimum_sector_coverage']*100:g}%。",'']
    for key,window in result['windows'].items():
        lines += ['## '+window['label']+'：'+window['start_date']+' → '+result['trade_date'],'','| 板块 | 排名 | 样本等权价格变化 | 覆盖 | 涨/跌/平 |','|---|---:|---:|---|---|']
        boards=sorted([board for board in result['sectors'] if board['symbols']],key=lambda board:(board['windows'][key]['rank'] is None,board['windows'][key]['rank'] or 0,board['id']))
        for board in boards:
            value=board['windows'][key]
            label=board['name'].replace('|','\\|').replace('\n',' ')
            lines.append(f"| {label} | {value['rank'] if value['rank'] is not None else '未排名'} | {percent(value['sample_equal_weight_price_return'])} | {value['observed_products']}/{value['expected_products']} | {value['advancing']}/{value['declining']}/{value['unchanged']} |")
    lines+=['','## 逐板块检查','']
    for board in result['sectors']:
        if not board['symbols']:
            continue
        lines += ['### '+board['name'],'','代表品种：'+(', '.join(board['symbols']) or '本次未配置')+'。','']
        lines += ['- '+value for value in board['drivers']]
        lines += ['- 下次检查：'+value for value in board['next_checks']]
        if not board['evidence']:
            lines+=['- 产业数据：本次未导入，需要补资料。']
        else:
            lines+=['- 产业数据：'+value['metric']+'='+str(value['value'])+' '+value['unit']+'；公布于 '+value['published_at'] for value in board['evidence']]
    lines+=['','## 读数口径','','比较使用固定合约和共同起止日期。样本等权涨跌幅不是官方指数，也没有计入杠杆、交易成本和换月收益。覆盖率只相对本次配置的代表品种计算。','',
            '[浏览器总览](index.html) · [完整计算](bundle.json) · [板块表](sector_returns.csv) · [品种表](products.csv) · [输入文件](inputs/)','']
    return '\n'.join(lines)
