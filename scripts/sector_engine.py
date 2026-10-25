"""Point-in-time sector comparisons of explicitly selected futures contracts."""
import csv
from datetime import date
import io
import math
import re
from statistics import mean

from analyze_structure import analyze as structure
from market_io import timestamp, number, records, kind, provenance
from price_setups import validate as validate_setup,evaluate as evaluate_setup

FRAMES={'MN1','W1','D1','H4','H1','M30'}


def iso_day(value):
    if not isinstance(value,str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}',value):
        raise ValueError('dates must be YYYY-MM-DD')
    return date.fromisoformat(value)


def validate_config(config,catalog):
    if config.get('schema_version')!=1 or catalog.get('schema_version')!=1:
        raise ValueError('schema_version=1 required')
    kind(config['data_kind'])
    timestamp(config['as_of'])
    end=iso_day(config['trade_date'])
    for field in ('minimum_sector_coverage','max_bar_age_hours'):
        if type(config[field]) not in (int,float):
            raise ValueError(f'{field} must be a JSON number')
    coverage=number(config['minimum_sector_coverage'],positive=True)
    if coverage>1:
        raise ValueError('minimum_sector_coverage must be in (0,1]')
    number(config['max_bar_age_hours'],positive=True)
    sectors={item['id']:item for item in catalog['sectors']}
    if len(sectors)!=len(catalog['sectors']) or not sectors:
        raise ValueError('sector identifiers must be unique')
    if any(not re.fullmatch(r'[a-z][a-z0-9-]*',key) or not str(value['name']).strip() for key,value in sectors.items()):
        raise ValueError('sector identifiers must be safe lowercase slugs with nonempty names')
    products=catalog['products']
    for symbol,item in products.items():
        if item['sector'] not in sectors or not re.fullmatch(r'[A-Z]+',symbol):
            raise ValueError('catalog product identity or sector mismatch')
    windows=config['windows']
    if not isinstance(windows,dict) or not windows:
        raise ValueError('at least one named common comparison window required')
    for key,item in windows.items():
        if not re.fullmatch(r'[a-z][a-z0-9_-]*',key) or not item['label'].strip() or iso_day(item['start_date'])>=end:
            raise ValueError('window names/labels and start dates must precede trade_date')
    universe={}
    for item in config['universe']:
        symbol=item['symbol']
        if symbol not in products or symbol in universe or not item['contract'].strip():
            raise ValueError('declare unique catalog symbols and an explicit contract for each')
        if not re.fullmatch(r'[A-Z]{3}',item['currency']) or not item['unit'].strip() or item.get('volume_unit')!='contracts':
            raise ValueError('declare currency, price unit and volume_unit=contracts')
        if item.get('exchange',products[symbol]['exchange'])!=products[symbol]['exchange']:
            raise ValueError('exchange must match catalog')
        for frame,settings in item.get('structure',{}).items():
            if frame not in FRAMES:
                raise ValueError('unsupported structure timeframe')
            for field in ('support','resistance'):
                if field in settings:
                    number(settings[field],positive=not products[symbol].get('allow_signed',False))
            if 'window_bars' in settings and (type(settings['window_bars']) is not int or settings['window_bars']<=0):
                raise ValueError('window_bars must be a positive integer')
        names=set()
        for setup in item.get('setups',[]):
            validate_setup(setup,products[symbol].get('allow_signed',False))
            if setup['name'] in names:
                raise ValueError('setup names must be unique within one product')
            names.add(setup['name'])
        universe[symbol]=item
    if not universe:
        raise ValueError('explicit nonempty universe required')
    return sectors,products,universe


