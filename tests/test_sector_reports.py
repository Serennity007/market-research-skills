import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import run_sectors as runner
import sector_reports as reports


class Resources(HTMLParser):
    def __init__(self):
        super().__init__()
        self.external=[]
    def handle_starttag(self,tag,attrs):
        if tag in ('iframe','link','img','script'):
            self.external += [value for key,value in attrs if key in ('src','href')]


class SectorReportTests(unittest.TestCase):
    def test_full_bundle_can_replay_without_original_paths(self):
        with tempfile.TemporaryDirectory() as temp:
            first=runner.run(ROOT/'examples/sector-demo/config.json',temp)
            data=json.loads((first/'bundle.json').read_text(encoding='utf-8'))
            self.assertEqual(data['catalog_sector_count'],11)
            self.assertEqual(data['configured_product_count'],30)
            self.assertTrue((first/'COMPLETE.json').is_file())
            self.assertEqual(len(list((first/'sectors').glob('*.html'))),11)
            for role,sha in data['source_sha256'].items():
                self.assertEqual(hashlib.sha256((first/'inputs'/f'{role}.csv').read_bytes()).hexdigest(),sha)
            self.assertEqual(hashlib.sha256((first/'inputs/catalog.json').read_bytes()).hexdigest(),data['catalog_sha256'])
            second=runner.run(first/'config.snapshot.json',temp)
            replay=json.loads((second/'bundle.json').read_text(encoding='utf-8'))
            for field in ('sectors','products','curves','source_sha256'):
                self.assertEqual(data[field],replay[field])
            self.assertNotEqual(first,second)

    def test_cli_runs_from_a_chinese_directory(self):
        with tempfile.TemporaryDirectory(prefix='期货研究-') as temp:
            process=subprocess.run([sys.executable,'-X','utf8',str(ROOT/'scripts/run_sectors.py'),'--config',str(ROOT/'examples/sector-demo/config.json'),'--out',temp,'--json'],cwd=temp,capture_output=True,text=True,encoding='utf-8')
            self.assertEqual(process.returncode,0,process.stderr)
            summary=json.loads(process.stdout)
            self.assertEqual(summary['status'],'complete')
            self.assertTrue((Path(summary['directory'])/'index.html').is_file())

    def test_imported_observations_need_provenance_before_export(self):
        config=json.loads((ROOT/'examples/sector-demo/config.json').read_text(encoding='utf-8'))
        config['data_kind']='imported_observations'
        config['catalog']=str(ROOT/'catalog/sectors.json')
        config['files']={key:str(ROOT/'examples/sector-demo'/value) for key,value in config['files'].items()}
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'config.json'
            path.write_text(json.dumps(config),encoding='utf-8')
            out=Path(temp)/'output'
            with self.assertRaises(ValueError):
                runner.run(path,out)
            self.assertFalse(out.exists())

    def test_html_escapes_sector_names_and_has_no_external_assets(self):
        _,_,_,data=runner.load(ROOT/'examples/sector-demo/config.json')
        data['sectors'][0]['name']='<img src=x onerror=alert(1)>'
        for html in [reports.overview_html(data),reports.sector_html(data['sectors'][0],data)]:
            parser=Resources()
            parser.feed(html)
            self.assertFalse(parser.external)
            self.assertNotIn('<img src=x',html)
            self.assertIn('&lt;img',html)

    def test_demo_keeps_missing_members_and_expired_windows_visible(self):
        _,_,_,data=runner.load(ROOT/'examples/sector-demo/config.json')
        metals=next(item for item in data['sectors'] if item['id']=='nonferrous')
        self.assertIsNone(metals['windows']['day']['rank'])
        self.assertAlmostEqual(metals['windows']['day']['coverage'],2/3)
        gold=next(item for item in data['products'] if item['symbol']=='AU')
        self.assertEqual(gold['structures']['H4']['reference_window']['window_state'],'expired')
        self.assertTrue(any('跨周期' in item for item in gold['attention']))
