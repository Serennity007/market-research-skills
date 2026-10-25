import copy
from datetime import datetime,timedelta,timezone
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import price_setups as setup

START=datetime(2024,1,8,1,tzinfo=timezone.utc)
def fixture():
    plan={'name':'模拟支撑收复','timeframe':'M30','side':'support_reclaim','anchor_time':START.isoformat(),
          'declared_at':START.isoformat(),'level':100,'invalidation_level':97,'retest_tolerance':.5,'validation_bars':4}
    values=[(99,99.2,97.8,98),(98,101.3,97.7,101),(101,101.2,99.7,100.3),(100.3,102.3,100.2,102)]
    bars=[dict(zip(['open','high','low','close'],row),close_time=START+timedelta(minutes=30*index)) for index,row in enumerate(values)]
    return plan,bars

class SetupTests(unittest.TestCase):
    def check(self,plan,bars):
        return setup.evaluate(plan,bars,'2024-01-09T00:00:00Z')

    def test_break_reclaim_and_later_retest_are_distinct_bars(self):
        plan,bars=fixture()
        result=self.check(plan,bars)
        self.assertEqual(result['state'],'retest_observed')
        self.assertEqual([item['event'] for item in result['observed_events']],['boundary_reclaimed','later_retest_held'])
        self.assertEqual(result['observed_events'][0]['bars_after_anchor'],1)
        self.assertEqual(result['observed_events'][1]['bars_after_anchor'],2)

    def test_same_reclaim_candle_cannot_confirm_a_later_retest(self):
        plan,bars=fixture()
        self.assertEqual(self.check(plan,bars[:2])['state'],'awaiting_retest')

    def test_completed_observation_can_later_be_invalidated(self):
        plan,bars=fixture()
        plan['validation_bars']=2
        bars.append({'open':102,'high':103,'low':97,'close':101,'close_time':START+timedelta(hours=3)})
        result=self.check(plan,bars)
        self.assertEqual(result['state'],'invalidated')
        self.assertEqual(result['observed_events'][-1]['event'],'structure_invalidated')

    def test_no_deadline_extension_or_post_expiry_confirmation(self):
        plan,bars=fixture()
        plan['validation_bars']=1
        result=self.check(plan,bars)
        self.assertEqual(result['state'],'expired')
        self.assertEqual(len(result['observed_events']),1)
        self.assertEqual(self.check(plan,bars[:2])['state'],'expired')

    def test_short_side_has_mirrored_rules(self):
        plan,bars=fixture()
        plan.update(side='resistance_rejection',invalidation_level=103)
        for bar in bars:
            bar.update(open=200-bar['open'],high=200-bar['low'],low=200-bar['high'],close=200-bar['close'])
        self.assertEqual(self.check(plan,bars)['state'],'retest_observed')

    def test_future_plan_and_future_price_are_not_current_observations(self):
        plan,bars=fixture()
        plan['declared_at']='2024-01-10T00:00:00Z'
        self.assertEqual(self.check(plan,bars)['state'],'plan_not_yet_available')
        plan,bars=fixture()
        future=dict(bars[-1],low=1,close_time=datetime(2024,1,10,tzinfo=timezone.utc))
        self.assertEqual(self.check(plan,bars+[future])['state'],'retest_observed')

    def test_late_rule_cannot_claim_events_before_declaration(self):
        plan,bars=fixture()
        plan['declared_at']=bars[2]['close_time'].isoformat()
        result=self.check(plan,bars)
        self.assertEqual(result['state'],'awaiting_retest')
        self.assertEqual(result['observed_events'][0]['close_time'],bars[3]['close_time'].isoformat())

    def test_bad_anchors_boundaries_and_windows_fail(self):
        plan,bars=fixture()
        for field,value in [('invalidation_level',101),('retest_tolerance',-1),('validation_bars',True)]:
            wrong=dict(plan,**{field:value})
            with self.subTest(field=field),self.assertRaises(ValueError):
                self.check(wrong,bars)
        wrong=dict(plan,anchor_time=bars[1]['close_time'].isoformat(),declared_at=bars[1]['close_time'].isoformat())
        with self.assertRaises(ValueError):
            self.check(wrong,bars)

    def test_missing_anchor_is_explicit(self):
        plan,bars=fixture()
        self.assertEqual(self.check(plan,bars[1:])['state'],'anchor_not_in_observations')

    def test_prior_invalidation_is_not_erased_by_a_late_declaration(self):
        plan,bars=fixture()
        bars[1]['low']=96
        plan['declared_at']=bars[2]['close_time'].isoformat()
        result=self.check(plan,bars)
        self.assertEqual(result['state'],'invalidated')
        self.assertTrue(result['observed_events'][0]['predates_declaration'])

    def test_price_thresholds_are_json_numbers(self):
        plan,bars=fixture()
        plan['level']='100'
        with self.assertRaises(ValueError):
            self.check(plan,bars)
