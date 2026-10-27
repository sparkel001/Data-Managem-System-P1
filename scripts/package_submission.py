"""Build a source/document/evidence archive without local environments or data."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
TOP_FILES = {'.env.example', '.gitignore', 'README.md', 'requirements.txt',
             'requirements-browser.txt', 'pytest.ini', 'run.py'}
SOURCE_DIRS = {'app', 'tests', 'scripts', 'docs'}
EVIDENCE_DIRS = {'coverage-audit', 'phase2', 'auth-20261026', 'registration-fix',
                 'password-policy', 'bank-copy-messages', 'submission-20261027',
                 'docs-final-20261027', 'registration-docs-20261027', 'documentation-review-20261027', 'documentation-consolidation-20261027'}
EXTENSIONS = {'.py', '.js', '.html', '.css', '.md', '.json', '.xml', '.png'}
EXCLUDED_PARTS = {'.venv', '__pycache__', '.pytest_cache', '.git', 'mongo-data', 'local-data', 'submission'}


def selected_files():
    for p in sorted(ROOT.rglob('*')):
        rel = p.relative_to(ROOT)
        if not p.is_file() or p.is_symlink() or any(part in EXCLUDED_PARTS for part in rel.parts):
            continue
        if rel.as_posix() in TOP_FILES:
            yield p, rel
        elif rel.parts[0] in SOURCE_DIRS and p.suffix in EXTENSIONS and not p.name.startswith('.'):
            yield p, rel
        elif len(rel.parts) == 3 and rel.parts[0] == 'test-results' and rel.parts[1] in EVIDENCE_DIRS and p.suffix in {'.json', '.xml', '.png'}:
            yield p, rel


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',default='submission/survey_system_phase2_20261027.zip')
    args=parser.parse_args()
    destination=ROOT/args.output
    if destination.exists(): raise SystemExit('Output already exists; choose a new name. Nothing overwritten.')
    required={'app/main.py','app/static/messages.js','tests/conftest.py','tests/mongo_config.py',
              'docs/REPORT_PHASE2.md','docs/TEST_CASES_PHASE2.md','docs/AI_USAGE_PHASE2.md',
              'docs/TEST_RESULTS.md','test-results/submission-20261027/full.json'}
    files=list(selected_files()); names={r.as_posix() for _,r in files}
    if required-names: raise SystemExit('Missing required files: '+str(sorted(required-names)))
    # Only build a passing, fully executed submission from the actual run.
    evidence=json.loads((ROOT/'test-results/submission-20261027/full.json').read_text(encoding='utf-8'))
    if not evidence['cases'] or any(c['status']!='passed' for c in evidence['cases']):
        raise SystemExit('Full test evidence contains failed/skipped/unexecuted cases; inspect before packaging.')
    manifest={'format':1,'root':'survey_system','test_evidence':'test-results/submission-20261027/full.json',
              'files':[{'path':r.as_posix(),'size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p,r in files],
              'excluded':'Virtual environments, caches, Git metadata, .env, database physical files, logs, cancelled diagnostic artifacts, old archives and unrelated workspace documents.'}
    destination.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(destination,'x',compression=zipfile.ZIP_DEFLATED) as archive:
        for p,r in files: archive.write(p,'survey_system/'+r.as_posix())
        archive.writestr('survey_system/SUBMISSION_MANIFEST.json',json.dumps(manifest,ensure_ascii=False,indent=2))
    with zipfile.ZipFile(destination) as archive:
        assert archive.testzip() is None
        for entry in manifest['files']:
            assert hashlib.sha256(archive.read('survey_system/'+entry['path'])).hexdigest()==entry['sha256']
    digest=hashlib.sha256(destination.read_bytes()).hexdigest()
    destination.with_suffix('.zip.sha256').write_text(digest+'  '+destination.name+'\n',encoding='ascii')
    print(json.dumps({'archive':str(destination),'files':len(files)+1,'bytes':destination.stat().st_size,'sha256':digest},ensure_ascii=False))


if __name__=='__main__': main()
