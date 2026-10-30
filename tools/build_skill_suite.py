"""Export deterministic self-contained Skills; never installs or publishes them.

python tools/build_skill_suite.py --out output/skill-release
Source for four existing specialists is supplied via --specialists-root.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import zipfile

ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT/"desk_core"
NEW = {"ferrous", "nonferrous", "chemicals", "agriculture"}
IGNORE = shutil.ignore_patterns(".git", "__pycache__", "*.pyc", "output", "node_modules", ".DS_Store",
                               ".venv", "venv", ".env", ".env.*")


def copy_core(target):
    shutil.copytree(CORE, target/"desk_core", ignore=IGNORE, dirs_exist_ok=True)


def zip_tree(root, target):
    """Fixed timestamps, stable ordering, forward slashes; no machine-local files."""
    with zipfile.ZipFile(target,"w",zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        for file in sorted(root.rglob("*")):
            if file.is_file():
                relative = file.relative_to(root)
                if any(IGNORE("", [part]) for part in relative.parts):
                    continue
                info = zipfile.ZipInfo(root.name+"/"+relative.as_posix(),(2025,1,1,0,0,0))
                info.compress_type=zipfile.ZIP_DEFLATED; info.external_attr=0o644<<16
                archive.writestr(info,file.read_bytes())


def build(output, specialists_root):
    output = Path(output).resolve()
    if output.is_relative_to(ROOT) and not output.is_relative_to(ROOT/"output"):
        raise ValueError("exports inside this checkout must stay under output/ to avoid copying themselves")
    # A new destination prevents stale files or silent replacement of a release.
    output.mkdir(parents=True,exist_ok=False)
    staged = output/"skills"; staged.mkdir()
    profiles = json.loads((CORE/"profiles.json").read_text(encoding="utf-8"))
    registry = []
    for key,profile in profiles.items():
        name = profile["skill"]
        source = ROOT/"skills"/name if key in NEW else Path(specialists_root)/name
        target = staged/name
        shutil.copytree(source,target,ignore=IGNORE)
        copy_core(target)
        # Export examples and schema used by the selected profile only.
        demo = target/"examples/desk-demo"/key
        shutil.copytree(ROOT/"examples/desk-demo"/key,demo,dirs_exist_ok=True)
        for doc in ("desk-data-contract.md","desk-risk-model.md","desk-source-policy.md"):
            (target/"docs").mkdir(exist_ok=True)
            shutil.copyfile(ROOT/"docs"/doc,target/"docs"/doc)
        (target/"CORE-MANIFEST.json").write_text(json.dumps({"version":"3.0.0","upstream":"https://github.com/Serennity007/taotao-futures-research","sha256":{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((target/"desk_core").iterdir()) if p.suffix in (".py",".json")}},indent=2)+"\n",encoding="utf-8",newline="\n")
        # The master MIT notice applies to the shared component/new Skills.
        if not (target/"LICENSE").exists():
            shutil.copyfile(ROOT/"LICENSE",target/"LICENSE")
        archive = output/(name+"-"+("1.0.0" if key in NEW else "2.0.0")+".zip")
        zip_tree(target,archive)
        registry.append(dict(profile=key,skill=name,archive=archive.name,version="1.0.0" if key in NEW else "2.0.0"))
    master = staged/"taotao-futures-research"
    # Avoid nesting the four Skill entrypoints inside the installed master.
    shutil.copytree(ROOT,master,ignore=lambda path,names: IGNORE(path,names) | ({"skills"} & set(names)))
    zip_tree(master,output/"taotao-futures-research-3.0.0.zip")
    zip_tree(staged,output/"futures-research-suite-3.0.0.zip")
    (output/"SUITE.json").write_text(json.dumps({"suite_version":"3.0.0","engine_version":"3.0.0","python":">=3.10","skills":registry},ensure_ascii=False,indent=2)+"\n",encoding="utf-8",newline="\n")
    shutil.copyfile(ROOT/"tools/install_suite.py",output/"install_suite.py")
    sums = "".join(hashlib.sha256(p.read_bytes()).hexdigest()+"  "+p.name+"\n" for p in sorted(output.iterdir()) if p.is_file())
    (output/"SHA256SUMS.txt").write_text(sums,encoding="utf-8",newline="\n")
    print(json.dumps({"directory":str(output),"specialists":len(registry),"archives":len(list(output.glob("*.zip")))}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out",type=Path,required=True)
    parser.add_argument("--specialists-root",type=Path,default=ROOT.parent)
    args=parser.parse_args()
    build(args.out,args.specialists_root)
