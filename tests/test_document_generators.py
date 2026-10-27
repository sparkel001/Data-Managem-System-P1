"""File-only regressions: no MongoDB fixture or connection."""
import json
from pathlib import Path
from scripts import build_test_audit_docs as audit


def test_preserve_user_manual_records(tmp_path, monkeypatch):
    (tmp_path / 'docs').mkdir()
    target = tmp_path / 'docs/MANUAL_TESTS.md'
    original = '# 人工检查\n通过（用户报告）；可选计划未执行。\n'
    target.write_text(original, encoding='utf-8')
    monkeypatch.setattr(audit, 'ROOT', tmp_path)
    audit.build_manual_plan()
    assert target.read_text(encoding='utf-8') == original


def test_generated_cases_do_not_infer_manual_status():
    report = json.loads((audit.EVIDENCE / 'cases.json').read_text(encoding='utf-8'))
    result = audit.build_cases(report)
    assert '已执行手工测试数量为0' not in result
    assert '[MANUAL_TESTS.md](MANUAL_TESTS.md)' in result
    assert '[TEST_CASES_PHASE2.md](TEST_CASES_PHASE2.md)' in result


def test_generator_preserves_later_results(tmp_path, monkeypatch):
    (tmp_path / 'docs').mkdir()
    target = tmp_path / 'docs/TEST_RESULTS.md'
    original = '# 已有结果\n## 本轮课程六类测试逐项审计\n旧记录\n## 后续验证\n175通过；人工检查另列。\n'
    target.write_text(original, encoding='utf-8')
    (tmp_path / 'docs/MANUAL_TESTS.md').write_text('用户报告检查', encoding='utf-8')
    evidence = tmp_path / 'evidence'
    evidence.mkdir()
    report = json.loads((audit.EVIDENCE / 'cases.json').read_text(encoding='utf-8'))
    (evidence / 'cases.json').write_text(json.dumps(report), encoding='utf-8')
    monkeypatch.setattr(audit, 'ROOT', tmp_path)
    monkeypatch.setattr(audit, 'EVIDENCE', evidence)
    monkeypatch.setattr(audit, 'business_unchanged', lambda: [])
    audit.main()
    assert target.read_text(encoding='utf-8').startswith(original.rstrip())
    assert (tmp_path / 'docs/MANUAL_TESTS.md').read_text(encoding='utf-8') == '用户报告检查'


def test_phase2_generator_uses_selected_evidence_and_output(tmp_path, monkeypatch):
    import sys
    from scripts import build_phase2_test_docs as phase2
    evidence = Path(__file__).parents[1] / 'test-results/submission-20261027'
    output = tmp_path / 'cases.md'
    manual = Path(__file__).parents[1] / 'docs/MANUAL_TESTS.md'
    before = manual.read_bytes()
    monkeypatch.setattr(sys, 'argv', ['build_phase2_test_docs', '--evidence-dir', str(evidence), '--output', str(output)])
    phase2.main()
    result = output.read_text(encoding='utf-8')
    assert result.count('## P2-AUTO-') == 175
    assert '| full.json | 175 | 0 | 0 | 0 |' in result
    assert '[MANUAL_TESTS.md](MANUAL_TESTS.md)' in result
    assert '均未执行' not in result
    assert manual.read_bytes() == before


def test_specialist_cases_preserved_in_complete_document():
    import re
    root = Path(__file__).parents[1]
    original = json.loads((root/'test-results/bank-copy-messages/full.json').read_text(encoding='utf-8'))
    complete = json.loads((root/'test-results/submission-20261027/full.json').read_text(encoding='utf-8'))
    by_node = {c['nodeid']: c for c in complete['cases']}
    rendered = (root/'docs/TEST_CASES_PHASE2.md').read_text(encoding='utf-8')
    selected = [c for c in original['cases'] if c['nodeid'].startswith(('tests/test_bank_copy_browser.py', 'tests/test_bank_copy_messages.py'))]
    assert len(selected) == 13
    for case in selected:
        target = by_node[case['nodeid']]
        for field in ['preconditions', 'steps', 'inputs', 'parameters', 'expected', 'status']:
            assert case[field] == target[field]
        assert [(p['phase'], p['outcome']) for p in case['phases']] == [(p['phase'], p['outcome']) for p in target['phases']]
        sections = [part for part in re.split(r'(?=^## P2-AUTO-)', rendered, flags=re.M) if case['nodeid'] in part.split('\n', 1)[0]]
        assert len(sections) == 1
        for field in ['preconditions', 'steps', 'inputs', 'expected']:
            assert case[field] in sections[0]
        assert json.dumps(case['parameters'], ensure_ascii=False) in sections[0]
        for phase in case['phases']:
            assert phase['phase']+'='+phase['outcome'] in sections[0]
        assert '是否通过：是' in sections[0]


def test_source_tree_uses_actual_files_and_omits_cache(tmp_path):
    from scripts.check_documentation import project_tree
    (tmp_path/'app').mkdir()
    (tmp_path/'app/main.py').write_text('# entry', encoding='utf-8')
    (tmp_path/'app/__pycache__').mkdir()
    (tmp_path/'app/__pycache__/main.pyc').write_bytes(b'cache')
    (tmp_path/'app/static').mkdir()
    (tmp_path/'app/static/index.html').write_text('<html>', encoding='utf-8')
    (tmp_path/'README.md').write_text('# project', encoding='utf-8')
    tree = project_tree(tmp_path)
    assert 'main.py' in tree and 'static/' in tree and 'index.html' in tree
    assert '__pycache__' not in tree and 'main.pyc' not in tree
    assert 'does_not_exist.py' not in tree
