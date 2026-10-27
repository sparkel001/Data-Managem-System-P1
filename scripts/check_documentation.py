"""Check local documentation and evidence without importing the app or MongoDB.

Usage: python -m scripts.check_documentation [--submission] [--report PATH]
"""
import argparse
import ast
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]


def project_tree(base):
    """Source tree for readers; evidence and submission directories are summarized."""
    lines = ['survey_system/']
    top = [base/name for name in ['app','tests','scripts','docs','.env.example','requirements.txt','requirements-browser.txt','pytest.ini','run.py','README.md']]
    def walk(entries, prefix=''):
        entries=[p for p in entries if p.exists() and p.name!='__pycache__' and (not p.name.startswith('.') or p.name=='.env.example')]
        for index,p in enumerate(entries):
            last=index==len(entries)-1
            lines.append(prefix+('└── ' if last else '├── ')+p.name+('/' if p.is_dir() else ''))
            if p.is_dir():
                children=sorted((c for c in p.iterdir() if c.is_dir() and c.name!='__pycache__' or c.suffix in {'.py','.md','.js','.html','.css'}),key=lambda c:(not c.is_dir(),c.name))
                walk(children,prefix+('    ' if last else '│   '))
    walk(top)
    return '\n'.join(lines)


def verify(base):
    paths = [base / 'README.md', *sorted((base / 'docs').glob('*.md'))]
    failures = []
    links = 0
    forbidden = ['待填写', '待补充', '提交时注意', '为了兼容文档存在性', '还需要人工填写', '自动审批', '内部审批', '待验证']
    for path in paths:
        text = path.read_text(encoding='utf-8')
        prose = re.sub(r'```.*?```', '', text, flags=re.S)
        headings = re.findall(r'^# (.+)$', prose, re.M)
        if len(headings) != 1:
            failures.append(f'{path.name}: expected one document title')
        for word in forbidden:
            if word in text:
                failures.append(f'{path.name}: editorial placeholder {word}')
        for target in re.findall(r'\[[^\]\n]*\]\(([^)\n]+)\)', text):
            target = target.strip('<>')
            if re.match(r'^[a-zA-Z]+://', target) or target.startswith('mailto:'):
                continue
            filename, _, fragment = target.partition('#')
            destination = path.parent / unquote(filename) if filename else path
            links += 1
            if not destination.is_file():
                failures.append(f'{path.name}: missing link {target}')
            elif fragment and destination.suffix == '.md':
                titles = re.findall(r'^#{1,6}\s+(.+)$', destination.read_text(encoding='utf-8'), re.M)
                slugs = [re.sub(r'[^\w\-\s]', '', t.lower()).replace(' ', '-') for t in titles]
                if unquote(fragment) not in slugs:
                    failures.append(f'{path.name}: missing anchor {target}')
    # Every document has an entry in the primary project index.
    readme = (base / 'README.md').read_text(encoding='utf-8')
    for path in paths[1:]:
        if f'docs/{path.name}' not in readme:
            failures.append(f'README: missing index entry {path.name}')
    # The displayed tree contains real source/config files, not machine paths.
    tree = readme.split('```text', 1)[1].split('```', 1)[0]
    for name in re.findall(r'(\.?[A-Za-z_][A-Za-z0-9_.-]*\.(?:py|txt|ini|example))', tree):
        if not any(p.name == name for p in base.glob('**/' + name) if '.venv' not in p.parts):
            failures.append(f'README tree: missing {name}')
    if tree.strip() != project_tree(base).strip():
        failures.append('README source tree differs from current source inventory')
    # Confirm module/file targets occurring in documented PowerShell commands.
    for path in paths:
        for block in re.findall(r'```powershell\n(.*?)```', path.read_text(encoding='utf-8'), re.S):
            for module in re.findall(r'-m ([A-Za-z_][A-Za-z0-9_.]+)', block):
                if module.startswith(('tests.', 'scripts.', 'app.')):
                    if not (base / (module.replace('.', '/') + '.py')).is_file():
                        failures.append(f'{path.name}: missing module {module}')
            for name in re.findall(r'(?:tests/|scripts/)[A-Za-z0-9_./-]+\.py', block):
                if not (base / name).is_file():
                    failures.append(f'{path.name}: missing command target {name}')
    # Every actual API route has a table/path entry; health uses the shortened table form.
    api = (base / 'docs/API.md').read_text(encoding='utf-8')
    routes = 0
    for path in (base / 'app').glob('*.py'):
        tree = ast.parse(path.read_text(encoding='utf-8'))
        prefix = ''
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'APIRouter':
                prefix = next((ast.literal_eval(k.value) for k in node.keywords if k.arg == 'prefix'), '')
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name) and node.func.value.id in {'router','app'} and node.func.attr in {'get','post','put','delete'} and node.args and isinstance(node.args[0], ast.Constant):
                route = prefix + node.args[0].value
                if not route.startswith('/api/'):
                    continue
                routes += 1
                if route not in api and route.removeprefix('/api') not in api:
                    failures.append(f'API: undocumented {route}')
    evidence_counts = {}
    for name, count in [('coverage-audit/cases.json',114),('phase2/full.json',145),('registration-fix/full.json',151),('password-policy/full.json',162),('submission-20261027/full.json',175)]:
        report = json.loads((base / 'test-results' / name).read_text(encoding='utf-8'))
        counter = dict(Counter(c['status'] for c in report['cases']))
        evidence_counts[name] = {'executed_at':report['executed_at'],'counts':counter}
        if counter != {'passed':count}:
            failures.append(f'evidence: unexpected count {name}')
    manual = (base / 'docs/MANUAL_TESTS.md').read_text(encoding='utf-8')
    if manual.count('| 通过（用户报告') != 5 or manual.count('| 未执行 | 未执行（可选计划） |') != 6:
        failures.append('manual state changed')
    for name, number, pattern in [('TEST_CASES.md',114,r'^## AUTO-'),('TEST_CASES_PHASE2.md',175,r'^## P2-AUTO-')]:
        found = len(re.findall(pattern,(base/'docs'/name).read_text(encoding='utf-8'),re.M))
        if found != number:
            failures.append(f'{name}: {found} case sections, expected {number}')
    retained = (base/'docs/TEST_CASES_PHASE2.md').read_text(encoding='utf-8')
    complete = json.loads((base/'test-results/submission-20261027/full.json').read_text(encoding='utf-8'))
    specialists = [c for c in complete['cases'] if c['nodeid'].startswith(('tests/test_bank_copy_browser.py', 'tests/test_bank_copy_messages.py'))]
    if len(specialists) != 13:
        failures.append('specialist evidence count changed')
    for case in specialists:
        sections = [block for block in re.split(r'(?=^## P2-AUTO-)',retained,flags=re.M) if case['nodeid'] in block.split('\n',1)[0]]
        if len(sections)!=1 or any(case[k] not in sections[0] for k in ('preconditions','steps','inputs','expected')):
            failures.append('specialist content missing: '+case['nodeid'])
        elif json.dumps(case['parameters'],ensure_ascii=False,default=str) not in sections[0] or any(p['phase']+'='+p['outcome'] not in sections[0] for p in case['phases']):
            failures.append('specialist parameter or actual result missing: '+case['nodeid'])
    return {'documents':len(paths),'local_links':links,'api_route_declarations':routes,'evidence':evidence_counts,'failures':failures}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--submission',action='store_true')
    parser.add_argument('--report')
    args = parser.parse_args()
    result = {'project':verify(ROOT)}
    if args.submission:
        result['submission'] = verify(ROOT / 'submission')
        manifest = json.loads((ROOT/'submission/SUBMISSION_MANIFEST.json').read_text(encoding='utf-8'))
        mismatches=[]
        for entry in manifest['files']:
            source=ROOT/entry['path']; target=ROOT/'submission'/entry['path']
            if source.read_bytes()!=target.read_bytes() or hashlib.sha256(target.read_bytes()).hexdigest()!=entry['sha256']:
                mismatches.append(entry['path'])
        result['comparison']={'files':len(manifest['files']),'mismatches':mismatches}
    failed = any(v.get('failures') or v.get('mismatches') for v in result.values())
    if args.report:
        path=ROOT/args.report;path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False))
    raise SystemExit(1 if failed else 0)


if __name__=='__main__':main()
