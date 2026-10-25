"""Observe predeclared break/reclaim/retest rules; no trading or predictive confirmation."""
from market_io import timestamp,number

STATE_LABELS={'plan_not_yet_available':'计划声明晚于本次截止','anchor_not_in_observations':'缺少参照柱',
              'awaiting_reclaim':'等待收盘回到边界内','awaiting_retest':'已收回边界，等待后续测试',
              'retest_observed':'已观察到后续测试守住边界','expired':'验证期限已到，条件未完成','invalidated':'已触及事先声明的失效位'}


def validate(plan,allow_signed=False):
    if not isinstance(plan,dict):
        raise ValueError('setup rules must be JSON objects')
    if not isinstance(plan.get('name'),str) or not plan['name'].strip():
        raise ValueError('a named setup rule is required')
    if plan['timeframe'] not in ('M30','H1','H4','D1','W1','MN1') or plan['side'] not in ('support_reclaim','resistance_rejection'):
        raise ValueError('unsupported setup timeframe or side')
    if type(plan['validation_bars']) is not int or plan['validation_bars']<=0:
        raise ValueError('validation_bars must be a positive integer')
    for field in ('level','invalidation_level','retest_tolerance'):
        if type(plan[field]) not in (int,float):
            raise ValueError('setup prices/tolerance must be JSON numbers')
    level=number(plan['level'],positive=not allow_signed)
    invalid=number(plan['invalidation_level'],positive=not allow_signed)
    tolerance=number(plan['retest_tolerance'])
    if tolerance<0 or (invalid>=level if plan['side']=='support_reclaim' else invalid<=level):
        raise ValueError('invalid structure boundary or absolute-price retest tolerance')
    if timestamp(plan['declared_at'])<timestamp(plan['anchor_time']):
        raise ValueError('a fixed observed anchor cannot be declared before its closing time')


def evaluate(plan,bars,as_of):
    validate(plan,allow_signed=True)
    cutoff=timestamp(as_of)
    anchor=timestamp(plan['anchor_time'])
    declared=timestamp(plan['declared_at'])
    result={'name':plan['name'],'timeframe':plan['timeframe'],'side':plan['side'],
            'declared_at':declared.isoformat(),'anchor_time':anchor.isoformat(),'level':plan['level'],
            'invalidation_level':plan['invalidation_level'],'retest_tolerance':plan['retest_tolerance'],
            'validation_bars':plan['validation_bars'],'state':None,'observed_events':[],
            'scope':'Predeclared rule observations, not a buy/sell signal, validated edge or guaranteed stop fill.'}
    if declared>cutoff:
        result['state']='plan_not_yet_available'
        return result
    selected=sorted([bar for bar in bars if bar['close_time']<=cutoff],key=lambda bar:bar['close_time'])
    matches=[index for index,bar in enumerate(selected) if bar['close_time']==anchor]
    if not matches:
        result['state']='anchor_not_in_observations'
        return result
    index=matches[0]
    long=plan['side']=='support_reclaim'
    level=float(plan['level'])
    invalid=float(plan['invalidation_level'])
    tolerance=float(plan['retest_tolerance'])
    if not (selected[index]['close']<level if long else selected[index]['close']>level):
        raise ValueError('anchor must close beyond the broken boundary on the declared side')
    state='awaiting_reclaim'
    for elapsed,bar in enumerate(selected[index+1:],1):
        if state!='retest_observed' and elapsed>plan['validation_bars']:
            state='expired'
            break
        moment=bar['close_time'].isoformat()
        if (bar['low']<=invalid if long else bar['high']>=invalid):
            result['observed_events'].append({'event':'structure_invalidated','close_time':moment,'bars_after_anchor':elapsed,
                                              'predates_declaration':bar['close_time']<=declared})
            state='invalidated'
            break
        if bar['close_time']<=declared:
            continue  # A late rule cannot claim earlier positive stages; prior invalidation still counts.
        reclaim=bar['close']>=level if long else bar['close']<=level
        if state=='awaiting_reclaim' and reclaim:
            result['observed_events'].append({'event':'boundary_reclaimed','close_time':moment,'bars_after_anchor':elapsed})
            state='awaiting_retest'
            continue  # The same candle cannot establish the subsequent retest.
        touches=bar['low']<=level+tolerance if long else bar['high']>=level-tolerance
        if state=='awaiting_retest' and reclaim and touches:
            result['observed_events'].append({'event':'later_retest_held','close_time':moment,'bars_after_anchor':elapsed})
            state='retest_observed'
    if state in ('awaiting_reclaim','awaiting_retest') and len(selected)-1-index>=plan['validation_bars']:
        state='expired'
    result['state']=state
    result['completed_bars_after_anchor']=len(selected)-1-index
    result['invalidation_rule']='touch of low <= invalidation_level' if long else 'touch of high >= invalidation_level'
    return result
