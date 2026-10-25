"""Golden arithmetic, historical availability, calendar and bundle boundary tests."""
import copy
import csv
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from decimal import Decimal as D

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from desk_core.validation import read_json, csv_rows, dec, stamp, inside, day
from desk_core.bundle import load, run, replay, verify, seal, code_hashes
from desk_core.engine import analyze
from desk_core.risk import capacity
from desk_core.reports import report

PROFILES = read_json((ROOT/"desk_core/profiles.json").read_bytes())


def csv_bytes(rows):
    out = io.StringIO(newline="")
    writer = csv.DictWriter(out, fieldnames=list(rows[0]))
    writer.writeheader(); writer.writerows(rows)
    return out.getvalue().encode("utf-8")


class DeskTests(unittest.TestCase):
    def setUp(self):
        self.config, self.raw, _ = load(ROOT/"examples/desk-demo/ferrous/config.json")

    def calc(self):
        return analyze(self.config, self.raw, PROFILES)

    def rows(self, role):
        return csv_rows(self.raw[role], [])

    def test_all_eight_profiles_and_hand_computed_fixture(self):
        for key in PROFILES:
            with self.subTest(profile=key):
                _, _, result = load(ROOT/"examples/desk-demo"/key/"config.json")
                self.assertEqual(result["quality"]["gaps"], [])
                self.assertEqual(result["quality"]["excluded_future_vintages"]["fundamentals"], 1)
                self.assertEqual(result["market"]["atr14_simple"], 4)
                self.assertEqual(result["market"]["open_interest_change"], 20)
                self.assertEqual(result["basis"]["spot_minus_future"], 5)
                self.assertEqual(result["curve"]["spreads"][0]["near_minus_far"], -10)
                self.assertEqual(result["fundamentals"][0]["prior_only_percentile"], 50)
                self.assertEqual(result["fundamentals"][0]["value"], 105)
                self.assertEqual(result["fundamentals"][0]["change_from_previous_observation"], -5)
        result = self.calc()
        self.assertEqual(result["risk"]["planned_loss_per_lot"], D("83.433"))
        self.assertEqual(result["risk"]["lots_ceiling"], 11)
        self.assertEqual(result["recipes"][0]["value"], 300)
        _,_,agri = load(ROOT/"examples/desk-demo/agriculture/config.json")
        self.assertEqual(agri["recipes"][0]["value"], 460)

    def test_revisions_enter_only_when_available(self):
        self.config["as_of"] = "2025-09-29T12:06:00+08:00"
        result = self.calc()
        self.assertEqual(result["fundamentals"][0]["value"], 999)
        self.assertEqual(result["quality"]["excluded_future_vintages"]["fundamentals"], 0)
        self.assertEqual(result["market"]["calendar"]["latest_completed_trade_date"], "2025-09-26")

    def test_friday_night_does_not_complete_monday_daily_bar(self):
        self.config["as_of"] = "2025-09-26T23:30:00+08:00"
        result = self.calc()
        self.assertEqual(result["market"]["calendar"]["latest_completed_trade_date"], "2025-09-26")
        self.assertNotIn("missing_latest_completed_session",result["quality"]["gaps"])
        self.config["as_of"] = "2025-09-29T15:10:00+08:00"
        result = self.calc()
        self.assertIn("missing_latest_completed_session",result["quality"]["gaps"])
        self.assertEqual(result["risk"]["status"], "blocked")

    def test_calendar_close_identity_horizon_and_overlap(self):
        rows = self.rows("sessions")
        self.raw["sessions"] = csv_bytes(rows+[rows[-1]])
        with self.assertRaisesRegex(ValueError,"overlapping"):
            self.calc()
        self.raw["sessions"] = csv_bytes(rows)
        self.config["calendar_valid_until"] = "2025-09-26T00:00:00+08:00"
        with self.assertRaisesRegex(ValueError,"horizon"):
            self.calc()
        self.config["calendar_valid_until"] = "2025-09-29T23:59:00+08:00"
        bars = self.rows("bars"); bars[-1]["observed_at"] = "2025-09-26T14:59:00+08:00"
        self.raw["bars"] = csv_bytes(bars)
        with self.assertRaisesRegex(ValueError,"final declared session"):
            self.calc()

    def test_no_calendar_elapsed_freshness(self):
        self.raw.pop("sessions")
        self.config["as_of"] = "2025-09-29T12:00:00+08:00"
        result = self.calc()
        self.assertIn("calendar_not_validated",result["quality"]["gaps"])
        self.assertIn("stale_bars",result["quality"]["gaps"])
        self.assertEqual(result["risk"]["status"],"blocked")

    def test_quote_skew_blocks_basis_curve_recipe(self):
        for role in ("spot","curve","prices"):
            original = self.raw[role]
            rows = self.rows(role); rows[0]["observed_at"] = "2025-09-26T14:00:00+08:00"
            self.raw[role] = csv_bytes(rows)
            result = self.calc()
            target = result[role if role=="curve" else "basis" if role=="spot" else "recipes"]
            self.assertEqual((target[0] if role=="prices" else target)["status"],"blocked")
            self.raw[role] = original

    def test_contract_roll_and_mixed_units_rejected(self):
        for role,key in [("bars","contract"),("spot","unit"),("curve","currency"),("prices","unit")]:
            original = self.raw[role]
            rows = self.rows(role); rows[0][key] = "WRONG"
            self.raw[role] = csv_bytes(rows)
            with self.subTest(role=role), self.assertRaises(ValueError):
                self.calc()
            self.raw[role] = original

    def test_duplicate_vintage_and_invalid_clock_rejected(self):
        rows = self.rows("fundamentals")
        self.raw["fundamentals"] = csv_bytes(rows+[rows[0]])
        with self.assertRaisesRegex(ValueError,"vintage"):
            self.calc()
        rows[0]["available_at"] = "2021-01-01T00:00:00+08:00"
        self.raw["fundamentals"] = csv_bytes(rows)
        with self.assertRaisesRegex(ValueError,"observed_at"):
            self.calc()

    def test_equivalent_offset_clocks_are_same_event(self):
        rows=self.rows("fundamentals")
        duplicate=dict(rows[0],observed_at="2021-09-26T02:00:00+00:00")
        self.raw["fundamentals"]=csv_bytes(rows+[duplicate])
        with self.assertRaisesRegex(ValueError,"vintage"):
            self.calc()

    def test_noncanonical_date_and_curve_scope(self):
        with self.assertRaises(ValueError):
            day("2025-W39-5")
        rows=self.rows("curve"); rows[0]["scope"]="different delivery grade"
        self.raw["curve"]=csv_bytes(rows)
        with self.assertRaisesRegex(ValueError,"scope"):
            self.calc()

    def test_imported_retrieval_cannot_be_backdated(self):
        self.config["data_kind"] = "imported_observations"
        self.config["sources"] = {role:dict(name="Snapshot",policy="retrieval_snapshot",retrieved_at="2025-09-26T16:00:00+08:00") for role in self.raw}
        with self.assertRaisesRegex(ValueError,"earlier availability"):
            self.calc()
        for item in self.config["sources"].values():
            item.update(policy="archived_publication",archive_reference="declared://vintage-store")
        result = self.calc()
        self.assertIn("historical_archive_claim_not_independently_verified",result["quality"]["gaps"])

    def test_same_year_not_in_seasonal_distribution(self):
        rows = self.rows("fundamentals")
        rows.append(dict(rows[0],observed_at="2025-01-01T10:00:00+08:00",published_at="2025-01-01T12:00:00+08:00",available_at="2025-01-01T12:05:00+08:00",value="999999"))
        self.raw["fundamentals"] = csv_bytes(rows)
        self.assertEqual(self.calc()["fundamentals"][0]["prior_only_percentile"],50)

    def test_signed_price_ratios_omitted(self):
        config, raw, _ = load(ROOT/"examples/desk-demo/crude-oil/config.json")
        config.pop("risk")
        rows = csv_rows(raw["bars"],[])
        rows[0].update(open="-5",high="-3",low="-7",close="-4")
        raw["bars"] = csv_bytes(rows)
        result = analyze(config,raw,PROFILES)
        self.assertIsNone(result["market"]["fixed_contract_change_pct"])

    def test_boolean_nan_duplicate_json_and_csv_width(self):
        for value in (True,False,"NaN","Infinity",None):
            with self.subTest(value=value), self.assertRaises(ValueError):
                dec(value)
        for raw in (b'{"x":1,"x":2}', b'{"x":NaN}'):
            with self.assertRaises(ValueError):
                read_json(raw)
        for raw in (b'a,a\n1,2\n', b'a,b\n1\n',b'a,b\n1,2,3\n'):
            with self.assertRaises(ValueError):
                csv_rows(raw,[])
        with self.assertRaises(ValueError):
            stamp("2025-09-26T15:00:00")

    def test_relative_paths_and_unicode_inputs(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)/"研究 测试"; root.mkdir()
            (root/"数据.csv").write_text("a\n1",encoding="utf-8")
            self.assertEqual(inside(root,"数据.csv").name,"数据.csv")
            for unsafe in ("../outside", "C:/data", "/data", "a\\b", "./数据.csv"):
                with self.subTest(path=unsafe), self.assertRaises(ValueError):
                    inside(root,unsafe)

    def test_bilingual_escape_and_report_scope(self):
        result = self.calc()
        result["domain"] = copy.deepcopy(result["domain"])
        result["domain"]["questions"]["en"].append("<script>alert('x')</script>")
        md,html = report(result,[],"en")
        self.assertNotIn("<script>",html)
        self.assertIn("&lt;script&gt;",html)
        self.assertNotIn("<script>",md)
        _,zh = report(result,[],"zh-CN")
        self.assertIn("假设容量",zh)
        self.assertIn("default-src 'none'",html)

    def test_bundle_replay_tamper_and_changed_engine(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp)/"输出"
            first = run(ROOT/"examples/desk-demo/ferrous/config.json",output)
            self.assertEqual(len(verify(first)["files"]),15)
            second = replay(first,output,"zh-CN")
            self.assertNotEqual(first,second)
            (first/"inputs/bars.csv").write_text("tampered",encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"hash mismatch"):
                load(first/"config.snapshot.json")
            payload = read_json((second/"bundle.json").read_bytes())
            payload["engine_sha256"]["engine.py"] = "0"*64
            (second/"bundle.json").write_text(json.dumps(payload),encoding="utf-8")
            seal(second)
            with self.assertRaisesRegex(ValueError,"engine changed"):
                replay(second,output)

    def test_manifest_extra_missing_and_profile_gate(self):
        with tempfile.TemporaryDirectory() as temp:
            root = run(ROOT/"examples/desk-demo/ferrous/config.json",temp)
            (root/"extra.txt").write_text("extra")
            with self.assertRaisesRegex(ValueError,"file set"):
                verify(root)
            (root/"extra.txt").unlink()
            (root/"REPORT.en.md").unlink()
            with self.assertRaisesRegex(ValueError,"file set"):
                verify(root)
        with self.assertRaisesRegex(ValueError,"only accepts"):
            load(ROOT/"examples/desk-demo/ferrous/config.json","gold")

    def test_recorded_import_is_not_a_historical_first_vintage(self):
        config,raw,result=load(ROOT/"examples/desk-imported/gold/config.json")
        self.assertEqual(result["market"]["observations"],225)
        self.assertEqual(result["market"]["contract"],"AU2612")
        self.assertIn("calendar_not_validated",result["quality"]["gaps"])
        self.assertEqual(result["risk"]["status"],"not_requested")
        config["as_of"]="2026-10-23T17:00:00+08:00"
        with self.assertRaisesRegex(ValueError,"historical availability"):
            analyze(config,raw,PROFILES)

    def test_frozen_desk_examples_verify_and_reproduce(self):
        with tempfile.TemporaryDirectory() as output:
            for root in sorted((ROOT/"examples/desk-reports").iterdir()):
                verify(root)
                replay(root,output)


