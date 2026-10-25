import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
import sys
sys.path.insert(0,str(ROOT/'scripts'))
import run_all as runner


class RunnerTests(unittest.TestCase):
    def fixture(self,root,kind='synthetic'):
        data=json.loads((ROOT/'registry.json').read_text(encoding='utf-8'))
        for item in data['skills']:
            repository=root/item['repository']
            (repository/'examples').mkdir(parents=True)
            (repository/'examples/workbench.json').write_text(json.dumps({'skill':item['skill'],'data_kind':kind}),encoding='utf-8')
            (repository/'SKILL.md').write_text(f"---\nname: {item['skill']}\n---\n",encoding='utf-8')
            for value in item['scripts']:
                path=repository/value
                path.parent.mkdir(parents=True,exist_ok=True)
                path.write_text('# fixture\n',encoding='utf-8')

    def test_non_synthetic_configuration_is_rejected_before_execution(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            self.fixture(root,'imported_observations')
            with patch.object(runner.subprocess,'run') as process,self.assertRaises(ValueError):
                runner.run(root,root/'output')
            process.assert_not_called()
            self.assertFalse((root/'output').exists())

    def test_worker_failure_does_not_mark_the_hub_run_complete(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            self.fixture(root)
            with patch.object(runner.subprocess,'run',return_value=subprocess.CompletedProcess([],2,'','bad input')),self.assertRaises(ValueError):
                runner.run(root,root/'output')
            output=next((root/'output').iterdir())
            self.assertTrue((output/'FAILURE.json').is_file())
            self.assertFalse((output/'COMPLETE.json').exists())

    def test_missing_repositories_fail_before_creating_output(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            with self.assertRaises(ValueError):
                runner.run(root,root/'output')
            self.assertFalse((root/'output').exists())