def load_panel(raw,config,products,universe):
    cutoff=timestamp(config['as_of'])
    decision=iso_day(config['trade_date'])
    groups={}
    excluded={'after_cutoff':0,'after_trade_date':0,'outside_universe_or_contract':0,'not_available_at_cutoff':0}
    seen=set()
    daily_days=set()
    for row in records(raw,['symbol','contract','timeframe','trade_date','close_time','open','high','low','close','volume','open_interest','currency','unit']):
        closing=timestamp(row['close_time'])
        if closing>cutoff:
            excluded['after_cutoff']+=1
            continue
        available=timestamp(row['available_at']) if row.get('available_at','').strip() else None
        if available is not None and available<closing:
            raise ValueError('bar availability cannot precede its closing time')
        if available is not None and available>cutoff:
            excluded['not_available_at_cutoff']+=1
            continue
        day=iso_day(row['trade_date'])
        if day>decision:
            excluded['after_trade_date']+=1
            continue
        symbol=row['symbol'].upper()
        if symbol not in universe or row['contract']!=universe[symbol]['contract']:
            excluded['outside_universe_or_contract']+=1
            continue
        settings=universe[symbol]
        if row['currency']!=settings['currency'] or row['unit']!=settings['unit']:
            raise ValueError(f'{symbol}: price currency/unit mismatch')
        frame=row['timeframe']
        if frame not in FRAMES:
            raise ValueError('unsupported declared timeframe')
        identity=(symbol,frame,closing)
        daily=(symbol,day)
        if identity in seen or (frame=='D1' and daily in daily_days):
            raise ValueError('duplicate closing time or duplicate daily trading date')
        seen.add(identity)
        if frame=='D1':
            daily_days.add(daily)
        values={key:number(row[key],positive=not products[symbol].get('allow_signed',False)) for key in ('open','high','low','close')}
        if values['high']<max(values.values()) or values['low']>min(values.values()):
            raise ValueError(f'{symbol}: inconsistent OHLC bounds')
        for key in ('volume','open_interest'):
            value=number(row[key])
            if value<0 or not value.is_integer():
                raise ValueError('volume/open_interest must be nonnegative whole contract counts')
            values[key]=int(value)
        groups.setdefault((symbol,frame),[]).append(dict(values,close_time=closing,trade_date=day,available_at=available))
    for bars in groups.values():
        bars.sort(key=lambda row:row['close_time'])
        if any(left['trade_date']>right['trade_date'] for left,right in zip(bars,bars[1:])):
            raise ValueError('trading dates go backwards in closing-time order')
    return groups,excluded


def structure_result(bars,entry,frame,config):
    body=io.StringIO()
    writer=csv.writer(body,lineterminator='\n')
    writer.writerow(['close_time','open','high','low','close'])
    for row in bars:
        writer.writerow([row['close_time'].isoformat(),*[row[key] for key in ('open','high','low','close')]])
    levels=entry.get('structure',{}).get(frame,{})
    result=structure(body.getvalue().encode('utf-8'),entry['contract'],frame,config['as_of'],config['data_kind'],
                     levels.get('support'),levels.get('resistance'),levels.get('reference_time'),levels.get('window_bars'))
    # The original panel's hash is recorded separately; this one describes the exact derived OHLC slice.
    result['input_slice']='derived OHLC slice from frozen panel.csv'
    return result


def analyze_product(symbol,entry,product,groups,config):
    end=iso_day(config['trade_date'])
    cutoff=timestamp(config['as_of'])
    daily=groups.get((symbol,'D1'),[])
    by_day={row['trade_date']:row for row in daily}
    current=by_day.get(end)
    alerts=[]
    if current is None:
        alerts.append('缺少目标交易日的日线，不能用旧报价顶替。')
    age=None if current is None else (cutoff-current['close_time']).total_seconds()/3600
    stale=age is not None and age>float(config['max_bar_age_hours'])
    if stale:
        alerts.append('目标交易日收盘数据超过配置的陈旧阈值。')
    comparisons={}
    for name,window in config['windows'].items():
        start=by_day.get(iso_day(window['start_date']))
        reason='missing_end_date' if current is None else 'stale_end_quote' if stale else 'missing_start_date' if start is None else 'nonpositive_start_price' if start['close']<=0 else None
        comparisons[name]={'start_date':window['start_date'],'end_date':config['trade_date'],
                           'start_price':None if start is None else start['close'],
                           'end_price':None if current is None else current['close'],
                           'price_return':None if reason else current['close']/start['close']-1,'unavailable_reason':reason}
    structures={frame:structure_result(bars,entry,frame,config) for (code,frame),bars in groups.items() if code==symbol}
    directions={value['ma_ordering'] for value in structures.values()}&{'ascending','descending'}
    if len(directions)>1:
        alerts.append('跨周期均线方向不一致，分别记录背景与触发。')
    for frame,result in structures.items():
        if result['reference_window'] and result['reference_window']['window_state']=='expired':
            alerts.append(f'{frame} 参照柱窗口已过期。')
    atr=None
    if current and len(daily)>=15:
        ranges=[max(row['high']-row['low'],abs(row['high']-previous['close']),abs(row['low']-previous['close'])) for previous,row in zip(daily,daily[1:])]
        atr=mean(ranges[-14:])
    flow={'volume':None,'open_interest':None,'open_interest_change':None,'volume_vs_prior5_mean':None,
          'previous_observation_trade_date':None,'price_change_since_previous_observation':None,
          'price_oi_observation':None}
    if current:
        index=daily.index(current)
        prior=daily[index-1] if index else None
        flow.update(volume=current['volume'],open_interest=current['open_interest'])
        if prior:
            price_delta=current['close']-prior['close']
            oi_delta=current['open_interest']-prior['open_interest']
            flow['open_interest_change']=oi_delta
            flow['previous_observation_trade_date']=prior['trade_date'].isoformat()
            flow['price_change_since_previous_observation']=price_delta
            direction=lambda x:'up' if x>0 else 'down' if x<0 else 'flat'
            flow['price_oi_observation']={'price':direction(price_delta),'open_interest':direction(oi_delta)}
        if index>=5:
            baseline=mean(row['volume'] for row in daily[index-5:index])
            flow['volume_vs_prior5_mean']=current['volume']/baseline if baseline>0 else None
    return {'symbol':symbol,'name':product['name'],'sector':product['sector'],'exchange':product['exchange'],
            'contract':entry['contract'],'currency':entry['currency'],'unit':entry['unit'],'volume_unit':'contracts',
            'latest_close':None if current is None else current['close'],'quote_age_hours':age,'daily_count':len(daily),
            'windows':comparisons,'atr14_simple':atr,'atr14_over_absolute_close':atr/abs(current['close']) if atr is not None and current['close'] else None,
            'flow':flow,'structures':structures,'attention':alerts,
            'setups':[evaluate_setup(plan,groups.get((symbol,plan['timeframe']),[]),config['as_of']) for plan in entry.get('setups',[])],
            'bars_without_available_at':sum(row['available_at'] is None for (code,_),bars in groups.items() if code==symbol for row in bars)}


