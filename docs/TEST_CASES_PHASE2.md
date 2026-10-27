# 完整问卷与题库系统自动化用例及结果

本文列出所选完整运行的逐项输入、预期、实际和状态。证据生成不重新执行测试；运行之后新增的文档测试不冒充已经包含在本次全量中。

本文件由 `scripts/build_phase2_test_docs.py` 从 `test-results/submission-20261027/full.json` 生成；仅该目录代表本页所列运行。
全部P2-AUTO编号均为自动化；用户报告检查及未执行的可选计划见[MANUAL_TESTS.md](MANUAL_TESTS.md)。各次测试时间和范围见[TEST_RESULTS_PHASE2.md](TEST_RESULTS_PHASE2.md)。
最终运行证据时间：2026-10-27T00:29:14.976873+08:00。

| 运行记录 | 通过 | 失败 | 跳过 | 未运行 |
|---|---:|---:|---:|---:|
| related.json | 30 | 0 | 0 | 0 |
| full.json | 175 | 0 | 0 | 0 |

独立browser_demo的成功记录保存在`test-results/submission-20261027/browser-phase1.json`，不计入pytest数量。
以下逐项列出最终全量运行的所有用例，包括保留的第一阶段用例。参数化实例单独列出；真实断言在所列测试函数中。

## 编号与回归范围

对比两份原始JSON的完整nodeid，第一阶段test-results/coverage-audit/cases.json中的114个实例均在本次175项中出现且通过，其余61项为该次新增或扩展实例；这里的对应按实例标识判定，不声明源码未变化。P2-AUTO-001至P2-AUTO-175连续、唯一，覆盖整次运行而非仅指新增题库功能。175项包含认证、题库复制及题库完整流程3项浏览器测试；独立browser_demo另列。此页未因文稿编辑重新执行这些测试。

## P2-AUTO-001 · tests/test_auth_browser.py::test_separate_auth_views

- 测试类型：自动化浏览器集成测试（真实Edge）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：登录页进入注册页并返回；验证必填、格式、密码长度、一致性和重复账号；注册后登录、退出；分享链接上注册登录。
- 输入数据：ui_user、password123；空字段、短密码、不一致密码、重复用户名
- 参数实例：`{}`
- 预期结果：独立表单；错误提示明确且无无效注册写入；注册成功返回登录且不自动登录；登录进入首页或原问卷；退出会话失效。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_5b638d3d642845aa97190438ee92e5e6

## P2-AUTO-002 · tests/test_bank_copy_browser.py::test_bank_copy_and_readable_errors

- 测试类型：自动化浏览器集成测试（真实Edge）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：浏览器模拟非JSON/网络错误；创建空题库，从自己的问卷复制题目，重复保存，加入另一题库。
- 输入数据：数字题年龄；他人私有问卷；纯文本/HTML/无效JSON/英文错误和断网响应
- 参数实例：`{}`
- 预期结果：提示全中文且无状态码或原始异常；空状态有引导；不显示私有问卷；复制保留内容，重复不新增；候选过滤正确。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_ad5f600e838f47b083f2da6c26447b54

## P2-AUTO-003 · tests/test_bank_copy_messages.py::test_copy_snapshot_preserves_data[single-a]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：创建并发布问卷、提交答卷；复制至题库；重复复制；比较原数据。
- 输入数据：四种题型及相应答案、完整校验配置
- 参数实例：`{"kind": "single", "value": "a"}`
- 预期结果：内容完整，复制初版无规则和实例ID；重复不新增族或版本；问卷、答卷不变。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_7edb2fc769e54cbab8147397ac0f3936

## P2-AUTO-004 · tests/test_bank_copy_messages.py::test_copy_snapshot_preserves_data[multiple-value1]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：创建并发布问卷、提交答卷；复制至题库；重复复制；比较原数据。
- 输入数据：四种题型及相应答案、完整校验配置
- 参数实例：`{"kind": "multiple", "value": ["a", "b"]}`
- 预期结果：内容完整，复制初版无规则和实例ID；重复不新增族或版本；问卷、答卷不变。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_7988682ed9fd4c01b65e8112fb57c007

## P2-AUTO-005 · tests/test_bank_copy_messages.py::test_copy_snapshot_preserves_data[text-\u8bfe\u7a0b\u8bc4\u4ef7]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：创建并发布问卷、提交答卷；复制至题库；重复复制；比较原数据。
- 输入数据：四种题型及相应答案、完整校验配置
- 参数实例：`{"kind": "text", "value": "课程评价"}`
- 预期结果：内容完整，复制初版无规则和实例ID；重复不新增族或版本；问卷、答卷不变。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_2360efef504b4df59247e5fa06f2f126

## P2-AUTO-006 · tests/test_bank_copy_messages.py::test_copy_snapshot_preserves_data[number-18]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：创建并发布问卷、提交答卷；复制至题库；重复复制；比较原数据。
- 输入数据：四种题型及相应答案、完整校验配置
- 参数实例：`{"kind": "number", "value": 18}`
- 预期结果：内容完整，复制初版无规则和实例ID；重复不新增族或版本；问卷、答卷不变。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_7dee0b5b5a9a421abe004d8f830ffb53

## P2-AUTO-007 · tests/test_bank_copy_messages.py::test_candidates_membership_and_permissions

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：排除当前题库后查询；加入另一题库、重复加入；尝试跨用户操作。
- 输入数据：两个题库、一个自有题目、另一用户
- 参数实例：`{}`
- 预期结果：候选只含未加入的自有题目；重复明确提示，无新增版本；跨用户404。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_c1ca013aa235449a91fa28d1b0097a34

## P2-AUTO-008 · tests/test_bank_copy_messages.py::test_copy_source_and_shared_ownership

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：自有来源题复用；他人尝试复制；共享接收人复制自己问卷中的快照。
- 输入数据：所有者、共享接收人、两个题库
- 参数实例：`{}`
- 预期结果：自有来源不新建版本；不读取他人问卷；共享快照复制为接收人自有题，不改原题。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_737a66259b6140e09227486cd90ccb85

## P2-AUTO-009 · tests/test_bank_copy_messages.py::test_copy_concurrent_and_changed_snapshot

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：并发复制同一草稿题；修改草稿后再次复制；比较旧版本。
- 输入数据：4个并发请求，题干修改
- 参数实例：`{}`
- 预期结果：第一次只有一族一版；内容改变生成独立题，旧版本不变。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_b8e03cb64d8049638b104e19fd0d88a2

## P2-AUTO-010 · tests/test_bank_copy_messages.py::test_number_messages[-1-\u8f93\u5165\u7684\u6570\u5b57\u4e0d\u80fd\u4f4e\u4e8e\u6700\u5c0f\u503c\u3002]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：发布数字题并提交越界值。
- 输入数据：下限0、上限120；-1和121
- 参数实例：`{"value": -1, "expected": "输入的数字不能低于最小值。"}`
- 预期结果：422，分别提示不能低于最小值和不能超过最大值。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_8c29711945c04e0281842c63d988a344

## P2-AUTO-011 · tests/test_bank_copy_messages.py::test_number_messages[121-\u8f93\u5165\u7684\u6570\u5b57\u4e0d\u80fd\u8d85\u8fc7\u6700\u5927\u503c\u3002]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：发布数字题并提交越界值。
- 输入数据：下限0、上限120；-1和121
- 参数实例：`{"value": 121, "expected": "输入的数字不能超过最大值。"}`
- 预期结果：422，分别提示不能低于最小值和不能超过最大值。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_8d023546b3bb4d558c2a683ea330acdf

## P2-AUTO-012 · tests/test_bank_copy_messages.py::test_validation_and_database_messages

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：提交缺少标题和过长密码；模拟数据库异常与未知路由。
- 输入数据：缺少title、17字符密码、读取异常
- 参数实例：`{}`
- 预期结果：中文JSON错误，不含英文校验结构；故障有日志且返回503。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_6674f1882779408b81dc74d56bc2e135

## P2-AUTO-013 · tests/test_bank_copy_messages.py::test_copy_closed_survey_without_rules

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：草稿配置数字跳转后发布并关闭；复制题目并尝试不存在题目。
- 输入数据：数字规则跳到结束；不存在的题目编号
- 参数实例：`{}`
- 预期结果：关闭问卷可以复制，规则不进入通用题目；原规则保留，非法请求404无额外版本。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_d769ffe725e240a6a2222dd0a7e6087f

## P2-AUTO-014 · tests/test_bank_copy_messages.py::test_unexpected_error_message

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：隔离应用注入未预期的运行异常并发起注册。
- 输入数据：模拟内部异常
- 参数实例：`{}`
- 预期结果：返回中文JSON错误，日志保留traceback；不向用户返回英文或内部细节。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_53155d09d15445a8b3a1963ff5ea9e61

## P2-AUTO-015 · tests/test_block1.py::test_health

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机MongoDB可用；每实例独立UUID测试库。
- 操作步骤：GET /api/health。
- 输入数据：无请求体。
- 参数实例：`{}`
- 预期结果：200，返回的数据库名以 survey_system_test_ 开头。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_4bbce220f21b496888e4e10e1265eb60

## P2-AUTO-016 · tests/test_block2.py::test_auth

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机MongoDB可用；每实例独立UUID测试库。
- 操作步骤：注册登录、检查身份、错误登录、重复注册、查看密码字段、退出并复查。
- 输入数据：alice/password123；错误密码incorrect。
- 参数实例：`{}`
- 预期结果：认证200；未登录/错误密码/退出后401；重复409；数据库仅存密码哈希。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_868d95504dfa405bb98ec070cf4e2cef

## P2-AUTO-017 · tests/test_block2.py::test_ownership

- 测试类型：自动化数据库集成测试（直接调用权限函数）
- 前置条件：本机MongoDB可用；每实例独立UUID测试库。
- 操作步骤：在测试库插入所有者a的问卷s；分别使用a/b调用owned。
- 输入数据：survey_id=s，owner_id=a。
- 参数实例：`{}`
- 预期结果：a读取成功；b抛HTTPException且状态404。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_4c37ea9e8e3f43699ca1830c56490cd6

## P2-AUTO-018 · tests/test_block3.py::test_management

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机MongoDB可用；每实例独立UUID测试库。
- 操作步骤：注册两用户；创建、查分享链接、越权查询、编辑、空问卷发布；测试库植入占位题再发布关闭。
- 输入数据：课堂调查→修改标题；用户alice/bobby；占位题q1。
- 参数实例：`{}`
- 预期结果：创建201；分享路径匹配；越权404/空列表；空问卷发布422；发布published；发布后编辑409；关闭closed。此用例使用直接写库占位题，不能单独证明加题API完整。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_2dec082fe9b84fcbb21a53c03228fbe5

## P2-AUTO-019 · tests/test_block3.py::test_deadline

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机MongoDB可用；每实例独立UUID测试库。
- 操作步骤：创建无时区时间；创建带时区过去时间；测试库植入占位题并发布。
- 输入数据：2020-01-01T12:00:00与2020-01-01T12:00:00Z。
- 参数实例：`{}`
- 预期结果：无时区创建422；带时区过去时间可存草稿，但发布422。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_42e67cdbb2934758af394a7e1b09408a

## P2-AUTO-020 · tests/test_block4.py::test_add_edit

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机MongoDB可用；每实例独立UUID测试库。
- 操作步骤：建草稿；添加文本题；改为数字题并比较ID；添加无选项单选。
- 输入数据：姓名/text→年龄/number/integer=true；single无options。
- 参数实例：`{}`
- 预期结果：添加201；编辑保持原题ID；无选项单选422。此用例未独立断言编辑请求状态码。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_8ece6ec54a4e47289987510801733d01

## P2-AUTO-021 · tests/test_block4.py::test_invalid[q0-None]

- 测试类型：自动化单元/文件检查
- 前置条件：纯函数/本地文件自动测试；无需MongoDB业务数据。
- 操作步骤：用QuestionInput构造题目；对指定输入调用validate_answer。
- 输入数据：完整题目q与value见各实例参数。
- 参数实例：`{"q": {"id": "q", "title": "问题", "type": "text", "required": true, "options": [], "min_choices": 0, "max_choices": null, "min_length": 0, "max_length": 1000, "min_value": null, "max_value": null, "integer": false, "rules": []}, "value": null}`
- 预期结果：抛HTTPException。原断言未验证异常状态码或具体消息；新增API测试补充422与零写入断言。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：本地纯函数/文件检查，不连接业务库

## P2-AUTO-022 · tests/test_block4.py::test_invalid[q1-a]

