import copy
import csv
from datetime import datetime,timedelta,timezone
import io
import json
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import sector_engine as engine

FIELDS=['symbol','contract','timeframe','trade_date','close_time','open','high','low','close','volume','open_interest','currency','unit']

def fixture():
    catalog=json.loads((ROOT/'catalog/sectors.json').read_text(encoding='utf-8'))
    config={'schema_version':1,'data_kind':'synthetic','as_of':'2024-01-16T16:00:00+08:00','trade_date':'2024-01-16',
            'minimum_sector_coverage':1.0,'max_bar_age_hours':24,
            'windows':{'day':{'label':'单日','start_date':'2024-01-15'},'long':{'label':'长区间','start_date':'2024-01-02'}},
            'universe':[{'symbol':symbol,'contract':symbol+'_DEMO','currency':'CNY','unit':'demo_points','volume_unit':'contracts'} for symbol in ['AU','CU','AL']]}
    rows=[]
    for symbol,last in [('AU',110),('CU',120),('AL',100)]:
        previous=100
        for index in range(16):
            day=datetime(2024,1,1,15,tzinfo=timezone(timedelta(hours=8)))+timedelta(days=index)
            close=last if index==15 else 100
            rows.append(dict(zip(FIELDS,[symbol,symbol+'_DEMO','D1',day.date().isoformat(),day.isoformat(),previous,
                                        max(previous,close)+1,min(previous,close)-1,close,10+index,100+2*index,'CNY','demo_points'])))
            previous=close
    return config,catalog,rows

def raw(rows):
    text=io.StringIO()
    writer=csv.DictWriter(text,fieldnames=FIELDS,lineterminator='\n')
    writer.writeheader()
    writer.writerows(rows)
    return text.getvalue().encode('utf-8')

def product(result,symbol):
    return next(value for value in result['products'] if value['symbol']==symbol)

def sector(result,name):
    return next(value for value in result['sectors'] if value['id']==name)


