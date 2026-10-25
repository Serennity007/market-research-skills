#!/usr/bin/env python3
"""Fetch bounded explicit-contract daily snapshots; normal report generation stays offline."""
import argparse
import csv
from datetime import datetime,time,timezone,timedelta
import hashlib
import io
import json
from pathlib import Path
import re
from urllib.parse import urlencode,urlparse
from urllib.request import Request,urlopen
import uuid

from market_io import number
from sector_engine import iso_day

ENDPOINT='https://stock2.finance.sina.com.cn/futures/api/jsonp.php/var%20_taotao=/InnerFuturesNewService.getDailyKLine'
MAX_BYTES=4_000_000
CHINA=timezone(timedelta(hours=8))
FIELDS=['symbol','contract','timeframe','trade_date','close_time','available_at','open','high','low','close','volume','open_interest','currency','unit']


def now():
    return datetime.now(timezone.utc)


def download(contract):
    url=ENDPOINT+'?'+urlencode({'symbol':contract})
    request=Request(url,headers={'User-Agent':'Mozilla/5.0 (compatible; TaotaoFuturesResearch/2.1)',
                                 'Referer':'https://finance.sina.com.cn/'})
    with urlopen(request,timeout=15) as response:
        if urlparse(response.geturl()).hostname!='stock2.finance.sina.com.cn' or urlparse(response.geturl()).scheme!='https':
            raise ValueError('unexpected quote-provider redirect')
        raw=response.read(MAX_BYTES+1)
        if len(raw)>MAX_BYTES:
            raise ValueError('provider response exceeds maximum size')
        if response.status!=200:
            raise ValueError(f'provider HTTP status {response.status}')
    return raw,url


def parse(raw):
    if len(raw)>MAX_BYTES:
        raise ValueError('oversized quote response')
    text=raw.decode('gb18030')
    match=re.fullmatch(r'\s*(?:/\*.*?\*/\s*)?var\s+_taotao\s*=\s*\(\s*(\[.*\])\s*\)\s*;?\s*',text,re.S)
    if not match:
        raise ValueError('unexpected provider payload; no script evaluation is supported')
    rows=json.loads(match.group(1))
    if not isinstance(rows,list) or not rows:
        raise ValueError('provider returned no daily observations')
    return rows


def validate_request(request,catalog):
    if request.get('schema_version')!=1 or not 1<=len(request.get('contracts',[]))<=6:
        raise ValueError('declare 1 to 6 explicit contracts per request')
    seen=set()
    for item in request['contracts']:
        symbol=item['symbol']
        contract=item['contract']
        if symbol not in catalog['products'] or symbol in seen:
            raise ValueError('select unique catalog products')
        seen.add(symbol)
        if not re.fullmatch(re.escape(symbol)+r'\d{3,4}',contract) or not 1<=int(contract[-2:])<=12:
            raise ValueError('use a dated explicit contract; main/continuous symbols are rejected')
        if not re.fullmatch(r'[A-Z]{3}',item['currency']) or not item['unit'].strip():
            raise ValueError('declare the real quote currency and unit')
        close=time.fromisoformat(item['session_close'])
        if close.utcoffset()!=timedelta(hours=8):
            raise ValueError('declare the exchange session close with +08:00 timezone')
    if type(request['max_bar_age_hours']) not in (int,float):
        raise ValueError('max_bar_age_hours must be a JSON number')
    number(request['max_bar_age_hours'],positive=True)


def convert(rows,item,product,retrieved):
    output,excluded=[],[]
    local_day=retrieved.astimezone(CHINA).date()
    seen=set()
    for raw in rows:
        day=iso_day(raw['d'])
        if day>=local_day:
            excluded.append({'date':raw['d'],'reason':'retrieval_day_or_later_is_not_used'})
            continue
        if day in seen:
            raise ValueError('provider has duplicate daily dates')
        seen.add(day)
        prices={field:number(raw[key]) for field,key in [('open','o'),('high','h'),('low','l'),('close','c')]}
        volume=number(raw['v'])
        interest=number(raw['p'])
        if min(volume,interest)<0 or not volume.is_integer() or not interest.is_integer():
            raise ValueError('provider volume/interest are not whole nonnegative counts')
        if volume==0 and all(value==0 for value in prices.values()):
            excluded.append({'date':raw['d'],'reason':'zero_volume_zero_ohlc_placeholder'})
            continue
        if not product.get('allow_signed',False) and min(prices.values())<=0:
            raise ValueError('provider supplied nonpositive prices for a positive-price product')
        if prices['high']<max(prices.values()) or prices['low']>min(prices.values()):
            raise ValueError('provider OHLC bounds are inconsistent')
        closing=datetime.fromisoformat(raw['d']+'T'+item['session_close'])
        output.append({'symbol':item['symbol'],'contract':item['contract'],'timeframe':'D1','trade_date':raw['d'],
                       'close_time':closing.isoformat(),'available_at':retrieved.isoformat(),**prices,
                       'volume':int(volume),'open_interest':int(interest),'currency':item['currency'],'unit':item['unit']})
    if not output:
        raise ValueError('no completed prior-date observations after filtering')
    output.sort(key=lambda row:row['trade_date'])
    return output,excluded