- 测试类型：自动化单元/文件检查
- 前置条件：纯函数/本地文件自动测试；无需MongoDB业务数据。
- 操作步骤：用QuestionInput构造题目；对指定输入调用validate_answer。
- 输入数据：完整题目q与value见各实例参数。
- 参数实例：`{"q": {"id": "q", "title": "问题", "type": "text", "required": true, "options": [], "min_choices": 0, "max_choices": null, "min_length": 2, "max_length": 1000, "min_value": null, "max_value": null, "integer": false, "rules": []}, "value": "a"}`
- 预期结果：抛HTTPException。原断言未验证异常状态码或具体消息；新增API测试补充422与零写入断言。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：本地纯函数/文件检查，不连接业务库

## P2-AUTO-023 · tests/test_block4.py::test_invalid[q2-abc]

- 测试类型：自动化单元/文件检查
- 前置条件：纯函数/本地文件自动测试；无需MongoDB业务数据。
- 操作步骤：用QuestionInput构造题目；对指定输入调用validate_answer。
- 输入数据：完整题目q与value见各实例参数。
- 参数实例：`{"q": {"id": "q", "title": "问题", "type": "text", "required": true, "options": [], "min_choices": 0, "max_choices": null, "min_length": 0, "max_length": 2, "min_value": null, "max_value": null, "integer": false, "rules": []}, "value": "abc"}`
- 预期结果：抛HTTPException。原断言未验证异常状态码或具体消息；新增API测试补充422与零写入断言。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：本地纯函数/文件检查，不连接业务库

## P2-AUTO-024 · tests/test_block4.py::test_invalid[q3-  ]

- 测试类型：自动化单元/文件检查
- 前置条件：纯函数/本地文件自动测试；无需MongoDB业务数据。
- 操作步骤：用QuestionInput构造题目；对指定输入调用validate_answer。
- 输入数据：完整题目q与value见各实例参数。
- 参数实例：`{"q": {"id": "q", "title": "问题", "type": "text", "required": true, "options": [], "min_choices": 0, "max_choices": null, "min_length": 0, "max_length": 1000, "min_value": null, "max_value": null, "integer": false, "rules": []}, "value": "  "}`
- 预期结果：抛HTTPException。原断言未验证异常状态码或具体消息；新增API测试补充422与零写入断言。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：本地纯函数/文件检查，不连接业务库

## P2-AUTO-025 · tests/test_block4.py::test_invalid[q4-1.5]

- 测试类型：自动化单元/文件检查
- 前置条件：纯函数/本地文件自动测试；无需MongoDB业务数据。
- 操作步骤：用QuestionInput构造题目；对指定输入调用validate_answer。
- 输入数据：完整题目q与value见各实例参数。
- 参数实例：`{"q": {"id": "q", "title": "问题", "type": "number", "required": true, "options": [], "min_choices": 0, "max_choices": null, "min_length": 0, "max_length": 1000, "min_value": null, "max_value": null, "integer": true, "rules": []}, "value": 1.5}`
- 预期结果：抛HTTPException。原断言未验证异常状态码或具体消息；新增API测试补充422与零写入断言。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：本地纯函数/文件检查，不连接业务库

## P2-AUTO-026 · tests/test_block4.py::test_invalid[q5--1]

- 测试类型：自动化单元/文件检查
- 前置条件：纯函数/本地文件自动测试；无需MongoDB业务数据。
- 操作步骤：用QuestionInput构造题目；对指定输入调用validate_answer。
- 输入数据：完整题目q与value见各实例参数。
- 参数实例：`{"q": {"id": "q", "title": "问题", "type": "number", "required": true, "options": [], "min_choices": 0, "max_choices": null, "min_length": 0, "max_length": 1000, "min_value": 0.0, "max_value": null, "integer": false, "rules": []}, "value": -1}`
- 预期结果：抛HTTPException。原断言未验证异常状态码或具体消息；新增API测试补充422与零写入断言。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：本地纯函数/文件检查，不连接业务库

## P2-AUTO-027 · tests/test_block4.py::test_invalid[q6-121]

- 测试类型：自动化单元/文件检查
- 前置条件：纯函数/本地文件自动测试；无需MongoDB业务数据。
- 操作步骤：用QuestionInput构造题目；对指定输入调用validate_answer。
- 输入数据：完整题目q与value见各实例参数。
- 参数实例：`{"q": {"id": "q", "title": "问题", "type": "number", "required": true, "options": [], "min_choices": 0, "max_choices": null, "min_length": 0, "max_length": 1000, "min_value": null, "max_value": 120.0, "integer": false, "rules": []}, "value": 121}`
- 预期结果：抛HTTPException。原断言未验证异常状态码或具体消息；新增API测试补充422与零写入断言。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：本地纯函数/文件检查，不连接业务库

## P2-AUTO-028 · tests/test_block4.py::test_invalid[q7-True]

- 测试类型：自动化单元/文件检查
- 前置条件：纯函数/本地文件自动测试；无需MongoDB业务数据。
- 操作步骤：用QuestionInput构造题目；对指定输入调用validate_answer。
- 输入数据：完整题目q与value见各实例参数。
- 参数实例：`{"q": {"id": "q", "title": "问题", "type": "number", "required": true, "options": [], "min_choices": 0, "max_choices": null, "min_length": 0, "max_length": 1000, "min_value": null, "max_value": null, "integer": false, "rules": []}, "value": true}`
- 预期结果：抛HTTPException。原断言未验证异常状态码或具体消息；新增API测试补充422与零写入断言。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：本地纯函数/文件检查，不连接业务库

## P2-AUTO-029 · tests/test_block4.py::test_invalid[q8-12]

- 测试类型：自动化单元/文件检查
- 前置条件：纯函数/本地文件自动测试；无需MongoDB业务数据。
- 操作步骤：用QuestionInput构造题目；对指定输入调用validate_answer。
- 输入数据：完整题目q与value见各实例参数。
- 参数实例：`{"q": {"id": "q", "title": "问题", "type": "number", "required": true, "options": [], "min_choices": 0, "max_choices": null, "min_length": 0, "max_length": 1000, "min_value": null, "max_value": null, "integer": false, "rules": []}, "value": "12"}`
- 预期结果：抛HTTPException。原断言未验证异常状态码或具体消息；新增API测试补充422与零写入断言。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：本地纯函数/文件检查，不连接业务库

## P2-AUTO-030 · tests/test_block4.py::test_invalid[q9-c]

- 测试类型：自动化单元/文件检查
- 前置条件：纯函数/本地文件自动测试；无需MongoDB业务数据。
- 操作步骤：用QuestionInput构造题目；对指定输入调用validate_answer。
- 输入数据：完整题目q与value见各实例参数。
- 参数实例：`{"q": {"id": "q", "title": "问题", "type": "single", "required": true, "options": [{"id": "a", "label": "A"}, {"id": "b", "label": "B"}], "min_choices": 0, "max_choices": null, "min_length": 0, "max_length": 1000, "min_value": null, "max_value": null, "integer": false, "rules": []}, "value": "c"}`
- 预期结果：抛HTTPException。原断言未验证异常状态码或具体消息；新增API测试补充422与零写入断言。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：本地纯函数/文件检查，不连接业务库

## P2-AUTO-031 · tests/test_block4.py::test_invalid[q10-value10]

- 测试类型：自动化单元/文件检查
- 前置条件：纯函数/本地文件自动测试；无需MongoDB业务数据。
- 操作步骤：用QuestionInput构造题目；对指定输入调用validate_answer。
- 输入数据：完整题目q与value见各实例参数。
- 参数实例：`{"q": {"id": "q", "title": "问题", "type": "multiple", "required": true, "options": [{"id": "a", "label": "A"}, {"id": "b", "label": "B"}], "min_choices": 2, "max_choices": null, "min_length": 0, "max_length": 1000, "min_value": null, "max_value": null, "integer": false, "rules": []}, "value": ["a"]}`
- 预期结果：抛HTTPException。原断言未验证异常状态码或具体消息；新增API测试补充422与零写入断言。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：本地纯函数/文件检查，不连接业务库

## P2-AUTO-032 · tests/test_block4.py::test_invalid[q11-value11]

- 测试类型：自动化单元/文件检查
- 前置条件：纯函数/本地文件自动测试；无需MongoDB业务数据。
- 操作步骤：用QuestionInput构造题目；对指定输入调用validate_answer。
- 输入数据：完整题目q与value见各实例参数。
- 参数实例：`{"q": {"id": "q", "title": "问题", "type": "multiple", "required": true, "options": [{"id": "a", "label": "A"}, {"id": "b", "label": "B"}], "min_choices": 0, "max_choices": null, "min_length": 0, "max_length": 1000, "min_value": null, "max_value": null, "integer": false, "rules": []}, "value": ["a", "a"]}`
- 预期结果：抛HTTPException。原断言未验证异常状态码或具体消息；新增API测试补充422与零写入断言。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：本地纯函数/文件检查，不连接业务库

## P2-AUTO-033 · tests/test_block4.py::test_valid

- 测试类型：自动化单元/文件检查
- 前置条件：纯函数/本地文件自动测试；无需MongoDB业务数据。
- 操作步骤：分别验证选答空值、数字上边界、中文文本精确长度。
- 输入数据：required=false/null；整数0～120输入120；2字文本输入中文。
- 参数实例：`{}`
- 预期结果：分别返回None、120、中文。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：本地纯函数/文件检查，不连接业务库

## P2-AUTO-034 · tests/test_block5.py::test_jump[single-eq-a-a]

- 测试类型：自动化单元/文件检查
- 前置条件：纯函数/本地文件自动测试；无需MongoDB业务数据。
- 操作步骤：构造带规则题与被跳过题；检查规则；完整walk；再加入路径外答案。
- 输入数据：kind/op/value/answer见实例参数；命中目标END；路径外题skip。
- 参数实例：`{"kind": "single", "op": "eq", "value": "a", "answer": "a"}`
- 预期结果：匹配路径仅[q]；包含skip答案时抛HTTPException。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：本地纯函数/文件检查，不连接业务库

## P2-AUTO-035 · tests/test_block5.py::test_jump[multiple-contains_any-value1-answer1]

- 测试类型：自动化单元/文件检查
- 前置条件：纯函数/本地文件自动测试；无需MongoDB业务数据。
- 操作步骤：构造带规则题与被跳过题；检查规则；完整walk；再加入路径外答案。
- 输入数据：kind/op/value/answer见实例参数；命中目标END；路径外题skip。
- 参数实例：`{"kind": "multiple", "op": "contains_any", "value": ["a"], "answer": ["a", "b"]}`
- 预期结果：匹配路径仅[q]；包含skip答案时抛HTTPException。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：本地纯函数/文件检查，不连接业务库

## P2-AUTO-036 · tests/test_block5.py::test_jump[multiple-contains_all-value2-answer2]

- 测试类型：自动化单元/文件检查
- 前置条件：纯函数/本地文件自动测试；无需MongoDB业务数据。
- 操作步骤：构造带规则题与被跳过题；检查规则；完整walk；再加入路径外答案。
- 输入数据：kind/op/value/answer见实例参数；命中目标END；路径外题skip。
- 参数实例：`{"kind": "multiple", "op": "contains_all", "value": ["a", "b"], "answer": ["a", "b"]}`
- 预期结果：匹配路径仅[q]；包含skip答案时抛HTTPException。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：本地纯函数/文件检查，不连接业务库

## P2-AUTO-037 · tests/test_block5.py::test_jump[number-gte-18-20]

- 测试类型：自动化单元/文件检查
- 前置条件：纯函数/本地文件自动测试；无需MongoDB业务数据。
- 操作步骤：构造带规则题与被跳过题；检查规则；完整walk；再加入路径外答案。
- 输入数据：kind/op/value/answer见实例参数；命中目标END；路径外题skip。
- 参数实例：`{"kind": "number", "op": "gte", "value": 18, "answer": 20}`
- 预期结果：匹配路径仅[q]；包含skip答案时抛HTTPException。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：本地纯函数/文件检查，不连接业务库

## P2-AUTO-038 · tests/test_block5.py::test_bad_target[q]

- 测试类型：自动化单元/文件检查
- 前置条件：纯函数/本地文件自动测试；无需MongoDB业务数据。
- 操作步骤：构造数字题q，设置gt 0规则到目标，调用validate_rules。
- 输入数据：target=q或missing。
- 参数实例：`{"target": "q"}`
- 预期结果：自跳/不存在目标均抛HTTPException。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：本地纯函数/文件检查，不连接业务库

## P2-AUTO-039 · tests/test_block5.py::test_bad_target[missing]

- 测试类型：自动化单元/文件检查
- 前置条件：纯函数/本地文件自动测试；无需MongoDB业务数据。
- 操作步骤：构造数字题q，设置gt 0规则到目标，调用validate_rules。
- 输入数据：target=q或missing。
- 参数实例：`{"target": "missing"}`
- 预期结果：自跳/不存在目标均抛HTTPException。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：本地纯函数/文件检查，不连接业务库

## P2-AUTO-040 · tests/test_block5.py::test_rule_persistence

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机MongoDB可用；每实例独立UUID测试库。
- 操作步骤：通过API创建问卷、数字题、规则，然后读取MongoDB。
- 输入数据：lt 18→END。
- 参数实例：`{}`
- 预期结果：配置规则200；数据库rules与请求一致。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_b721c5f1c15544129f4cfd1b94ef3ea9