class SectorEngineTests(unittest.TestCase):
    def setUp(self):
        self.config,self.catalog,self.rows=fixture()

    def analyze(self,rows=None,**kwargs):
        return engine.analyze(self.config,self.catalog,raw(self.rows if rows is None else rows),**kwargs)

    def test_common_window_mean_and_breadth_use_configured_representatives(self):
        result=self.analyze()
        value=sector(result,'nonferrous')['windows']['day']
        self.assertAlmostEqual(value['sample_equal_weight_price_return'],.1)
        self.assertEqual((value['expected_products'],value['observed_products']),(2,2))
        self.assertEqual((value['advancing'],value['declining'],value['unchanged']),(1,0,1))
        self.assertEqual(value['rank'],sector(result,'precious-metals')['windows']['day']['rank'])

    def test_incomplete_sector_is_visible_but_not_ranked_by_default(self):
        rows=[row for row in self.rows if not(row['symbol']=='AL' and row['trade_date']=='2024-01-16')]
        value=sector(self.analyze(rows),'nonferrous')['windows']['day']
        self.assertEqual(value['coverage'],.5)
        self.assertAlmostEqual(value['sample_equal_weight_price_return'],.2)
        self.assertFalse(value['eligible_for_ranking'])
        self.assertIsNone(value['rank'])
        self.assertIsNone(product(self.analyze(rows),'AL')['latest_close'])

    def test_lower_coverage_is_an_explicit_option(self):
        self.config['minimum_sector_coverage']=.5
        rows=[row for row in self.rows if not(row['symbol']=='AL' and row['trade_date']=='2024-01-16')]
        self.assertTrue(sector(self.analyze(rows),'nonferrous')['windows']['day']['eligible_for_ranking'])

    def test_missing_exact_window_start_is_not_forward_filled(self):
        rows=[row for row in self.rows if not(row['symbol']=='AU' and row['trade_date']=='2024-01-15')]
        item=product(self.analyze(rows),'AU')
        self.assertEqual(item['windows']['day']['unavailable_reason'],'missing_start_date')
        self.assertIsNone(item['windows']['day']['price_return'])
        self.assertIsNotNone(item['windows']['long']['price_return'])

    def test_future_counterfactual_prices_cannot_change_past_rankings(self):
        reports=[]
        for value in ('NaN',999999):
            future=dict(self.rows[15],trade_date='2024-01-17',close_time='2024-01-17T15:00:00+08:00',close=value)
            reports.append(self.analyze(self.rows+[future]))
        self.assertEqual(reports[0]['sectors'],reports[1]['sectors'])
        self.assertEqual(reports[0]['products'],reports[1]['products'])
        self.assertEqual(reports[0]['excluded_panel_rows']['after_cutoff'],1)

    def test_another_contract_does_not_silently_replace_selected_contract(self):
        extra=dict(self.rows[15],contract='AU_NEW_MONTH',close=999999,high=1000000)
        result=self.analyze(self.rows+[extra])
        self.assertEqual(product(result,'AU')['latest_close'],110)
        self.assertEqual(result['excluded_panel_rows']['outside_universe_or_contract'],1)

    def test_same_day_and_equivalent_timestamp_duplicates_are_rejected(self):
        for extra in [dict(self.rows[15],close_time='2024-01-16T14:00:00+08:00'),dict(self.rows[15],close_time='2024-01-16T07:00:00Z')]:
            with self.subTest(extra=extra),self.assertRaises(ValueError):
                self.analyze(self.rows+[extra])

    def test_units_ohlc_and_contract_counts_are_checked(self):
        for field,value in [('unit','USD_per_barrel'),('high',1),('volume',-1),('open_interest',1.5),('close',float('nan'))]:
            rows=copy.deepcopy(self.rows)
            rows[0][field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):
                self.analyze(rows)

    def test_stale_current_bar_is_excluded_from_ranking(self):
        self.config['as_of']='2024-01-19T16:00:00+08:00'
        result=self.analyze()
        self.assertEqual(product(result,'AU')['windows']['day']['unavailable_reason'],'stale_end_quote')
        self.assertIsNone(sector(result,'precious-metals')['windows']['day']['rank'])

    def test_atr_volume_baseline_and_price_oi_are_hand_checkable(self):
        result=self.analyze()
        item=product(result,'AU')
        self.assertAlmostEqual(item['atr14_simple'],38/14)
        self.assertEqual(item['flow']['open_interest_change'],2)
        self.assertAlmostEqual(item['flow']['volume_vs_prior5_mean'],25/22)
        self.assertEqual(item['flow']['price_oi_observation'],{'price':'up','open_interest':'up'})
        self.assertAlmostEqual(product(result,'AL')['atr14_simple'],2)

    def test_short_history_and_zero_volume_do_not_create_infinite_ratios(self):
        rows=[dict(row,volume=0) for row in self.rows if row['trade_date']>='2024-01-14']
        item=product(self.analyze(rows),'AU')
        self.assertIsNone(item['atr14_simple'])
        self.assertIsNone(item['flow']['volume_vs_prior5_mean'])
        self.assertFalse(item['structures']['D1']['macd']['ready'])

    def test_signed_oil_baseline_omits_percentage_and_negative_metals_fail(self):
        self.config['universe']=[dict(self.config['universe'][0],symbol='SC',contract='SC_DEMO')]
        rows=[dict(row,symbol='SC',contract='SC_DEMO',open=-10,high=-8,low=-12,close=-9) for row in self.rows if row['symbol']=='AU']
        self.assertEqual(product(self.analyze(rows),'SC')['windows']['day']['unavailable_reason'],'nonpositive_start_price')
        self.config,self.catalog,self.rows=fixture()
        with self.assertRaises(ValueError):
            self.analyze([dict(row,open=-10,high=-8,low=-12,close=-9) for row in self.rows])

    def test_panel_file_order_does_not_change_results(self):
        first=self.analyze()
        second=self.analyze(list(reversed(self.rows)))
        self.assertEqual(first['products'],second['products'])
        self.assertEqual(first['sectors'],second['sectors'])

    def test_duplicate_universe_and_unsafe_catalog_sectors_are_rejected(self):
        self.config['universe'].append(self.config['universe'][0])
        with self.assertRaises(ValueError):
            self.analyze()
        self.config,self.catalog,self.rows=fixture()
        self.catalog['sectors'][0]['id']='../outside'
        with self.assertRaises(ValueError):
            self.analyze()

    def test_thresholds_are_numbers_and_selected_sector_count_is_explicit(self):
        self.assertEqual(self.analyze()['configured_sector_count'],2)
        for field in ('minimum_sector_coverage','max_bar_age_hours'):
            previous=self.config[field]
            self.config[field]=str(previous)
            with self.subTest(field=field),self.assertRaises(ValueError):
                self.analyze()
            self.config[field]=previous

    def test_night_session_trading_date_is_not_inferred_from_calendar_date(self):
        rows=copy.deepcopy(self.rows)
        for row in rows:
            if row['trade_date']=='2024-01-16':
                row['close_time']='2024-01-15T23:00:00+08:00'
        result=self.analyze(rows)
        self.assertEqual(product(result,'AU')['latest_close'],110)


