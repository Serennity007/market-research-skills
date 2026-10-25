"""Install a verified release suite without replacing existing Skills.

Python 3.10+. Use SHA256SUMS.txt and SUITE.json beside the downloaded ZIP.
Hashes establish consistency with the supplied list, not publisher authenticity.
"""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import tempfile
import zipfile


def install(bundle, destination):
    bundle=Path(bundle).resolve()
    catalog_bytes=(bundle.parent/"SUITE.json").read_bytes()
    catalog=json.loads(catalog_bytes.decode("utf-8"))
    checksums={}
    for line in (bundle.parent/"SHA256SUMS.txt").read_text(encoding="utf-8").splitlines():
        digest,name=line.split("  ",1)
        if name in checksums:
            raise ValueError("duplicate checksum name")
        checksums[name]=digest
    digest=hashlib.sha256(bundle.read_bytes()).hexdigest()
    if checksums.get(bundle.name)!=digest:
        raise ValueError("suite ZIP checksum mismatch")
    if checksums.get("SUITE.json")!=hashlib.sha256(catalog_bytes).hexdigest():
        raise ValueError("suite catalog checksum mismatch")
    expected={row["skill"] for row in catalog["skills"]}|{"taotao-futures-research"}
    if len(expected)!=9 or any(not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*",name) for name in expected):
        raise ValueError("unexpected suite catalog")
    destination=Path(destination).expanduser().resolve()
    destination.mkdir(parents=True,exist_ok=True)
    conflicts=[name for name in sorted(expected) if (destination/name).exists() or (destination/name).is_symlink()]
    if conflicts:
        raise ValueError("existing Skills were not replaced: "+", ".join(conflicts))
    with tempfile.TemporaryDirectory(prefix="futures-suite-") as temporary:
        temporary=Path(temporary)
        with zipfile.ZipFile(bundle) as archive:
            names=set(); size=0
            for member in archive.infolist():
                path=PurePosixPath(member.filename)
                if member.filename in names or len(path.parts)<3 or path.parts[0]!="skills" or path.parts[1] not in expected or ".." in path.parts or "\\" in member.filename or ":" in member.filename or path.is_absolute():
                    raise ValueError("unsafe/duplicate suite member")
                names.add(member.filename)
                if (member.external_attr>>16)&0o170000==0o120000:
                    raise ValueError("symlinks are not supported")
                size+=member.file_size
                if size>256*1024*1024:
                    raise ValueError("expanded suite exceeds 256 MiB")
            archive.extractall(temporary)
        for name in expected:
            root=temporary/"skills"/name
            skill=(root/"SKILL.md").read_text(encoding="utf-8")
            if not re.search(r"(?m)^name:\s*"+re.escape(name)+r"\s*$",skill):
                raise ValueError("Skill metadata mismatch: "+name)
        installed=[]
        for name in sorted(expected):
            # copytree's exclusive destination also guards a race with another installer.
            shutil.copytree(temporary/"skills"/name,destination/name)
            installed.append(str(destination/name))
    return {"status":"installed","suite_version":catalog["suite_version"],"bundle_sha256":digest,"skills":installed,"discovery":"Restart the host or start a new session to discover newly installed Skills."}


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle",type=Path,required=True)
    parser.add_argument("--dest",type=Path,default=Path.home()/".codex/skills")
    args=parser.parse_args()
    try:
        result=install(args.bundle,args.dest)
    except (ValueError,OSError,KeyError,TypeError,zipfile.BadZipFile) as exc:
        parser.exit(2,"ERROR: "+str(exc)+"\n")
    print(json.dumps(result,ensure_ascii=True,indent=2))
