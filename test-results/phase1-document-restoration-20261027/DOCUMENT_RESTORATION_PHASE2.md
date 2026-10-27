# 第一阶段文稿恢复与第二阶段材料分离核验

本文说明按用户提供的“第一阶段.zip”恢复原始文稿的范围、摘要、文稿分离方案及现有文档工具冲突。它属于第二阶段材料维护记录，不改写或替代第一阶段原文。

## 权威来源及保护范围

权威来源为第一阶段完整项目ZIP，项目根前缀为Data-Managem-System-P1-main/survey_system/。扫描发现八份第一阶段Markdown文稿以及README。README按当前项目单独编写，八份文稿从ZIP读取原始字节并写回，不经过编码、换行或格式转换。

第一阶段证据包括十份JSON/XML测试记录及一张浏览器截图；恢复前它们已与ZIP一致，保持原样。app中的HTML是运行页面，依赖清单与pytest.ini是配置，按本次不改程序和配置的要求仅核对，不从旧包覆盖当前版本。

## 第二阶段增量材料

新增API_PHASE2.md、DATABASE_PHASE2.md、LOGIC_PHASE2.md及TEST_RESULTS_PHASE2.md，分别承接原合并文档中的扩展接口、数据结构、逻辑和测试记录，不复制整篇基础设计。原第二阶段AI日志、实验报告、用例和迁移文档继续独立保存；MANUAL_TESTS.md不在第一阶段ZIP中，保留其五项用户报告和六项未执行计划的来源边界。

README及第二阶段文稿更新引用；第一阶段链接、提示词、日期、测试数量、人工参与记录和措辞均不更改。部分原稿仍保留其当时状态，这是原始记录，不视为当前新增功能说明。

## 原样恢复清单

以下文件的ZIP内容、当前项目与submission对应文件应逐字节相等。完整SHA-256及检查结果列于下方。

| 文件 | SHA-256（ZIP原文） | 核验方式 |
|---|---|---|
| docs/AI_USAGE_LOG.md | `59ec091e47e24de39b8a870d41dc38d3f33715588ee5fcabd449a396e5cd349e` | 原始字节与项目、提交副本比较 |
| docs/API.md | `ea0340896c33c1beaeead732e6b2eb09bb27a6231b5b5220986bb258ecd0eb23` | 原始字节与项目、提交副本比较 |
| docs/DATABASE.md | `25172af76d02d99daddec0c74b3368b8c8adcff7c2428c7706b508d45fb97872` | 原始字节与项目、提交副本比较 |
| docs/LOGIC.md | `152cc8a43a19b81d960ec1fb82b909b2b45d9aa9d06f70aa8dedc9ba909adee7` | 原始字节与项目、提交副本比较 |
| docs/REPORT.md | `c7e59ec8c496c011e32e0592b6d716adab1582afef1d1b44a581f80040221715` | 原始字节与项目、提交副本比较 |
| docs/TEST_CASES.md | `e98dbe1d09a871444ecc9cffdeea99e8116a4701bef5b37fe7069b098975b8ac` | 原始字节与项目、提交副本比较 |
| docs/TEST_COVERAGE_AUDIT.md | `86eb1ed2c622a7bb88295af252c48e28090f1723575aea7fbde1eb2949e8d39b` | 原始字节与项目、提交副本比较 |
| docs/TEST_RESULTS.md | `312549cec876fe3d0c846ee969f325bf4a5dbee18eb628331b881127e781340d` | 原始字节与项目、提交副本比较 |


## 实际文档检查与工具冲突

实际执行的pytest命令仅检查文档存在性，不使用数据库夹具：

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_block9.py::test_documentation_present -q -p no:cacheprovider --junitxml=test-results/phase1-document-restoration-20261027/docs.xml --audit-report=test-results/phase1-document-restoration-20261027/docs.json
```

结果为1通过、0失败、0跳过，0.08秒，保留一项Starlette/httpx弃用警告。未运行完整业务测试、浏览器测试或生成器回归；尤其未执行会在临时目录调用基础生成器的test_generator_preserves_later_results。

只读旧校验命令：

```powershell
python -m scripts.check_documentation --report test-results/phase1-document-restoration-20261027/legacy-checker.json
```

该命令实际退出码1，报告22处新增路由声明缺失。原因是scripts/check_documentation.py只检查第一阶段API.md，尚不读取独立API_PHASE2.md。对两份API的只读合并范围核对42处声明均有说明；该结果不能写成旧校验器已通过。

其他已识别的工具冲突：scripts/build_test_audit_docs.py会改写TEST_CASES.md、TEST_COVERAGE_AUDIT.md并追加TEST_RESULTS.md；不符合原稿保护规则，本次未执行。scripts/build_phase2_test_docs.py的输出仍引用旧TEST_RESULTS.md，且会重新生成部分历史输入说明；本次未执行。tests/test_document_generators.py含生成器调用，本次未运行该测试文件。tests/test_block9.py::test_documentation_present只检查文件存在性，不会覆盖原稿，本次单独执行通过。

上述脚本、测试和配置保持原代码，不通过修改第一阶段文字迎合检查器。第二阶段用例当前指向TEST_RESULTS_PHASE2.md，其后若重新生成需重新核对引用，但不应执行会覆盖原稿的生成流程。

## 文件级核验记录

通过PowerShell中的Python标准库只读扫描ZIP及文件内容，检查本次受保护代码、配置和原ZIP的SHA-256；README和第二阶段文稿的链接及锚点单独核对。细节保存在test-results/phase1-document-restoration-20261027下的archive-comparison-before.json、verification.json、links.json和combined-api-check.json。第一阶段原文即使包含不同于当前实现的描述也不改写，当前差异由第二阶段文稿承接。

最终核验结果：8份原稿及11份原始证据在ZIP、当前项目、submission三处逐字节一致；66个代码、配置及原ZIP保护项摘要未变。README与第二阶段文稿两处各检查11份、51个本地链接和锚点，均有效。第一阶段文件不追加本核验信息，所有新增记录仅存放于本页和第二阶段证据目录。


## 后续维护核验补记（已有记录归集）

后续归档核对曾发现第二阶段AI日志和报告的大小、SHA-256与清单失配，已同步源文稿、提交目录和ZIP后逐项更新清单。该维护事实不作为系统功能或业务测试结果。

第一阶段原始日志保留原文。既有审查发现其提及提示词附录而未有独立附录、来源表R03指向L13而日志止于L12；这些是原文结构的记录差异，未据此修改原稿，也不据原文引述推定所有提示词均为完整逐字原文。

后续一次执行`python -m scripts.check_documentation`的结果为退出码1、23项报告：22项来自只读取第一阶段API.md查找全部当前接口，另1项来自固定匹配“通过（用户报告）”而非“通过（项目作者报告）”。这是后续维护记录，与上文更早的22项记录分别保留。检查器未被写成通过，这些报告也不计入业务测试失败数；本轮未重新执行该检查器。

该次维护核对还比较了第一阶段114个nodeid与完整175项、P2-AUTO连续编号、3项pytest浏览器测试及独立browser_demo；读取JSON/XML、检查链接和归档摘要不产生新的业务测试通过结果。第一阶段原稿逐字节保护，覆盖原稿的生成器未运行，原始失败、警告与未执行状态仍保留。

本轮精简仅调整第二阶段五份文稿，并将上述维护细节集中于此；未运行pytest、浏览器流程、迁移或文档生成器，未连接MongoDB。提交目录与现有ZIP在修改前已逐文件一致；定稿后的文件清单不对自身循环哈希，目录和原位置ZIP按路径、大小及SHA-256核验。
