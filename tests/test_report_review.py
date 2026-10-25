import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import compare_reports as review
import run_sectors as runner
import sector_engine as engine
from test_sector_engine import fixture,raw


def pair():
    config,catalog,rows=fixture()
    before=copy.deepcopy(config)
    before['trade_date']='2024-01-15'
    before['as_of']='2024-01-15T16:00:00+08:00'
    before['windows']['day']['start_date']='2024-01-14'
    a=engine.analyze(before,catalog,raw(rows))
    b=engine.analyze(config,catalog,raw(rows))
    for value in (a,b):
        value['catalog_sha256']='same_catalog'
    return before,config,catalog,rows,a,b


class ReviewTests(unittest.TestCase):
    def test_matching_contract_changes_are_hand_checkable(self):
        *_,a,b=pair()
        result=review.compare(a,b)
        au=next(item for item in result['products'] if item['symbol']=='AU')
        self.assertAlmostEqual(au['matched_price_change'],.1)
        day=next(item for item in result['anchored_rank_comparisons'] if item['window']=='day')
        self.assertEqual(day['unavailable_reason'],'window_anchor_changed')
        long=next(item for item in result['anchored_rank_comparisons'] if item['window']=='long')
        self.assertIsNone(long['unavailable_reason'])

    def test_rollover_is_not_interpreted_as_price_performance(self):
        *_,a,b=pair()
        b['products'][0]['contract']='AU_NEW'
        result=review.compare(a,b)
        item=next(item for item in result['products'] if item['symbol']=='AU')
        self.assertIsNone(item['matched_price_change'])
        self.assertEqual(item['unavailable_reason'],'contract_or_quote_identity_changed')

    def test_missing_and_stale_endpoints_remain_unavailable(self):
        for field,value in [('latest_close',None),('quote_age_hours',999)]:
            *_,a,b=pair()
            b['products'][0][field]=value
            self.assertIsNone(next(item for item in review.compare(a,b)['products'] if item['symbol']=='AU')['matched_price_change'])

    def test_changed_data_kind_taxonomy_and_backwards_time_fail(self):
        for field,value in [('data_kind','imported_observations'),('catalog_sha256','other'),('trade_date','2024-01-14')]:
            *_,a,b=pair()
            b[field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):
                review.compare(a,b)

    def test_incomplete_sector_is_not_a_rank_comparison(self):
        *_,a,b=pair()
        next(item for item in b['sectors'] if item['id']=='nonferrous')['windows']['long']['coverage']=.5
        value=next(item for item in review.compare(a,b)['anchored_rank_comparisons'] if item['sector']=='nonferrous' and item['window']=='long')
        self.assertEqual(value['unavailable_reason'],'incomplete_samples')

    def test_two_frozen_runs_can_be_reviewed_without_modifying_them(self):
        before,after,catalog,rows,_,_=pair()
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            (root/'catalog.json').write_text(json.dumps(catalog),encoding='utf-8')
            (root/'panel.csv').write_bytes(raw(rows))
            directories=[]
            for index,config in enumerate((before,after)):
                config=dict(config,catalog='catalog.json',files={'panel':'panel.csv'})
                path=root/f'config-{index}.json'
                path.write_text(json.dumps(config),encoding='utf-8')
                directories.append(runner.run(path,root/'reports'))
            original=(directories[0]/'bundle.json').read_bytes()
            result=review.run(*directories,root/'reviews')
            self.assertTrue((result/'REVIEW.md').is_file())
            self.assertEqual((directories[0]/'bundle.json').read_bytes(),original)

    def test_changed_manual_rules_are_disclosed(self):
        *_,a,b=pair()
        plan={'name':'测试','timeframe':'H4','side':'support_reclaim','declared_at':'2024-01-01T00:00:00Z',
              'anchor_time':'2024-01-01T00:00:00Z','level':100,'invalidation_level':97,'retest_tolerance':.5,'validation_bars':3}
        a['products'][0]['setups']=[plan]
        b['products'][0]['setups']=[dict(plan,level=101)]
        result=review.compare(a,b)
        item=next(value for value in result['products'] if value['symbol']=='AU')
        self.assertEqual(item['rule_changes'][0]['change'],'rule_parameters_changed')
