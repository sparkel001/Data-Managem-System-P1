# 自动化测试用例与实际结果

执行时间：2026-10-16T19:30:09.657881+08:00（UTC+08:00）。执行者：Codex代理。

执行命令：

```powershell
.venv/Scripts/python -m pytest -q --junitxml=test-results/coverage-audit/pytest.xml --audit-report=test-results/coverage-audit/cases.json
```

这些全部是自动化测试。每个参数化输入单独编号；测试通过以 setup、call、teardown 全部成功为准，失败/跳过/未执行不会记为通过。

公共输入约定：新增题目默认 title=课程测试题，required=true；选择题选项为 a/A、b/B、c/C。问卷默认 title=课程核对、draft、非匿名、每人一次。新用例的准备动作通过注册/登录/建卷/加题/发布API执行。UUID在运行时生成，参数中的题目位置在步骤中映射为对应UUID；密码与令牌不写入证据。

已有用例未采集原始HTTP响应时，实际结果仅记为pytest断言通过，不编造具体响应值。新增用例另外列出实际采集的状态码、数量或统计值；预期结果同时包含数据库、ID或路径等额外断言。

| 分类 | 结果 |
| --- | --- |
| 已有 | 43通过 / 0失败 / 0跳过 / 0未执行 |
| 新增 | 71通过 / 0失败 / 0跳过 / 0未执行 |

## AUTO-001 tests/test_block1.py::test_health

- 测试编号：AUTO-001
- 测试类型：自动化API集成测试（真实MongoDB）；已有；课程类别：其他。
- 前置条件：本机MongoDB可用；每实例独立UUID测试库。
- 操作步骤：GET /api/health。
- 输入数据：无请求体。
- 预期结果：200，返回的数据库名以 survey_system_test_ 开头。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_3bea988a3b0f4bde9ee6212b5cef6afe`。

对应测试源代码：`tests/test_block1.py::test_health`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-002 tests/test_block2.py::test_auth

- 测试编号：AUTO-002
- 测试类型：自动化API集成测试（真实MongoDB）；已有；课程类别：其他。
- 前置条件：本机MongoDB可用；每实例独立UUID测试库。
- 操作步骤：注册登录、检查身份、错误登录、重复注册、查看密码字段、退出并复查。
- 输入数据：alice/password123；错误密码incorrect。
- 预期结果：认证200；未登录/错误密码/退出后401；重复409；数据库仅存密码哈希。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_cbb8abb44f8345a6aa22f6a7cf44e8a0`。

对应测试源代码：`tests/test_block2.py::test_auth`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-003 tests/test_block2.py::test_ownership

- 测试编号：AUTO-003
- 测试类型：自动化数据库集成测试（直接调用权限函数）；已有；课程类别：其他。
- 前置条件：本机MongoDB可用；每实例独立UUID测试库。
- 操作步骤：在测试库插入所有者a的问卷s；分别使用a/b调用owned。
- 输入数据：survey_id=s，owner_id=a。
- 预期结果：a读取成功；b抛HTTPException且状态404。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_269b4ddb7f154ec5a2818fb448087a22`。

对应测试源代码：`tests/test_block2.py::test_ownership`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-004 tests/test_block3.py::test_management

- 测试编号：AUTO-004
- 测试类型：自动化API集成测试（真实MongoDB）；已有；课程类别：创建问卷。
- 前置条件：本机MongoDB可用；每实例独立UUID测试库。
- 操作步骤：注册两用户；创建、查分享链接、越权查询、编辑、空问卷发布；测试库植入占位题再发布关闭。
- 输入数据：课堂调查→修改标题；用户alice/bobby；占位题q1。
- 预期结果：创建201；分享路径匹配；越权404/空列表；空问卷发布422；发布published；发布后编辑409；关闭closed。此用例使用直接写库占位题，不能单独证明加题API完整。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_9c81354ee90046c8a501afcf2625549a`。

对应测试源代码：`tests/test_block3.py::test_management`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-005 tests/test_block3.py::test_deadline

- 测试编号：AUTO-005
- 测试类型：自动化API集成测试（真实MongoDB）；已有；课程类别：创建问卷。
- 前置条件：本机MongoDB可用；每实例独立UUID测试库。
- 操作步骤：创建无时区时间；创建带时区过去时间；测试库植入占位题并发布。
- 输入数据：2020-01-01T12:00:00与2020-01-01T12:00:00Z。
- 预期结果：无时区创建422；带时区过去时间可存草稿，但发布422。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_89e80dc79f164ee1aa51c928502ed547`。

对应测试源代码：`tests/test_block3.py::test_deadline`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-006 tests/test_block4.py::test_add_edit

- 测试编号：AUTO-006
- 测试类型：自动化API集成测试（真实MongoDB）；已有；课程类别：添加题目。
- 前置条件：本机MongoDB可用；每实例独立UUID测试库。
- 操作步骤：建草稿；添加文本题；改为数字题并比较ID；添加无选项单选。
- 输入数据：姓名/text→年龄/number/integer=true；single无options。
- 预期结果：添加201；编辑保持原题ID；无选项单选422。此用例未独立断言编辑请求状态码。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_b43d0d02149f4b93ab4c95d569e50e6a`。

对应测试源代码：`tests/test_block4.py::test_add_edit`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-007 tests/test_block4.py::test_invalid[q0-None]

- 测试编号：AUTO-007
- 测试类型：自动化单元/文件检查；已有；课程类别：答案校验。
- 前置条件：纯函数/本地文件自动测试；无需MongoDB业务数据。
- 操作步骤：用QuestionInput构造题目；对指定输入调用validate_answer。
- 输入数据：完整题目q与value见各实例参数。
- 预期结果：抛HTTPException。原断言未验证异常状态码或具体消息；新增API测试补充422与零写入断言。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。

本实例精确参数：

```json
{
  "q": {
    "id": "q",
    "title": "问题",
    "type": "text",
    "required": true,
    "options": [],
    "min_choices": 0,
    "max_choices": null,
    "min_length": 0,
    "max_length": 1000,
    "min_value": null,
    "max_value": null,
    "integer": false,
    "rules": []
  },
  "value": null
}
```

对应测试源代码：`tests/test_block4.py::test_invalid`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-008 tests/test_block4.py::test_invalid[q1-a]

- 测试编号：AUTO-008
- 测试类型：自动化单元/文件检查；已有；课程类别：答案校验。
- 前置条件：纯函数/本地文件自动测试；无需MongoDB业务数据。
- 操作步骤：用QuestionInput构造题目；对指定输入调用validate_answer。
- 输入数据：完整题目q与value见各实例参数。
- 预期结果：抛HTTPException。原断言未验证异常状态码或具体消息；新增API测试补充422与零写入断言。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。

本实例精确参数：

```json
{
  "q": {
    "id": "q",
    "title": "问题",
    "type": "text",
    "required": true,
    "options": [],
    "min_choices": 0,
    "max_choices": null,
    "min_length": 2,
    "max_length": 1000,
    "min_value": null,
    "max_value": null,
    "integer": false,
    "rules": []
  },
  "value": "a"
}
```

对应测试源代码：`tests/test_block4.py::test_invalid`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-009 tests/test_block4.py::test_invalid[q2-abc]

- 测试编号：AUTO-009
- 测试类型：自动化单元/文件检查；已有；课程类别：答案校验。
- 前置条件：纯函数/本地文件自动测试；无需MongoDB业务数据。
- 操作步骤：用QuestionInput构造题目；对指定输入调用validate_answer。
- 输入数据：完整题目q与value见各实例参数。
- 预期结果：抛HTTPException。原断言未验证异常状态码或具体消息；新增API测试补充422与零写入断言。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。

本实例精确参数：

```json
{
  "q": {
    "id": "q",
    "title": "问题",
    "type": "text",
    "required": true,
    "options": [],
    "min_choices": 0,
    "max_choices": null,
    "min_length": 0,
    "max_length": 2,
    "min_value": null,
    "max_value": null,
    "integer": false,
    "rules": []
  },
  "value": "abc"
}
```

对应测试源代码：`tests/test_block4.py::test_invalid`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-010 tests/test_block4.py::test_invalid[q3-  ]

- 测试编号：AUTO-010
- 测试类型：自动化单元/文件检查；已有；课程类别：答案校验。
- 前置条件：纯函数/本地文件自动测试；无需MongoDB业务数据。
- 操作步骤：用QuestionInput构造题目；对指定输入调用validate_answer。
- 输入数据：完整题目q与value见各实例参数。
- 预期结果：抛HTTPException。原断言未验证异常状态码或具体消息；新增API测试补充422与零写入断言。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。

本实例精确参数：

```json
{
  "q": {
    "id": "q",
    "title": "问题",
    "type": "text",
    "required": true,
    "options": [],
    "min_choices": 0,
    "max_choices": null,
    "min_length": 0,
    "max_length": 1000,
    "min_value": null,
    "max_value": null,
    "integer": false,
    "rules": []
  },
  "value": "  "
}
```

对应测试源代码：`tests/test_block4.py::test_invalid`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-011 tests/test_block4.py::test_invalid[q4-1.5]

- 测试编号：AUTO-011
- 测试类型：自动化单元/文件检查；已有；课程类别：答案校验。
- 前置条件：纯函数/本地文件自动测试；无需MongoDB业务数据。
- 操作步骤：用QuestionInput构造题目；对指定输入调用validate_answer。
- 输入数据：完整题目q与value见各实例参数。
- 预期结果：抛HTTPException。原断言未验证异常状态码或具体消息；新增API测试补充422与零写入断言。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。

本实例精确参数：

```json
{
  "q": {
    "id": "q",
    "title": "问题",
    "type": "number",
    "required": true,
    "options": [],
    "min_choices": 0,
    "max_choices": null,
    "min_length": 0,
    "max_length": 1000,
    "min_value": null,
    "max_value": null,
    "integer": true,
    "rules": []
  },
  "value": 1.5
}
```

对应测试源代码：`tests/test_block4.py::test_invalid`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-012 tests/test_block4.py::test_invalid[q5--1]

- 测试编号：AUTO-012
- 测试类型：自动化单元/文件检查；已有；课程类别：答案校验。
- 前置条件：纯函数/本地文件自动测试；无需MongoDB业务数据。
- 操作步骤：用QuestionInput构造题目；对指定输入调用validate_answer。
- 输入数据：完整题目q与value见各实例参数。
- 预期结果：抛HTTPException。原断言未验证异常状态码或具体消息；新增API测试补充422与零写入断言。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。

本实例精确参数：

```json
{
  "q": {
    "id": "q",
    "title": "问题",
    "type": "number",
    "required": true,
    "options": [],
    "min_choices": 0,
    "max_choices": null,
    "min_length": 0,
    "max_length": 1000,
    "min_value": 0.0,
    "max_value": null,
    "integer": false,
    "rules": []
  },
  "value": -1
}
```

对应测试源代码：`tests/test_block4.py::test_invalid`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-013 tests/test_block4.py::test_invalid[q6-121]

- 测试编号：AUTO-013
- 测试类型：自动化单元/文件检查；已有；课程类别：答案校验。
- 前置条件：纯函数/本地文件自动测试；无需MongoDB业务数据。
- 操作步骤：用QuestionInput构造题目；对指定输入调用validate_answer。
- 输入数据：完整题目q与value见各实例参数。
- 预期结果：抛HTTPException。原断言未验证异常状态码或具体消息；新增API测试补充422与零写入断言。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。

本实例精确参数：

```json
{
  "q": {
    "id": "q",
    "title": "问题",
    "type": "number",
    "required": true,
    "options": [],
    "min_choices": 0,
    "max_choices": null,
    "min_length": 0,
    "max_length": 1000,
    "min_value": null,
    "max_value": 120.0,
    "integer": false,
    "rules": []
  },
  "value": 121
}
```

对应测试源代码：`tests/test_block4.py::test_invalid`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-014 tests/test_block4.py::test_invalid[q7-True]

- 测试编号：AUTO-014
- 测试类型：自动化单元/文件检查；已有；课程类别：答案校验。
- 前置条件：纯函数/本地文件自动测试；无需MongoDB业务数据。
- 操作步骤：用QuestionInput构造题目；对指定输入调用validate_answer。
- 输入数据：完整题目q与value见各实例参数。
- 预期结果：抛HTTPException。原断言未验证异常状态码或具体消息；新增API测试补充422与零写入断言。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。

