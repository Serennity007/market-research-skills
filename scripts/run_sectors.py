#!/usr/bin/env python3
"""Generate the self-contained sector futures report from explicit dated inputs."""
import argparse
import csv
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import uuid

from sector_engine import analyze
from sector_reports import overview_html,sector_html,markdown
from market_io import timestamp
from bundle_integrity import verify,verify_source,write_completion


def csv_text(fields,rows):
    body=io.StringIO()
    writer=csv.DictWriter(body,fieldnames=fields,lineterminator='\n')
    writer.writeheader()
    writer.writerows(rows)
    return body.getvalue()


def load(config_path):
    config_path=Path(config_path).resolve()
    if config_path.name=='config.snapshot.json':
        verify(config_path.parent)
    elif config_path.name=='config.json' and (config_path.parent/'SOURCE_COMPLETE.json').exists():
        verify_source(config_path.parent)
    config_raw=config_path.read_bytes()
    config=json.loads(config_raw.decode('utf-8-sig'))
    catalog_raw=(config_path.parent/config['catalog']).read_bytes()
    catalog=json.loads(catalog_raw.decode('utf-8-sig'))
    if set(config['files'])-{'panel','evidence','curves'} or 'panel' not in config['files']:
        raise ValueError('input roles must be panel and optional evidence/curves')
    raw={role:(config_path.parent/value).read_bytes() for role,value in config['files'].items()}
    sources={}
    for role in raw:
        if config['data_kind']=='synthetic':
            sources[role]={'name':'Constructed sector exercise','url':'synthetic://local'}
        else:
            source=config.get('sources',{}).get(role)
            if not isinstance(source,dict) or not str(source.get('name','')).strip() or 'retrieved_at' not in source:
                raise ValueError(f'{role}: source name and retrieved_at required for imported observations')
            timestamp(source['retrieved_at'])
            sources[role]=source
    result=analyze(config,catalog,raw['panel'],raw.get('evidence'),raw.get('curves'))
    result.update(sources=sources,catalog_sha256=hashlib.sha256(catalog_raw).hexdigest(),
                  config_sha256=hashlib.sha256(config_raw).hexdigest())
    return config,catalog_raw,raw,result


def run(config_path,output):
    config,catalog_raw,raw,result=load(config_path)
    result['generated_at_utc']=datetime.now(timezone.utc).isoformat()
    root=Path(output)/('sectors-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')+'-'+uuid.uuid4().hex[:8])
    artifacts={'index.html':overview_html(result),'REPORT.md':markdown(result),
               'bundle.json':json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)+'\n'}
    rows=[]
    for board in result['sectors']:
        for key,values in board['windows'].items():
            rows.append(dict(sector=board['id'],sector_name=board['name'],window=key,start_date=result['windows'][key]['start_date'],
                             end_date=result['trade_date'],**values))
        artifacts['sectors/'+board['id']+'.html']=sector_html(board,result)
    fields=['sector','sector_name','window','start_date','end_date','expected_products','observed_products','coverage','eligible_for_ranking','sample_equal_weight_price_return','advancing','declining','unchanged','rank']
    artifacts['sector_returns.csv']=csv_text(fields,rows)
    fields=['symbol','name','sector','exchange','contract','currency','unit','window','start_date','end_date','price_return','unavailable_reason']
    rows=[]
    for item in result['products']:
        for key,value in item['windows'].items():
            rows.append({**{field:item[field] for field in fields[:7]},'window':key,
                         **{field:value[field] for field in fields[8:]}})
    artifacts['products.csv']=csv_text(fields,rows)
    snapshot=dict(config,catalog='inputs/catalog.json',files={role:f'inputs/{role}.csv' for role in raw})
    artifacts['config.snapshot.json']=json.dumps(snapshot,ensure_ascii=False,indent=2)+'\n'
    root.mkdir(parents=True,exist_ok=False)
    (root/'inputs').mkdir()
    (root/'inputs/catalog.json').write_bytes(catalog_raw)
    for role,content in raw.items():
        (root/'inputs'/f'{role}.csv').write_bytes(content)
    for name,body in artifacts.items():
        path=root/name
        path.parent.mkdir(parents=True,exist_ok=True)
        with path.open('x',encoding='utf-8',newline='\n') as handle:
            handle.write(body)
    write_completion(root,result)
    return root


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config',type=Path,required=True)
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--json',action='store_true')
    args=parser.parse_args()
    try:
        directory=run(args.config,args.out)
    except (ValueError,OSError,KeyError,TypeError) as exc:
        parser.exit(2,f'ERROR: {exc}\n')
    if args.json:
        print(json.dumps({'status':'complete','skill':'taotao-futures-research','directory':str(directory.resolve())},ensure_ascii=True))
    else:
        print(f'PASS / sector report -> {directory / "index.html"}')


if __name__=='__main__':
    main()
