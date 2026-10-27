"""Build an honest per-case document from this run's pytest evidence."""
import json
import copy
import argparse
from pathlib import Path


def main():
    root=Path(__file__).resolve().parents[1]
    parser=argparse.ArgumentParser()
    parser.add_argument('--evidence-dir', default='test-results/submission-20261027')
    parser.add_argument('--output', default='docs/TEST_CASES_PHASE2.md')
    args=parser.parse_args()
    evidence=root/args.evidence_dir
    full=json.loads((evidence/'full.json').read_text(encoding='utf-8'))
    full=copy.deepcopy(full)
    for case in full['cases']:
        if case['nodeid'].endswith('::test_documentation_present'):
            case['inputs']='当时检查七份文档与配置示例；历史报告索引现并入README，当前文档检查改为完整阶段报告。原始输入保留于JSON证据。'
    lines=['# 完整问卷与题库系统自动化用例及结果','',
           '本文列出所选完整运行的逐项输入、预期、实际和状态。证据生成不重新执行测试；运行之后新增的文档测试不冒充已经包含在本次全量中。', '',
           f'本文件由 `scripts/build_phase2_test_docs.py` 从 `{args.evidence_dir}/full.json` 生成；仅该目录代表本页所列运行。',
           '全部P2-AUTO编号均为自动化；用户报告检查及未执行的可选计划见[MANUAL_TESTS.md](MANUAL_TESTS.md)。各次测试时间和范围见[TEST_RESULTS.md](TEST_RESULTS.md)。',
           f'最终运行证据时间：{full["executed_at"]}。','',
           '| 运行记录 | 通过 | 失败 | 跳过 | 未运行 |','|---|---:|---:|---:|---:|']
    for path in [evidence/'baseline.json', evidence/'related.json', *sorted(evidence.glob('block*.json')), evidence/'full.json']:
        if not path.exists(): continue
        result=json.loads(path.read_text(encoding='utf-8'))
        counts={s:sum(c['status']==s for c in result['cases']) for s in ('passed','failed','skipped','not_run')}
        lines.append('| '+path.name+' | '+' | '.join(str(v) for v in counts.values())+' |')
    lines.extend(['',f'第一阶段独立浏览器脚本的结果另见 `{args.evidence_dir}/browser-phase1.json`（若存在），不计入pytest数量。',
                  '以下逐项列出最终全量运行的所有用例，包括保留的第一阶段用例。参数化实例单独列出；真实断言在所列测试函数中。',''])
    for index,c in enumerate(full['cases'],1):
        browser='browser' in c['nodeid']
        kind='自动化浏览器集成测试（真实Edge）' if browser else c['type']
        lines.extend([f'## P2-AUTO-{index:03d} · {c["nodeid"]}','',
                      f'- 测试类型：{kind}',f'- 前置条件：{c["preconditions"]}',
                      f'- 操作步骤：{c["steps"]}',f'- 输入数据：{c["inputs"]}',
                      '- 参数实例：`'+json.dumps(c['parameters'],ensure_ascii=False,default=str)+'`',
                      f'- 预期结果：{c["expected"]}',
                      f'- 实际结果：pytest {c["status"]}；阶段状态为 '+', '.join(p['phase']+'='+p['outcome'] for p in c['phases']),
                      '- 是否通过：'+('是' if c['status']=='passed' else '否' if c['status']=='failed' else '未判定'),
                      f'- 隔离数据库：{c["database"] or "本地纯函数/文件检查，不连接业务库"}',''])
        for phase in c['phases']:
            if phase['failure']:lines.extend(['```text',phase['failure'],'```',''])
        if c['observations']: lines.extend(['实际观察：','```json',json.dumps(c['observations'],ensure_ascii=False,indent=2),'```',''])
    output=root/args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text('\n'.join(lines)+'\n',encoding='utf-8')


if __name__=='__main__':main()
