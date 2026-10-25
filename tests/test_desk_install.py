"""Installer boundary cases using tiny controlled release fixtures."""
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import zipfile

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("install_suite",ROOT/"tools/install_suite.py")
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        self.bundle=self.root/"suite.zip"
        self.destination=self.root/"installed 研究"
        self.names={"test-skill-"+str(i) for i in range(8)}|{"taotao-futures-research"}
        (self.root/"SUITE.json").write_text(json.dumps(dict(suite_version="3.0.0",skills=[dict(skill=name) for name in sorted(self.names) if name!="taotao-futures-research"])),encoding="utf-8")
        with zipfile.ZipFile(self.bundle,"w") as archive:
            for name in self.names:
                archive.writestr(f"skills/{name}/SKILL.md",f"---\nname: {name}\n---\n")
        self.sums()

    def sums(self):
        (self.root/"SHA256SUMS.txt").write_text("".join(hashlib.sha256(file.read_bytes()).hexdigest()+"  "+file.name+"\n" for file in (self.bundle,self.root/"SUITE.json")),encoding="utf-8")

    def install(self):
        return module.install(self.bundle,self.destination)

    def test_install_all_nine_then_refuse_overwrite(self):
        receipt=self.install()
        self.assertEqual(len(receipt["skills"]),9)
        keep=self.destination/"taotao-futures-research/SKILL.md"
        keep.write_text("user edits",encoding="utf-8")
        with self.assertRaisesRegex(ValueError,"not replaced"):
            self.install()
        self.assertEqual(keep.read_text(),"user edits")

    def test_preflight_conflict_does_not_copy_any_skill(self):
        self.destination.mkdir()
        (self.destination/"test-skill-4").mkdir()
        with self.assertRaises(ValueError):
            self.install()
        self.assertEqual(len(list(self.destination.iterdir())),1)

    def test_tampered_zip_and_catalog_rejected(self):
        original=self.bundle.read_bytes()
        self.bundle.write_bytes(original+b"tampered")
        with self.assertRaisesRegex(ValueError,"ZIP checksum"):
            self.install()
        self.bundle.write_bytes(original)
        catalog=self.root/"SUITE.json"
        catalog.write_text(catalog.read_text()+" ",encoding="utf-8")
        with self.assertRaisesRegex(ValueError,"catalog checksum"):
            self.install()

    def test_zip_traversal_rejected_before_extraction(self):
        with zipfile.ZipFile(self.bundle,"a") as archive:
            archive.writestr("skills/test-skill-0/../../escaped.txt","bad")
        self.sums()
        with self.assertRaisesRegex(ValueError,"unsafe"):
            self.install()
        self.assertFalse((self.root/"escaped.txt").exists())

    def test_duplicate_archive_member_rejected(self):
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore",UserWarning)
            with zipfile.ZipFile(self.bundle,"a") as archive:
                archive.writestr("skills/test-skill-0/SKILL.md","duplicate")
        self.sums()
        with self.assertRaisesRegex(ValueError,"duplicate"):
            self.install()

    def test_metadata_mismatch_rejected_before_copy(self):
        with zipfile.ZipFile(self.bundle,"w") as archive:
            for name in self.names:
                archive.writestr(f"skills/{name}/SKILL.md","---\nname: wrong-name\n---")
        self.sums()
        with self.assertRaisesRegex(ValueError,"metadata mismatch"):
            self.install()
        self.assertEqual(list(self.destination.iterdir()),[])


if __name__=="__main__":
    unittest.main()
