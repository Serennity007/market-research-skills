#!/usr/bin/env python3
"""Run the four independently cloned synthetic demos and build a local report index."""
import argparse
from datetime import datetime, timezone
from html import escape
import json
from pathlib import Path
import subprocess
import sys
import uuid

from validate_registry import validate, DEFAULT


def run(local_root, output, manifest=DEFAULT):
    data=json.loads(Path(manifest).read_text(encoding='utf-8'))
    validate(data,local_root)
    for item in data['skills']:
        config=Path(local_root)/item['repository']/'examples/workbench.json'
        settings=json.loads(config.read_text(encoding='utf-8'))
        if settings.get('data_kind')!='synthetic' or settings.get('skill')!=item['skill']:
            raise ValueError('run_all only runs registered synthetic example configurations')
    root=(Path(output)/('market-run-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')+'-'+uuid.uuid4().hex[:8])).resolve()
    root.mkdir(parents=True,exist_ok=False)
    jobs=[]
    try:
        for item in data['skills']:
            repository=(Path(local_root)/item['repository']).resolve()
            process=subprocess.run([sys.executable,'-X','utf8',str(repository/'scripts/run_research.py'),'--config',str(repository/'examples/workbench.json'),
                                    '--out',str(root/item['repository']),'--json'],cwd=repository,capture_output=True,text=True,encoding='utf-8')
            if process.returncode:
                raise ValueError(f"{item['skill']} failed: {process.stderr.strip()}")
            status=json.loads(process.stdout)
            directory=Path(status['directory']).resolve()
            if status.get('status')!='complete' or status.get('skill')!=item['skill'] or not directory.is_relative_to(root) or not (directory/'COMPLETE.json').is_file():
                raise ValueError('worker completion summary or output scope mismatch')
            bundle=json.loads((directory/'bundle.json').read_text(encoding='utf-8'))
            jobs.append({'skill':item['skill'],'title':item['title'],'url':item['url'],
                         'report':(directory.relative_to(root)/'REPORT.html').as_posix(),
                         'data_kind':bundle['data_kind'],'as_of_utc':bundle['as_of_utc']})
        cards=''.join(f'<article><h2>{escape(item["title"])}</h2><p>{escape(item["data_kind"])} · {escape(item["as_of_utc"])}</p><a href="{escape(item["report"],quote=True)}">打开研究报告 →</a></article>' for item in jobs)
        page=f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>跨市场研究工作台</title>
<style>body{{background:#0b101a;color:#e2eaf5;font:16px/1.7 system-ui;margin:0}}main{{max-width:1000px;margin:40px auto;padding:20px}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px}}article{{background:#121d2c;border:1px solid #2c3b52;padding:24px;border-radius:10px}}a{{color:#70dbc5}}p{{color:#aab7cc}}h1{{font-size:36px}}h2{{font-size:22px}}</style><main><p>SERENNITY007 / MARKET RESEARCH</p><h1>跨市场研究工作台</h1><p>四份独立的 synthetic 模拟报告。此页只导航，不汇总成买卖评分或组合收益。</p><div class="grid">{cards}</div></main></html>'''
        (root/'index.html').write_text(page,encoding='utf-8',newline='\n')
        (root/'COMPLETE.json').write_text(json.dumps({'status':'complete','reports':jobs},ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    except (ValueError,OSError,KeyError,TypeError) as exc:
        (root/'FAILURE.json').write_text(json.dumps({'status':'failed','error':str(exc),'completed_reports':jobs},ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
        raise
    return root


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--local-root',type=Path,required=True)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    try:
        directory=run(args.local_root,args.out)
    except (ValueError,OSError,KeyError,TypeError) as exc:
        parser.exit(2,f'ERROR: {exc}\n')
    print(f'PASS / 4 independent demos -> {directory / "index.html"}')


if __name__=='__main__':
    main()