class EvidenceCurveTests(unittest.TestCase):
    def setUp(self):
        self.config,self.catalog,self.rows=fixture()
        self.evidence=b'sector,metric,observed_at,published_at,value,unit,source\nprecious-metals,inventory,2024-01-12T00:00:00Z,2024-01-15T00:00:00Z,100,tonnes,synthetic://test\n'
        self.curves=b'symbol,contract,delivery_month,quote_time,price,currency,unit\nAU,AU_ONE,2024-03,2024-01-16T07:00:00Z,100,CNY,demo_points\nAU,AU_TWO,2024-04,2024-01-16T07:00:00Z,102,CNY,demo_points\n'

    def analyze(self,**kwargs):
        return engine.analyze(self.config,self.catalog,raw(self.rows),**kwargs)

    def test_publication_not_observation_date_controls_evidence_visibility(self):
        future=b'precious-metals,inventory,2024-01-13T00:00:00Z,2024-01-17T00:00:00Z,999,tonnes,synthetic://future\n'
        result=self.analyze(evidence_raw=self.evidence+future)
        self.assertEqual(sector(result,'precious-metals')['evidence'][0]['value'],100)
        self.assertEqual(result['excluded_unpublished_evidence'],1)

    def test_available_revision_is_selected_without_overwriting_old_input(self):
        revised=b'precious-metals,inventory,2024-01-12T00:00:00Z,2024-01-16T00:00:00Z,105,tonnes,synthetic://revised\n'
        result=self.analyze(evidence_raw=self.evidence+revised)
        self.assertEqual(sector(result,'precious-metals')['evidence'][0]['value'],105)

    def test_mixed_evidence_units_and_impossible_publication_order_fail(self):
        mixed=self.evidence+b'precious-metals,inventory,2024-01-13T00:00:00Z,2024-01-16T00:00:00Z,105,kg,synthetic://test\n'
        for value in (mixed,self.evidence.replace(b'2024-01-12',b'2024-01-16')):
            with self.subTest(value=value),self.assertRaises(ValueError):
                self.analyze(evidence_raw=value)

    def test_generic_curve_shape_spread_and_timestamp_span(self):
        result=self.analyze(curves_raw=self.curves)
        self.assertEqual(result['curves'][0]['shape'],'contango')
        self.assertEqual(result['curves'][0]['near_minus_far'],-2)
        self.assertEqual(result['curves'][0]['quote_span_seconds'],0)

    def test_future_curve_quote_is_excluded_and_duplicates_fail(self):
        future=b'AU,AU_FUTURE,2024-05,2024-01-17T07:00:00Z,90000,CNY,demo_points\n'
        result=self.analyze(curves_raw=self.curves+future)
        self.assertEqual(len(result['curves'][0]['quotes']),2)
        self.assertEqual(result['excluded_future_curve_quotes'],1)
        with self.assertRaises(ValueError):
            self.analyze(curves_raw=self.curves+self.curves.splitlines()[1]+b'\n')

    def test_curve_currency_and_negative_gold_prices_fail(self):
        for value in (self.curves.replace(b'CNY',b'USD'),self.curves.replace(b',100,',b',-100,')):
            with self.subTest(value=value),self.assertRaises(ValueError):
                self.analyze(curves_raw=value)