## P2-AUTO-041 · tests/test_block6.py::test_submit

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机MongoDB可用；每实例独立UUID测试库。
- 操作步骤：发布匿名数字问卷；检查未登录读取、next、非法提交、合法提交、再次提交；创建者/他人读取答卷。
- 输入数据：必答整数0～120；200→20→21；独立filler用户。
- 参数实例：`{}`
- 预期结果：读取未登录401；next首题；非法422；合法201；重复409；仅一答卷，隐藏respondent、respondent_id、once_key；他人详情404。注意原用例401针对读取，不是提交。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_1970cb1488e041e6b7f8f11a85651b26

## P2-AUTO-042 · tests/test_block6.py::test_repeated[True-201]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机MongoDB可用；每实例独立UUID测试库。
- 操作步骤：根据多次配置发布；同用户提交10、20；关闭后提交30。
- 输入数据：multiple和expected见实例参数。
- 参数实例：`{"multiple": true, "expected": 201}`
- 预期结果：首次201；第二次按配置201或409；关闭后404。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_2fc4642b949f4242adae88a486ddde9a

## P2-AUTO-043 · tests/test_block6.py::test_repeated[False-409]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机MongoDB可用；每实例独立UUID测试库。
- 操作步骤：根据多次配置发布；同用户提交10、20；关闭后提交30。
- 输入数据：multiple和expected见实例参数。
- 参数实例：`{"multiple": false, "expected": 409}`
- 预期结果：首次201；第二次按配置201或409；关闭后404。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_ef357a6d0a0b488ba220714019b02e09

## P2-AUTO-044 · tests/test_block6.py::test_page

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机MongoDB可用；每实例独立UUID测试库。
- 操作步骤：请求首页、分享页面和脚本。
- 输入数据：/、/survey/example、/static/app.js。
- 参数实例：`{}`
- 预期结果：均200，仅验证路由可达，不代表人工浏览器验收。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_5577bb00ef464ff9991ab50d61fb1fe1

## P2-AUTO-045 · tests/test_block7.py::test_statistics

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机MongoDB可用；每实例独立UUID测试库。
- 操作步骤：添加四题并发布；查空统计；提交两份完整答卷；查全卷、数字单题及越权统计。
- 输入数据：single:a/b；multiple:[a,b]/[b]；text:甲/乙；number:10/20；允许多次。
- 参数实例：`{}`
- 预期结果：空总数0且均值null；提交各201；总数2；单选[1,1]、多选[1,2]、文本[甲,乙]、数字均值15；数字单题count2；越权整卷/单题404。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_4d4dc4311ea6459a8f0449c785939313

## P2-AUTO-046 · tests/test_block8.py::test_concurrent_submit

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机MongoDB可用；每实例独立UUID测试库。
- 操作步骤：每人一次问卷；4线程同用户同时提交；查询库数量。
- 输入数据：数字答案30，共4次并发。
- 参数实例：`{}`
- 预期结果：状态码排序[201,409,409,409]；数据库仅1条答卷。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_67c294f2ed104ba3901a72da6c070b39

## P2-AUTO-047 · tests/test_block8.py::test_expired

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机MongoDB可用；每实例独立UUID测试库。
- 操作步骤：发布后在测试库设置已过期时间；读取与提交；查询答卷数量。
- 输入数据：deadline=now-1秒；数字10。
- 参数实例：`{}`
- 预期结果：读取/提交410；答卷0。时间状态由测试库直接设置，未等待真实时间。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_9f85b4ec78cc42bfbb7b8522b069e1e3

## P2-AUTO-048 · tests/test_block8.py::test_full_jump_workflow

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机MongoDB可用；每实例独立UUID测试库。
- 操作步骤：通过API创建3题；设置首题跳第三题；发布；尝试改规则；逐题next、提交、读库和统计。
- 输入数据：年龄number、职业text、反馈text；年龄lt18跳反馈；答案16/很好。
- 参数实例：`{}`
- 预期结果：发布200；发布后改409；next为第三题；提交201；answers/path不含职业；职业count0、反馈values[很好]。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_b1dd13b02234463d92ad7c2f72d8ad96

## P2-AUTO-049 · tests/test_block8.py::test_edit_invalidates_rule

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机MongoDB可用；每实例独立UUID测试库。
- 操作步骤：数字题配置gt规则；改题型为文本；重新读取。
- 输入数据：gt10→END；number→text。
- 参数实例：`{}`
- 预期结果：编辑422；题型仍number。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_943f2686ab6d4e5d8c3377b9472f4a76

## P2-AUTO-050 · tests/test_block8.py::test_schema_rejects[kwargs0]

- 测试类型：自动化单元/文件检查
- 前置条件：纯函数/本地文件自动测试；无需MongoDB业务数据。
- 操作步骤：直接构造QuestionInput，不通过HTTP；以pytest.raises检查。
- 输入数据：非法kwargs见各参数实例。
- 参数实例：`{"kwargs": {"min_length": 3, "max_length": 2}}`
- 预期结果：抛ValueError：文本上下限、数字上下限、选项ID重复、多选最少超出选项数。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：本地纯函数/文件检查，不连接业务库

## P2-AUTO-051 · tests/test_block8.py::test_schema_rejects[kwargs1]

- 测试类型：自动化单元/文件检查
- 前置条件：纯函数/本地文件自动测试；无需MongoDB业务数据。
- 操作步骤：直接构造QuestionInput，不通过HTTP；以pytest.raises检查。
- 输入数据：非法kwargs见各参数实例。
- 参数实例：`{"kwargs": {"type": "number", "min_value": 10, "max_value": 1}}`
- 预期结果：抛ValueError：文本上下限、数字上下限、选项ID重复、多选最少超出选项数。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：本地纯函数/文件检查，不连接业务库

## P2-AUTO-052 · tests/test_block8.py::test_schema_rejects[kwargs2]

- 测试类型：自动化单元/文件检查
- 前置条件：纯函数/本地文件自动测试；无需MongoDB业务数据。
- 操作步骤：直接构造QuestionInput，不通过HTTP；以pytest.raises检查。
- 输入数据：非法kwargs见各参数实例。
- 参数实例：`{"kwargs": {"type": "single", "options": [{"id": "a", "label": "A"}, {"id": "a", "label": "B"}]}}`
- 预期结果：抛ValueError：文本上下限、数字上下限、选项ID重复、多选最少超出选项数。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：本地纯函数/文件检查，不连接业务库

## P2-AUTO-053 · tests/test_block8.py::test_schema_rejects[kwargs3]

- 测试类型：自动化单元/文件检查
- 前置条件：纯函数/本地文件自动测试；无需MongoDB业务数据。
- 操作步骤：直接构造QuestionInput，不通过HTTP；以pytest.raises检查。
- 输入数据：非法kwargs见各参数实例。
- 参数实例：`{"kwargs": {"type": "multiple", "options": [{"id": "a", "label": "A"}, {"id": "b", "label": "B"}], "min_choices": 3}}`
- 预期结果：抛ValueError：文本上下限、数字上下限、选项ID重复、多选最少超出选项数。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：本地纯函数/文件检查，不连接业务库

## P2-AUTO-054 · tests/test_block8.py::test_missing_unknown_and_priority

- 测试类型：自动化单元/文件检查
- 前置条件：纯函数/本地文件自动测试；无需MongoDB业务数据。
- 操作步骤：构造两条同时匹配的规则；完整walk；再传未知题或缺失必答。
- 输入数据：number q：gt0→END优先于gt0→later；答案q=1/unknown=1/q=0。
- 参数实例：`{}`
- 预期结果：首匹配路径[q]；未知题与缺少later必答均抛HTTPException。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：本地纯函数/文件检查，不连接业务库

## P2-AUTO-055 · tests/test_block8.py::test_real_name_details

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机MongoDB可用；每实例独立UUID测试库。
- 操作步骤：发布实名问卷；filler填写；创建者读详情。
- 输入数据：anonymous=false；数字22。
- 参数实例：`{}`
- 预期结果：详情respondent.username=filler。原用例没有独立断言提交状态。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_dbb2080e88a041fe9c881a19c509eda6

## P2-AUTO-056 · tests/test_block9.py::test_offline_docs

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机MongoDB可用；每实例独立UUID测试库。
- 操作步骤：读取/docs、OpenAPI；扫描本地静态文件。
- 输入数据：5个本地资源文件。
- 参数实例：`{}`
- 预期结果：docs200；schema含单题统计路径与QuestionInput；静态文件没有外部http链接。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_5140e7b388824d858309bd7a443fc654

## P2-AUTO-057 · tests/test_block9.py::test_documentation_present

- 测试类型：自动化单元/文件检查
- 前置条件：纯函数/本地文件自动测试；无需MongoDB业务数据。
- 操作步骤：检查7份文档存在且长度大于100；检查.env.example。
- 输入数据：当时检查七份文档与配置示例；历史报告索引现并入README，当前文档检查改为完整阶段报告。原始输入保留于JSON证据。
- 参数实例：`{}`
- 预期结果：文档非空且环境示例含MONGODB_URI；仅检查存在性，不证明文档业务覆盖。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：本地纯函数/文件检查，不连接业务库

## P2-AUTO-058 · tests/test_course_requirements.py::test_create_defaults_persisted

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：登录；POST 创建；查询 MongoDB；GET 详情和列表对照。
- 输入数据：{"title":"  课程问卷  "}，其余设置省略。
- 参数实例：`{}`
- 预期结果：201；稳定 UUID；标题去空白；draft、非匿名、每人一次、无截止、无题目；创建者正确；时间按BSON毫秒精度与落库一致；详情/列表与落库一致。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_74c35387059a4944aaa577b557070779

实际观察：
```json
[
  {
    "status": 201
  },
  {
    "creation_time": "2026-10-26T16:27:07.965508+00:00",
    "read_time": "2026-10-26T16:27:07.965000+00:00",
    "bson_precision": "milliseconds"
  },
  {
    "stored_defaults": {
      "title": "课程问卷",
      "status": "draft",
      "anonymous": false,
      "allow_multiple": false,
      "deadline": null,
      "questions": []
    }
  }
]
```

## P2-AUTO-059 · tests/test_course_requirements.py::test_create_rejects_invalid_without_write[missing-title]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：登录；POST 非法问卷；查询测试库问卷数量。
- 输入数据：payload 参数。
- 参数实例：`{"payload": {}}`
- 预期结果：422；surveys 集合仍为 0 条。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_7f4392abde644ad1b2fd5c6fb8f64ad2

实际观察：
```json
[
  {
    "status": 422,
    "surveys": 0
  }
]
```

## P2-AUTO-060 · tests/test_course_requirements.py::test_create_rejects_invalid_without_write[empty-title]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：登录；POST 非法问卷；查询测试库问卷数量。
- 输入数据：payload 参数。
- 参数实例：`{"payload": {"title": ""}}`
- 预期结果：422；surveys 集合仍为 0 条。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_5d85bdd9d11b4d439ef4c38553221fff

实际观察：
```json
[
  {
    "status": 422,
    "surveys": 0
  }
]
```

## P2-AUTO-061 · tests/test_course_requirements.py::test_create_rejects_invalid_without_write[blank-title]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：登录；POST 非法问卷；查询测试库问卷数量。
- 输入数据：payload 参数。
- 参数实例：`{"payload": {"title": "   "}}`
- 预期结果：422；surveys 集合仍为 0 条。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_c21d27a7308045cfad2516b631d3e435

实际观察：
```json
[
  {
    "status": 422,
    "surveys": 0
  }
]
```

## P2-AUTO-062 · tests/test_course_requirements.py::test_create_rejects_invalid_without_write[too-long-title]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：登录；POST 非法问卷；查询测试库问卷数量。
- 输入数据：payload 参数。
- 参数实例：`{"payload": {"title": "长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长"}}`
- 预期结果：422；surveys 集合仍为 0 条。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_55a34610cdd24d5197069ec76c654ba9

实际观察：
```json
[
  {
    "status": 422,
    "surveys": 0
  }
]
```

## P2-AUTO-063 · tests/test_course_requirements.py::test_create_requires_login

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：不登录；POST 合法问卷；检查库中数量。
- 输入数据：{"title":"未登录创建"}。
- 参数实例：`{}`
- 预期结果：401；surveys 集合无写入。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_cf74fbfa323544458e53a9d6e2a29d42

实际观察：
```json
[
  {
    "status": 401,
    "surveys": 0
  }
]
```

