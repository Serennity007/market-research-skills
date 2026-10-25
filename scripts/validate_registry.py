#!/usr/bin/env python3
"""Validate a navigation manifest, optionally checking independently cloned skill roots."""
import argparse
import json
from pathlib import Path
import re

DEFAULT = Path(__file__).resolve().parents[1] / 'registry.json'


def relative_file(value):
    if not isinstance(value,str) or not value or '\\' in value:
        raise ValueError('repository path must be a nonempty POSIX relative file')
    path=Path(value)
    if value.startswith('/') or path.is_absolute() or '..' in path.parts or ':' in value:
        raise ValueError('repository path must stay inside its repository')
    return path


def validate(data, local_root=None):
    if data.get('schema_version') != 1 or not isinstance(data.get('skills'),list) or not data['skills']:
        raise ValueError('schema_version=1 and a nonempty skills list required')
    owner=data.get('owner','')
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9-]*',owner):
        raise ValueError('invalid owner')
    skills,repos=set(),set()
    for item in data['skills']:
        skill,repo=item.get('skill',''),item.get('repository','')
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',skill) or skill != repo:
            raise ValueError('each skill name must match its independent repository')
        if skill in skills or repo in repos:
            raise ValueError('duplicate skill or repository')
        skills.add(skill)
        repos.add(repo)
        if item.get('url') != f'https://github.com/{owner}/{repo}':
            raise ValueError('URL must match owner/repository exactly')
        if item.get('entrypoint') != 'SKILL.md' or item.get('demo_data_kind') != 'synthetic':
            raise ValueError('entrypoint and demo provenance required')
        scripts=item.get('scripts')
        if not isinstance(scripts,list) or not scripts or len(scripts)!=len(set(scripts)):
            raise ValueError('declare unique nonempty script paths')
        files=[relative_file(item['entrypoint']),*[relative_file(value) for value in scripts]]
        if local_root is not None:
            root=(Path(local_root)/repo).resolve()
            for path in files:
                resolved=(root/path).resolve()
                if not resolved.is_relative_to(root) or not resolved.is_file():
                    raise ValueError(f'missing or escaping file: {repo}/{path}')
            text=(root/'SKILL.md').read_text(encoding='utf-8')
            if not re.search(r'^name:\s*'+re.escape(skill)+r'\s*$',text,re.M):
                raise ValueError(f'SKILL.md name mismatch: {repo}')
    return len(skills)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest',type=Path,default=DEFAULT)
    parser.add_argument('--local-root',type=Path)
    args=parser.parse_args()
    try:
        count=validate(json.loads(args.manifest.read_text(encoding='utf-8')),args.local_root)
    except (ValueError,OSError,KeyError,TypeError) as exc:
        parser.exit(2,f'ERROR: {exc}\n')
    print(f'Validated {count} independent skills; remote availability not checked.')


if __name__=='__main__':
    main()
