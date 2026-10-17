# 课程六类测试覆盖核对

本清单逐项阅读原有断言后建立，不能用旧总数43推断覆盖完整。已有与新增指本次核对之前和之后。参数化实例逐一执行，跨类别的同一实例只执行一次。

## 原有测试文件与名称

| 课程类别 | 原有文件和函数 | 原有覆盖与不足 |
| --- | --- | --- |
| 创建问卷 | `tests/test_block3.py::test_deadline`<br>`tests/test_block3.py::test_management` | 已有创建/分享/所有权/截止；缺默认值与落库、非法标题及未登录零写入断言。 |
| 添加题目 | `tests/test_block4.py::test_add_edit`<br>`tests/test_block8.py::test_schema_rejects` | 已有文本添加、ID稳定和部分非法配置单元检查；缺四类API落库、非法配置无副作用、权限与发布状态检查。 |
| 跳转逻辑 | `tests/test_block5.py::test_bad_target`<br>`tests/test_block5.py::test_jump`<br>`tests/test_block5.py::test_rule_persistence`<br>`tests/test_block8.py::test_edit_invalidates_rule`<br>`tests/test_block8.py::test_full_jump_workflow`<br>`tests/test_block8.py::test_missing_unknown_and_priority` | 已有END、规则持久化、数字跳后题、自跳/未知目标和首匹配；缺数字各运算边界、选择不匹配回退、真正回跳第一题的API拒绝。 |
| 答案校验 | `tests/test_block4.py::test_invalid`<br>`tests/test_block4.py::test_valid`<br>`tests/test_block8.py::test_missing_unknown_and_priority`<br>`tests/test_block8.py::test_schema_rejects` | 已有部分必答、文本/数字/选项边界单元检查；缺四类必答/选答、最多/精确数量以及API合法与非法输入的落库验证。 |
| 提交问卷 | `tests/test_block6.py::test_repeated`<br>`tests/test_block6.py::test_submit`<br>`tests/test_block8.py::test_concurrent_submit`<br>`tests/test_block8.py::test_expired`<br>`tests/test_block8.py::test_full_jump_workflow`<br>`tests/test_block8.py::test_real_name_details` | 已有保存、重复/并发、匿名/实名、过期/关闭；缺提交本身未登录、草稿和路径外输入拒绝、不同用户分别保存。 |
| 统计结果 | `tests/test_block7.py::test_statistics`<br>`tests/test_block8.py::test_full_jump_workflow` | 已有四类整卷、数字单题、跳过题不计数；缺四类单题一致性、零选项、选答空值、跨问卷隔离和后续提交刷新。 |

原有 test_management/test_deadline 曾直接向测试库插入占位题；不能用它们替代添加题目API测试。原有部分 raises 断言只检查异常类型，不能推断具体422或无写入；新增接口用例已补充。

## 本次逐类结果

| 类别 | 原有实例 | 新增实例 | 关联实例实际结果 | 新增函数 |
| --- | ---: | ---: | --- | --- |
| 创建问卷 | 2 | 6 | 8通过 / 0失败 / 0跳过 / 0未执行 | `test_create_defaults_persisted`<br>`test_create_rejects_invalid_without_write`<br>`test_create_requires_login` |
| 添加题目 | 5 | 11 | 16通过 / 0失败 / 0跳过 / 0未执行 | `test_add_each_type_persists_with_stable_ids`<br>`test_add_question_authorization_and_state`<br>`test_invalid_question_does_not_mutate_survey` |
| 跳转逻辑 | 10 | 20 | 30通过 / 0失败 / 0跳过 / 0未执行 | `test_choice_jump_and_fallback_api`<br>`test_invalid_jump_api_does_not_mutate`<br>`test_numeric_jump_operator_boundaries_api` |
| 答案校验 | 18 | 27 | 45通过 / 0失败 / 0跳过 / 0未执行 | `test_answer_validation_submission_boundaries`<br>`test_required_and_optional_all_types_api` |
| 提交问卷 | 7 | 5 | 12通过 / 0失败 / 0跳过 / 0未执行 | `test_distinct_users_can_each_submit_and_persist`<br>`test_submit_rejects_invalid_context_without_save` |
| 统计结果 | 2 | 2 | 4通过 / 0失败 / 0跳过 / 0未执行 | `test_all_question_stats_zero_optional_and_refresh`<br>`test_stats_isolate_surveys_and_reject_foreign_questions` |

类别间有交叉，不要相加得到总测试数。全套唯一实例结果：114通过 / 0失败 / 0跳过 / 0未执行。

以上覆盖结论限定于文档中列出的实际断言，不声称穷尽所有输入、负载或安全情形。已有其他类别测试（健康检查、认证、静态资源、文档）仍保留运行。

## 数据隔离与证据

conftest.py 显式连接本机 MongoDB，每用例使用 survey_system_test_<32位UUID>，不继承 MONGODB_DATABASE。创建之前和清理之前都校验名称；finalizer 在用例失败时仍仅清理自己的数据库。未扫描、删除、读取或写入开发库业务记录。

逐项用例见 [TEST_CASES.md](TEST_CASES.md)，原始结果见 test-results/coverage-audit/cases.json 与 pytest.xml。原始 JSON 同时保存每个用例的 setup/call/teardown 结果、测试库名和新增用例采集的实际观察值。