## P2-AUTO-064 · tests/test_course_requirements.py::test_add_each_type_persists_with_stable_ids[single]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：创建草稿；分别 POST 四类题目；再次添加另一题；检查 API 与 MongoDB 中 ID/配置。
- 输入数据：kind 参数；选择题 a/b/c；文本2～4字；数字0～120整数。
- 参数实例：`{"kind": "single"}`
- 预期结果：两次添加均201；题型和配置落库一致；两道题 UUID 不同，后续添加不改变已有 ID。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_aaa133344e8b4a8986acb235f0d58b73

实际观察：
```json
[
  {
    "add_status": 201,
    "second_status": 201,
    "kind": "single",
    "stored_questions": 2,
    "first_id_stable": true
  }
]
```

## P2-AUTO-065 · tests/test_course_requirements.py::test_add_each_type_persists_with_stable_ids[multiple]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：创建草稿；分别 POST 四类题目；再次添加另一题；检查 API 与 MongoDB 中 ID/配置。
- 输入数据：kind 参数；选择题 a/b/c；文本2～4字；数字0～120整数。
- 参数实例：`{"kind": "multiple"}`
- 预期结果：两次添加均201；题型和配置落库一致；两道题 UUID 不同，后续添加不改变已有 ID。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_c8683c9e61eb48c3b04fc0f8f3346503

实际观察：
```json
[
  {
    "add_status": 201,
    "second_status": 201,
    "kind": "multiple",
    "stored_questions": 2,
    "first_id_stable": true
  }
]
```

## P2-AUTO-066 · tests/test_course_requirements.py::test_add_each_type_persists_with_stable_ids[text]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：创建草稿；分别 POST 四类题目；再次添加另一题；检查 API 与 MongoDB 中 ID/配置。
- 输入数据：kind 参数；选择题 a/b/c；文本2～4字；数字0～120整数。
- 参数实例：`{"kind": "text"}`
- 预期结果：两次添加均201；题型和配置落库一致；两道题 UUID 不同，后续添加不改变已有 ID。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_e25abc1903e5467b922ea916f363e7a9

实际观察：
```json
[
  {
    "add_status": 201,
    "second_status": 201,
    "kind": "text",
    "stored_questions": 2,
    "first_id_stable": true
  }
]
```

## P2-AUTO-067 · tests/test_course_requirements.py::test_add_each_type_persists_with_stable_ids[number]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：创建草稿；分别 POST 四类题目；再次添加另一题；检查 API 与 MongoDB 中 ID/配置。
- 输入数据：kind 参数；选择题 a/b/c；文本2～4字；数字0～120整数。
- 参数实例：`{"kind": "number"}`
- 预期结果：两次添加均201；题型和配置落库一致；两道题 UUID 不同，后续添加不改变已有 ID。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_05e2400a054445efa57736cfbce1aec7

实际观察：
```json
[
  {
    "add_status": 201,
    "second_status": 201,
    "kind": "number",
    "stored_questions": 2,
    "first_id_stable": true
  }
]
```

## P2-AUTO-068 · tests/test_course_requirements.py::test_invalid_question_does_not_mutate_survey[single-no-options]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：创建草稿；保存文档快照；POST 非法题目；重新读取文档比较。
- 输入数据：payload 参数。
- 参数实例：`{"payload": {"title": "课程测试题", "type": "single", "options": []}}`
- 预期结果：422；整个问卷文档（包括 revision 和 questions）不变。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_f3305244e70f486fbf7ec77844d67184

实际观察：
```json
[
  {
    "status": 422,
    "document_unchanged": true
  }
]
```

## P2-AUTO-069 · tests/test_course_requirements.py::test_invalid_question_does_not_mutate_survey[multiple-invalid-limits]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：创建草稿；保存文档快照；POST 非法题目；重新读取文档比较。
- 输入数据：payload 参数。
- 参数实例：`{"payload": {"title": "课程测试题", "type": "multiple", "options": [{"id": "a", "label": "A"}, {"id": "b", "label": "B"}, {"id": "c", "label": "C"}], "min_choices": 3, "max_choices": 2}}`
- 预期结果：422；整个问卷文档（包括 revision 和 questions）不变。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_20a1812aa0b1459e84e44831c2b694c6

实际观察：
```json
[
  {
    "status": 422,
    "document_unchanged": true
  }
]
```

## P2-AUTO-070 · tests/test_course_requirements.py::test_invalid_question_does_not_mutate_survey[text-invalid-limits]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：创建草稿；保存文档快照；POST 非法题目；重新读取文档比较。
- 输入数据：payload 参数。
- 参数实例：`{"payload": {"title": "课程测试题", "type": "text", "min_length": 5, "max_length": 2}}`
- 预期结果：422；整个问卷文档（包括 revision 和 questions）不变。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_fe3544ffb9a9439c9c692fc1db64db83

实际观察：
```json
[
  {
    "status": 422,
    "document_unchanged": true
  }
]
```

## P2-AUTO-071 · tests/test_course_requirements.py::test_invalid_question_does_not_mutate_survey[number-invalid-limits]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：创建草稿；保存文档快照；POST 非法题目；重新读取文档比较。
- 输入数据：payload 参数。
- 参数实例：`{"payload": {"title": "课程测试题", "type": "number", "min_value": 10, "max_value": 0}}`
- 预期结果：422；整个问卷文档（包括 revision 和 questions）不变。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_7cae5b8051324c4d998fa1d57e775eeb

实际观察：
```json
[
  {
    "status": 422,
    "document_unchanged": true
  }
]
```

## P2-AUTO-072 · tests/test_course_requirements.py::test_add_question_authorization_and_state[anonymous-401]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：准备草稿或已发布问卷；以指定身份 POST 新题；比较前后文档。
- 输入数据：actor 参数：未登录、其他用户、已发布问卷的创建者。
- 参数实例：`{"actor": "anonymous", "expected": 401}`
- 预期结果：分别401、404、409；问卷文档不变。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_c25b6891b4bf442d96e48c5c7ff05374

实际观察：
```json
[
  {
    "status": 401,
    "document_unchanged": true
  }
]
```

## P2-AUTO-073 · tests/test_course_requirements.py::test_add_question_authorization_and_state[other-404]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：准备草稿或已发布问卷；以指定身份 POST 新题；比较前后文档。
- 输入数据：actor 参数：未登录、其他用户、已发布问卷的创建者。
- 参数实例：`{"actor": "other", "expected": 404}`
- 预期结果：分别401、404、409；问卷文档不变。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_b574876c6aa94d72b61630bda9df5385

实际观察：
```json
[
  {
    "status": 404,
    "document_unchanged": true
  }
]
```

## P2-AUTO-074 · tests/test_course_requirements.py::test_add_question_authorization_and_state[published_owner-409]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：准备草稿或已发布问卷；以指定身份 POST 新题；比较前后文档。
- 输入数据：actor 参数：未登录、其他用户、已发布问卷的创建者。
- 参数实例：`{"actor": "published_owner", "expected": 409}`
- 预期结果：分别401、404、409；问卷文档不变。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_32be077a959942f1aff2ac5f6c3c3359

实际观察：
```json
[
  {
    "status": 409,
    "document_unchanged": true
  }
]
```

## P2-AUTO-075 · tests/test_course_requirements.py::test_numeric_jump_operator_boundaries_api[eq-18-True]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：API 创建数字题和后续文本题；设置数字规则到 END；发布；调用 next。
- 输入数据：比较阈值18，op/answer/matched 参数。
- 参数实例：`{"op": "eq", "answer": 18, "matched": true}`
- 预期结果：匹配时 next_question_id=END，否则进入后续文本题；规则从 MongoDB 读取。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_c10c7b48cbca422fbad384db6ce3db50

实际观察：
```json
[
  {
    "status": 200,
    "next_is_end": true,
    "matched": true
  }
]
```

## P2-AUTO-076 · tests/test_course_requirements.py::test_numeric_jump_operator_boundaries_api[eq-19-False]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：API 创建数字题和后续文本题；设置数字规则到 END；发布；调用 next。
- 输入数据：比较阈值18，op/answer/matched 参数。
- 参数实例：`{"op": "eq", "answer": 19, "matched": false}`
- 预期结果：匹配时 next_question_id=END，否则进入后续文本题；规则从 MongoDB 读取。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_e963e48c022d439db4743d7dc12154b8

实际观察：
```json
[
  {
    "status": 200,
    "next_is_end": false,
    "matched": false
  }
]
```

## P2-AUTO-077 · tests/test_course_requirements.py::test_numeric_jump_operator_boundaries_api[gt-18-False]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：API 创建数字题和后续文本题；设置数字规则到 END；发布；调用 next。
- 输入数据：比较阈值18，op/answer/matched 参数。
- 参数实例：`{"op": "gt", "answer": 18, "matched": false}`
- 预期结果：匹配时 next_question_id=END，否则进入后续文本题；规则从 MongoDB 读取。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_ef7c9c38163c4728b220d9945e461b68

实际观察：
```json
[
  {
    "status": 200,
    "next_is_end": false,
    "matched": false
  }
]
```

## P2-AUTO-078 · tests/test_course_requirements.py::test_numeric_jump_operator_boundaries_api[gt-19-True]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：API 创建数字题和后续文本题；设置数字规则到 END；发布；调用 next。
- 输入数据：比较阈值18，op/answer/matched 参数。
- 参数实例：`{"op": "gt", "answer": 19, "matched": true}`
- 预期结果：匹配时 next_question_id=END，否则进入后续文本题；规则从 MongoDB 读取。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_0b13f4b93dd74a50a01d94f617d35b43

实际观察：
```json
[
  {
    "status": 200,
    "next_is_end": true,
    "matched": true
  }
]
```

## P2-AUTO-079 · tests/test_course_requirements.py::test_numeric_jump_operator_boundaries_api[gte-18-True]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：API 创建数字题和后续文本题；设置数字规则到 END；发布；调用 next。
- 输入数据：比较阈值18，op/answer/matched 参数。
- 参数实例：`{"op": "gte", "answer": 18, "matched": true}`
- 预期结果：匹配时 next_question_id=END，否则进入后续文本题；规则从 MongoDB 读取。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_59e6e9dc44544aa28d62b4ff244e8c50

实际观察：
```json
[
  {
    "status": 200,
    "next_is_end": true,
    "matched": true
  }
]
```

## P2-AUTO-080 · tests/test_course_requirements.py::test_numeric_jump_operator_boundaries_api[gte-17-False]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：API 创建数字题和后续文本题；设置数字规则到 END；发布；调用 next。
- 输入数据：比较阈值18，op/answer/matched 参数。
- 参数实例：`{"op": "gte", "answer": 17, "matched": false}`
- 预期结果：匹配时 next_question_id=END，否则进入后续文本题；规则从 MongoDB 读取。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_376124ce6f144e6489ab4bd42ef0be38

实际观察：
```json
[
  {
    "status": 200,
    "next_is_end": false,
    "matched": false
  }
]
```

## P2-AUTO-081 · tests/test_course_requirements.py::test_numeric_jump_operator_boundaries_api[lt-18-False]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：API 创建数字题和后续文本题；设置数字规则到 END；发布；调用 next。
- 输入数据：比较阈值18，op/answer/matched 参数。
- 参数实例：`{"op": "lt", "answer": 18, "matched": false}`
- 预期结果：匹配时 next_question_id=END，否则进入后续文本题；规则从 MongoDB 读取。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_fafe51c32d534fc3a73cc9f5ad58bb60

实际观察：
```json
[
  {
    "status": 200,
    "next_is_end": false,
    "matched": false
  }
]
```

## P2-AUTO-082 · tests/test_course_requirements.py::test_numeric_jump_operator_boundaries_api[lt-17-True]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：API 创建数字题和后续文本题；设置数字规则到 END；发布；调用 next。
- 输入数据：比较阈值18，op/answer/matched 参数。
- 参数实例：`{"op": "lt", "answer": 17, "matched": true}`
- 预期结果：匹配时 next_question_id=END，否则进入后续文本题；规则从 MongoDB 读取。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_0919412b0a234bdca2c0c818de94fc83

实际观察：
```json
[
  {
    "status": 200,
    "next_is_end": true,
    "matched": true
  }
]
```

## P2-AUTO-083 · tests/test_course_requirements.py::test_numeric_jump_operator_boundaries_api[lte-18-True]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：API 创建数字题和后续文本题；设置数字规则到 END；发布；调用 next。
- 输入数据：比较阈值18，op/answer/matched 参数。
- 参数实例：`{"op": "lte", "answer": 18, "matched": true}`
- 预期结果：匹配时 next_question_id=END，否则进入后续文本题；规则从 MongoDB 读取。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_b3e3eab02ea8440f92f93361ed039627

实际观察：
```json
[
  {
    "status": 200,
    "next_is_end": true,
    "matched": true
  }
]
```

## P2-AUTO-084 · tests/test_course_requirements.py::test_numeric_jump_operator_boundaries_api[lte-19-False]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：API 创建数字题和后续文本题；设置数字规则到 END；发布；调用 next。
- 输入数据：比较阈值18，op/answer/matched 参数。
- 参数实例：`{"op": "lte", "answer": 19, "matched": false}`
- 预期结果：匹配时 next_question_id=END，否则进入后续文本题；规则从 MongoDB 读取。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_d97e2ce5d0d6445ca0e5564d61c2b365

