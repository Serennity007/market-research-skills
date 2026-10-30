"""Exercise real ZIP exports with fake development files, never real credentials."""
import contextlib
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('suite_builder', ROOT/'tools/build_skill_suite.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class SuiteExportTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def source(self, root, name):
        root.mkdir(parents=True, exist_ok=True)
        (root/'SKILL.md').write_text(f'---\nname: {name}\n---\n', encoding='utf-8')
        (root/'run.py').write_text('print("synthetic fixture")\n', encoding='utf-8')
        for relative in ['.env', '.env.local', '.venv/pyvenv.cfg', 'venv/local.txt', '__pycache__/module.pyc', '.git/config', 'node_modules/dependency/index.js']:
            path = root/relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('FAKE_LOCAL_ONLY_MARKER', encoding='utf-8')

    def assert_clean(self, archive):
        with zipfile.ZipFile(archive) as bundle:
            names = bundle.namelist()
            self.assertTrue(any(name.endswith('/SKILL.md') for name in names))
            self.assertTrue(any(name.endswith('/run.py') for name in names))
            for name in names:
                self.assertNotIn(b'FAKE_LOCAL_ONLY_MARKER', bundle.read(name), name)

    def test_direct_zip_omits_development_files(self):
        source = self.root/'skill'
        self.source(source, 'skill')
        output = self.root/'skill.zip'
        builder.zip_tree(source, output)
        self.assert_clean(output)

    def test_full_export_filters_master_and_all_specialists(self):
        master = self.root/'master'
        specialists = self.root/'specialists'
        self.source(master, 'taotao-futures-research')
        core = master/'desk_core'
        core.mkdir()
        profiles = {key: {'skill': key+'-test-skill'} for key in ['gold', 'crude-oil', 'shipping', 'equity-index', 'ferrous', 'nonferrous', 'chemicals', 'agriculture']}
        (core/'profiles.json').write_text(json.dumps(profiles), encoding='utf-8')
        (core/'engine.py').write_text('# synthetic engine\n', encoding='utf-8')
        (master/'docs').mkdir()
        for doc in ['desk-data-contract.md', 'desk-risk-model.md', 'desk-source-policy.md']:
            (master/'docs'/doc).write_text('synthetic documentation', encoding='utf-8')
        (master/'LICENSE').write_text('synthetic license', encoding='utf-8')
        (master/'tools').mkdir()
        (master/'tools/install_suite.py').write_text('# synthetic installer\n', encoding='utf-8')
        for key, profile in profiles.items():
            source = (master/'skills' if key in builder.NEW else specialists)/profile['skill']
            self.source(source, profile['skill'])
            demo = master/'examples/desk-demo'/key
            demo.mkdir(parents=True)
            (demo/'config.json').write_text('{"fixture":true}', encoding='utf-8')
        output = self.root/'exports'
        with patch.object(builder, 'ROOT', master), patch.object(builder, 'CORE', core), contextlib.redirect_stdout(io.StringIO()):
            builder.build(output, specialists)
        archives = list(output.glob('*.zip'))
        self.assertEqual(len(archives), 10)
        for archive in archives:
            with self.subTest(archive=archive.name):
                self.assert_clean(archive)
        sums = dict(line.split('  ', 1)[::-1] for line in (output/'SHA256SUMS.txt').read_text().splitlines())
        for archive in archives:
            self.assertEqual(sums[archive.name], hashlib.sha256(archive.read_bytes()).hexdigest())
        # Exporting must not modify the developer's originals.
        self.assertEqual((master/'.env').read_text(), 'FAKE_LOCAL_ONLY_MARKER')

    def test_clean_zip_remains_deterministic(self):
        source = self.root/'skill'
        self.source(source, 'skill')
        first, second = self.root/'first.zip', self.root/'second.zip'
        builder.zip_tree(source, first)
        (source/'.env').write_text('another fake local setting', encoding='utf-8')
        builder.zip_tree(source, second)
        self.assertEqual(first.read_bytes(), second.read_bytes())


if __name__ == '__main__':
    unittest.main()
