"""Check frozen research bundles; hashes detect changes, not source authenticity."""
import argparse
import hashlib
import json
from pathlib import Path
from market_io import timestamp


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def file_inside(root,name):
    if not isinstance(name,str) or not name or '\\' in name or ':' in name or name.startswith('/') or '..' in Path(name).parts:
        raise ValueError('unsafe artifact path')
    path=(root/name).resolve()
    if not path.is_relative_to(root.resolve()) or not path.is_file():
        raise ValueError(f'missing or escaping artifact: {name}')
    return path


def write_completion(root,result):
    root=Path(root)
    hashes={path.relative_to(root).as_posix():digest(path.read_bytes()) for path in sorted(root.rglob('*')) if path.is_file() and path.name!='COMPLETE.json'}
    body={'schema_version':2,'status':'complete','data_kind':result['data_kind'],
          'configured_products':result['configured_product_count'],'sha256':hashes}
    (root/'COMPLETE.json').write_text(json.dumps(body,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')


def verify(root):
    root=Path(root).resolve()
    complete=json.loads((root/'COMPLETE.json').read_text(encoding='utf-8'))
    if complete.get('status')!='complete':
        raise ValueError('bundle is not marked complete')
    version=complete.get('schema_version',1)
    if version not in (1,2):
        raise ValueError('unsupported completion manifest version')
    if version==2:
        hashes=complete.get('sha256')
        if not isinstance(hashes,dict) or not hashes:
            raise ValueError('completion manifest has no artifact hashes')
        mandatory={'bundle.json','config.snapshot.json','index.html','REPORT.md','products.csv','sector_returns.csv','inputs/catalog.json'}
        if not mandatory.issubset(hashes):
            raise ValueError('completion manifest omits required artifacts')
        for name,expected in hashes.items():
            if digest(file_inside(root,name).read_bytes())!=expected:
                raise ValueError(f'artifact hash mismatch: {name}')
        actual={path.relative_to(root).as_posix() for path in root.rglob('*') if path.is_file() and path!=root/'COMPLETE.json'}
        if actual!=set(hashes):
            raise ValueError('bundle contains unlisted or missing artifacts')
    data=json.loads((root/'bundle.json').read_text(encoding='utf-8'))
    if data.get('skill')!='taotao-futures-research':
        raise ValueError('not a sector-research bundle')
    for role,expected in data['source_sha256'].items():
        if role not in ('panel','evidence','curves'):
            raise ValueError('unexpected input role')
        name=f'inputs/{role}.csv'
        if version==2 and name not in hashes:
            raise ValueError('input is missing from completion manifest')
        if digest(file_inside(root,name).read_bytes())!=expected:
            raise ValueError(f'input hash mismatch: {role}')
    if digest(file_inside(root,'inputs/catalog.json').read_bytes())!=data['catalog_sha256']:
        raise ValueError('catalog hash mismatch')
    config=json.loads((root/'config.snapshot.json').read_text(encoding='utf-8'))
    expected_files={role:f'inputs/{role}.csv' for role in data['source_sha256']}
    if config.get('files')!=expected_files or config.get('catalog')!='inputs/catalog.json':
        raise ValueError('replay config does not point to frozen inputs')
    if config.get('data_kind')!=data['data_kind'] or config.get('trade_date')!=data['trade_date']:
        raise ValueError('bundle/config research identity mismatch')
    for field in ('as_of','windows','universe'):
        if field not in config:
            raise ValueError('incomplete replay config')
    if timestamp(config['as_of'])!=timestamp(data['as_of_utc']) or config['windows']!=data['windows']:
        raise ValueError('bundle/config cutoff or comparison windows mismatch')
    return {'status':'verified','manifest_version':version,'verified_artifacts':len(complete.get('sha256',{})),
            'input_roles':sorted(expected_files),'assurance':'local consistency, not independent authenticity'}


def verify_source(root):
    root=Path(root).resolve()
    data=json.loads((root/'SOURCE_COMPLETE.json').read_text(encoding='utf-8'))
    if data.get('status')!='complete' or data.get('data_kind')!='imported_observations':
        raise ValueError('not a completed source snapshot')
    for name,key in [('panel.csv','panel_sha256'),('catalog.json','catalog_sha256'),('request.snapshot.json','request_sha256')]:
        if digest(file_inside(root,name).read_bytes())!=data[key]:
            raise ValueError(f'source snapshot hash mismatch: {name}')
    for item in data['sources']:
        if digest(file_inside(root,item['raw_file']).read_bytes())!=item['raw_sha256']:
            raise ValueError('raw provider response changed')
    if 'config_sha256' in data and digest(file_inside(root,'config.json').read_bytes())!=data['config_sha256']:
        raise ValueError('source snapshot config changed')
    config=json.loads(file_inside(root,'config.json').read_text(encoding='utf-8'))
    if config.get('files')!={'panel':'panel.csv'} or config.get('catalog')!='catalog.json' or config.get('data_kind')!='imported_observations':
        raise ValueError('source config does not point to the recorded snapshot')
    if config.get('trade_date')!=data['common_trade_date'] or timestamp(config['as_of'])<max(timestamp(item['retrieved_at']) for item in data['sources']):
        raise ValueError('source config cutoff precedes recorded retrieval')
    return {'status':'verified','source_count':len(data['sources']),'assurance':'stored response consistency, not exchange authentication'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory',type=Path)
    args=parser.parse_args()
    try:
        result=verify(args.directory) if (args.directory/'COMPLETE.json').exists() else verify_source(args.directory)
    except (ValueError,OSError,KeyError,TypeError) as exc:
        parser.exit(2,f'ERROR: {exc}\n')
    print(json.dumps(result,ensure_ascii=False))


if __name__=='__main__':
    main()