def load_evidence(raw,config,sectors):
    if raw is None:
        return [],0
    cutoff=timestamp(config['as_of'])
    selected,seen,excluded={},set(),0
    units={}
    for row in records(raw,['sector','metric','observed_at','published_at','value','unit','source']):
        published=timestamp(row['published_at'])
        if published>cutoff:
            excluded+=1
            continue
        observed=timestamp(row['observed_at'])
        if observed>published or row['sector'] not in sectors or not all(row[key].strip() for key in ('metric','unit','source')):
            raise ValueError('invalid evidence identity, units, source or publication order')
        key=(row['sector'],row['metric'])
        identity=(*key,observed,published)
        if identity in seen:
            raise ValueError('duplicate evidence observation/publication')
        seen.add(identity)
        if key in units and units[key]!=row['unit']:
            raise ValueError('same evidence metric has mixed units')
        units[key]=row['unit']
        item=dict(row,value=number(row['value']),observed_at=observed.isoformat(),published_at=published.isoformat())
        order=(observed,published)
        if key not in selected or order>selected[key][0]:
            selected[key]=(order,item)
    return [selected[key][1] for key in sorted(selected)],excluded


def load_curves(raw,config,universe,products):
    if raw is None:
        return [],0
    cutoff=timestamp(config['as_of'])
    groups,seen,months={},set(),set()
    excluded=0
    for row in records(raw,['symbol','contract','delivery_month','quote_time','price','currency','unit']):
        observed=timestamp(row['quote_time'])
        if observed>cutoff:
            excluded+=1
            continue
        symbol=row['symbol'].upper()
        if symbol not in universe:
            raise ValueError('curve symbol outside declared universe')
        if row['currency']!=universe[symbol]['currency'] or row['unit']!=universe[symbol]['unit']:
            raise ValueError('curve and declared price units must match')
        if not re.fullmatch(r'\d{4}-\d{2}',row['delivery_month']):
            raise ValueError('curve month must be YYYY-MM')
        date.fromisoformat(row['delivery_month']+'-01')
        if not row['contract'] or (symbol,row['contract']) in seen or (symbol,row['delivery_month']) in months:
            raise ValueError('curve snapshot requires unique contracts and months')
        seen.add((symbol,row['contract']))
        months.add((symbol,row['delivery_month']))
        groups.setdefault(symbol,[]).append(dict(row,price=number(row['price'],positive=not products[symbol].get('allow_signed',False)),quote_time=observed.isoformat()))
    results=[]
    for symbol,quotes in sorted(groups.items()):
        if len(quotes)<2:
            raise ValueError('each curve requires at least two months')
        quotes.sort(key=lambda row:row['delivery_month'])
        changes=[b['price']-a['price'] for a,b in zip(quotes,quotes[1:])]
        shape='contango' if all(x>0 for x in changes) else 'backwardation' if all(x<0 for x in changes) else 'flat' if all(x==0 for x in changes) else 'mixed'
        times=[timestamp(row['quote_time']) for row in quotes]
        results.append({'symbol':symbol,'currency':quotes[0]['currency'],'unit':quotes[0]['unit'],
                        'shape':shape,'near_minus_far':quotes[0]['price']-quotes[-1]['price'],
                        'quote_span_seconds':(max(times)-min(times)).total_seconds(),
                        'oldest_quote_age_hours':(cutoff-min(times)).total_seconds()/3600,'quotes':quotes})
    return results,excluded