def fetch(request_path,output,downloader=download,clock=now):
    request_path=Path(request_path).resolve()
    request_raw=request_path.read_bytes()
    request=json.loads(request_raw.decode('utf-8-sig'))
    catalog_raw=(request_path.parent/request['catalog']).read_bytes()
    catalog=json.loads(catalog_raw.decode('utf-8-sig'))
    validate_request(request,catalog)
    root=Path(output)/('sina-'+clock().strftime('%Y%m%dT%H%M%S%fZ')+'-'+uuid.uuid4().hex[:8])
    root.mkdir(parents=True,exist_ok=False)
    (root/'raw').mkdir()
    sources=[]
    all_rows=[]
    try:
        for item in request['contracts']:
            response,url=downloader(item['contract'])
            retrieved=clock()
            if retrieved.tzinfo is None or retrieved.utcoffset() is None:
                raise ValueError('retrieval clock must include timezone')
            (root/'raw'/(item['contract']+'.jsonp.txt')).write_bytes(response)
            rows,excluded=convert(parse(response),item,catalog['products'][item['symbol']],retrieved)
            all_rows.extend(rows)
            sources.append({'symbol':item['symbol'],'contract':item['contract'],'url':url,'retrieved_at':retrieved.isoformat(),
                            'raw_file':'raw/'+item['contract']+'.jsonp.txt','raw_sha256':hashlib.sha256(response).hexdigest(),
                            'accepted_rows':len(rows),'first_date':rows[0]['trade_date'],'last_date':rows[-1]['trade_date'],
                            'excluded_rows':excluded,'session_close_declared':item['session_close']})
        sets=[{row['trade_date'] for row in all_rows if row['symbol']==item['symbol']} for item in request['contracts']]
        common=sorted(set.intersection(*sets))
        if len(common)<21:
            raise ValueError('need at least 21 common dates across all selected contracts')
        latest=common[-1]
        # Never include rows after the chosen common terminal date, even if one contract is newer.
        trimmed=[row for row in all_rows if row['trade_date']<=latest]
        text=io.StringIO()
        writer=csv.DictWriter(text,fieldnames=FIELDS,lineterminator='\n')
        writer.writeheader()
        writer.writerows(trimmed)
        panel=text.getvalue().encode('utf-8')
        (root/'panel.csv').write_bytes(panel)
        (root/'catalog.json').write_bytes(catalog_raw)
        (root/'request.snapshot.json').write_bytes(request_raw)
        finished=clock()
        if finished<max(datetime.fromisoformat(item['retrieved_at']) for item in sources):
            raise ValueError('retrieval clock moved backwards')
        policy='retrieval_snapshot'
        time_policy='取数时可见的历史版本；日期配合使用者声明的日收盘时刻，排除取数当日；available_at记录取数时间。'
        config={'schema_version':1,'data_kind':'imported_observations','as_of':finished.isoformat(),'trade_date':latest,
                'minimum_sector_coverage':1.0,'max_bar_age_hours':request['max_bar_age_hours'],'catalog':'catalog.json',
                'files':{'panel':'panel.csv'},'windows':{'day':{'label':'最近共同观测区间','start_date':common[-2]},
                                                     'week':{'label':'共同5段观测区间','start_date':common[-6]},
                                                     'month':{'label':'共同20段观测区间','start_date':common[-21]}},
                'universe':[{key:item[key] for key in ('symbol','contract','currency','unit')}|{'volume_unit':'contracts'} for item in request['contracts']],
                'sources':{'panel':{'name':'Sina explicit-contract daily snapshot','retrieved_at':finished.isoformat(),
                                    'vintage_policy':policy,'time_policy':time_policy,'contracts':sources}}}
        (root/'config.json').write_text(json.dumps(config,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
        manifest={'status':'complete','data_kind':'imported_observations','generated_at_utc':finished.isoformat(),
                  'common_trade_date':latest,'common_date_count':len(common),'panel_sha256':hashlib.sha256(panel).hexdigest(),
                  'catalog_sha256':hashlib.sha256(catalog_raw).hexdigest(),'request_sha256':hashlib.sha256(request_raw).hexdigest(),
                  'config_sha256':hashlib.sha256((root/'config.json').read_bytes()).hexdigest(),
                  'sources':sources,'vintage_policy':policy,'time_policy':time_policy}
        (root/'SOURCE_COMPLETE.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    except (ValueError,OSError,KeyError,TypeError) as exc:
        (root/'FAILURE.json').write_text(json.dumps({'status':'failed','error':str(exc),'completed_sources':sources},ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
        raise
    return root


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--request',type=Path,required=True)
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--analyze',action='store_true',help='also generate a verified sector report from the downloaded snapshot')
    args=parser.parse_args()
    try:
        root=fetch(args.request,args.out)
        report=None
        if args.analyze:
            from run_sectors import run
            report=run(root/'config.json',Path(args.out)/'reports')
    except (ValueError,OSError,KeyError,TypeError) as exc:
        parser.exit(2,f'ERROR: {exc}\n')
    print(f'PASS / explicit-contract source snapshot -> {root / "config.json"}')
    if report is not None:
        print(f'PASS / sector report -> {report / "index.html"}')


if __name__=='__main__':
    main()