实际观察：
```json
[
  {
    "status": 200,
    "next_is_end": false,
    "matched": false
  }
]
```

## P2-AUTO-085 · tests/test_course_requirements.py::test_choice_jump_and_fallback_api[single-eq-a-a-True]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：创建选择题+后续文本题；配置跳转规则；发布；使用指定答案调用 next。
- 输入数据：kind、op、condition、answer、matched 参数，选项 a/b/c。
- 参数实例：`{"kind": "single", "op": "eq", "condition": "a", "answer": "a", "matched": true}`
- 预期结果：匹配则 END；不匹配则按顺序进入后续题；contains_all 允许额外选项但必须包含全部条件。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_44d93f8cd1eb4a09b6211dc5a1023bfb

实际观察：
```json
[
  {
    "status": 200,
    "next_is_end": true,
    "matched": true
  }
]
```

## P2-AUTO-086 · tests/test_course_requirements.py::test_choice_jump_and_fallback_api[single-eq-a-b-False]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：创建选择题+后续文本题；配置跳转规则；发布；使用指定答案调用 next。
- 输入数据：kind、op、condition、answer、matched 参数，选项 a/b/c。
- 参数实例：`{"kind": "single", "op": "eq", "condition": "a", "answer": "b", "matched": false}`
- 预期结果：匹配则 END；不匹配则按顺序进入后续题；contains_all 允许额外选项但必须包含全部条件。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_048caf2b3f7e4276a364d89b6bb39e08

实际观察：
```json
[
  {
    "status": 200,
    "next_is_end": false,
    "matched": false
  }
]
```

## P2-AUTO-087 · tests/test_course_requirements.py::test_choice_jump_and_fallback_api[multiple-contains_any-condition2-answer2-True]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：创建选择题+后续文本题；配置跳转规则；发布；使用指定答案调用 next。
- 输入数据：kind、op、condition、answer、matched 参数，选项 a/b/c。
- 参数实例：`{"kind": "multiple", "op": "contains_any", "condition": ["a", "b"], "answer": ["b"], "matched": true}`
- 预期结果：匹配则 END；不匹配则按顺序进入后续题；contains_all 允许额外选项但必须包含全部条件。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_730a4fb8bb714d95ae3702735764390e

实际观察：
```json
[
  {
    "status": 200,
    "next_is_end": true,
    "matched": true
  }
]
```

## P2-AUTO-088 · tests/test_course_requirements.py::test_choice_jump_and_fallback_api[multiple-contains_any-condition3-answer3-False]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：创建选择题+后续文本题；配置跳转规则；发布；使用指定答案调用 next。
- 输入数据：kind、op、condition、answer、matched 参数，选项 a/b/c。
- 参数实例：`{"kind": "multiple", "op": "contains_any", "condition": ["a", "b"], "answer": ["c"], "matched": false}`
- 预期结果：匹配则 END；不匹配则按顺序进入后续题；contains_all 允许额外选项但必须包含全部条件。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_a19086c0ffd24b33987ba78678fa3b16

实际观察：
```json
[
  {
    "status": 200,
    "next_is_end": false,
    "matched": false
  }
]
```

## P2-AUTO-089 · tests/test_course_requirements.py::test_choice_jump_and_fallback_api[multiple-contains_all-condition4-answer4-True]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：创建选择题+后续文本题；配置跳转规则；发布；使用指定答案调用 next。
- 输入数据：kind、op、condition、answer、matched 参数，选项 a/b/c。
- 参数实例：`{"kind": "multiple", "op": "contains_all", "condition": ["a", "b"], "answer": ["a", "b", "c"], "matched": true}`
- 预期结果：匹配则 END；不匹配则按顺序进入后续题；contains_all 允许额外选项但必须包含全部条件。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_268b4e99efa74a2ab08a1cec88d24d2b

实际观察：
```json
[
  {
    "status": 200,
    "next_is_end": true,
    "matched": true
  }
]
```

## P2-AUTO-090 · tests/test_course_requirements.py::test_choice_jump_and_fallback_api[multiple-contains_all-condition5-answer5-False]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：创建选择题+后续文本题；配置跳转规则；发布；使用指定答案调用 next。
- 输入数据：kind、op、condition、answer、matched 参数，选项 a/b/c。
- 参数实例：`{"kind": "multiple", "op": "contains_all", "condition": ["a", "b"], "answer": ["a"], "matched": false}`
- 预期结果：匹配则 END；不匹配则按顺序进入后续题；contains_all 允许额外选项但必须包含全部条件。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_98be3e013d4a4ed58d8345d8275b285a

实际观察：
```json
[
  {
    "status": 200,
    "next_is_end": false,
    "matched": false
  }
]
```

## P2-AUTO-091 · tests/test_course_requirements.py::test_invalid_jump_api_does_not_mutate[self]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：创建两道数字题草稿；向第二题 PUT 非法规则；比较 MongoDB 文档。
- 输入数据：invalid 参数：自跳、回跳第一题、不存在的目标、数字题使用 contains_any。
- 参数实例：`{"invalid": "self"}`
- 预期结果：422；规则和 revision 均不变。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_7b90d984bcd14258b59ed18aad32a91c

实际观察：
```json
[
  {
    "status": 422,
    "document_unchanged": true
  }
]
```

## P2-AUTO-092 · tests/test_course_requirements.py::test_invalid_jump_api_does_not_mutate[backward]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：创建两道数字题草稿；向第二题 PUT 非法规则；比较 MongoDB 文档。
- 输入数据：invalid 参数：自跳、回跳第一题、不存在的目标、数字题使用 contains_any。
- 参数实例：`{"invalid": "backward"}`
- 预期结果：422；规则和 revision 均不变。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_27919172112d4102b4ccb66b9c5767aa

实际观察：
```json
[
  {
    "status": 422,
    "document_unchanged": true
  }
]
```

## P2-AUTO-093 · tests/test_course_requirements.py::test_invalid_jump_api_does_not_mutate[missing]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：创建两道数字题草稿；向第二题 PUT 非法规则；比较 MongoDB 文档。
- 输入数据：invalid 参数：自跳、回跳第一题、不存在的目标、数字题使用 contains_any。
- 参数实例：`{"invalid": "missing"}`
- 预期结果：422；规则和 revision 均不变。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_c4b5c861217d492584b648077861ee2b

实际观察：
```json
[
  {
    "status": 422,
    "document_unchanged": true
  }
]
```

## P2-AUTO-094 · tests/test_course_requirements.py::test_invalid_jump_api_does_not_mutate[wrong-operator]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：创建两道数字题草稿；向第二题 PUT 非法规则；比较 MongoDB 文档。
- 输入数据：invalid 参数：自跳、回跳第一题、不存在的目标、数字题使用 contains_any。
- 参数实例：`{"invalid": "wrong-operator"}`
- 预期结果：422；规则和 revision 均不变。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_339fa6fb068c422b9250cf60162f7fe0

实际观察：
```json
[
  {
    "status": 422,
    "document_unchanged": true
  }
]
```

## P2-AUTO-095 · tests/test_course_requirements.py::test_required_and_optional_all_types_api[required-single]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：创建并发布指定题型；按 required 配置留空提交；检查 responses。
- 输入数据：kind×required；answers={}。
- 参数实例：`{"required": true, "kind": "single"}`
- 预期结果：必答422且不保存；选答201，answers={}，path 包含该题。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_64eb6e506e5f46b0bb4b21b1dd723b04

实际观察：
```json
[
  {
    "status": 422,
    "saved_count": 0,
    "stored_answers": []
  }
]
```

## P2-AUTO-096 · tests/test_course_requirements.py::test_required_and_optional_all_types_api[required-multiple]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：创建并发布指定题型；按 required 配置留空提交；检查 responses。
- 输入数据：kind×required；answers={}。
- 参数实例：`{"required": true, "kind": "multiple"}`
- 预期结果：必答422且不保存；选答201，answers={}，path 包含该题。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_32cb0c35261e4783bc61b74a83fc4a47

实际观察：
```json
[
  {
    "status": 422,
    "saved_count": 0,
    "stored_answers": []
  }
]
```

## P2-AUTO-097 · tests/test_course_requirements.py::test_required_and_optional_all_types_api[required-text]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：创建并发布指定题型；按 required 配置留空提交；检查 responses。
- 输入数据：kind×required；answers={}。
- 参数实例：`{"required": true, "kind": "text"}`
- 预期结果：必答422且不保存；选答201，answers={}，path 包含该题。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_27565b4154ed4dc3af71b620a2f2b3fb

实际观察：
```json
[
  {
    "status": 422,
    "saved_count": 0,
    "stored_answers": []
  }
]
```

## P2-AUTO-098 · tests/test_course_requirements.py::test_required_and_optional_all_types_api[required-number]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：创建并发布指定题型；按 required 配置留空提交；检查 responses。
- 输入数据：kind×required；answers={}。
- 参数实例：`{"required": true, "kind": "number"}`
- 预期结果：必答422且不保存；选答201，answers={}，path 包含该题。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_e3bc69813a854643b6427a13d8097adb

实际观察：
```json
[
  {
    "status": 422,
    "saved_count": 0,
    "stored_answers": []
  }
]
```

## P2-AUTO-099 · tests/test_course_requirements.py::test_required_and_optional_all_types_api[optional-single]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：创建并发布指定题型；按 required 配置留空提交；检查 responses。
- 输入数据：kind×required；answers={}。
- 参数实例：`{"required": false, "kind": "single"}`
- 预期结果：必答422且不保存；选答201，answers={}，path 包含该题。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_27a436287b8343b69bd95992b855e333

实际观察：
```json
[
  {
    "status": 201,
    "saved_count": 1,
    "stored_answers": [
      {}
    ]
  }
]
```

## P2-AUTO-100 · tests/test_course_requirements.py::test_required_and_optional_all_types_api[optional-multiple]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：创建并发布指定题型；按 required 配置留空提交；检查 responses。
- 输入数据：kind×required；answers={}。
- 参数实例：`{"required": false, "kind": "multiple"}`
- 预期结果：必答422且不保存；选答201，answers={}，path 包含该题。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_fa50e6be32dd400e82c63fadc00b91a8

实际观察：
```json
[
  {
    "status": 201,
    "saved_count": 1,
    "stored_answers": [
      {}
    ]
  }
]
```

## P2-AUTO-101 · tests/test_course_requirements.py::test_required_and_optional_all_types_api[optional-text]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：创建并发布指定题型；按 required 配置留空提交；检查 responses。
- 输入数据：kind×required；answers={}。
- 参数实例：`{"required": false, "kind": "text"}`
- 预期结果：必答422且不保存；选答201，answers={}，path 包含该题。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_413fa3253a874ac18872c782a252ebcb

实际观察：
```json
[
  {
    "status": 201,
    "saved_count": 1,
    "stored_answers": [
      {}
    ]
  }
]
```

## P2-AUTO-102 · tests/test_course_requirements.py::test_required_and_optional_all_types_api[optional-number]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：创建并发布指定题型；按 required 配置留空提交；检查 responses。
- 输入数据：kind×required；answers={}。
- 参数实例：`{"required": false, "kind": "number"}`
- 预期结果：必答422且不保存；选答201，answers={}，path 包含该题。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_5235cc93fef34c3bb9da4af29c8b0e71

实际观察：
```json
[
  {
    "status": 201,
    "saved_count": 1,
    "stored_answers": [
      {}
    ]
  }
]
```

## P2-AUTO-103 · tests/test_course_requirements.py::test_answer_validation_submission_boundaries[multi-below]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：按配置创建发布单题问卷；提交参数答案；同时核对 HTTP 与 MongoDB。
- 输入数据：kind、constraints、answer、expected 参数；选项 a/b/c。
- 参数实例：`{"kind": "multiple", "constraints": {"min_choices": 2, "max_choices": 2}, "answer": ["a"], "expected": 422}`
- 预期结果：合法边界201且原值保存；非法422且零答卷。多选精确2项、文本2～4字符、数字0～120整数。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_2445fb043b404ecd9c04c7df5b4573b0

实际观察：
```json
[
  {
    "status": 422,
    "saved_count": 0,
    "stored_values": []
  }
]
```

## P2-AUTO-104 · tests/test_course_requirements.py::test_answer_validation_submission_boundaries[multi-exact]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：按配置创建发布单题问卷；提交参数答案；同时核对 HTTP 与 MongoDB。
- 输入数据：kind、constraints、answer、expected 参数；选项 a/b/c。
- 参数实例：`{"kind": "multiple", "constraints": {"min_choices": 2, "max_choices": 2}, "answer": ["a", "b"], "expected": 201}`
- 预期结果：合法边界201且原值保存；非法422且零答卷。多选精确2项、文本2～4字符、数字0～120整数。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_cc913c64cfec471e87cc5287f3a69770