def analyze(config,catalog,panel_raw,evidence_raw=None,curves_raw=None):
    sectors,products,universe=validate_config(config,catalog)
    groups,excluded=load_panel(panel_raw,config,products,universe)
    members=[analyze_product(symbol,entry,products[symbol],groups,config) for symbol,entry in universe.items()]
    evidence,excluded_evidence=load_evidence(evidence_raw,config,sectors)
    curves,excluded_curves=load_curves(curves_raw,config,universe,products)
    boards=[]
    for sector in catalog['sectors']:
        included=[item for item in members if item['sector']==sector['id']]
        windows={}
        for key in config['windows']:
            values=[item['windows'][key]['price_return'] for item in included if item['windows'][key]['price_return'] is not None]
            coverage=len(values)/len(included) if included else 0
            eligible=bool(values) and coverage>=float(config['minimum_sector_coverage'])
            windows[key]={'expected_products':len(included),'observed_products':len(values),'coverage':coverage,
                          'eligible_for_ranking':eligible,'sample_equal_weight_price_return':mean(values) if values else None,
                          'advancing':sum(value>0 for value in values),'declining':sum(value<0 for value in values),
                          'unchanged':sum(value==0 for value in values),'rank':None}
        boards.append({'id':sector['id'],'name':sector['name'],'windows':windows,'symbols':[item['symbol'] for item in included],
                       'drivers':sector['drivers'],'next_checks':sector['next_checks'],
                       'evidence':[item for item in evidence if item['sector']==sector['id']],
                       'reference':sector['reference']})
    for key in config['windows']:
        ranked=sorted([board for board in boards if board['windows'][key]['eligible_for_ranking']],
                      key=lambda board:(-board['windows'][key]['sample_equal_weight_price_return'],board['id']))
        last=None
        rank=0
        for index,board in enumerate(ranked,1):
            value=board['windows'][key]['sample_equal_weight_price_return']
            if last is None or not math.isclose(last,value,rel_tol=1e-12,abs_tol=1e-12):
                rank=index
            board['windows'][key]['rank']=rank
            last=value
    inputs={'panel':provenance(panel_raw)}
    if evidence_raw is not None:
        inputs['evidence']=provenance(evidence_raw)
    if curves_raw is not None:
        inputs['curves']=provenance(curves_raw)
    result={'schema_version':1,'skill':'taotao-futures-research','data_kind':config['data_kind'],
            'as_of_utc':timestamp(config['as_of']).isoformat(),'trade_date':config['trade_date'],'windows':config['windows'],
            'minimum_sector_coverage':config['minimum_sector_coverage'],'max_bar_age_hours':config['max_bar_age_hours'],
            'configured_product_count':len(universe),
            'catalog_product_count':len(products),'catalog_sector_count':len(sectors),
            'configured_sector_count':sum(bool(board['symbols']) for board in boards),'sectors':boards,'products':members,
            'curves':curves,'source_sha256':inputs,'excluded_panel_rows':excluded,
            'excluded_unpublished_evidence':excluded_evidence,'excluded_future_curve_quotes':excluded_curves,
            'scope':'Common-window, selected-contract price observations; no official sector index, leveraged P&L or predictive score.',
            'limitations':['Universe and sector taxonomy are user research choices, not an exchange classification or full-market coverage',
                           'Trading dates, units, source authenticity, sessions and continuous-contract adjustments require independent checks',
                           'Volume/open interest are contract counts, not capital flows or proof of long/short ownership',
                           'ATR is a simple 14-range mean, not Wilder smoothing; no execution, margin or guaranteed stop fill']}
    # Also catches arithmetic overflow in derived observations.
    import json
    json.dumps(result,allow_nan=False)
    return result