本实例精确参数：

```json
{
  "q": {
    "id": "q",
    "title": "问题",
    "type": "number",
    "required": true,
    "options": [],
    "min_choices": 0,
    "max_choices": null,
    "min_length": 0,
    "max_length": 1000,
    "min_value": null,
    "max_value": null,
    "integer": false,
    "rules": []
  },
  "value": true
}
```

对应测试源代码：`tests/test_block4.py::test_invalid`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-015 tests/test_block4.py::test_invalid[q8-12]

- 测试编号：AUTO-015
- 测试类型：自动化单元/文件检查；已有；课程类别：答案校验。
- 前置条件：纯函数/本地文件自动测试；无需MongoDB业务数据。
- 操作步骤：用QuestionInput构造题目；对指定输入调用validate_answer。
- 输入数据：完整题目q与value见各实例参数。
- 预期结果：抛HTTPException。原断言未验证异常状态码或具体消息；新增API测试补充422与零写入断言。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。

本实例精确参数：

```json
{
  "q": {
    "id": "q",
    "title": "问题",
    "type": "number",
    "required": true,
    "options": [],
    "min_choices": 0,
    "max_choices": null,
    "min_length": 0,
    "max_length": 1000,
    "min_value": null,
    "max_value": null,
    "integer": false,
    "rules": []
  },
  "value": "12"
}
```

对应测试源代码：`tests/test_block4.py::test_invalid`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-016 tests/test_block4.py::test_invalid[q9-c]

- 测试编号：AUTO-016
- 测试类型：自动化单元/文件检查；已有；课程类别：答案校验。
- 前置条件：纯函数/本地文件自动测试；无需MongoDB业务数据。
- 操作步骤：用QuestionInput构造题目；对指定输入调用validate_answer。
- 输入数据：完整题目q与value见各实例参数。
- 预期结果：抛HTTPException。原断言未验证异常状态码或具体消息；新增API测试补充422与零写入断言。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。

本实例精确参数：

```json
{
  "q": {
    "id": "q",
    "title": "问题",
    "type": "single",
    "required": true,
    "options": [
      {
        "id": "a",
        "label": "A"
      },
      {
        "id": "b",
        "label": "B"
      }
    ],
    "min_choices": 0,
    "max_choices": null,
    "min_length": 0,
    "max_length": 1000,
    "min_value": null,
    "max_value": null,
    "integer": false,
    "rules": []
  },
  "value": "c"
}
```

对应测试源代码：`tests/test_block4.py::test_invalid`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-017 tests/test_block4.py::test_invalid[q10-value10]

- 测试编号：AUTO-017
- 测试类型：自动化单元/文件检查；已有；课程类别：答案校验。
- 前置条件：纯函数/本地文件自动测试；无需MongoDB业务数据。
- 操作步骤：用QuestionInput构造题目；对指定输入调用validate_answer。
- 输入数据：完整题目q与value见各实例参数。
- 预期结果：抛HTTPException。原断言未验证异常状态码或具体消息；新增API测试补充422与零写入断言。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。

本实例精确参数：

```json
{
  "q": {
    "id": "q",
    "title": "问题",
    "type": "multiple",
    "required": true,
    "options": [
      {
        "id": "a",
        "label": "A"
      },
      {
        "id": "b",
        "label": "B"
      }
    ],
    "min_choices": 2,
    "max_choices": null,
    "min_length": 0,
    "max_length": 1000,
    "min_value": null,
    "max_value": null,
    "integer": false,
    "rules": []
  },
  "value": [
    "a"
  ]
}
```

对应测试源代码：`tests/test_block4.py::test_invalid`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-018 tests/test_block4.py::test_invalid[q11-value11]

- 测试编号：AUTO-018
- 测试类型：自动化单元/文件检查；已有；课程类别：答案校验。
- 前置条件：纯函数/本地文件自动测试；无需MongoDB业务数据。
- 操作步骤：用QuestionInput构造题目；对指定输入调用validate_answer。
- 输入数据：完整题目q与value见各实例参数。
- 预期结果：抛HTTPException。原断言未验证异常状态码或具体消息；新增API测试补充422与零写入断言。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。

本实例精确参数：

```json
{
  "q": {
    "id": "q",
    "title": "问题",
    "type": "multiple",
    "required": true,
    "options": [
      {
        "id": "a",
        "label": "A"
      },
      {
        "id": "b",
        "label": "B"
      }
    ],
    "min_choices": 0,
    "max_choices": null,
    "min_length": 0,
    "max_length": 1000,
    "min_value": null,
    "max_value": null,
    "integer": false,
    "rules": []
  },
  "value": [
    "a",
    "a"
  ]
}
```

对应测试源代码：`tests/test_block4.py::test_invalid`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-019 tests/test_block4.py::test_valid

- 测试编号：AUTO-019
- 测试类型：自动化单元/文件检查；已有；课程类别：答案校验。
- 前置条件：纯函数/本地文件自动测试；无需MongoDB业务数据。
- 操作步骤：分别验证选答空值、数字上边界、中文文本精确长度。
- 输入数据：required=false/null；整数0～120输入120；2字文本输入中文。
- 预期结果：分别返回None、120、中文。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。

对应测试源代码：`tests/test_block4.py::test_valid`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-020 tests/test_block5.py::test_jump[single-eq-a-a]

- 测试编号：AUTO-020
- 测试类型：自动化单元/文件检查；已有；课程类别：跳转逻辑。
- 前置条件：纯函数/本地文件自动测试；无需MongoDB业务数据。
- 操作步骤：构造带规则题与被跳过题；检查规则；完整walk；再加入路径外答案。
- 输入数据：kind/op/value/answer见实例参数；命中目标END；路径外题skip。
- 预期结果：匹配路径仅[q]；包含skip答案时抛HTTPException。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。

本实例精确参数：

```json
{
  "kind": "single",
  "op": "eq",
  "value": "a",
  "answer": "a"
}
```

对应测试源代码：`tests/test_block5.py::test_jump`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-021 tests/test_block5.py::test_jump[multiple-contains_any-value1-answer1]

- 测试编号：AUTO-021
- 测试类型：自动化单元/文件检查；已有；课程类别：跳转逻辑。
- 前置条件：纯函数/本地文件自动测试；无需MongoDB业务数据。
- 操作步骤：构造带规则题与被跳过题；检查规则；完整walk；再加入路径外答案。
- 输入数据：kind/op/value/answer见实例参数；命中目标END；路径外题skip。
- 预期结果：匹配路径仅[q]；包含skip答案时抛HTTPException。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。

本实例精确参数：

```json
{
  "kind": "multiple",
  "op": "contains_any",
  "value": [
    "a"
  ],
  "answer": [
    "a",
    "b"
  ]
}
```

对应测试源代码：`tests/test_block5.py::test_jump`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-022 tests/test_block5.py::test_jump[multiple-contains_all-value2-answer2]

- 测试编号：AUTO-022
- 测试类型：自动化单元/文件检查；已有；课程类别：跳转逻辑。
- 前置条件：纯函数/本地文件自动测试；无需MongoDB业务数据。
- 操作步骤：构造带规则题与被跳过题；检查规则；完整walk；再加入路径外答案。
- 输入数据：kind/op/value/answer见实例参数；命中目标END；路径外题skip。
- 预期结果：匹配路径仅[q]；包含skip答案时抛HTTPException。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。

本实例精确参数：

```json
{
  "kind": "multiple",
  "op": "contains_all",
  "value": [
    "a",
    "b"
  ],
  "answer": [
    "a",
    "b"
  ]
}
```

对应测试源代码：`tests/test_block5.py::test_jump`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-023 tests/test_block5.py::test_jump[number-gte-18-20]

- 测试编号：AUTO-023
- 测试类型：自动化单元/文件检查；已有；课程类别：跳转逻辑。
- 前置条件：纯函数/本地文件自动测试；无需MongoDB业务数据。
- 操作步骤：构造带规则题与被跳过题；检查规则；完整walk；再加入路径外答案。
- 输入数据：kind/op/value/answer见实例参数；命中目标END；路径外题skip。
- 预期结果：匹配路径仅[q]；包含skip答案时抛HTTPException。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。

本实例精确参数：

```json
{
  "kind": "number",
  "op": "gte",
  "value": 18,
  "answer": 20
}
```

对应测试源代码：`tests/test_block5.py::test_jump`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-024 tests/test_block5.py::test_bad_target[q]

- 测试编号：AUTO-024
- 测试类型：自动化单元/文件检查；已有；课程类别：跳转逻辑。
- 前置条件：纯函数/本地文件自动测试；无需MongoDB业务数据。
- 操作步骤：构造数字题q，设置gt 0规则到目标，调用validate_rules。
- 输入数据：target=q或missing。
- 预期结果：自跳/不存在目标均抛HTTPException。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。

本实例精确参数：

```json
{
  "target": "q"
}
```

对应测试源代码：`tests/test_block5.py::test_bad_target`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-025 tests/test_block5.py::test_bad_target[missing]

- 测试编号：AUTO-025
- 测试类型：自动化单元/文件检查；已有；课程类别：跳转逻辑。
- 前置条件：纯函数/本地文件自动测试；无需MongoDB业务数据。
- 操作步骤：构造数字题q，设置gt 0规则到目标，调用validate_rules。
- 输入数据：target=q或missing。
- 预期结果：自跳/不存在目标均抛HTTPException。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。

本实例精确参数：

```json
{
  "target": "missing"
}
```

对应测试源代码：`tests/test_block5.py::test_bad_target`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-026 tests/test_block5.py::test_rule_persistence

- 测试编号：AUTO-026
- 测试类型：自动化API集成测试（真实MongoDB）；已有；课程类别：跳转逻辑。
- 前置条件：本机MongoDB可用；每实例独立UUID测试库。
- 操作步骤：通过API创建问卷、数字题、规则，然后读取MongoDB。
- 输入数据：lt 18→END。
- 预期结果：配置规则200；数据库rules与请求一致。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_60cfaa32f7ed4156a3b213fd3cc88d37`。

对应测试源代码：`tests/test_block5.py::test_rule_persistence`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-027 tests/test_block6.py::test_submit

- 测试编号：AUTO-027
- 测试类型：自动化API集成测试（真实MongoDB）；已有；课程类别：提交问卷。
- 前置条件：本机MongoDB可用；每实例独立UUID测试库。
- 操作步骤：发布匿名数字问卷；检查未登录读取、next、非法提交、合法提交、再次提交；创建者/他人读取答卷。
- 输入数据：必答整数0～120；200→20→21；独立filler用户。
- 预期结果：读取未登录401；next首题；非法422；合法201；重复409；仅一答卷，隐藏respondent、respondent_id、once_key；他人详情404。注意原用例401针对读取，不是提交。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_5315c4899dd942a6b1db3b905d1efa59`。

对应测试源代码：`tests/test_block6.py::test_submit`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-028 tests/test_block6.py::test_repeated[True-201]

- 测试编号：AUTO-028
- 测试类型：自动化API集成测试（真实MongoDB）；已有；课程类别：提交问卷。
- 前置条件：本机MongoDB可用；每实例独立UUID测试库。
- 操作步骤：根据多次配置发布；同用户提交10、20；关闭后提交30。
- 输入数据：multiple和expected见实例参数。
- 预期结果：首次201；第二次按配置201或409；关闭后404。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_6751e5aa04d7463281496078a0cf3f75`。

本实例精确参数：

```json
{
  "multiple": true,
  "expected": 201
}
```

对应测试源代码：`tests/test_block6.py::test_repeated`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-029 tests/test_block6.py::test_repeated[False-409]

- 测试编号：AUTO-029
- 测试类型：自动化API集成测试（真实MongoDB）；已有；课程类别：提交问卷。
- 前置条件：本机MongoDB可用；每实例独立UUID测试库。
- 操作步骤：根据多次配置发布；同用户提交10、20；关闭后提交30。
- 输入数据：multiple和expected见实例参数。
- 预期结果：首次201；第二次按配置201或409；关闭后404。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_9b3fdb172ab8491d8e7b7e30a85da9b0`。

本实例精确参数：

```json
{
  "multiple": false,
  "expected": 409
}
```

对应测试源代码：`tests/test_block6.py::test_repeated`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-030 tests/test_block6.py::test_page

