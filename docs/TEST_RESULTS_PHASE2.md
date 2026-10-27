# 第二阶段测试结果与验证范围

本文汇总已保存的原始JSON/XML运行结果，并区分自动化测试、独立browser_demo和项目作者报告的人工检查。最近完整pytest运行时间为2026-10-27。后续文稿修订未产生新的业务测试结果。不同运行范围存在重叠，不相加作为独立测试总数。

## 最近保存的完整运行

| 项目 | 实际记录 | 证据 |
|---|---|---|
| 完整pytest | 175通过、0失败、0跳过；176.307秒 | test-results/submission-20261027/full.json及full.xml |
| 其中的浏览器测试 | 3项，已包含在175项中 | test_auth_browser、test_bank_copy_browser、test_phase2_block7_browser对应实例 |
| 独立browser_demo | 1通过、0失败，不计入175项 | test-results/submission-20261027/browser-phase1.json |
| 人工检查 | 5项，由项目作者执行并报告完成，日期和详细环境未记录 | MANUAL_TESTS.md及项目对话 |

175项中有172项非浏览器pytest实例、3项浏览器pytest实例。按完整nodeid对比，第一阶段coverage-audit/cases.json中的114个实例均在该次175项中出现且通过，另外61项属于该次新增或扩展实例。该关系按实例标识确认，不代表测试源码未变化。用例文档P2-AUTO-001至P2-AUTO-175连续且唯一，对应整次运行而非仅表示第二阶段新功能。

浏览器测试为自动操作，独立browser_demo为另一次自动化流程，人工检查为项目作者的报告；三类证据不相加。课程要求的创建问卷、添加题目、跳转、校验、提交、统计均有自动化用例及运行依据；六项可选人工演示计划仍为“未执行（可选计划）”，不表示课程自动化测试尚待完成。

## 历史运行与范围

每行只表示该次保存的结果；“全量”按该次代码及用例集合定义。日期和失败数保留原始证据，不用本轮文稿修改覆盖。

| 证据时间（UTC+08:00） | 范围 | 通过 | 失败 | 跳过 | 原始证据 |
|---|---|---:|---:|---:|---|
| 2026-10-22T13:51:06.859911+08:00 | 题库扩展实施前基线 | 113 | 1 | 0 | `test-results/phase2/baseline.json` |
| 2026-10-22T14:05:36.924807+08:00 | 题库扩展实现后完整运行 | 145 | 0 | 0 | `test-results/phase2/full.json` |
| 2026-10-26T18:26:04.348313+08:00 | 认证页面专项 | 3 | 0 | 0 | `test-results/auth-20261026/auth.json` |
| 2026-10-26T18:29:16.185734+08:00 | 认证页面变更后全量 | 146 | 0 | 0 | `test-results/auth-20261026/full.json` |
| 2026-10-26T18:56:11.275329+08:00 | 注册完整性专项 | 8 | 0 | 0 | `test-results/registration-fix/auth.json` |
| 2026-10-26T18:58:53.459938+08:00 | 注册完整性变更后全量 | 151 | 0 | 0 | `test-results/registration-fix/full.json` |
| 2026-10-26T23:44:07.207796+08:00 | 密码兼容专项 | 19 | 0 | 0 | `test-results/password-policy/auth.json` |
| 2026-10-26T23:47:37.470678+08:00 | 密码调整后全量 | 162 | 0 | 0 | `test-results/password-policy/full.json` |
| 2026-10-27T00:10:18.448186+08:00 | 复制与提示后端专项 | 20 | 0 | 0 | `test-results/bank-copy-messages/targeted.json` |
| 2026-10-27T00:12:15.777238+08:00 | 复制与提示浏览器首轮 | 2 | 1 | 0 | `test-results/bank-copy-messages/browser.json` |
| 2026-10-27T00:12:56.253370+08:00 | 修正测试等待后重跑 | 1 | 0 | 0 | `test-results/bank-copy-messages/browser-rerun.json` |
| 2026-10-27T00:17:51.248745+08:00 | 复制与提示修复后全量 | 175 | 0 | 0 | `test-results/bank-copy-messages/full.json` |
| 2026-10-27T00:25:17.292211+08:00 | 完整验证前相关测试 | 30 | 0 | 0 | `test-results/submission-20261027/related.json` |
| 2026-10-27T00:29:14.976873+08:00 | 最近保存的完整业务验证 | 175 | 0 | 0 | `test-results/submission-20261027/full.json` |
| 2026-10-27T00:37:18.536584+08:00 | 文档存在性与离线页检查 | 2 | 0 | 0 | `test-results/submission-20261027/docs.json` |
| 2026-10-27T01:13:50.470976+08:00 | 文档及可选计划相关回归 | 7 | 0 | 0 | `test-results/docs-final-20261027/related.json` |
| 2026-10-27T01:32:57.335460+08:00 | 文档生成器回归 | 4 | 0 | 0 | `test-results/registration-docs-20261027/related.json` |

第一阶段的原始结果与失败修正过程见[TEST_RESULTS.md](TEST_RESULTS.md)，正文保持原样。当前完整用例见[TEST_CASES_PHASE2.md](TEST_CASES_PHASE2.md)。

## 失败、复测和警告

题库扩展基线113通过、1失败源于文档缺失，补齐当时缺失文档后继续实施。复制入口浏览器首轮2通过、1失败，原因是新增测试在候选列表异步加载前断言数量；只修正测试等待，单例重跑1通过，再执行175项全量通过。失败、重跑JSON/XML保留于test-results/phase2和test-results/bank-copy-messages，不将失败记录删除或替换为后续成功。

既有文档与生成器回归记录分别为5通过、7通过，原始JSON/XML位于test-results/documentation-review-20261027和test-results/documentation-consolidation-20261027。这些是独立的历史文档检查，不计入175项业务运行；工具误报及修正细节见下文的核验记录。

既有pytest记录保留一项Starlette/httpx弃用警告。已有pip check输出为No broken requirements found。相关命令和阶段结果保留在已有证据及[AI使用日志](AI_USAGE_PHASE2.md)中。

## 数据库及迁移验证范围

完整验证使用27018独立MongoDB服务，后续定向回归使用27019；每例数据库名为survey_system_test_后接32位UUID。测试不继承业务MONGODB_DATABASE，结束只清理自己的测试库。

迁移相关的两个实际用例为test_additive_repeat_legacy和test_migration_retry_and_validation：在隔离库重复执行迁移并比较原四集合，验证旧接口读取、故障注入后恢复及非法结构拒绝。2026-10-22的block1.json共4通过，另外两项是离线文档和文档存在性检查，不能全部称作迁移测试。这些隔离库测试不能证明实际运行库的初始化状态或迁移验收情况；部署语义见[MIGRATION_PHASE2.md](MIGRATION_PHASE2.md)。

## 人工检查与可选计划

五项作者报告的结果及六项可选计划集中在[MANUAL_TESTS.md](MANUAL_TESTS.md)。数字121拒绝、20成功没有附完整题目配置，不能据此推断上限；页面无问题的报告限于实际检查范围。计划所用输入和操作顺序与自动化断言的差异继续逐项保留，未执行的计划不写为通过。

## 文稿核验记录

文档工具的检查范围、历史退出结果、生成器覆盖风险及原稿保护、链接和归档摘要等维护核验，集中见[文稿恢复核验记录](../test-results/phase1-document-restoration-20261027/DOCUMENT_RESTORATION_PHASE2.md)。旧检查器的范围或固定措辞不匹配未被记为通过，也不计入业务测试失败数；相关原始记录保留。文稿修订及静态文件核验不产生新的业务测试结果。