实际观察：
```json
[
  {
    "status": 201,
    "saved_count": 1,
    "stored_values": [
      [
        [
          "a",
          "b"
        ]
      ]
    ]
  }
]
```

## P2-AUTO-105 · tests/test_course_requirements.py::test_answer_validation_submission_boundaries[multi-above]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：按配置创建发布单题问卷；提交参数答案；同时核对 HTTP 与 MongoDB。
- 输入数据：kind、constraints、answer、expected 参数；选项 a/b/c。
- 参数实例：`{"kind": "multiple", "constraints": {"min_choices": 2, "max_choices": 2}, "answer": ["a", "b", "c"], "expected": 422}`
- 预期结果：合法边界201且原值保存；非法422且零答卷。多选精确2项、文本2～4字符、数字0～120整数。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_1df9a3ced73f4e59a0d76471464e90bd

实际观察：
```json
[
  {
    "status": 422,
    "saved_count": 0,
    "stored_values": []
  }
]
```

## P2-AUTO-106 · tests/test_course_requirements.py::test_answer_validation_submission_boundaries[multi-duplicate]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：按配置创建发布单题问卷；提交参数答案；同时核对 HTTP 与 MongoDB。
- 输入数据：kind、constraints、answer、expected 参数；选项 a/b/c。
- 参数实例：`{"kind": "multiple", "constraints": {}, "answer": ["a", "a"], "expected": 422}`
- 预期结果：合法边界201且原值保存；非法422且零答卷。多选精确2项、文本2～4字符、数字0～120整数。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_4d323b9c6c784223a1cf4579a7f081cb

实际观察：
```json
[
  {
    "status": 422,
    "saved_count": 0,
    "stored_values": []
  }
]
```

## P2-AUTO-107 · tests/test_course_requirements.py::test_answer_validation_submission_boundaries[multi-unknown]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：按配置创建发布单题问卷；提交参数答案；同时核对 HTTP 与 MongoDB。
- 输入数据：kind、constraints、answer、expected 参数；选项 a/b/c。
- 参数实例：`{"kind": "multiple", "constraints": {}, "answer": ["a", "missing"], "expected": 422}`
- 预期结果：合法边界201且原值保存；非法422且零答卷。多选精确2项、文本2～4字符、数字0～120整数。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_b352284d3241445480bb9f05a44067cd

实际观察：
```json
[
  {
    "status": 422,
    "saved_count": 0,
    "stored_values": []
  }
]
```

## P2-AUTO-108 · tests/test_course_requirements.py::test_answer_validation_submission_boundaries[single-valid]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：按配置创建发布单题问卷；提交参数答案；同时核对 HTTP 与 MongoDB。
- 输入数据：kind、constraints、answer、expected 参数；选项 a/b/c。
- 参数实例：`{"kind": "single", "constraints": {}, "answer": "a", "expected": 201}`
- 预期结果：合法边界201且原值保存；非法422且零答卷。多选精确2项、文本2～4字符、数字0～120整数。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_6f19624ec5434b0086e3e8d73a9da0f6

实际观察：
```json
[
  {
    "status": 201,
    "saved_count": 1,
    "stored_values": [
      [
        "a"
      ]
    ]
  }
]
```

## P2-AUTO-109 · tests/test_course_requirements.py::test_answer_validation_submission_boundaries[single-unknown]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：按配置创建发布单题问卷；提交参数答案；同时核对 HTTP 与 MongoDB。
- 输入数据：kind、constraints、answer、expected 参数；选项 a/b/c。
- 参数实例：`{"kind": "single", "constraints": {}, "answer": "missing", "expected": 422}`
- 预期结果：合法边界201且原值保存；非法422且零答卷。多选精确2项、文本2～4字符、数字0～120整数。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_9c43844179ec4e059b95adbd251ef0b5

实际观察：
```json
[
  {
    "status": 422,
    "saved_count": 0,
    "stored_values": []
  }
]
```

## P2-AUTO-110 · tests/test_course_requirements.py::test_answer_validation_submission_boundaries[text-below]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：按配置创建发布单题问卷；提交参数答案；同时核对 HTTP 与 MongoDB。
- 输入数据：kind、constraints、answer、expected 参数；选项 a/b/c。
- 参数实例：`{"kind": "text", "constraints": {"min_length": 2, "max_length": 4}, "answer": "中", "expected": 422}`
- 预期结果：合法边界201且原值保存；非法422且零答卷。多选精确2项、文本2～4字符、数字0～120整数。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_6caa1a9a729645a3a820c89ff58971da

实际观察：
```json
[
  {
    "status": 422,
    "saved_count": 0,
    "stored_values": []
  }
]
```

## P2-AUTO-111 · tests/test_course_requirements.py::test_answer_validation_submission_boundaries[text-min]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：按配置创建发布单题问卷；提交参数答案；同时核对 HTTP 与 MongoDB。
- 输入数据：kind、constraints、answer、expected 参数；选项 a/b/c。
- 参数实例：`{"kind": "text", "constraints": {"min_length": 2, "max_length": 4}, "answer": "中文", "expected": 201}`
- 预期结果：合法边界201且原值保存；非法422且零答卷。多选精确2项、文本2～4字符、数字0～120整数。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_feb4a7e4f6ee4352b69a1384f7e5b65b

实际观察：
```json
[
  {
    "status": 201,
    "saved_count": 1,
    "stored_values": [
      [
        "中文"
      ]
    ]
  }
]
```

## P2-AUTO-112 · tests/test_course_requirements.py::test_answer_validation_submission_boundaries[text-max]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：按配置创建发布单题问卷；提交参数答案；同时核对 HTTP 与 MongoDB。
- 输入数据：kind、constraints、answer、expected 参数；选项 a/b/c。
- 参数实例：`{"kind": "text", "constraints": {"min_length": 2, "max_length": 4}, "answer": "中文反馈", "expected": 201}`
- 预期结果：合法边界201且原值保存；非法422且零答卷。多选精确2项、文本2～4字符、数字0～120整数。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_6ce6872b8160490d846f584bc726b556

实际观察：
```json
[
  {
    "status": 201,
    "saved_count": 1,
    "stored_values": [
      [
        "中文反馈"
      ]
    ]
  }
]
```

## P2-AUTO-113 · tests/test_course_requirements.py::test_answer_validation_submission_boundaries[text-above]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：按配置创建发布单题问卷；提交参数答案；同时核对 HTTP 与 MongoDB。
- 输入数据：kind、constraints、answer、expected 参数；选项 a/b/c。
- 参数实例：`{"kind": "text", "constraints": {"min_length": 2, "max_length": 4}, "answer": "中文反馈好", "expected": 422}`
- 预期结果：合法边界201且原值保存；非法422且零答卷。多选精确2项、文本2～4字符、数字0～120整数。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_78f08686e392437aa4d420589f6eaf5a

实际观察：
```json
[
  {
    "status": 422,
    "saved_count": 0,
    "stored_values": []
  }
]
```

## P2-AUTO-114 · tests/test_course_requirements.py::test_answer_validation_submission_boundaries[number-below]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：按配置创建发布单题问卷；提交参数答案；同时核对 HTTP 与 MongoDB。
- 输入数据：kind、constraints、answer、expected 参数；选项 a/b/c。
- 参数实例：`{"kind": "number", "constraints": {"min_value": 0, "max_value": 120, "integer": true}, "answer": -1, "expected": 422}`
- 预期结果：合法边界201且原值保存；非法422且零答卷。多选精确2项、文本2～4字符、数字0～120整数。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_560b1719701a47c3af967bb52bb79cb4

实际观察：
```json
[
  {
    "status": 422,
    "saved_count": 0,
    "stored_values": []
  }
]
```

## P2-AUTO-115 · tests/test_course_requirements.py::test_answer_validation_submission_boundaries[number-min]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：按配置创建发布单题问卷；提交参数答案；同时核对 HTTP 与 MongoDB。
- 输入数据：kind、constraints、answer、expected 参数；选项 a/b/c。
- 参数实例：`{"kind": "number", "constraints": {"min_value": 0, "max_value": 120, "integer": true}, "answer": 0, "expected": 201}`
- 预期结果：合法边界201且原值保存；非法422且零答卷。多选精确2项、文本2～4字符、数字0～120整数。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_8c9102729a17427c94b9984412eeeecb

实际观察：
```json
[
  {
    "status": 201,
    "saved_count": 1,
    "stored_values": [
      [
        0
      ]
    ]
  }
]
```

## P2-AUTO-116 · tests/test_course_requirements.py::test_answer_validation_submission_boundaries[number-max]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：按配置创建发布单题问卷；提交参数答案；同时核对 HTTP 与 MongoDB。
- 输入数据：kind、constraints、answer、expected 参数；选项 a/b/c。
- 参数实例：`{"kind": "number", "constraints": {"min_value": 0, "max_value": 120, "integer": true}, "answer": 120, "expected": 201}`
- 预期结果：合法边界201且原值保存；非法422且零答卷。多选精确2项、文本2～4字符、数字0～120整数。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_5bbfcdd6a1da4bd788885a754a90e1b0

实际观察：
```json
[
  {
    "status": 201,
    "saved_count": 1,
    "stored_values": [
      [
        120
      ]
    ]
  }
]
```

## P2-AUTO-117 · tests/test_course_requirements.py::test_answer_validation_submission_boundaries[number-above]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：按配置创建发布单题问卷；提交参数答案；同时核对 HTTP 与 MongoDB。
- 输入数据：kind、constraints、answer、expected 参数；选项 a/b/c。
- 参数实例：`{"kind": "number", "constraints": {"min_value": 0, "max_value": 120, "integer": true}, "answer": 121, "expected": 422}`
- 预期结果：合法边界201且原值保存；非法422且零答卷。多选精确2项、文本2～4字符、数字0～120整数。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_66218384406447cf92cabafaacd9b64c

实际观察：
```json
[
  {
    "status": 422,
    "saved_count": 0,
    "stored_values": []
  }
]
```

## P2-AUTO-118 · tests/test_course_requirements.py::test_answer_validation_submission_boundaries[integer-fraction]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：按配置创建发布单题问卷；提交参数答案；同时核对 HTTP 与 MongoDB。
- 输入数据：kind、constraints、answer、expected 参数；选项 a/b/c。
- 参数实例：`{"kind": "number", "constraints": {"integer": true}, "answer": 1.5, "expected": 422}`
- 预期结果：合法边界201且原值保存；非法422且零答卷。多选精确2项、文本2～4字符、数字0～120整数。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_b7b5e5820a174248b059a9c36874ef5d

实际观察：
```json
[
  {
    "status": 422,
    "saved_count": 0,
    "stored_values": []
  }
]
```

## P2-AUTO-119 · tests/test_course_requirements.py::test_answer_validation_submission_boundaries[decimal-valid]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：按配置创建发布单题问卷；提交参数答案；同时核对 HTTP 与 MongoDB。
- 输入数据：kind、constraints、answer、expected 参数；选项 a/b/c。
- 参数实例：`{"kind": "number", "constraints": {"integer": false}, "answer": 1.5, "expected": 201}`
- 预期结果：合法边界201且原值保存；非法422且零答卷。多选精确2项、文本2～4字符、数字0～120整数。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_99023ce72eed41bc9f77c7cbcaf780b1

实际观察：
```json
[
  {
    "status": 201,
    "saved_count": 1,
    "stored_values": [
      [
        1.5
      ]
    ]
  }
]
```

## P2-AUTO-120 · tests/test_course_requirements.py::test_answer_validation_submission_boundaries[number-bool]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：按配置创建发布单题问卷；提交参数答案；同时核对 HTTP 与 MongoDB。
- 输入数据：kind、constraints、answer、expected 参数；选项 a/b/c。
- 参数实例：`{"kind": "number", "constraints": {}, "answer": true, "expected": 422}`
- 预期结果：合法边界201且原值保存；非法422且零答卷。多选精确2项、文本2～4字符、数字0～120整数。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_83b36b9b37fd4ee8bf1aba0a41cfd64b

实际观察：
```json
[
  {
    "status": 422,
    "saved_count": 0,
    "stored_values": []
  }
]
```

## P2-AUTO-121 · tests/test_course_requirements.py::test_answer_validation_submission_boundaries[number-string]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：按配置创建发布单题问卷；提交参数答案；同时核对 HTTP 与 MongoDB。
- 输入数据：kind、constraints、answer、expected 参数；选项 a/b/c。
- 参数实例：`{"kind": "number", "constraints": {}, "answer": "12", "expected": 422}`
- 预期结果：合法边界201且原值保存；非法422且零答卷。多选精确2项、文本2～4字符、数字0～120整数。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_5dc04204fdb140fca453d970d4b06b85