- 测试编号：AUTO-030
- 测试类型：自动化API集成测试（真实MongoDB）；已有；课程类别：其他。
- 前置条件：本机MongoDB可用；每实例独立UUID测试库。
- 操作步骤：请求首页、分享页面和脚本。
- 输入数据：/、/survey/example、/static/app.js。
- 预期结果：均200，仅验证路由可达，不代表人工浏览器验收。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_c325c0f05b1b4c6784a10842c387c2ee`。

对应测试源代码：`tests/test_block6.py::test_page`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-031 tests/test_block7.py::test_statistics

- 测试编号：AUTO-031
- 测试类型：自动化API集成测试（真实MongoDB）；已有；课程类别：统计结果。
- 前置条件：本机MongoDB可用；每实例独立UUID测试库。
- 操作步骤：添加四题并发布；查空统计；提交两份完整答卷；查全卷、数字单题及越权统计。
- 输入数据：single:a/b；multiple:[a,b]/[b]；text:甲/乙；number:10/20；允许多次。
- 预期结果：空总数0且均值null；提交各201；总数2；单选[1,1]、多选[1,2]、文本[甲,乙]、数字均值15；数字单题count2；越权整卷/单题404。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_f52b8a55345a4f6e843c03b9a9629090`。

对应测试源代码：`tests/test_block7.py::test_statistics`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-032 tests/test_block8.py::test_concurrent_submit

- 测试编号：AUTO-032
- 测试类型：自动化API集成测试（真实MongoDB）；已有；课程类别：提交问卷。
- 前置条件：本机MongoDB可用；每实例独立UUID测试库。
- 操作步骤：每人一次问卷；4线程同用户同时提交；查询库数量。
- 输入数据：数字答案30，共4次并发。
- 预期结果：状态码排序[201,409,409,409]；数据库仅1条答卷。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_36dac51d3f2a436bbb3f39abd260d92d`。

对应测试源代码：`tests/test_block8.py::test_concurrent_submit`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-033 tests/test_block8.py::test_expired

- 测试编号：AUTO-033
- 测试类型：自动化API集成测试（真实MongoDB）；已有；课程类别：提交问卷。
- 前置条件：本机MongoDB可用；每实例独立UUID测试库。
- 操作步骤：发布后在测试库设置已过期时间；读取与提交；查询答卷数量。
- 输入数据：deadline=now-1秒；数字10。
- 预期结果：读取/提交410；答卷0。时间状态由测试库直接设置，未等待真实时间。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_2f09cbb9526840e09f14e29140d43489`。

对应测试源代码：`tests/test_block8.py::test_expired`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-034 tests/test_block8.py::test_full_jump_workflow

- 测试编号：AUTO-034
- 测试类型：自动化API集成测试（真实MongoDB）；已有；课程类别：跳转逻辑、提交问卷、统计结果。
- 前置条件：本机MongoDB可用；每实例独立UUID测试库。
- 操作步骤：通过API创建3题；设置首题跳第三题；发布；尝试改规则；逐题next、提交、读库和统计。
- 输入数据：年龄number、职业text、反馈text；年龄lt18跳反馈；答案16/很好。
- 预期结果：发布200；发布后改409；next为第三题；提交201；answers/path不含职业；职业count0、反馈values[很好]。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_67f5736b5be04e1aa10349e81bb37f88`。

对应测试源代码：`tests/test_block8.py::test_full_jump_workflow`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-035 tests/test_block8.py::test_edit_invalidates_rule

- 测试编号：AUTO-035
- 测试类型：自动化API集成测试（真实MongoDB）；已有；课程类别：跳转逻辑。
- 前置条件：本机MongoDB可用；每实例独立UUID测试库。
- 操作步骤：数字题配置gt规则；改题型为文本；重新读取。
- 输入数据：gt10→END；number→text。
- 预期结果：编辑422；题型仍number。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_c6865d5210d24d4290d66ecedf8eef0f`。

对应测试源代码：`tests/test_block8.py::test_edit_invalidates_rule`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-036 tests/test_block8.py::test_schema_rejects[kwargs0]

- 测试编号：AUTO-036
- 测试类型：自动化单元/文件检查；已有；课程类别：添加题目、答案校验。
- 前置条件：纯函数/本地文件自动测试；无需MongoDB业务数据。
- 操作步骤：直接构造QuestionInput，不通过HTTP；以pytest.raises检查。
- 输入数据：非法kwargs见各参数实例。
- 预期结果：抛ValueError：文本上下限、数字上下限、选项ID重复、多选最少超出选项数。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。

本实例精确参数：

```json
{
  "kwargs": {
    "min_length": 3,
    "max_length": 2
  }
}
```

对应测试源代码：`tests/test_block8.py::test_schema_rejects`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-037 tests/test_block8.py::test_schema_rejects[kwargs1]

- 测试编号：AUTO-037
- 测试类型：自动化单元/文件检查；已有；课程类别：添加题目、答案校验。
- 前置条件：纯函数/本地文件自动测试；无需MongoDB业务数据。
- 操作步骤：直接构造QuestionInput，不通过HTTP；以pytest.raises检查。
- 输入数据：非法kwargs见各参数实例。
- 预期结果：抛ValueError：文本上下限、数字上下限、选项ID重复、多选最少超出选项数。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。

本实例精确参数：

```json
{
  "kwargs": {
    "type": "number",
    "min_value": 10,
    "max_value": 1
  }
}
```

对应测试源代码：`tests/test_block8.py::test_schema_rejects`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-038 tests/test_block8.py::test_schema_rejects[kwargs2]

- 测试编号：AUTO-038
- 测试类型：自动化单元/文件检查；已有；课程类别：添加题目、答案校验。
- 前置条件：纯函数/本地文件自动测试；无需MongoDB业务数据。
- 操作步骤：直接构造QuestionInput，不通过HTTP；以pytest.raises检查。
- 输入数据：非法kwargs见各参数实例。
- 预期结果：抛ValueError：文本上下限、数字上下限、选项ID重复、多选最少超出选项数。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。

本实例精确参数：

```json
{
  "kwargs": {
    "type": "single",
    "options": [
      {
        "id": "a",
        "label": "A"
      },
      {
        "id": "a",
        "label": "B"
      }
    ]
  }
}
```

对应测试源代码：`tests/test_block8.py::test_schema_rejects`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-039 tests/test_block8.py::test_schema_rejects[kwargs3]

- 测试编号：AUTO-039
- 测试类型：自动化单元/文件检查；已有；课程类别：添加题目、答案校验。
- 前置条件：纯函数/本地文件自动测试；无需MongoDB业务数据。
- 操作步骤：直接构造QuestionInput，不通过HTTP；以pytest.raises检查。
- 输入数据：非法kwargs见各参数实例。
- 预期结果：抛ValueError：文本上下限、数字上下限、选项ID重复、多选最少超出选项数。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。

本实例精确参数：

```json
{
  "kwargs": {
    "type": "multiple",
    "options": [
      {
        "id": "a",
        "label": "A"
      },
      {
        "id": "b",
        "label": "B"
      }
    ],
    "min_choices": 3
  }
}
```

对应测试源代码：`tests/test_block8.py::test_schema_rejects`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-040 tests/test_block8.py::test_missing_unknown_and_priority

- 测试编号：AUTO-040
- 测试类型：自动化单元/文件检查；已有；课程类别：跳转逻辑、答案校验。
- 前置条件：纯函数/本地文件自动测试；无需MongoDB业务数据。
- 操作步骤：构造两条同时匹配的规则；完整walk；再传未知题或缺失必答。
- 输入数据：number q：gt0→END优先于gt0→later；答案q=1/unknown=1/q=0。
- 预期结果：首匹配路径[q]；未知题与缺少later必答均抛HTTPException。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。

对应测试源代码：`tests/test_block8.py::test_missing_unknown_and_priority`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-041 tests/test_block8.py::test_real_name_details

- 测试编号：AUTO-041
- 测试类型：自动化API集成测试（真实MongoDB）；已有；课程类别：提交问卷。
- 前置条件：本机MongoDB可用；每实例独立UUID测试库。
- 操作步骤：发布实名问卷；filler填写；创建者读详情。
- 输入数据：anonymous=false；数字22。
- 预期结果：详情respondent.username=filler。原用例没有独立断言提交状态。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_0970be33468b4bbb8e54c8d456bbda5c`。

对应测试源代码：`tests/test_block8.py::test_real_name_details`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-042 tests/test_block9.py::test_offline_docs

- 测试编号：AUTO-042
- 测试类型：自动化API集成测试（真实MongoDB）；已有；课程类别：其他。
- 前置条件：本机MongoDB可用；每实例独立UUID测试库。
- 操作步骤：读取/docs、OpenAPI；扫描本地静态文件。
- 输入数据：5个本地资源文件。
- 预期结果：docs200；schema含单题统计路径与QuestionInput；静态文件没有外部http链接。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_7f1b2879e1c147c3a20cfe4661837e6a`。

对应测试源代码：`tests/test_block9.py::test_offline_docs`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-043 tests/test_block9.py::test_documentation_present

- 测试编号：AUTO-043
- 测试类型：自动化单元/文件检查；已有；课程类别：其他。
- 前置条件：纯函数/本地文件自动测试；无需MongoDB业务数据。
- 操作步骤：检查6份文档存在且长度大于100；检查.env.example。
- 输入数据：DATABASE/API/LOGIC/REPORT_TEMPLATE/AI_USAGE_LOG/TEST_RESULTS。
- 预期结果：文档非空且环境示例含MONGODB_URI；仅检查存在性，不证明文档业务覆盖。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。

对应测试源代码：`tests/test_block9.py::test_documentation_present`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-044 tests/test_course_requirements.py::test_create_defaults_persisted

