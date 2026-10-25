import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('registry',ROOT/'scripts/validate_registry.py')
tool=importlib.util.module_from_spec(spec)
spec.loader.exec_module(tool)

class RegistryTests(unittest.TestCase):
    def setUp(self):
        self.data=json.loads((ROOT/'registry.json').read_text(encoding='utf-8'))

    def test_manifest_is_valid(self):
        self.assertEqual(tool.validate(self.data),4)

    def test_duplicate_and_mismatched_urls_are_rejected(self):
        duplicate=copy.deepcopy(self.data)
        duplicate['skills'].append(duplicate['skills'][0])
        bad_url=copy.deepcopy(self.data)
        bad_url['skills'][0]['url']='https://github.com/someone/unrelated'
        for data in (duplicate,bad_url):
            with self.subTest(data=data),self.assertRaises(ValueError):
                tool.validate(data)

    def test_path_escape_is_rejected(self):
        for value in ('../outside.py','/etc/passwd','C:/outside.py','scripts\\outside.py'):
            data=copy.deepcopy(self.data)
            data['skills'][0]['scripts']=[value]
            with self.subTest(path=value),self.assertRaises(ValueError):
                tool.validate(data)

    def test_local_missing_files_and_skill_mismatch_are_detected(self):
        data=copy.deepcopy(self.data)
        data['skills']=data['skills'][:1]
        item=data['skills'][0]
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)/item['repository']
            root.mkdir()
            (root/'SKILL.md').write_text(f"---\nname: {item['skill']}\n---\n",encoding='utf-8')
            with self.assertRaises(ValueError):
                tool.validate(data,Path(temp))
            for script in item['scripts']:
                path=root/script
                path.parent.mkdir(exist_ok=True)
                path.write_text('print(1)\n',encoding='utf-8')
            self.assertEqual(tool.validate(data,Path(temp)),1)
            (root/'SKILL.md').write_text('---\nname: wrong-name\n---\n',encoding='utf-8')
            with self.assertRaises(ValueError):
                tool.validate(data,Path(temp))