实际观察：
```json
[
  {
    "status": 422,
    "saved_count": 0,
    "stored_values": []
  }
]
```

## P2-AUTO-122 · tests/test_course_requirements.py::test_submit_rejects_invalid_context_without_save[unauthenticated-401]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：准备问卷；按 failure 场景调用 submit；检查零答卷。
- 输入数据：未登录、草稿、包含未知题目、包含被跳过题目的额外答案。
- 参数实例：`{"failure": "unauthenticated", "expected": 401}`
- 预期结果：分别401、404、422、422；responses 不新增记录。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_42392a8c86794466838030aeb658db12

实际观察：
```json
[
  {
    "status": 401,
    "responses": 0
  }
]
```

## P2-AUTO-123 · tests/test_course_requirements.py::test_submit_rejects_invalid_context_without_save[draft-404]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：准备问卷；按 failure 场景调用 submit；检查零答卷。
- 输入数据：未登录、草稿、包含未知题目、包含被跳过题目的额外答案。
- 参数实例：`{"failure": "draft", "expected": 404}`
- 预期结果：分别401、404、422、422；responses 不新增记录。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_17e81837f0f94a5f8580357f54831a75

实际观察：
```json
[
  {
    "status": 404,
    "responses": 0
  }
]
```

## P2-AUTO-124 · tests/test_course_requirements.py::test_submit_rejects_invalid_context_without_save[unknown-answer-422]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：准备问卷；按 failure 场景调用 submit；检查零答卷。
- 输入数据：未登录、草稿、包含未知题目、包含被跳过题目的额外答案。
- 参数实例：`{"failure": "unknown-answer", "expected": 422}`
- 预期结果：分别401、404、422、422；responses 不新增记录。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_4109b7d2cc5144bab446dfb3f2df7726

实际观察：
```json
[
  {
    "status": 422,
    "responses": 0
  }
]
```

## P2-AUTO-125 · tests/test_course_requirements.py::test_submit_rejects_invalid_context_without_save[skipped-answer-422]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：准备问卷；按 failure 场景调用 submit；检查零答卷。
- 输入数据：未登录、草稿、包含未知题目、包含被跳过题目的额外答案。
- 参数实例：`{"failure": "skipped-answer", "expected": 422}`
- 预期结果：分别401、404、422、422；responses 不新增记录。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_f26f7cafd4a448f08ba7bdf753adcc64

实际观察：
```json
[
  {
    "status": 422,
    "responses": 0
  }
]
```

## P2-AUTO-126 · tests/test_course_requirements.py::test_distinct_users_can_each_submit_and_persist

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：创建每人一次问卷；两位不同用户分别提交；读取数据库。
- 输入数据：第一用户数字10，第二用户数字30。
- 参数实例：`{}`
- 预期结果：两次201，答卷ID不同，survey_id一致、respondent_id不同，各自答案与路径保存准确。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_5391d24d9b3540d39d2d3e1805adefb3

实际观察：
```json
[
  {
    "statuses": [
      201,
      201
    ],
    "responses": 2,
    "distinct_response_ids": 2,
    "distinct_users": 2
  }
]
```

## P2-AUTO-127 · tests/test_course_requirements.py::test_all_question_stats_zero_optional_and_refresh

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：创建四类选答题并发布，允许多次；先读空统计；提交完整答卷和全空答卷；逐题与整卷比较；再提交并检查统计更新。
- 输入数据：完整答案 single=a、multiple=[a,b]、text=反馈、number=10；第二份为空；第三份数字30。
- 参数实例：`{}`
- 预期结果：总答卷数0→2→3；四类单题结果与整卷一致；未选c=0；空答案不计有效回答；数字均值10→20。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_fe3a557ccac04d1a8c396d1c90877027

实际观察：
```json
[
  {
    "first_total": 2,
    "answer_counts": [
      1,
      1,
      1,
      1
    ],
    "single_question_types_checked": [
      "single",
      "multiple",
      "text",
      "number"
    ],
    "refreshed": {
      "survey_id": "330da391-d1f4-4335-9861-12c9b74e0d8a",
      "total_responses": 3,
      "question_id": "03d63851-59b8-4e32-8d45-9dca849b8de0",
      "title": "课程测试题",
      "type": "number",
      "answer_count": 2,
      "values": [
        10,
        30
      ],
      "average": 20.0
    }
  }
]
```

## P2-AUTO-128 · tests/test_course_requirements.py::test_stats_isolate_surveys_and_reject_foreign_questions

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：同一创建者建立两份问卷并各提交；查询整卷、其他问卷题ID、不存在题ID。
- 输入数据：问卷A答案10，问卷B答案1000。
- 参数实例：`{}`
- 预期结果：各自总数1、均值10和1000；A的单题接口使用B的题ID或未知ID返回404。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_a7df2f1ccb2a4087aca82c09167400b8

实际观察：
```json
[
  {
    "survey_averages": [
      10,
      1000
    ],
    "invalid_question_statuses": [
      404,
      404
    ]
  }
]
```

## P2-AUTO-129 · tests/test_password_policy.py::test_registration_password_bounds[aaaaaaa-422]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：用指定长度注册；核对响应与用户数；合法密码再次登录。
- 输入数据：7、8、16、17、128字符及8/16/17个Unicode字符
- 参数实例：`{"password": "aaaaaaa", "expected": 422}`
- 预期结果：仅8～16字符可注册，非法请求422且不写入；合法账号可登录。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_d4f8a0c61b524949b5f25867c45eb056

## P2-AUTO-130 · tests/test_password_policy.py::test_registration_password_bounds[aaaaaaaa-201]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：用指定长度注册；核对响应与用户数；合法密码再次登录。
- 输入数据：7、8、16、17、128字符及8/16/17个Unicode字符
- 参数实例：`{"password": "aaaaaaaa", "expected": 201}`
- 预期结果：仅8～16字符可注册，非法请求422且不写入；合法账号可登录。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_e037f6c3b5fb44e8ab534e528e4631b9

## P2-AUTO-131 · tests/test_password_policy.py::test_registration_password_bounds[aaaaaaaaaaaaaaaa-201]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：用指定长度注册；核对响应与用户数；合法密码再次登录。
- 输入数据：7、8、16、17、128字符及8/16/17个Unicode字符
- 参数实例：`{"password": "aaaaaaaaaaaaaaaa", "expected": 201}`
- 预期结果：仅8～16字符可注册，非法请求422且不写入；合法账号可登录。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_63647c6678844de2b4b6c87f0df3b28a

## P2-AUTO-132 · tests/test_password_policy.py::test_registration_password_bounds[aaaaaaaaaaaaaaaaa-422]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：用指定长度注册；核对响应与用户数；合法密码再次登录。
- 输入数据：7、8、16、17、128字符及8/16/17个Unicode字符
- 参数实例：`{"password": "aaaaaaaaaaaaaaaaa", "expected": 422}`
- 预期结果：仅8～16字符可注册，非法请求422且不写入；合法账号可登录。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_6c0a99936b6a495f880eeafa033de140

## P2-AUTO-133 · tests/test_password_policy.py::test_registration_password_bounds[aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa-422]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：用指定长度注册；核对响应与用户数；合法密码再次登录。
- 输入数据：7、8、16、17、128字符及8/16/17个Unicode字符
- 参数实例：`{"password": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", "expected": 422}`
- 预期结果：仅8～16字符可注册，非法请求422且不写入；合法账号可登录。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_d92390ef9ea44b24a18b2d62f6523d3e

## P2-AUTO-134 · tests/test_password_policy.py::test_registration_password_bounds[\U0001f600\U0001f600\U0001f600\U0001f600\U0001f600\U0001f600\U0001f600\U0001f600-201]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：用指定长度注册；核对响应与用户数；合法密码再次登录。
- 输入数据：7、8、16、17、128字符及8/16/17个Unicode字符
- 参数实例：`{"password": "😀😀😀😀😀😀😀😀", "expected": 201}`
- 预期结果：仅8～16字符可注册，非法请求422且不写入；合法账号可登录。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_2ea88db02cdb4a8e9a2834ff7533e997

## P2-AUTO-135 · tests/test_password_policy.py::test_registration_password_bounds[\U0001f600\U0001f600\U0001f600\U0001f600\U0001f600\U0001f600\U0001f600\U0001f600\U0001f600\U0001f600\U0001f600\U0001f600\U0001f600\U0001f600\U0001f600\U0001f600-201]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：用指定长度注册；核对响应与用户数；合法密码再次登录。
- 输入数据：7、8、16、17、128字符及8/16/17个Unicode字符
- 参数实例：`{"password": "😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀", "expected": 201}`
- 预期结果：仅8～16字符可注册，非法请求422且不写入；合法账号可登录。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_39c4f27e08ad47e6802072bb2a96024d

## P2-AUTO-136 · tests/test_password_policy.py::test_registration_password_bounds[\U0001f600\U0001f600\U0001f600\U0001f600\U0001f600\U0001f600\U0001f600\U0001f600\U0001f600\U0001f600\U0001f600\U0001f600\U0001f600\U0001f600\U0001f600\U0001f600\U0001f600-422]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：用指定长度注册；核对响应与用户数；合法密码再次登录。
- 输入数据：7、8、16、17、128字符及8/16/17个Unicode字符
- 参数实例：`{"password": "😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀", "expected": 422}`
- 预期结果：仅8～16字符可注册，非法请求422且不写入；合法账号可登录。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_71d2e0bb21a54d3ca5a29b5d2201a705

## P2-AUTO-137 · tests/test_password_policy.py::test_legacy_long_password_login[17]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：在隔离库按原哈希算法准备历史账号；正确和错误密码登录；比较用户记录。
- 输入数据：17、64、128字符历史密码
- 参数实例：`{"length": 17}`
- 预期结果：正确密码200，错误密码401；用户记录不变。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_f0361a7c146541c9883c1d45165959db

## P2-AUTO-138 · tests/test_password_policy.py::test_legacy_long_password_login[64]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：在隔离库按原哈希算法准备历史账号；正确和错误密码登录；比较用户记录。
- 输入数据：17、64、128字符历史密码
- 参数实例：`{"length": 64}`
- 预期结果：正确密码200，错误密码401；用户记录不变。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_aead5a3f5f9a491493ccb1265636a38f

## P2-AUTO-139 · tests/test_password_policy.py::test_legacy_long_password_login[128]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：在隔离库按原哈希算法准备历史账号；正确和错误密码登录；比较用户记录。
- 输入数据：17、64、128字符历史密码
- 参数实例：`{"length": 128}`
- 预期结果：正确密码200，错误密码401；用户记录不变。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_6383c1aeea8641008c789b411a2d280d

## P2-AUTO-140 · tests/test_phase2_block1.py::test_additive_repeat_legacy

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：保存旧问卷与答卷；执行迁移两次；读取旧接口并比较原文档。
- 输入数据：无source的旧问卷和答卷
- 参数实例：`{}`
- 预期结果：两次迁移成功；旧文档完全不变；旧接口可读。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_cf1bf6ff018e4605b171d45503fb96b7

## P2-AUTO-141 · tests/test_phase2_block1.py::test_migration_retry_and_validation

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：故障注入使索引创建中断；恢复后重复迁移；尝试非法写入。
- 输入数据：模拟create_index抛出异常；缺少必要字段的版本
- 参数实例：`{}`
- 预期结果：可安全重试；新集合验证拒绝非法文档。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_a728398255514e3d8643ab8de870cf16

## P2-AUTO-142 · tests/test_phase2_block2.py::test_bank_crud_four_types[single]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：创建题库与题目；读取、编辑题库；移出再加入；对比MongoDB版本。
- 输入数据：四种题型，题库名称更新
- 参数实例：`{"kind": "single"}`
- 预期结果：完整保存内容；稳定题目族；移出不删除版本；可重新加入。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_a965dceb109841ae9419d6cd1e08019f

## P2-AUTO-143 · tests/test_phase2_block2.py::test_bank_crud_four_types[multiple]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：创建题库与题目；读取、编辑题库；移出再加入；对比MongoDB版本。
- 输入数据：四种题型，题库名称更新
- 参数实例：`{"kind": "multiple"}`
- 预期结果：完整保存内容；稳定题目族；移出不删除版本；可重新加入。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_8bca296cb455434882a95830ea6e5117

## P2-AUTO-144 · tests/test_phase2_block2.py::test_bank_crud_four_types[text]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：创建题库与题目；读取、编辑题库；移出再加入；对比MongoDB版本。
- 输入数据：四种题型，题库名称更新
- 参数实例：`{"kind": "text"}`
- 预期结果：完整保存内容；稳定题目族；移出不删除版本；可重新加入。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_a9e6e863390e4f1385f9a4269024c286

## P2-AUTO-145 · tests/test_phase2_block2.py::test_bank_crud_four_types[number]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：创建题库与题目；读取、编辑题库；移出再加入；对比MongoDB版本。
- 输入数据：四种题型，题库名称更新
- 参数实例：`{"kind": "number"}`
- 预期结果：完整保存内容；稳定题目族；移出不删除版本；可重新加入。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_2f9595f6cf544b99ad99b5e562ab4d3c