- 测试编号：AUTO-044
- 测试类型：自动化API集成测试（真实MongoDB）；新增；课程类别：创建问卷。
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：登录；POST 创建；查询 MongoDB；GET 详情和列表对照。
- 输入数据：{"title":"  课程问卷  "}，其余设置省略。
- 预期结果：201；稳定 UUID；标题去空白；draft、非匿名、每人一次、无截止、无题目；创建者正确；时间按BSON毫秒精度与落库一致；详情/列表与落库一致。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_60213da8acc94a7aa7e612a8326638f5`。

本次实际采集结果：

```json
[
  {
    "status": 201
  },
  {
    "creation_time": "2026-10-16T11:29:04.800767+00:00",
    "read_time": "2026-10-16T11:29:04.800000+00:00",
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

对应测试源代码：`tests/test_course_requirements.py::test_create_defaults_persisted`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-045 tests/test_course_requirements.py::test_create_rejects_invalid_without_write[missing-title]

- 测试编号：AUTO-045
- 测试类型：自动化API集成测试（真实MongoDB）；新增；课程类别：创建问卷。
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：登录；POST 非法问卷；查询测试库问卷数量。
- 输入数据：payload 参数。
- 预期结果：422；surveys 集合仍为 0 条。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_d6e820536524443eb4f1b1bb0cfc4946`。

本实例精确参数：

```json
{
  "payload": {}
}
```

本次实际采集结果：

```json
[
  {
    "status": 422,
    "surveys": 0
  }
]
```

对应测试源代码：`tests/test_course_requirements.py::test_create_rejects_invalid_without_write`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-046 tests/test_course_requirements.py::test_create_rejects_invalid_without_write[empty-title]

- 测试编号：AUTO-046
- 测试类型：自动化API集成测试（真实MongoDB）；新增；课程类别：创建问卷。
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：登录；POST 非法问卷；查询测试库问卷数量。
- 输入数据：payload 参数。
- 预期结果：422；surveys 集合仍为 0 条。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_d98c0654d43a49ef96d166478ead2678`。

本实例精确参数：

```json
{
  "payload": {
    "title": ""
  }
}
```

本次实际采集结果：

```json
[
  {
    "status": 422,
    "surveys": 0
  }
]
```

对应测试源代码：`tests/test_course_requirements.py::test_create_rejects_invalid_without_write`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-047 tests/test_course_requirements.py::test_create_rejects_invalid_without_write[blank-title]

- 测试编号：AUTO-047
- 测试类型：自动化API集成测试（真实MongoDB）；新增；课程类别：创建问卷。
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：登录；POST 非法问卷；查询测试库问卷数量。
- 输入数据：payload 参数。
- 预期结果：422；surveys 集合仍为 0 条。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_17c88d01ce784c438173d1835cfe9a87`。

本实例精确参数：

```json
{
  "payload": {
    "title": "   "
  }
}
```

本次实际采集结果：

```json
[
  {
    "status": 422,
    "surveys": 0
  }
]
```

对应测试源代码：`tests/test_course_requirements.py::test_create_rejects_invalid_without_write`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-048 tests/test_course_requirements.py::test_create_rejects_invalid_without_write[too-long-title]

- 测试编号：AUTO-048
- 测试类型：自动化API集成测试（真实MongoDB）；新增；课程类别：创建问卷。
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：登录；POST 非法问卷；查询测试库问卷数量。
- 输入数据：payload 参数。
- 预期结果：422；surveys 集合仍为 0 条。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_c15a4843b49e4cacb479ea6f2fca1bb9`。

本实例精确参数：

```json
{
  "payload": {
    "title": "长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长"
  }
}
```

本次实际采集结果：

```json
[
  {
    "status": 422,
    "surveys": 0
  }
]
```

对应测试源代码：`tests/test_course_requirements.py::test_create_rejects_invalid_without_write`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-049 tests/test_course_requirements.py::test_create_requires_login

- 测试编号：AUTO-049
- 测试类型：自动化API集成测试（真实MongoDB）；新增；课程类别：创建问卷。
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：不登录；POST 合法问卷；检查库中数量。
- 输入数据：{"title":"未登录创建"}。
- 预期结果：401；surveys 集合无写入。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_706b0086375e4aa985a6947cfec510e3`。

本次实际采集结果：

```json
[
  {
    "status": 401,
    "surveys": 0
  }
]
```

对应测试源代码：`tests/test_course_requirements.py::test_create_requires_login`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-050 tests/test_course_requirements.py::test_add_each_type_persists_with_stable_ids[single]

- 测试编号：AUTO-050
- 测试类型：自动化API集成测试（真实MongoDB）；新增；课程类别：添加题目。
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：创建草稿；分别 POST 四类题目；再次添加另一题；检查 API 与 MongoDB 中 ID/配置。
- 输入数据：kind 参数；选择题 a/b/c；文本2～4字；数字0～120整数。
- 预期结果：两次添加均201；题型和配置落库一致；两道题 UUID 不同，后续添加不改变已有 ID。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_4a4ca9db73e74b4fa51ee7ddc97a105d`。

本实例精确参数：

```json
{
  "kind": "single"
}
```

本次实际采集结果：

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

对应测试源代码：`tests/test_course_requirements.py::test_add_each_type_persists_with_stable_ids`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-051 tests/test_course_requirements.py::test_add_each_type_persists_with_stable_ids[multiple]

- 测试编号：AUTO-051
- 测试类型：自动化API集成测试（真实MongoDB）；新增；课程类别：添加题目。
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：创建草稿；分别 POST 四类题目；再次添加另一题；检查 API 与 MongoDB 中 ID/配置。
- 输入数据：kind 参数；选择题 a/b/c；文本2～4字；数字0～120整数。
- 预期结果：两次添加均201；题型和配置落库一致；两道题 UUID 不同，后续添加不改变已有 ID。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_414d15c6704843189ac5ddb0204823c6`。

本实例精确参数：

```json
{
  "kind": "multiple"
}
```

本次实际采集结果：

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

对应测试源代码：`tests/test_course_requirements.py::test_add_each_type_persists_with_stable_ids`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-052 tests/test_course_requirements.py::test_add_each_type_persists_with_stable_ids[text]

- 测试编号：AUTO-052
- 测试类型：自动化API集成测试（真实MongoDB）；新增；课程类别：添加题目。
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：创建草稿；分别 POST 四类题目；再次添加另一题；检查 API 与 MongoDB 中 ID/配置。
- 输入数据：kind 参数；选择题 a/b/c；文本2～4字；数字0～120整数。
- 预期结果：两次添加均201；题型和配置落库一致；两道题 UUID 不同，后续添加不改变已有 ID。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_ef5e6685096b477087e99a2b0e654523`。

本实例精确参数：

```json
{
  "kind": "text"
}
```

本次实际采集结果：

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

对应测试源代码：`tests/test_course_requirements.py::test_add_each_type_persists_with_stable_ids`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-053 tests/test_course_requirements.py::test_add_each_type_persists_with_stable_ids[number]

- 测试编号：AUTO-053
- 测试类型：自动化API集成测试（真实MongoDB）；新增；课程类别：添加题目。
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：创建草稿；分别 POST 四类题目；再次添加另一题；检查 API 与 MongoDB 中 ID/配置。
- 输入数据：kind 参数；选择题 a/b/c；文本2～4字；数字0～120整数。
- 预期结果：两次添加均201；题型和配置落库一致；两道题 UUID 不同，后续添加不改变已有 ID。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_5cfa90ef4ab9403380dcf8b7ba8b9c45`。

本实例精确参数：

```json
{
  "kind": "number"
}
```

本次实际采集结果：

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

对应测试源代码：`tests/test_course_requirements.py::test_add_each_type_persists_with_stable_ids`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-054 tests/test_course_requirements.py::test_invalid_question_does_not_mutate_survey[single-no-options]

- 测试编号：AUTO-054
- 测试类型：自动化API集成测试（真实MongoDB）；新增；课程类别：添加题目。
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：创建草稿；保存文档快照；POST 非法题目；重新读取文档比较。
- 输入数据：payload 参数。
- 预期结果：422；整个问卷文档（包括 revision 和 questions）不变。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_41df03cb76b742bf8b2d247128ec54a8`。

本实例精确参数：

```json
{
  "payload": {
    "title": "课程测试题",
    "type": "single",
    "options": []
  }
}
```

本次实际采集结果：

```json
[
  {
    "status": 422,
    "document_unchanged": true
  }
]
```

对应测试源代码：`tests/test_course_requirements.py::test_invalid_question_does_not_mutate_survey`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-055 tests/test_course_requirements.py::test_invalid_question_does_not_mutate_survey[multiple-invalid-limits]

- 测试编号：AUTO-055
- 测试类型：自动化API集成测试（真实MongoDB）；新增；课程类别：添加题目。
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：创建草稿；保存文档快照；POST 非法题目；重新读取文档比较。
- 输入数据：payload 参数。
- 预期结果：422；整个问卷文档（包括 revision 和 questions）不变。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_9beffabf9a8848869b8c680086f8667a`。

本实例精确参数：

```json
{
  "payload": {
    "title": "课程测试题",
    "type": "multiple",
    "options": [
      {
        "id": "a",
        "label": "A"
      },
      {
        "id": "b",
        "label": "B"
      },
      {
        "id": "c",
        "label": "C"
      }
    ],
    "min_choices": 3,
    "max_choices": 2
  }
}
```

本次实际采集结果：

```json
[
  {
    "status": 422,
    "document_unchanged": true
  }
]
```

对应测试源代码：`tests/test_course_requirements.py::test_invalid_question_does_not_mutate_survey`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-056 tests/test_course_requirements.py::test_invalid_question_does_not_mutate_survey[text-invalid-limits]

- 测试编号：AUTO-056
- 测试类型：自动化API集成测试（真实MongoDB）；新增；课程类别：添加题目。
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：创建草稿；保存文档快照；POST 非法题目；重新读取文档比较。
- 输入数据：payload 参数。
- 预期结果：422；整个问卷文档（包括 revision 和 questions）不变。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_00688a6c51d84651ab77f666458f0c5e`。

本实例精确参数：

```json
{
  "payload": {
    "title": "课程测试题",
    "type": "text",
    "min_length": 5,
    "max_length": 2
  }
}
```

本次实际采集结果：

```json
[
  {
    "status": 422,
    "document_unchanged": true
  }
]
```

对应测试源代码：`tests/test_course_requirements.py::test_invalid_question_does_not_mutate_survey`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-057 tests/test_course_requirements.py::test_invalid_question_does_not_mutate_survey[number-invalid-limits]

- 测试编号：AUTO-057
- 测试类型：自动化API集成测试（真实MongoDB）；新增；课程类别：添加题目。
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：创建草稿；保存文档快照；POST 非法题目；重新读取文档比较。
- 输入数据：payload 参数。
- 预期结果：422；整个问卷文档（包括 revision 和 questions）不变。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_d243abb0d4f147728b21a5a192dbbbec`。

本实例精确参数：

```json
{
  "payload": {
    "title": "课程测试题",
    "type": "number",
    "min_value": 10,
    "max_value": 0
  }
}
```

本次实际采集结果：

```json
[
  {
    "status": 422,
    "document_unchanged": true
  }
]
```

对应测试源代码：`tests/test_course_requirements.py::test_invalid_question_does_not_mutate_survey`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-058 tests/test_course_requirements.py::test_add_question_authorization_and_state[anonymous-401]

- 测试编号：AUTO-058
- 测试类型：自动化API集成测试（真实MongoDB）；新增；课程类别：添加题目。
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：准备草稿或已发布问卷；以指定身份 POST 新题；比较前后文档。
- 输入数据：actor 参数：未登录、其他用户、已发布问卷的创建者。
- 预期结果：分别401、404、409；问卷文档不变。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_97d9eadbadf34634ad42e5849ff91120`。

本实例精确参数：

```json
{
  "actor": "anonymous",
  "expected": 401
}
```

本次实际采集结果：

```json
[
  {
    "status": 401,
    "document_unchanged": true
  }
]
```

对应测试源代码：`tests/test_course_requirements.py::test_add_question_authorization_and_state`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-059 tests/test_course_requirements.py::test_add_question_authorization_and_state[other-404]

- 测试编号：AUTO-059
- 测试类型：自动化API集成测试（真实MongoDB）；新增；课程类别：添加题目。
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：准备草稿或已发布问卷；以指定身份 POST 新题；比较前后文档。
- 输入数据：actor 参数：未登录、其他用户、已发布问卷的创建者。
- 预期结果：分别401、404、409；问卷文档不变。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_a9bec7797e8b47c0845c943cfd7443e5`。

本实例精确参数：

```json
{
  "actor": "other",
  "expected": 404
}
```

本次实际采集结果：

```json
[
  {
    "status": 404,
    "document_unchanged": true
  }
]
```

对应测试源代码：`tests/test_course_requirements.py::test_add_question_authorization_and_state`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-060 tests/test_course_requirements.py::test_add_question_authorization_and_state[published_owner-409]

- 测试编号：AUTO-060
- 测试类型：自动化API集成测试（真实MongoDB）；新增；课程类别：添加题目。
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：准备草稿或已发布问卷；以指定身份 POST 新题；比较前后文档。
- 输入数据：actor 参数：未登录、其他用户、已发布问卷的创建者。
- 预期结果：分别401、404、409；问卷文档不变。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_aaa0cb08ffdf42d0ab6d018636fbea22`。

本实例精确参数：

```json
{
  "actor": "published_owner",
  "expected": 409
}
```

本次实际采集结果：

```json
[
  {
    "status": 409,
    "document_unchanged": true
  }
]
```

对应测试源代码：`tests/test_course_requirements.py::test_add_question_authorization_and_state`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-061 tests/test_course_requirements.py::test_numeric_jump_operator_boundaries_api[eq-18-True]

- 测试编号：AUTO-061
- 测试类型：自动化API集成测试（真实MongoDB）；新增；课程类别：跳转逻辑。
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：API 创建数字题和后续文本题；设置数字规则到 END；发布；调用 next。
- 输入数据：比较阈值18，op/answer/matched 参数。
- 预期结果：匹配时 next_question_id=END，否则进入后续文本题；规则从 MongoDB 读取。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_bd995a27cd984127b6843aca0d847e02`。

本实例精确参数：

```json
{
  "op": "eq",
  "answer": 18,
  "matched": true
}
```

本次实际采集结果：

```json
[
  {
    "status": 200,
    "next_is_end": true,
    "matched": true
  }
]
```

对应测试源代码：`tests/test_course_requirements.py::test_numeric_jump_operator_boundaries_api`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-062 tests/test_course_requirements.py::test_numeric_jump_operator_boundaries_api[eq-19-False]

- 测试编号：AUTO-062
- 测试类型：自动化API集成测试（真实MongoDB）；新增；课程类别：跳转逻辑。
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：API 创建数字题和后续文本题；设置数字规则到 END；发布；调用 next。
- 输入数据：比较阈值18，op/answer/matched 参数。
- 预期结果：匹配时 next_question_id=END，否则进入后续文本题；规则从 MongoDB 读取。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_06f08ca6e8ee4b4e97a8be177eae17fd`。

本实例精确参数：

```json
{
  "op": "eq",
  "answer": 19,
  "matched": false
}
```

本次实际采集结果：

```json
[
  {
    "status": 200,
    "next_is_end": false,
    "matched": false
  }
]
```

对应测试源代码：`tests/test_course_requirements.py::test_numeric_jump_operator_boundaries_api`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-063 tests/test_course_requirements.py::test_numeric_jump_operator_boundaries_api[gt-18-False]

- 测试编号：AUTO-063
- 测试类型：自动化API集成测试（真实MongoDB）；新增；课程类别：跳转逻辑。
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：API 创建数字题和后续文本题；设置数字规则到 END；发布；调用 next。
- 输入数据：比较阈值18，op/answer/matched 参数。
- 预期结果：匹配时 next_question_id=END，否则进入后续文本题；规则从 MongoDB 读取。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_0c4cec18fc7e4f3e95a4434c4421c500`。

本实例精确参数：

```json
{
  "op": "gt",
  "answer": 18,
  "matched": false
}
```

本次实际采集结果：

```json
[
  {
    "status": 200,
    "next_is_end": false,
    "matched": false
  }
]
```

对应测试源代码：`tests/test_course_requirements.py::test_numeric_jump_operator_boundaries_api`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-064 tests/test_course_requirements.py::test_numeric_jump_operator_boundaries_api[gt-19-True]

- 测试编号：AUTO-064
- 测试类型：自动化API集成测试（真实MongoDB）；新增；课程类别：跳转逻辑。
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：API 创建数字题和后续文本题；设置数字规则到 END；发布；调用 next。
- 输入数据：比较阈值18，op/answer/matched 参数。
- 预期结果：匹配时 next_question_id=END，否则进入后续文本题；规则从 MongoDB 读取。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_f4ce600469d542a3a81e9c4480fa4afd`。

本实例精确参数：

```json
{
  "op": "gt",
  "answer": 19,
  "matched": true
}
```

本次实际采集结果：

```json
[
  {
    "status": 200,
    "next_is_end": true,
    "matched": true
  }
]
```

对应测试源代码：`tests/test_course_requirements.py::test_numeric_jump_operator_boundaries_api`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-065 tests/test_course_requirements.py::test_numeric_jump_operator_boundaries_api[gte-18-True]

- 测试编号：AUTO-065
- 测试类型：自动化API集成测试（真实MongoDB）；新增；课程类别：跳转逻辑。
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：API 创建数字题和后续文本题；设置数字规则到 END；发布；调用 next。
- 输入数据：比较阈值18，op/answer/matched 参数。
- 预期结果：匹配时 next_question_id=END，否则进入后续文本题；规则从 MongoDB 读取。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_9648652b3c9f42bdb744bd9c62d2f2bc`。

本实例精确参数：

```json
{
  "op": "gte",
  "answer": 18,
  "matched": true
}
```

本次实际采集结果：

```json
[
  {
    "status": 200,
    "next_is_end": true,
    "matched": true
  }
]
```

对应测试源代码：`tests/test_course_requirements.py::test_numeric_jump_operator_boundaries_api`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-066 tests/test_course_requirements.py::test_numeric_jump_operator_boundaries_api[gte-17-False]

- 测试编号：AUTO-066
- 测试类型：自动化API集成测试（真实MongoDB）；新增；课程类别：跳转逻辑。
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：API 创建数字题和后续文本题；设置数字规则到 END；发布；调用 next。
- 输入数据：比较阈值18，op/answer/matched 参数。
- 预期结果：匹配时 next_question_id=END，否则进入后续文本题；规则从 MongoDB 读取。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_12506a9bf8594716b8adb836ddadeb05`。

本实例精确参数：

```json
{
  "op": "gte",
  "answer": 17,
  "matched": false
}
```

本次实际采集结果：

```json
[
  {
    "status": 200,
    "next_is_end": false,
    "matched": false
  }
]
```

对应测试源代码：`tests/test_course_requirements.py::test_numeric_jump_operator_boundaries_api`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-067 tests/test_course_requirements.py::test_numeric_jump_operator_boundaries_api[lt-18-False]

- 测试编号：AUTO-067
- 测试类型：自动化API集成测试（真实MongoDB）；新增；课程类别：跳转逻辑。
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：API 创建数字题和后续文本题；设置数字规则到 END；发布；调用 next。
- 输入数据：比较阈值18，op/answer/matched 参数。
- 预期结果：匹配时 next_question_id=END，否则进入后续文本题；规则从 MongoDB 读取。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_2510e97289624db79863e356fb0f19e2`。

本实例精确参数：

```json
{
  "op": "lt",
  "answer": 18,
  "matched": false
}
```

本次实际采集结果：

```json
[
  {
    "status": 200,
    "next_is_end": false,
    "matched": false
  }
]
```

对应测试源代码：`tests/test_course_requirements.py::test_numeric_jump_operator_boundaries_api`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-068 tests/test_course_requirements.py::test_numeric_jump_operator_boundaries_api[lt-17-True]

- 测试编号：AUTO-068
- 测试类型：自动化API集成测试（真实MongoDB）；新增；课程类别：跳转逻辑。
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：API 创建数字题和后续文本题；设置数字规则到 END；发布；调用 next。
- 输入数据：比较阈值18，op/answer/matched 参数。
- 预期结果：匹配时 next_question_id=END，否则进入后续文本题；规则从 MongoDB 读取。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_35f1a1bad71c474aaabafd578a20dce3`。

本实例精确参数：

```json
{
  "op": "lt",
  "answer": 17,
  "matched": true
}
```

本次实际采集结果：

```json
[
  {
    "status": 200,
    "next_is_end": true,
    "matched": true
  }
]
```

对应测试源代码：`tests/test_course_requirements.py::test_numeric_jump_operator_boundaries_api`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-069 tests/test_course_requirements.py::test_numeric_jump_operator_boundaries_api[lte-18-True]

- 测试编号：AUTO-069
- 测试类型：自动化API集成测试（真实MongoDB）；新增；课程类别：跳转逻辑。
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：API 创建数字题和后续文本题；设置数字规则到 END；发布；调用 next。
- 输入数据：比较阈值18，op/answer/matched 参数。
- 预期结果：匹配时 next_question_id=END，否则进入后续文本题；规则从 MongoDB 读取。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_fd8ed09c44c540799db4e6a4fab8d9ca`。

本实例精确参数：

```json
{
  "op": "lte",
  "answer": 18,
  "matched": true
}
```

本次实际采集结果：

```json
[
  {
    "status": 200,
    "next_is_end": true,
    "matched": true
  }
]
```

对应测试源代码：`tests/test_course_requirements.py::test_numeric_jump_operator_boundaries_api`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-070 tests/test_course_requirements.py::test_numeric_jump_operator_boundaries_api[lte-19-False]

- 测试编号：AUTO-070
- 测试类型：自动化API集成测试（真实MongoDB）；新增；课程类别：跳转逻辑。
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：API 创建数字题和后续文本题；设置数字规则到 END；发布；调用 next。
- 输入数据：比较阈值18，op/answer/matched 参数。
- 预期结果：匹配时 next_question_id=END，否则进入后续文本题；规则从 MongoDB 读取。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_1f61b66806d14fb3ab226950e805aec4`。

本实例精确参数：

```json
{
  "op": "lte",
  "answer": 19,
  "matched": false
}
```

本次实际采集结果：

```json
[
  {
    "status": 200,
    "next_is_end": false,
    "matched": false
  }
]
```

对应测试源代码：`tests/test_course_requirements.py::test_numeric_jump_operator_boundaries_api`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-071 tests/test_course_requirements.py::test_choice_jump_and_fallback_api[single-eq-a-a-True]

- 测试编号：AUTO-071
- 测试类型：自动化API集成测试（真实MongoDB）；新增；课程类别：跳转逻辑。
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：创建选择题+后续文本题；配置跳转规则；发布；使用指定答案调用 next。
- 输入数据：kind、op、condition、answer、matched 参数，选项 a/b/c。
- 预期结果：匹配则 END；不匹配则按顺序进入后续题；contains_all 允许额外选项但必须包含全部条件。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_0ea82665d7264dd0a967afa304a01b1c`。

本实例精确参数：

```json
{
  "kind": "single",
  "op": "eq",
  "condition": "a",
  "answer": "a",
  "matched": true
}
```

本次实际采集结果：

```json
[
  {
    "status": 200,
    "next_is_end": true,
    "matched": true
  }
]
```

对应测试源代码：`tests/test_course_requirements.py::test_choice_jump_and_fallback_api`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-072 tests/test_course_requirements.py::test_choice_jump_and_fallback_api[single-eq-a-b-False]

- 测试编号：AUTO-072
- 测试类型：自动化API集成测试（真实MongoDB）；新增；课程类别：跳转逻辑。
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：创建选择题+后续文本题；配置跳转规则；发布；使用指定答案调用 next。
- 输入数据：kind、op、condition、answer、matched 参数，选项 a/b/c。
- 预期结果：匹配则 END；不匹配则按顺序进入后续题；contains_all 允许额外选项但必须包含全部条件。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_f97018cf453247c68c979053e416d4c6`。

本实例精确参数：

```json
{
  "kind": "single",
  "op": "eq",
  "condition": "a",
  "answer": "b",
  "matched": false
}
```

本次实际采集结果：

```json
[
  {
    "status": 200,
    "next_is_end": false,
    "matched": false
  }
]
```

对应测试源代码：`tests/test_course_requirements.py::test_choice_jump_and_fallback_api`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-073 tests/test_course_requirements.py::test_choice_jump_and_fallback_api[multiple-contains_any-condition2-answer2-True]

- 测试编号：AUTO-073
- 测试类型：自动化API集成测试（真实MongoDB）；新增；课程类别：跳转逻辑。
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：创建选择题+后续文本题；配置跳转规则；发布；使用指定答案调用 next。
- 输入数据：kind、op、condition、answer、matched 参数，选项 a/b/c。
- 预期结果：匹配则 END；不匹配则按顺序进入后续题；contains_all 允许额外选项但必须包含全部条件。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_e8538019b4534e89b0fb8b4833388099`。

本实例精确参数：

```json
{
  "kind": "multiple",
  "op": "contains_any",
  "condition": [
    "a",
    "b"
  ],
  "answer": [
    "b"
  ],
  "matched": true
}
```

本次实际采集结果：

```json
[
  {
    "status": 200,
    "next_is_end": true,
    "matched": true
  }
]
```

对应测试源代码：`tests/test_course_requirements.py::test_choice_jump_and_fallback_api`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-074 tests/test_course_requirements.py::test_choice_jump_and_fallback_api[multiple-contains_any-condition3-answer3-False]

- 测试编号：AUTO-074
- 测试类型：自动化API集成测试（真实MongoDB）；新增；课程类别：跳转逻辑。
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：创建选择题+后续文本题；配置跳转规则；发布；使用指定答案调用 next。
- 输入数据：kind、op、condition、answer、matched 参数，选项 a/b/c。
- 预期结果：匹配则 END；不匹配则按顺序进入后续题；contains_all 允许额外选项但必须包含全部条件。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_fb45cd5fc7984af8821e49eea0be21bb`。

本实例精确参数：

```json
{
  "kind": "multiple",
  "op": "contains_any",
  "condition": [
    "a",
    "b"
  ],
  "answer": [
    "c"
  ],
  "matched": false
}
```

本次实际采集结果：

```json
[
  {
    "status": 200,
    "next_is_end": false,
    "matched": false
  }
]
```

对应测试源代码：`tests/test_course_requirements.py::test_choice_jump_and_fallback_api`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-075 tests/test_course_requirements.py::test_choice_jump_and_fallback_api[multiple-contains_all-condition4-answer4-True]

- 测试编号：AUTO-075
- 测试类型：自动化API集成测试（真实MongoDB）；新增；课程类别：跳转逻辑。
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：创建选择题+后续文本题；配置跳转规则；发布；使用指定答案调用 next。
- 输入数据：kind、op、condition、answer、matched 参数，选项 a/b/c。
- 预期结果：匹配则 END；不匹配则按顺序进入后续题；contains_all 允许额外选项但必须包含全部条件。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_cc6a84866d9b4624a57a06c6f58b2845`。

本实例精确参数：

```json
{
  "kind": "multiple",
  "op": "contains_all",
  "condition": [
    "a",
    "b"
  ],
  "answer": [
    "a",
    "b",
    "c"
  ],
  "matched": true
}
```

本次实际采集结果：

```json
[
  {
    "status": 200,
    "next_is_end": true,
    "matched": true
  }
]
```

对应测试源代码：`tests/test_course_requirements.py::test_choice_jump_and_fallback_api`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-076 tests/test_course_requirements.py::test_choice_jump_and_fallback_api[multiple-contains_all-condition5-answer5-False]

- 测试编号：AUTO-076
- 测试类型：自动化API集成测试（真实MongoDB）；新增；课程类别：跳转逻辑。
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：创建选择题+后续文本题；配置跳转规则；发布；使用指定答案调用 next。
- 输入数据：kind、op、condition、answer、matched 参数，选项 a/b/c。
- 预期结果：匹配则 END；不匹配则按顺序进入后续题；contains_all 允许额外选项但必须包含全部条件。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_daf58f9939af41d680e1845be2fe58e6`。

本实例精确参数：

```json
{
  "kind": "multiple",
  "op": "contains_all",
  "condition": [
    "a",
    "b"
  ],
  "answer": [
    "a"
  ],
  "matched": false
}
```

本次实际采集结果：

```json
[
  {
    "status": 200,
    "next_is_end": false,
    "matched": false
  }
]
```

对应测试源代码：`tests/test_course_requirements.py::test_choice_jump_and_fallback_api`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-077 tests/test_course_requirements.py::test_invalid_jump_api_does_not_mutate[self]

- 测试编号：AUTO-077
- 测试类型：自动化API集成测试（真实MongoDB）；新增；课程类别：跳转逻辑。
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：创建两道数字题草稿；向第二题 PUT 非法规则；比较 MongoDB 文档。
- 输入数据：invalid 参数：自跳、回跳第一题、不存在的目标、数字题使用 contains_any。
- 预期结果：422；规则和 revision 均不变。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_06ed0a5027fd49eea099b58f10d71df2`。

本实例精确参数：

```json
{
  "invalid": "self"
}
```

本次实际采集结果：

```json
[
  {
    "status": 422,
    "document_unchanged": true
  }
]
```

对应测试源代码：`tests/test_course_requirements.py::test_invalid_jump_api_does_not_mutate`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-078 tests/test_course_requirements.py::test_invalid_jump_api_does_not_mutate[backward]

- 测试编号：AUTO-078
- 测试类型：自动化API集成测试（真实MongoDB）；新增；课程类别：跳转逻辑。
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：创建两道数字题草稿；向第二题 PUT 非法规则；比较 MongoDB 文档。
- 输入数据：invalid 参数：自跳、回跳第一题、不存在的目标、数字题使用 contains_any。
- 预期结果：422；规则和 revision 均不变。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_79a8583cbae94dbbb66886eba2f16505`。

本实例精确参数：

```json
{
  "invalid": "backward"
}
```

本次实际采集结果：

```json
[
  {
    "status": 422,
    "document_unchanged": true
  }
]
```

对应测试源代码：`tests/test_course_requirements.py::test_invalid_jump_api_does_not_mutate`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-079 tests/test_course_requirements.py::test_invalid_jump_api_does_not_mutate[missing]

- 测试编号：AUTO-079
- 测试类型：自动化API集成测试（真实MongoDB）；新增；课程类别：跳转逻辑。
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：创建两道数字题草稿；向第二题 PUT 非法规则；比较 MongoDB 文档。
- 输入数据：invalid 参数：自跳、回跳第一题、不存在的目标、数字题使用 contains_any。
- 预期结果：422；规则和 revision 均不变。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_b92697b051764bbb856d405cdc066add`。

本实例精确参数：

```json
{
  "invalid": "missing"
}
```

本次实际采集结果：

```json
[
  {
    "status": 422,
    "document_unchanged": true
  }
]
```

对应测试源代码：`tests/test_course_requirements.py::test_invalid_jump_api_does_not_mutate`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-080 tests/test_course_requirements.py::test_invalid_jump_api_does_not_mutate[wrong-operator]

- 测试编号：AUTO-080
- 测试类型：自动化API集成测试（真实MongoDB）；新增；课程类别：跳转逻辑。
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：创建两道数字题草稿；向第二题 PUT 非法规则；比较 MongoDB 文档。
- 输入数据：invalid 参数：自跳、回跳第一题、不存在的目标、数字题使用 contains_any。
- 预期结果：422；规则和 revision 均不变。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_434b2fb6afa64079b4534cb30b266c38`。

本实例精确参数：

```json
{
  "invalid": "wrong-operator"
}
```

本次实际采集结果：

```json
[
  {
    "status": 422,
    "document_unchanged": true
  }
]
```

对应测试源代码：`tests/test_course_requirements.py::test_invalid_jump_api_does_not_mutate`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-081 tests/test_course_requirements.py::test_required_and_optional_all_types_api[required-single]

- 测试编号：AUTO-081
- 测试类型：自动化API集成测试（真实MongoDB）；新增；课程类别：答案校验。
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：创建并发布指定题型；按 required 配置留空提交；检查 responses。
- 输入数据：kind×required；answers={}。
- 预期结果：必答422且不保存；选答201，answers={}，path 包含该题。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_8a0b53565e5045ef9a57be224ad95053`。

本实例精确参数：

```json
{
  "required": true,
  "kind": "single"
}
```

本次实际采集结果：

```json
[
  {
    "status": 422,
    "saved_count": 0,
    "stored_answers": []
  }
]
```

对应测试源代码：`tests/test_course_requirements.py::test_required_and_optional_all_types_api`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-082 tests/test_course_requirements.py::test_required_and_optional_all_types_api[required-multiple]

- 测试编号：AUTO-082
- 测试类型：自动化API集成测试（真实MongoDB）；新增；课程类别：答案校验。
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：创建并发布指定题型；按 required 配置留空提交；检查 responses。
- 输入数据：kind×required；answers={}。
- 预期结果：必答422且不保存；选答201，answers={}，path 包含该题。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_a2f527b685fb4ee89332f19435595a14`。

本实例精确参数：

```json
{
  "required": true,
  "kind": "multiple"
}
```

本次实际采集结果：

```json
[
  {
    "status": 422,
    "saved_count": 0,
    "stored_answers": []
  }
]
```

对应测试源代码：`tests/test_course_requirements.py::test_required_and_optional_all_types_api`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-083 tests/test_course_requirements.py::test_required_and_optional_all_types_api[required-text]

- 测试编号：AUTO-083
- 测试类型：自动化API集成测试（真实MongoDB）；新增；课程类别：答案校验。
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：创建并发布指定题型；按 required 配置留空提交；检查 responses。
- 输入数据：kind×required；answers={}。
- 预期结果：必答422且不保存；选答201，answers={}，path 包含该题。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_e0c252045b5b4f7faeb9bde910bc0c26`。

本实例精确参数：

```json
{
  "required": true,
  "kind": "text"
}
```

本次实际采集结果：

```json
[
  {
    "status": 422,
    "saved_count": 0,
    "stored_answers": []
  }
]
```

对应测试源代码：`tests/test_course_requirements.py::test_required_and_optional_all_types_api`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-084 tests/test_course_requirements.py::test_required_and_optional_all_types_api[required-number]

- 测试编号：AUTO-084
- 测试类型：自动化API集成测试（真实MongoDB）；新增；课程类别：答案校验。
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：创建并发布指定题型；按 required 配置留空提交；检查 responses。
- 输入数据：kind×required；answers={}。
- 预期结果：必答422且不保存；选答201，answers={}，path 包含该题。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_a0959d406dd54be5909bc01c2e95a47b`。

本实例精确参数：

```json
{
  "required": true,
  "kind": "number"
}
```

本次实际采集结果：

```json
[
  {
    "status": 422,
    "saved_count": 0,
    "stored_answers": []
  }
]
```

对应测试源代码：`tests/test_course_requirements.py::test_required_and_optional_all_types_api`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-085 tests/test_course_requirements.py::test_required_and_optional_all_types_api[optional-single]

- 测试编号：AUTO-085
- 测试类型：自动化API集成测试（真实MongoDB）；新增；课程类别：答案校验。
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：创建并发布指定题型；按 required 配置留空提交；检查 responses。
- 输入数据：kind×required；answers={}。
- 预期结果：必答422且不保存；选答201，answers={}，path 包含该题。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_6509bc326b1e4eb39a47f401dfcafb03`。

本实例精确参数：

```json
{
  "required": false,
  "kind": "single"
}
```

本次实际采集结果：

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

对应测试源代码：`tests/test_course_requirements.py::test_required_and_optional_all_types_api`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-086 tests/test_course_requirements.py::test_required_and_optional_all_types_api[optional-multiple]

- 测试编号：AUTO-086
- 测试类型：自动化API集成测试（真实MongoDB）；新增；课程类别：答案校验。
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：创建并发布指定题型；按 required 配置留空提交；检查 responses。
- 输入数据：kind×required；answers={}。
- 预期结果：必答422且不保存；选答201，answers={}，path 包含该题。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_0c0b91e17c7d434fbfda21aa1d034d1d`。

本实例精确参数：

```json
{
  "required": false,
  "kind": "multiple"
}
```

本次实际采集结果：

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

对应测试源代码：`tests/test_course_requirements.py::test_required_and_optional_all_types_api`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-087 tests/test_course_requirements.py::test_required_and_optional_all_types_api[optional-text]

- 测试编号：AUTO-087
- 测试类型：自动化API集成测试（真实MongoDB）；新增；课程类别：答案校验。
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：创建并发布指定题型；按 required 配置留空提交；检查 responses。
- 输入数据：kind×required；answers={}。
- 预期结果：必答422且不保存；选答201，answers={}，path 包含该题。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_98118acea3ba44d5ac6db171272a22f4`。

本实例精确参数：

```json
{
  "required": false,
  "kind": "text"
}
```

本次实际采集结果：

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

对应测试源代码：`tests/test_course_requirements.py::test_required_and_optional_all_types_api`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-088 tests/test_course_requirements.py::test_required_and_optional_all_types_api[optional-number]

- 测试编号：AUTO-088
- 测试类型：自动化API集成测试（真实MongoDB）；新增；课程类别：答案校验。
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：创建并发布指定题型；按 required 配置留空提交；检查 responses。
- 输入数据：kind×required；answers={}。
- 预期结果：必答422且不保存；选答201，answers={}，path 包含该题。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_3aea65b773f24e668bab86b51679c8b8`。

本实例精确参数：

```json
{
  "required": false,
  "kind": "number"
}
```

本次实际采集结果：

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

对应测试源代码：`tests/test_course_requirements.py::test_required_and_optional_all_types_api`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-089 tests/test_course_requirements.py::test_answer_validation_submission_boundaries[multi-below]

- 测试编号：AUTO-089
- 测试类型：自动化API集成测试（真实MongoDB）；新增；课程类别：答案校验。
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：按配置创建发布单题问卷；提交参数答案；同时核对 HTTP 与 MongoDB。
- 输入数据：kind、constraints、answer、expected 参数；选项 a/b/c。
- 预期结果：合法边界201且原值保存；非法422且零答卷。多选精确2项、文本2～4字符、数字0～120整数。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_02dd91f4ffb84d22aefde910d89fd501`。

本实例精确参数：

```json
{
  "kind": "multiple",
  "constraints": {
    "min_choices": 2,
    "max_choices": 2
  },
  "answer": [
    "a"
  ],
  "expected": 422
}
```

本次实际采集结果：

```json
[
  {
    "status": 422,
    "saved_count": 0,
    "stored_values": []
  }
]
```

对应测试源代码：`tests/test_course_requirements.py::test_answer_validation_submission_boundaries`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-090 tests/test_course_requirements.py::test_answer_validation_submission_boundaries[multi-exact]

- 测试编号：AUTO-090
- 测试类型：自动化API集成测试（真实MongoDB）；新增；课程类别：答案校验。
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：按配置创建发布单题问卷；提交参数答案；同时核对 HTTP 与 MongoDB。
- 输入数据：kind、constraints、answer、expected 参数；选项 a/b/c。
- 预期结果：合法边界201且原值保存；非法422且零答卷。多选精确2项、文本2～4字符、数字0～120整数。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_4acf66ac556049ef9cc20d77f28fd654`。

本实例精确参数：

```json
{
  "kind": "multiple",
  "constraints": {
    "min_choices": 2,
    "max_choices": 2
  },
  "answer": [
    "a",
    "b"
  ],
  "expected": 201
}
```

本次实际采集结果：

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

对应测试源代码：`tests/test_course_requirements.py::test_answer_validation_submission_boundaries`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-091 tests/test_course_requirements.py::test_answer_validation_submission_boundaries[multi-above]

- 测试编号：AUTO-091
- 测试类型：自动化API集成测试（真实MongoDB）；新增；课程类别：答案校验。
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：按配置创建发布单题问卷；提交参数答案；同时核对 HTTP 与 MongoDB。
- 输入数据：kind、constraints、answer、expected 参数；选项 a/b/c。
- 预期结果：合法边界201且原值保存；非法422且零答卷。多选精确2项、文本2～4字符、数字0～120整数。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_e46d5c5267f84fc7b7cc407c28597792`。

本实例精确参数：

```json
{
  "kind": "multiple",
  "constraints": {
    "min_choices": 2,
    "max_choices": 2
  },
  "answer": [
    "a",
    "b",
    "c"
  ],
  "expected": 422
}
```

本次实际采集结果：

```json
[
  {
    "status": 422,
    "saved_count": 0,
    "stored_values": []
  }
]
```

对应测试源代码：`tests/test_course_requirements.py::test_answer_validation_submission_boundaries`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-092 tests/test_course_requirements.py::test_answer_validation_submission_boundaries[multi-duplicate]

- 测试编号：AUTO-092
- 测试类型：自动化API集成测试（真实MongoDB）；新增；课程类别：答案校验。
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：按配置创建发布单题问卷；提交参数答案；同时核对 HTTP 与 MongoDB。
- 输入数据：kind、constraints、answer、expected 参数；选项 a/b/c。
- 预期结果：合法边界201且原值保存；非法422且零答卷。多选精确2项、文本2～4字符、数字0～120整数。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_d8c3097bc797451fa888d3535a73409b`。

本实例精确参数：

```json
{
  "kind": "multiple",
  "constraints": {},
  "answer": [
    "a",
    "a"
  ],
  "expected": 422
}
```

本次实际采集结果：

```json
[
  {
    "status": 422,
    "saved_count": 0,
    "stored_values": []
  }
]
```

对应测试源代码：`tests/test_course_requirements.py::test_answer_validation_submission_boundaries`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-093 tests/test_course_requirements.py::test_answer_validation_submission_boundaries[multi-unknown]

- 测试编号：AUTO-093
- 测试类型：自动化API集成测试（真实MongoDB）；新增；课程类别：答案校验。
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：按配置创建发布单题问卷；提交参数答案；同时核对 HTTP 与 MongoDB。
- 输入数据：kind、constraints、answer、expected 参数；选项 a/b/c。
- 预期结果：合法边界201且原值保存；非法422且零答卷。多选精确2项、文本2～4字符、数字0～120整数。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_7e746a0447694e889851f268321cc372`。

本实例精确参数：

```json
{
  "kind": "multiple",
  "constraints": {},
  "answer": [
    "a",
    "missing"
  ],
  "expected": 422
}
```

本次实际采集结果：

```json
[
  {
    "status": 422,
    "saved_count": 0,
    "stored_values": []
  }
]
```

对应测试源代码：`tests/test_course_requirements.py::test_answer_validation_submission_boundaries`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-094 tests/test_course_requirements.py::test_answer_validation_submission_boundaries[single-valid]

- 测试编号：AUTO-094
- 测试类型：自动化API集成测试（真实MongoDB）；新增；课程类别：答案校验。
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：按配置创建发布单题问卷；提交参数答案；同时核对 HTTP 与 MongoDB。
- 输入数据：kind、constraints、answer、expected 参数；选项 a/b/c。
- 预期结果：合法边界201且原值保存；非法422且零答卷。多选精确2项、文本2～4字符、数字0～120整数。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_08cc34b98fa44be18dd41c845d813d87`。

本实例精确参数：

```json
{
  "kind": "single",
  "constraints": {},
  "answer": "a",
  "expected": 201
}
```

本次实际采集结果：

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

对应测试源代码：`tests/test_course_requirements.py::test_answer_validation_submission_boundaries`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-095 tests/test_course_requirements.py::test_answer_validation_submission_boundaries[single-unknown]

- 测试编号：AUTO-095
- 测试类型：自动化API集成测试（真实MongoDB）；新增；课程类别：答案校验。
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：按配置创建发布单题问卷；提交参数答案；同时核对 HTTP 与 MongoDB。
- 输入数据：kind、constraints、answer、expected 参数；选项 a/b/c。
- 预期结果：合法边界201且原值保存；非法422且零答卷。多选精确2项、文本2～4字符、数字0～120整数。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_cfcb92546a9e43dabb4a5c4ed93f2fdb`。

本实例精确参数：

```json
{
  "kind": "single",
  "constraints": {},
  "answer": "missing",
  "expected": 422
}
```

本次实际采集结果：

```json
[
  {
    "status": 422,
    "saved_count": 0,
    "stored_values": []
  }
]
```

对应测试源代码：`tests/test_course_requirements.py::test_answer_validation_submission_boundaries`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-096 tests/test_course_requirements.py::test_answer_validation_submission_boundaries[text-below]

- 测试编号：AUTO-096
- 测试类型：自动化API集成测试（真实MongoDB）；新增；课程类别：答案校验。
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：按配置创建发布单题问卷；提交参数答案；同时核对 HTTP 与 MongoDB。
- 输入数据：kind、constraints、answer、expected 参数；选项 a/b/c。
- 预期结果：合法边界201且原值保存；非法422且零答卷。多选精确2项、文本2～4字符、数字0～120整数。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_5fa4eb04956644a58df7de5dbb08907a`。

本实例精确参数：

```json
{
  "kind": "text",
  "constraints": {
    "min_length": 2,
    "max_length": 4
  },
  "answer": "中",
  "expected": 422
}
```

本次实际采集结果：

```json
[
  {
    "status": 422,
    "saved_count": 0,
    "stored_values": []
  }
]
```

对应测试源代码：`tests/test_course_requirements.py::test_answer_validation_submission_boundaries`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-097 tests/test_course_requirements.py::test_answer_validation_submission_boundaries[text-min]

- 测试编号：AUTO-097
- 测试类型：自动化API集成测试（真实MongoDB）；新增；课程类别：答案校验。
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：按配置创建发布单题问卷；提交参数答案；同时核对 HTTP 与 MongoDB。
- 输入数据：kind、constraints、answer、expected 参数；选项 a/b/c。
- 预期结果：合法边界201且原值保存；非法422且零答卷。多选精确2项、文本2～4字符、数字0～120整数。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_7e6aa490f41c4ed383ad025bd31310e1`。

本实例精确参数：

```json
{
  "kind": "text",
  "constraints": {
    "min_length": 2,
    "max_length": 4
  },
  "answer": "中文",
  "expected": 201
}
```

本次实际采集结果：

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

对应测试源代码：`tests/test_course_requirements.py::test_answer_validation_submission_boundaries`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-098 tests/test_course_requirements.py::test_answer_validation_submission_boundaries[text-max]

- 测试编号：AUTO-098
- 测试类型：自动化API集成测试（真实MongoDB）；新增；课程类别：答案校验。
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：按配置创建发布单题问卷；提交参数答案；同时核对 HTTP 与 MongoDB。
- 输入数据：kind、constraints、answer、expected 参数；选项 a/b/c。
- 预期结果：合法边界201且原值保存；非法422且零答卷。多选精确2项、文本2～4字符、数字0～120整数。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_fa5d4d775852473893745ee45d4b3469`。

本实例精确参数：

```json
{
  "kind": "text",
  "constraints": {
    "min_length": 2,
    "max_length": 4
  },
  "answer": "中文反馈",
  "expected": 201
}
```

本次实际采集结果：

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

对应测试源代码：`tests/test_course_requirements.py::test_answer_validation_submission_boundaries`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-099 tests/test_course_requirements.py::test_answer_validation_submission_boundaries[text-above]

- 测试编号：AUTO-099
- 测试类型：自动化API集成测试（真实MongoDB）；新增；课程类别：答案校验。
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：按配置创建发布单题问卷；提交参数答案；同时核对 HTTP 与 MongoDB。
- 输入数据：kind、constraints、answer、expected 参数；选项 a/b/c。
- 预期结果：合法边界201且原值保存；非法422且零答卷。多选精确2项、文本2～4字符、数字0～120整数。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_9d7a29a23e944b3c915715349277821d`。

本实例精确参数：

```json
{
  "kind": "text",
  "constraints": {
    "min_length": 2,
    "max_length": 4
  },
  "answer": "中文反馈好",
  "expected": 422
}
```

本次实际采集结果：

```json
[
  {
    "status": 422,
    "saved_count": 0,
    "stored_values": []
  }
]
```

对应测试源代码：`tests/test_course_requirements.py::test_answer_validation_submission_boundaries`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-100 tests/test_course_requirements.py::test_answer_validation_submission_boundaries[number-below]

- 测试编号：AUTO-100
- 测试类型：自动化API集成测试（真实MongoDB）；新增；课程类别：答案校验。
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：按配置创建发布单题问卷；提交参数答案；同时核对 HTTP 与 MongoDB。
- 输入数据：kind、constraints、answer、expected 参数；选项 a/b/c。
- 预期结果：合法边界201且原值保存；非法422且零答卷。多选精确2项、文本2～4字符、数字0～120整数。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_6f4729ec735a4e34b654b2b58127cff0`。

本实例精确参数：

```json
{
  "kind": "number",
  "constraints": {
    "min_value": 0,
    "max_value": 120,
    "integer": true
  },
  "answer": -1,
  "expected": 422
}
```

本次实际采集结果：

```json
[
  {
    "status": 422,
    "saved_count": 0,
    "stored_values": []
  }
]
```

对应测试源代码：`tests/test_course_requirements.py::test_answer_validation_submission_boundaries`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-101 tests/test_course_requirements.py::test_answer_validation_submission_boundaries[number-min]

- 测试编号：AUTO-101
- 测试类型：自动化API集成测试（真实MongoDB）；新增；课程类别：答案校验。
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：按配置创建发布单题问卷；提交参数答案；同时核对 HTTP 与 MongoDB。
- 输入数据：kind、constraints、answer、expected 参数；选项 a/b/c。
- 预期结果：合法边界201且原值保存；非法422且零答卷。多选精确2项、文本2～4字符、数字0～120整数。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_ac3ea6f841b2400c85095d9ffb152c2b`。

本实例精确参数：

```json
{
  "kind": "number",
  "constraints": {
    "min_value": 0,
    "max_value": 120,
    "integer": true
  },
  "answer": 0,
  "expected": 201
}
```

本次实际采集结果：

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

对应测试源代码：`tests/test_course_requirements.py::test_answer_validation_submission_boundaries`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-102 tests/test_course_requirements.py::test_answer_validation_submission_boundaries[number-max]

- 测试编号：AUTO-102
- 测试类型：自动化API集成测试（真实MongoDB）；新增；课程类别：答案校验。
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：按配置创建发布单题问卷；提交参数答案；同时核对 HTTP 与 MongoDB。
- 输入数据：kind、constraints、answer、expected 参数；选项 a/b/c。
- 预期结果：合法边界201且原值保存；非法422且零答卷。多选精确2项、文本2～4字符、数字0～120整数。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_9bb34eadf13e4b2c860f80d692a48843`。

本实例精确参数：

```json
{
  "kind": "number",
  "constraints": {
    "min_value": 0,
    "max_value": 120,
    "integer": true
  },
  "answer": 120,
  "expected": 201
}
```

本次实际采集结果：

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

对应测试源代码：`tests/test_course_requirements.py::test_answer_validation_submission_boundaries`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-103 tests/test_course_requirements.py::test_answer_validation_submission_boundaries[number-above]

- 测试编号：AUTO-103
- 测试类型：自动化API集成测试（真实MongoDB）；新增；课程类别：答案校验。
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：按配置创建发布单题问卷；提交参数答案；同时核对 HTTP 与 MongoDB。
- 输入数据：kind、constraints、answer、expected 参数；选项 a/b/c。
- 预期结果：合法边界201且原值保存；非法422且零答卷。多选精确2项、文本2～4字符、数字0～120整数。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_2133540d6607499bbcb86df4c06f4c1b`。

本实例精确参数：

```json
{
  "kind": "number",
  "constraints": {
    "min_value": 0,
    "max_value": 120,
    "integer": true
  },
  "answer": 121,
  "expected": 422
}
```

本次实际采集结果：

```json
[
  {
    "status": 422,
    "saved_count": 0,
    "stored_values": []
  }
]
```

对应测试源代码：`tests/test_course_requirements.py::test_answer_validation_submission_boundaries`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-104 tests/test_course_requirements.py::test_answer_validation_submission_boundaries[integer-fraction]

- 测试编号：AUTO-104
- 测试类型：自动化API集成测试（真实MongoDB）；新增；课程类别：答案校验。
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：按配置创建发布单题问卷；提交参数答案；同时核对 HTTP 与 MongoDB。
- 输入数据：kind、constraints、answer、expected 参数；选项 a/b/c。
- 预期结果：合法边界201且原值保存；非法422且零答卷。多选精确2项、文本2～4字符、数字0～120整数。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_88202af8c1164153bacc4c40927f003a`。

本实例精确参数：

```json
{
  "kind": "number",
  "constraints": {
    "integer": true
  },
  "answer": 1.5,
  "expected": 422
}
```

本次实际采集结果：

```json
[
  {
    "status": 422,
    "saved_count": 0,
    "stored_values": []
  }
]
```

对应测试源代码：`tests/test_course_requirements.py::test_answer_validation_submission_boundaries`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-105 tests/test_course_requirements.py::test_answer_validation_submission_boundaries[decimal-valid]

- 测试编号：AUTO-105
- 测试类型：自动化API集成测试（真实MongoDB）；新增；课程类别：答案校验。
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：按配置创建发布单题问卷；提交参数答案；同时核对 HTTP 与 MongoDB。
- 输入数据：kind、constraints、answer、expected 参数；选项 a/b/c。
- 预期结果：合法边界201且原值保存；非法422且零答卷。多选精确2项、文本2～4字符、数字0～120整数。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_f3a70d93b8674e94b81287fda66de065`。

本实例精确参数：

```json
{
  "kind": "number",
  "constraints": {
    "integer": false
  },
  "answer": 1.5,
  "expected": 201
}
```

本次实际采集结果：

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

对应测试源代码：`tests/test_course_requirements.py::test_answer_validation_submission_boundaries`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-106 tests/test_course_requirements.py::test_answer_validation_submission_boundaries[number-bool]

- 测试编号：AUTO-106
- 测试类型：自动化API集成测试（真实MongoDB）；新增；课程类别：答案校验。
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：按配置创建发布单题问卷；提交参数答案；同时核对 HTTP 与 MongoDB。
- 输入数据：kind、constraints、answer、expected 参数；选项 a/b/c。
- 预期结果：合法边界201且原值保存；非法422且零答卷。多选精确2项、文本2～4字符、数字0～120整数。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_bdc7d8e315b3490b9e73175a478eec90`。

本实例精确参数：

```json
{
  "kind": "number",
  "constraints": {},
  "answer": true,
  "expected": 422
}
```

本次实际采集结果：

```json
[
  {
    "status": 422,
    "saved_count": 0,
    "stored_values": []
  }
]
```

对应测试源代码：`tests/test_course_requirements.py::test_answer_validation_submission_boundaries`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-107 tests/test_course_requirements.py::test_answer_validation_submission_boundaries[number-string]

- 测试编号：AUTO-107
- 测试类型：自动化API集成测试（真实MongoDB）；新增；课程类别：答案校验。
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：按配置创建发布单题问卷；提交参数答案；同时核对 HTTP 与 MongoDB。
- 输入数据：kind、constraints、answer、expected 参数；选项 a/b/c。
- 预期结果：合法边界201且原值保存；非法422且零答卷。多选精确2项、文本2～4字符、数字0～120整数。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_9f48bdf64a25453594de3ea3ebc94759`。

本实例精确参数：

```json
{
  "kind": "number",
  "constraints": {},
  "answer": "12",
  "expected": 422
}
```

本次实际采集结果：

```json
[
  {
    "status": 422,
    "saved_count": 0,
    "stored_values": []
  }
]
```

对应测试源代码：`tests/test_course_requirements.py::test_answer_validation_submission_boundaries`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-108 tests/test_course_requirements.py::test_submit_rejects_invalid_context_without_save[unauthenticated-401]

- 测试编号：AUTO-108
- 测试类型：自动化API集成测试（真实MongoDB）；新增；课程类别：提交问卷。
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：准备问卷；按 failure 场景调用 submit；检查零答卷。
- 输入数据：未登录、草稿、包含未知题目、包含被跳过题目的额外答案。
- 预期结果：分别401、404、422、422；responses 不新增记录。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_05ea7198cd8f4ebda548eb324b7e7aef`。

本实例精确参数：

```json
{
  "failure": "unauthenticated",
  "expected": 401
}
```

本次实际采集结果：

```json
[
  {
    "status": 401,
    "responses": 0
  }
]
```

对应测试源代码：`tests/test_course_requirements.py::test_submit_rejects_invalid_context_without_save`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-109 tests/test_course_requirements.py::test_submit_rejects_invalid_context_without_save[draft-404]

- 测试编号：AUTO-109
- 测试类型：自动化API集成测试（真实MongoDB）；新增；课程类别：提交问卷。
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：准备问卷；按 failure 场景调用 submit；检查零答卷。
- 输入数据：未登录、草稿、包含未知题目、包含被跳过题目的额外答案。
- 预期结果：分别401、404、422、422；responses 不新增记录。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_8a2e5b1d1017457993790088e28b1e75`。

本实例精确参数：

```json
{
  "failure": "draft",
  "expected": 404
}
```

本次实际采集结果：

```json
[
  {
    "status": 404,
    "responses": 0
  }
]
```

对应测试源代码：`tests/test_course_requirements.py::test_submit_rejects_invalid_context_without_save`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-110 tests/test_course_requirements.py::test_submit_rejects_invalid_context_without_save[unknown-answer-422]

- 测试编号：AUTO-110
- 测试类型：自动化API集成测试（真实MongoDB）；新增；课程类别：提交问卷。
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：准备问卷；按 failure 场景调用 submit；检查零答卷。
- 输入数据：未登录、草稿、包含未知题目、包含被跳过题目的额外答案。
- 预期结果：分别401、404、422、422；responses 不新增记录。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_27cffe9fc47c45e5a60117e6ad282f81`。

本实例精确参数：

```json
{
  "failure": "unknown-answer",
  "expected": 422
}
```

本次实际采集结果：

```json
[
  {
    "status": 422,
    "responses": 0
  }
]
```

对应测试源代码：`tests/test_course_requirements.py::test_submit_rejects_invalid_context_without_save`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-111 tests/test_course_requirements.py::test_submit_rejects_invalid_context_without_save[skipped-answer-422]

- 测试编号：AUTO-111
- 测试类型：自动化API集成测试（真实MongoDB）；新增；课程类别：提交问卷。
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：准备问卷；按 failure 场景调用 submit；检查零答卷。
- 输入数据：未登录、草稿、包含未知题目、包含被跳过题目的额外答案。
- 预期结果：分别401、404、422、422；responses 不新增记录。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_d48af350b0d04162a79c066b3daf83bc`。

本实例精确参数：

```json
{
  "failure": "skipped-answer",
  "expected": 422
}
```

本次实际采集结果：

```json
[
  {
    "status": 422,
    "responses": 0
  }
]
```

对应测试源代码：`tests/test_course_requirements.py::test_submit_rejects_invalid_context_without_save`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-112 tests/test_course_requirements.py::test_distinct_users_can_each_submit_and_persist

- 测试编号：AUTO-112
- 测试类型：自动化API集成测试（真实MongoDB）；新增；课程类别：提交问卷。
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：创建每人一次问卷；两位不同用户分别提交；读取数据库。
- 输入数据：第一用户数字10，第二用户数字30。
- 预期结果：两次201，答卷ID不同，survey_id一致、respondent_id不同，各自答案与路径保存准确。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_d7cc32f8372944f4b07c3ff78a6be7e4`。

本次实际采集结果：

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

对应测试源代码：`tests/test_course_requirements.py::test_distinct_users_can_each_submit_and_persist`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-113 tests/test_course_requirements.py::test_all_question_stats_zero_optional_and_refresh

- 测试编号：AUTO-113
- 测试类型：自动化API集成测试（真实MongoDB）；新增；课程类别：统计结果。
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：创建四类选答题并发布，允许多次；先读空统计；提交完整答卷和全空答卷；逐题与整卷比较；再提交并检查统计更新。
- 输入数据：完整答案 single=a、multiple=[a,b]、text=反馈、number=10；第二份为空；第三份数字30。
- 预期结果：总答卷数0→2→3；四类单题结果与整卷一致；未选c=0；空答案不计有效回答；数字均值10→20。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_ea00d298880141e2ba60132063027484`。

本次实际采集结果：

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
      "survey_id": "2b6a16c5-6b5d-4896-a96a-5bde777db4a9",
      "total_responses": 3,
      "question_id": "b6c13bb7-314a-4b50-9759-8f56fc3535af",
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

对应测试源代码：`tests/test_course_requirements.py::test_all_question_stats_zero_optional_and_refresh`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## AUTO-114 tests/test_course_requirements.py::test_stats_isolate_surveys_and_reject_foreign_questions

- 测试编号：AUTO-114
- 测试类型：自动化API集成测试（真实MongoDB）；新增；课程类别：统计结果。
- 前置条件：本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。
- 操作步骤：同一创建者建立两份问卷并各提交；查询整卷、其他问卷题ID、不存在题ID。
- 输入数据：问卷A答案10，问卷B答案1000。
- 预期结果：各自总数1、均值10和1000；A的单题接口使用B的题ID或未知ID返回404。
- 实际结果：pytest 通过；阶段结果为 setup=passed、call=passed、teardown=passed。
- 测试是否通过：是。
- 本实例独立数据库：`survey_system_test_6d00fa687f014cb4a04add376f2bb36a`。

本次实际采集结果：

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

对应测试源代码：`tests/test_course_requirements.py::test_stats_isolate_surveys_and_reject_foreign_questions`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。

## BROWSER-001 浏览器自动化场景

- 测试编号：BROWSER-001
- 测试类型：浏览器自动化端到端测试。
- 前置条件：本机MongoDB、Microsoft Edge、Playwright；脚本创建独立UUID测试库和临时本机服务。
- 操作步骤：自动注册登录→建问卷→添加年龄/反馈题→配置未成年人END→发布→输入200触发错误→改16→跳转结束→提交→查看匿名统计→检查390px宽度。
- 输入数据：browser_user、匿名问卷、年龄0～120整数、lt18→END、无效200、有效16。
- 预期结果：能完成流程；200显示最大值错误；16跳过反馈；总答卷数1、平均16、不显示身份；无页面JS异常、窄屏不横向溢出。
- 实际结果：进程退出码 0；输出见下。
- 测试是否通过：是。

```text
Browser scenario: 1 passed, 0 failed (register/create/questions/rules/publish/validate/jump/submit/statistics/mobile width)
```

## 首轮失败与测试修正记录

首轮结果：113通过 / 1失败 / 0跳过 / 0未执行。原始结果保留为 first-run-cases.json / first-run-pytest.xml。

失败用例：test_create_defaults_persisted。创建响应 created_at 保留 Python 微秒，读取响应经过 BSON Date 毫秒存储，直接全对象相等断言错误。涉及测试文件 tests/test_course_requirements.py 与业务响应位置 app/surveys.py；已在修正前向用户说明。

仅修正测试：将创建时间向下截断到毫秒，严格比较读取时间与数据库时间；原始创建时间差还必须小于1毫秒；其他字段仍完全相等。不改业务代码、不放宽其他断言。单用例重跑1通过0失败，证据 timestamp-recheck.json/xml；随后重新执行全部用例，结果见上文。
