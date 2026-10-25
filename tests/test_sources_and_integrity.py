import copy
import csv
from datetime import datetime,timedelta,timezone
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import bundle_integrity as integrity
import fetch_sina as source
import market_io
import run_sectors as runner
import sector_engine as engine
from test_sector_engine import fixture,raw,FIELDS,product


def payload(count=31):
    day=datetime(2024,1,1)
    return [{'d':(day+timedelta(days=index)).date().isoformat(),'o':'100','h':'102','l':'99','c':str(100+index/100),
             'v':'100','p':'200','s':'100'} for index in range(count)]

def encoded(rows):
    return ('/* source comment */\nvar _taotao=('+json.dumps(rows)+');').encode()

def request_file(root):
    catalog=(ROOT/'catalog/sectors.json').read_bytes()
    (root/'catalog.json').write_bytes(catalog)
    config={'schema_version':1,'catalog':'catalog.json','max_bar_age_hours':96,
            'contracts':[{'symbol':'AU','contract':'AU2406','currency':'CNY','unit':'CNY_per_gram','session_close':'15:00:00+08:00'}]}
    path=root/'request.json'
    path.write_text(json.dumps(config),encoding='utf-8')
    return path,config


class SourceTests(unittest.TestCase):
    def test_parser_never_evaluates_provider_scripts(self):
        self.assertEqual(len(source.parse(encoded(payload()))),31)
        for value in [b'alert(1);',encoded(payload())+b'alert(1);',b'var _other=([]);',b'<html>Access denied</html>']:
            with self.subTest(value=value[:30]),self.assertRaises(ValueError):
                source.parse(value)

    def test_empty_and_oversized_responses_fail(self):
        for value in (encoded([]),b' '* (source.MAX_BYTES+1)):
            with self.assertRaises(ValueError):
                source.parse(value)

    def test_explicit_contracts_only_and_maximum_batch_size(self):
        catalog=json.loads((ROOT/'catalog/sectors.json').read_text(encoding='utf-8'))
        with tempfile.TemporaryDirectory() as temp:
            _,config=request_file(Path(temp))
            for contract in ('AU0','AU8888','AU9999','AU2400','AU2406&other=1'):
                config['contracts'][0]['contract']=contract
                with self.subTest(contract=contract),self.assertRaises(ValueError):
                    source.validate_request(config,catalog)
            config['contracts']*=7
            with self.assertRaises(ValueError):
                source.validate_request(config,catalog)

    def test_current_retrieval_day_is_excluded(self):
        item={'symbol':'AU','contract':'AU2406','currency':'CNY','unit':'CNY_per_gram','session_close':'15:00:00+08:00'}
        rows,excluded=source.convert(payload(),item,{'allow_signed':False},datetime(2024,1,31,20,tzinfo=timezone.utc))
        # This instant is already February 1 in Beijing, so Jan 31 remains a prior date.
        self.assertEqual(len(rows),31)
        rows,excluded=source.convert(payload(),item,{'allow_signed':False},datetime(2024,1,31,10,tzinfo=timezone.utc))
        self.assertEqual(len(rows),30)
        self.assertEqual(excluded[0]['reason'],'retrieval_day_or_later_is_not_used')

    def test_snapshot_records_raw_hashes_and_generated_config_runs_offline(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            request,_=request_file(root)
            response=encoded(payload())
            archive=source.fetch(request,root/'sources',downloader=lambda contract:(response,'https://example.invalid/'+contract),
                                 clock=lambda:datetime(2024,2,2,10,tzinfo=timezone.utc))
            self.assertEqual(integrity.verify_source(archive)['source_count'],1)
            config,catalog,files,result=runner.load(archive/'config.json')
            self.assertEqual(result['data_kind'],'imported_observations')
            self.assertEqual(result['trade_date'],'2024-01-31')
            self.assertEqual(product(result,'AU')['bars_without_available_at'],0)
            report=runner.run(archive/'config.json',root/'reports')
            self.assertEqual(integrity.verify(report)['manifest_version'],2)
            (archive/'raw/AU2406.jsonp.txt').write_bytes(b'changed')
            with self.assertRaises(ValueError):
                integrity.verify_source(archive)

    def test_partial_failure_preserves_failure_record_not_success(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            request,_=request_file(root)
            def unavailable(_):
                raise OSError('provider unavailable')
            with self.assertRaises(OSError):
                source.fetch(request,root/'output',downloader=unavailable,clock=lambda:datetime(2024,2,2,tzinfo=timezone.utc))
            archive=next((root/'output').iterdir())
            self.assertTrue((archive/'FAILURE.json').is_file())
            self.assertFalse((archive/'SOURCE_COMPLETE.json').exists())

    def test_zero_volume_placeholders_are_explicit_and_bad_ohlc_fails(self):
        item={'symbol':'AU','contract':'AU2406','currency':'CNY','unit':'CNY_per_gram','session_close':'15:00:00+08:00'}
        rows=payload()
        rows[0].update(o='0',h='0',l='0',c='0',v='0')
        accepted,excluded=source.convert(rows,item,{},datetime(2024,2,2,tzinfo=timezone.utc))
        self.assertEqual(len(accepted),30)
        self.assertEqual(excluded[0]['reason'],'zero_volume_zero_ohlc_placeholder')
        rows=payload()
        rows[0]['h']='1'
        with self.assertRaises(ValueError):
            source.convert(rows,item,{},datetime(2024,2,2,tzinfo=timezone.utc))

    def test_retrieved_vintage_cannot_be_rewound_into_historical_knowledge(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            request,_=request_file(root)
            archive=source.fetch(request,root/'sources',downloader=lambda _: (encoded(payload()),'https://example.invalid/quote'),
                                 clock=lambda:datetime(2024,2,2,10,tzinfo=timezone.utc))
            config,catalog,files,_=runner.load(archive/'config.json')
            config['as_of']='2024-02-01T10:00:00Z'
            result=engine.analyze(config,json.loads(catalog),files['panel'])
            self.assertIsNone(product(result,'AU')['latest_close'])
            self.assertEqual(result['excluded_panel_rows']['not_available_at_cutoff'],31)


class IntegrityTests(unittest.TestCase):
    def make(self,temp):
        return runner.run(ROOT/'examples/sector-demo/config.json',temp)

    def test_frozen_input_change_is_detected_before_replay(self):
        with tempfile.TemporaryDirectory() as temp:
            root=self.make(temp)
            path=root/'inputs/panel.csv'
            path.write_bytes(path.read_bytes().replace(b'100.0',b'101.0',1)+b'\n')
            with self.assertRaises(ValueError):
                runner.load(root/'config.snapshot.json')

    def test_report_and_config_tampering_are_detected(self):
        for name in ('REPORT.md','config.snapshot.json','sectors/energy.html'):
            with self.subTest(name=name),tempfile.TemporaryDirectory() as temp:
                root=self.make(temp)
                path=root/name
                path.write_bytes(path.read_bytes()+b'changed')
                with self.assertRaises(ValueError):
                    integrity.verify(root)

    def test_unsafe_paths_extra_files_and_missing_files_fail(self):
        with tempfile.TemporaryDirectory() as temp:
            root=self.make(temp)
            manifest=json.loads((root/'COMPLETE.json').read_text(encoding='utf-8'))
            manifest['sha256']['../outside']='0'*64
            (root/'COMPLETE.json').write_text(json.dumps(manifest),encoding='utf-8')
            with self.assertRaises(ValueError):
                integrity.verify(root)
        with tempfile.TemporaryDirectory() as temp:
            root=self.make(temp)
            (root/'unlisted.txt').write_text('extra')
            with self.assertRaises(ValueError):
                integrity.verify(root)
        with tempfile.TemporaryDirectory() as temp:
            root=self.make(temp)
            (root/'REPORT.md').unlink()
            with self.assertRaises(ValueError):
                integrity.verify(root)

    def test_v1_input_verification_remains_supported(self):
        with tempfile.TemporaryDirectory() as temp:
            root=self.make(temp)
            (root/'COMPLETE.json').write_text(json.dumps({'status':'complete','files':['bundle.json']}),encoding='utf-8')
            self.assertEqual(integrity.verify(root)['manifest_version'],1)
            (root/'inputs/catalog.json').write_bytes(b'{}')
            with self.assertRaises(ValueError):
                integrity.verify(root)

    def test_malformed_csv_headers_and_row_width_fail_clearly(self):
        for value in (b'a,a\n1,2\n',b'a,b\n1\n',b'a,b\n1,2,3\n'):
            with self.subTest(value=value),self.assertRaises(ValueError):
                market_io.records(value,['a'])
        with self.assertRaises(ValueError):
            market_io.timestamp(None)
        with self.assertRaises(ValueError):
            market_io.number(True)

    def test_missing_daily_row_names_the_actual_previous_observation(self):
        config,catalog,rows=fixture()
        rows=[row for row in rows if not(row['symbol']=='AU' and row['trade_date']=='2024-01-15')]
        result=engine.analyze(config,catalog,raw(rows))
        flow=product(result,'AU')['flow']
        self.assertEqual(flow['previous_observation_trade_date'],'2024-01-14')
        self.assertEqual(flow['open_interest_change'],4)