## P2-AUTO-146 · tests/test_phase2_block2.py::test_bank_validation_permissions

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：尝试额外字段、无效题目和他人访问；检查数据库。
- 输入数据：source伪造、选项不足、其他用户
- 参数实例：`{}`
- 预期结果：422或404/401；没有无效写入。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_7124e716916c4caf8242ddfc3ca59ba4

## P2-AUTO-147 · tests/test_phase2_block3.py::test_branch_restore_immutable

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：创建新版本、从初版分支、恢复初版；比较历史文档并重复恢复。
- 输入数据：V1→V2，V1→V3，恢复V1生成V4
- 参数实例：`{}`
- 预期结果：父版本与恢复来源正确；V1未变；重复请求返回同一V4。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_cdfbec800c7b464ebac5a87886a9ea61

## P2-AUTO-148 · tests/test_phase2_block3.py::test_version_concurrent_idempotency

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：并发发送相同请求；再并发发送不同请求；复用键改变内容。
- 输入数据：4个相同请求、4个不同键、冲突内容
- 参数实例：`{}`
- 预期结果：相同请求仅一版本；不同请求序号唯一；冲突409。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_4aa3e97987c34797a8dadb472772a657

## P2-AUTO-149 · tests/test_phase2_block3.py::test_version_retry_after_lost_ack

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：模拟版本写入成功但响应丢失；相同键重试；检查数量。
- 输入数据：insert_one完成后抛出RuntimeError
- 参数实例：`{}`
- 预期结果：异常后恢复同一已提交版本；不重复插入。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_4acc211b877e4705872bb1d5cdc0dcd9

## P2-AUTO-150 · tests/test_phase2_block3.py::test_version_invalid_parent_and_permissions

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：他人创建/恢复；不存在或其他题目版本作为父版本；尝试覆盖版本。
- 输入数据：其他账号、错误parent、PUT版本
- 参数实例：`{}`
- 预期结果：404/405；历史内容不变。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_71ba5e5abafc437d8f868e687448443f

## P2-AUTO-151 · tests/test_phase2_block4.py::test_snapshots_and_published_freeze

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：同版本加入两次；创建新版本；显式换版；发布、提交后尝试换版。
- 输入数据：数字题V1、V2；答案键为实例ID
- 参数实例：`{}`
- 预期结果：实例ID不同；原快照不自动更新；换版保持ID；发布后拒绝；答卷不变。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_895bd2bc45a54e3a906631ba7f32c268

## P2-AUTO-152 · tests/test_phase2_block4.py::test_replacement_atomic_rule_rejection[type]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：配置规则后换成不兼容版本，或模拟损坏目标；比较完整问卷。
- 输入数据：数字gt规则改文本；单选移除条件选项；无效跳转目标
- 参数实例：`{"scenario": "type"}`
- 预期结果：422且问卷快照、规则、revision完全不变。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_84f3d9e9194a46de98b3792d215a64c4

## P2-AUTO-153 · tests/test_phase2_block4.py::test_replacement_atomic_rule_rejection[option]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：配置规则后换成不兼容版本，或模拟损坏目标；比较完整问卷。
- 输入数据：数字gt规则改文本；单选移除条件选项；无效跳转目标
- 参数实例：`{"scenario": "option"}`
- 预期结果：422且问卷快照、规则、revision完全不变。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_bad9533683864530b782b6360f6fcc71

## P2-AUTO-154 · tests/test_phase2_block4.py::test_replacement_atomic_rule_rejection[target]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：配置规则后换成不兼容版本，或模拟损坏目标；比较完整问卷。
- 输入数据：数字gt规则改文本；单选移除条件选项；无效跳转目标
- 参数实例：`{"scenario": "target"}`
- 预期结果：422且问卷快照、规则、revision完全不变。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_6ed5d857504947039a25e7b92512da0c

## P2-AUTO-155 · tests/test_phase2_block5.py::test_share_revoke_snapshot_and_usage_isolation

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：分享给另一账号；复用；尝试编辑、查看问卷答卷；撤销后再访问。
- 输入数据：owner/alice、reader、stranger
- 参数实例：`{}`
- 预期结果：共享仅查看复用；撤销阻止新复用；已有快照仍可发布填写；使用清单不泄露他人问卷。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_38c3db1744fd4d42bead0faaa81d8f5b

## P2-AUTO-156 · tests/test_phase2_block5.py::test_share_validation_idempotency

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：无权限账号撤销、分享不存在账号、重复分享和撤销。
- 输入数据：missing用户名、reader、匿名请求
- 参数实例：`{}`
- 预期结果：401/404；重复操作幂等，不重复存储共享对象。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_b75cd1dfeb7b42d4b79a5a4a33d733b9

## P2-AUTO-157 · tests/test_phase2_block6.py::test_cross_four_types[single-values0]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：同一版本加入两个问卷；分别提交；查询跨问卷统计。
- 输入数据：单选a/b，多选[a,b]/[b]，文本甲/乙，数字10/20
- 参数实例：`{"kind": "single", "values": ["a", "b"]}`
- 预期结果：答卷2、实例2、回答2；选项/文本/均值和分布精确。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_957d1c33ec174dbb8236a1a36bbe1472

## P2-AUTO-158 · tests/test_phase2_block6.py::test_cross_four_types[multiple-values1]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：同一版本加入两个问卷；分别提交；查询跨问卷统计。
- 输入数据：单选a/b，多选[a,b]/[b]，文本甲/乙，数字10/20
- 参数实例：`{"kind": "multiple", "values": [["a", "b"], ["b"]]}`
- 预期结果：答卷2、实例2、回答2；选项/文本/均值和分布精确。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_44b6b05a80b145269ff0bd905f4908fe

## P2-AUTO-159 · tests/test_phase2_block6.py::test_cross_four_types[text-values2]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：同一版本加入两个问卷；分别提交；查询跨问卷统计。
- 输入数据：单选a/b，多选[a,b]/[b]，文本甲/乙，数字10/20
- 参数实例：`{"kind": "text", "values": ["甲", "乙"]}`
- 预期结果：答卷2、实例2、回答2；选项/文本/均值和分布精确。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_78f75d26f9f44ef78b61d77792c321fb

## P2-AUTO-160 · tests/test_phase2_block6.py::test_cross_four_types[number-values3]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：同一版本加入两个问卷；分别提交；查询跨问卷统计。
- 输入数据：单选a/b，多选[a,b]/[b]，文本甲/乙，数字10/20
- 参数实例：`{"kind": "number", "values": [10, 20]}`
- 预期结果：答卷2、实例2、回答2；选项/文本/均值和分布精确。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_99fe7df91b454524a564d5ba4e74f27d

## P2-AUTO-161 · tests/test_phase2_block6.py::test_cross_empty[single]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：保存题目但无问卷答卷；查询统计。
- 输入数据：四种题型
- 参数实例：`{"kind": "single"}`
- 预期结果：答卷和回答数0；数字平均值null、分布空。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_6c277d8ea0394233b81ceb6e1ca7c0d2

## P2-AUTO-162 · tests/test_phase2_block6.py::test_cross_empty[multiple]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：保存题目但无问卷答卷；查询统计。
- 输入数据：四种题型
- 参数实例：`{"kind": "multiple"}`
- 预期结果：答卷和回答数0；数字平均值null、分布空。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_cfb04725c8754aa0ac18972b6b780004

## P2-AUTO-163 · tests/test_phase2_block6.py::test_cross_empty[text]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：保存题目但无问卷答卷；查询统计。
- 输入数据：四种题型
- 参数实例：`{"kind": "text"}`
- 预期结果：答卷和回答数0；数字平均值null、分布空。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_0e3f477eb39b42749b1daf2b91799664

## P2-AUTO-164 · tests/test_phase2_block6.py::test_cross_empty[number]

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：保存题目但无问卷答卷；查询统计。
- 输入数据：四种题型
- 参数实例：`{"kind": "number"}`
- 预期结果：答卷和回答数0；数字平均值null、分布空。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_0e536aa63935426fbf2978d1d76cf44c

## P2-AUTO-165 · tests/test_phase2_block6.py::test_versions_multi_instances_restore_and_filter

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：同卷放V1两次和V2一次；提交；查询全部及单版本；恢复V1再查询。
- 输入数据：V1答案10、20；V2答案100
- 参数实例：`{}`
- 预期结果：总答卷1；V1回答2均值15；V2回答1均值100；恢复版本单独空组。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_ff28e633c4fb47d1969ce9e04735e352

## P2-AUTO-166 · tests/test_phase2_block6.py::test_cross_permissions_anonymity_revocation

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：共享题目，双方各收答卷；跨问卷查询；撤销共享后重查自己的统计。
- 输入数据：匿名答卷12和99；第三账号
- 参数实例：`{}`
- 预期结果：各只统计自己问卷；无身份字段；撤销不影响已有快照统计。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_9bc40b0778674e81afae1942bda2c348

## P2-AUTO-167 · tests/test_phase2_block7_browser.py::test_library_browser_flow

- 测试类型：自动化浏览器集成测试（真实Edge）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：Edge中创建题库/题目、分支/恢复、分享/撤销；选题加入问卷、换版、发布填写、查使用及统计。
- 输入数据：数字题年龄、答案16，reader共享账号，390px视窗
- 参数实例：`{}`
- 预期结果：页面流程完成；三版本；快照换版成功；统计16；使用清单可见；无JS异常和横向溢出。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_20659d61842c42cc9c6669d49d61498c

## P2-AUTO-168 · tests/test_phase2_boundaries.py::test_import_ownership_and_version_validation

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：他人导入自己的问卷、错误版本族、伪造source、未知实例换版；对比原问卷。
- 输入数据：另一账号和不存在的版本/实例
- 参数实例：`{}`
- 预期结果：404或422；没有部分写入。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_d9b500fe56c64dc880aa536c1812ab3a

## P2-AUTO-169 · tests/test_phase2_boundaries.py::test_tampered_snapshot_statistics_rejected

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：在隔离库中模拟快照被直接数据库工具篡改，再统计。
- 输入数据：已关联版本的标题改变，摘要保持原值
- 参数实例：`{}`
- 预期结果：409停止统计，不把篡改内容混入原版本。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_23970695e4bc42908e0a255c792ce201

## P2-AUTO-170 · tests/test_phase2_boundaries.py::test_family_creation_retry

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：中断初始版本插入；用同一题库和请求键重试两次，再更改内容重试。
- 输入数据：固定request_key，第一次版本写入前失败
- 参数实例：`{}`
- 预期结果：只有一个题目族和一个版本；冲突内容409。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_3dc241a9662a4348a467f9a00c9d57fa

## P2-AUTO-171 · tests/test_registration_integrity.py::test_register_duplicate

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：首次注册，再同名及大小写变体注册；检查用户数。
- 输入数据：same_user、SAME_USER
- 参数实例：`{}`
- 预期结果：201、409、409；只有一条用户；唯一索引存在。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_542312125d8f47c4815e6d5b9096a5fd

## P2-AUTO-172 · tests/test_registration_integrity.py::test_concurrent_duplicate

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：8个请求在密码哈希前汇合，确保均通过预查询后竞争插入。
- 输入数据：8次相同用户名
- 参数实例：`{}`
- 预期结果：只有1个201、7个409；MongoDB只有1条用户。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_73962a8699794f289cf912939d16634f

## P2-AUTO-173 · tests/test_registration_integrity.py::test_existing_duplicates_safe_startup

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：隔离库删除测试索引并植入重复用户；重新启动应用；注册、登录及健康检查。
- 输入数据：两条同名历史记录；一个新用户名
- 参数实例：`{}`
- 预期结果：启动可用；同名409、新账号503、重复登录409；健康降级；所有历史记录保持不变。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_0c3ba76c601c4cc2af4828ff30a73824

## P2-AUTO-174 · tests/test_registration_integrity.py::test_missing_index_rebuilt

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：在隔离库移除索引后注册；重复请求；检查索引。
- 输入数据：空用户集合、缺失索引
- 参数实例：`{}`
- 预期结果：注册前重建唯一索引，201后409。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_32efe6848e204fd088662605efc8e284

## P2-AUTO-175 · tests/test_registration_integrity.py::test_nonunique_index_blocks_without_replacement

- 测试类型：自动化API集成测试（真实MongoDB）
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：隔离库用非唯一同名索引代替唯一索引；尝试注册。
- 输入数据：username_1非唯一
- 参数实例：`{}`
- 预期结果：503；不删除索引、不写用户。
- 实际结果：pytest passed；阶段状态为 setup=passed, call=passed, teardown=passed
- 是否通过：是
- 隔离数据库：survey_system_test_979525c433e24d718c47c166ccaefd5b