class CapacityTests(unittest.TestCase):
    def setUp(self):
        config,raw,result = load(ROOT/"examples/desk-demo/ferrous/config.json")
        self.request = dict(config["risk"],entry="100",stop="95",margin_budget="10000")
        self.spec = read_json(raw["spec"])
        self.market = dict(result["market"],close="100",previous_volume=2000)
        self.cutoff = stamp(config["as_of"])

    def calc(self):
        return capacity(self.request,self.spec,self.market,self.cutoff,{"policy":"synthetic"})

    def test_hand_computed_fees_ticks_rounding_and_stress(self):
        result = self.calc()
        self.assertEqual(result["fees_at_stop_per_lot"],D("7.195"))
        self.assertEqual(result["planned_loss_per_lot"],D("77.195"))
        self.assertEqual(result["initial_margin_per_lot"],100)
        self.assertEqual(result["lots_ceiling"],12)
        self.assertEqual(result["planned_loss_total"],D("926.340"))
        self.assertGreater(result["stress"][0]["stress_loss"],D(1000))
        self.request["close_kind"]="close"
        self.assertEqual(self.calc()["lots_ceiling"],13)

    def test_decimal_boundary_and_zero_budget(self):
        self.request["risk_budget"]="77.194999999999999999"
        self.assertEqual(self.calc()["lots_ceiling"],0)
        self.request["risk_budget"]="77.195"
        self.assertEqual(self.calc()["lots_ceiling"],1)
        self.request["risk_budget"]=0
        self.assertEqual(self.calc()["lots_ceiling"],0)

    def test_margin_liquidity_and_short_scenarios(self):
        self.request["margin_budget"]="199"
        self.assertEqual(self.calc()["lots_ceiling"],1)
        self.request["margin_budget"]="10000"
        self.market["previous_volume"]=10
        self.assertEqual(self.calc()["lots_ceiling"],0)
        self.market["previous_volume"]=2000
        self.request.update(side="short",stop="105")
        self.assertEqual(self.calc()["planned_loss_per_lot"],D("77.205"))

    def test_tick_stop_unknown_fee_and_expiry(self):
        for key,value in [("entry","100.1"),("stop","101"),("max_lots",True),("max_previous_volume_fraction","1.1")]:
            request = self.request.copy(); self.request[key]=value
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.calc()
            self.request=request
        self.spec[0]["expires_at"]="2025-09-26T00:00:00+08:00"
        self.assertEqual(self.calc()["status"],"blocked")

    def test_overlapping_schedules_and_unknown_close_today(self):
        self.spec.append(dict(self.spec[0],version="SYNTHETIC-2"))
        self.assertEqual(self.calc()["status"],"blocked")
        self.spec.pop()
        self.spec[0]["fees"].pop("close_today")
        with self.assertRaises(KeyError):
            self.calc()


if __name__ == "__main__":
    unittest.main()
