# 基于 MongoDB 的问卷系统

本项目用于离线课堂演示问卷的设计、发布、填写和统计。创建者可以维护问卷、配置答案校验与跳转规则，并将常用题目保存到题库反复使用。系统用完整问卷快照保存每份问卷的题目，用不可变版本管理题库内容，使题目更新不会改变已发布问卷及已有答卷的含义。

## 功能

| 功能 | 已实现内容 |
|---|---|
| 账号与权限 | 独立注册、登录页面；密码哈希；会话与退出；服务端用户名查重和唯一索引；按所有者限制管理及统计权限 |
| 问卷管理 | 新建、列表、编辑草稿、发布、关闭、截止时间、填写分享链接；发布后冻结题目结构 |
| 题型与校验 | 单选、多选、文本、数字；必答、选择数量、文本长度、数字上下限和整数要求 |
| 条件跳转 | 单选、多选和数字条件；按规则顺序取首个匹配；目标限后续题目或结束，防止循环 |
| 填写与答卷 | 登录后逐题填写，服务端重新计算路径并校验后保存；可限制每人一次或允许重复填写 |
| 问卷统计 | 总答卷数、选项计数、文本及数字答案列表、数字平均值；整卷和单题接口 |
| 题库与复用 | 创建和编辑题库，保存新题、从自有问卷复制、加入或移出已有题库题目；指定版本加入草稿 |
| 题目版本 | 创建新版本、查看版本关系、从指定版本分支、恢复旧版本为新版本；草稿显式换版 |
| 共享与查询 | 按用户名分享题目、查看共享列表、撤销分享；查询自己有权管理的使用问卷 |
| 跨问卷统计 | 按题目族查询并按不可变版本分别汇总；支持版本筛选与数字频数分布 |

匿名问卷仍要求填写者登录，但创建者的答卷详情和统计不返回填写者身份。内部身份关联用于填写次数限制，匿名不等于数据库层面不可追溯。

系统适合课堂规模数据。未实现删除问卷、删除或重排题目、未提交答卷的自动保存、答卷导出、找回密码和互联网部署。关闭的问卷不能重新开启，跳转不支持回跳，统计没有分页。完整限制见[系统逻辑](docs/LOGIC_PHASE2.md)。

## 技术栈与环境

- 后端：Python、FastAPI 0.143.2、Pydantic 2.14.1、Uvicorn 0.54.0。
- 数据：MongoDB、PyMongo 4.19.0；所有业务数据写入MongoDB，不使用关系数据库或现成问卷框架。
- 前端：原生HTML/CSS/JavaScript，静态资源由应用提供，不依赖CDN。
- 测试：pytest 9.1.1、httpx；可选Playwright 1.64.0和本机Microsoft Edge。
- 已验证环境：Windows、PowerShell、Python 3.14.4。MongoDB服务版本未在现有记录中注明；其他Python版本未验证。

依赖锁定于`requirements.txt`和`requirements-browser.txt`。首次安装依赖通常需要联网；依赖和本机服务准备好后，演示不依赖外网。

## 项目结构

以下目录树根据当前实际源码生成；虚拟环境、缓存及测试数据库物理文件未列入。`app`存放业务与页面，`tests`包含自动测试，`scripts`提供迁移与文档工具，`docs`保存设计及验证材料。`test-results`保存原始JSON/XML结果、截图及核验记录，不在源码树中展开。

```text
survey_system/
├── app/
│   ├── static/
│   │   ├── app.js
│   │   ├── auth.js
│   │   ├── banks.js
│   │   ├── docs.html
│   │   ├── docs.js
│   │   ├── index.html
│   │   ├── messages.js
│   │   └── style.css
│   ├── __init__.py
│   ├── auth.py
│   ├── banks.py
│   ├── config.py
│   ├── cross_statistics.py
│   ├── errors.py
│   ├── logic.py
│   ├── main.py
│   ├── migrations.py
│   ├── questions.py
│   ├── responses.py
│   ├── reuse.py
│   ├── statistics.py
│   ├── surveys.py
│   └── user_indexes.py
├── tests/
│   ├── __init__.py
│   ├── audit_catalog.py
│   ├── audit_plugin.py
│   ├── browser_demo.py
│   ├── conftest.py
│   ├── mongo_config.py
│   ├── test_auth_browser.py
│   ├── test_bank_copy_browser.py
│   ├── test_bank_copy_messages.py
│   ├── test_block1.py
│   ├── test_block2.py
│   ├── test_block3.py
│   ├── test_block4.py
│   ├── test_block5.py
│   ├── test_block6.py
│   ├── test_block7.py
│   ├── test_block8.py
│   ├── test_block9.py
│   ├── test_course_requirements.py
│   ├── test_document_generators.py
│   ├── test_password_policy.py
│   ├── test_phase2_block1.py
│   ├── test_phase2_block2.py
│   ├── test_phase2_block3.py
│   ├── test_phase2_block4.py
│   ├── test_phase2_block5.py
│   ├── test_phase2_block6.py
│   ├── test_phase2_block7_browser.py
│   ├── test_phase2_boundaries.py
│   └── test_registration_integrity.py
├── scripts/
│   ├── build_phase2_test_docs.py
│   ├── build_test_audit_docs.py
│   ├── check_documentation.py
│   ├── migrate_phase2.py
│   └── package_submission.py
├── docs/
│   ├── AI_USAGE_LOG.md
│   ├── AI_USAGE_PHASE2.md
│   ├── API.md
│   ├── API_PHASE2.md
│   ├── DATABASE.md
│   ├── DATABASE_PHASE2.md
│   ├── LOGIC.md
│   ├── LOGIC_PHASE2.md
│   ├── MANUAL_TESTS.md
│   ├── MIGRATION_PHASE2.md
│   ├── REPORT.md
│   ├── REPORT_PHASE2.md
│   ├── TEST_CASES.md
│   ├── TEST_CASES_PHASE2.md
│   ├── TEST_COVERAGE_AUDIT.md
│   ├── TEST_RESULTS.md
│   └── TEST_RESULTS_PHASE2.md
├── .env.example
├── requirements.txt
├── requirements-browser.txt
├── pytest.ini
├── run.py
└── README.md
```

## 安装与运行

在包含`requirements.txt`的项目根目录打开PowerShell。

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
```

`.env`默认配置如下，已有配置文件无需覆盖：

```dotenv
MONGODB_URI=mongodb://127.0.0.1:27017
MONGODB_DATABASE=survey_system
```

MongoDB需要单独安装。本项目不假定它已注册为Windows服务。若已有MongoDB进程，请保持它原有的数据目录和启动方式；若为首次运行，可在独立PowerShell终端启动：

```powershell
# mongod须已加入PATH；否则使用本机实际安装位置的mongod.exe
Get-Command mongod
New-Item -ItemType Directory -Path local-data -Force | Out-Null
mongod --dbpath (Resolve-Path local-data).Path --bind_ip 127.0.0.1 --port 27017
```

该终端保持运行，`local-data`是首次使用的新数据目录。已有数据不能通过替换目录来“修复”。若端口已占用，先确认占用服务，避免启动第二个同端口进程。

在项目终端启动应用：

```powershell
.\.venv\Scripts\python.exe run.py
```

等效命令为：

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

访问首页`http://127.0.0.1:8000`、离线API浏览页`http://127.0.0.1:8000/docs`和健康接口`http://127.0.0.1:8000/api/health`。应用启动会为配置指向的数据库建立索引及题库新增结构；原有问卷、答卷不做来源回填。初始化边界见[迁移说明](docs/MIGRATION_PHASE2.md)。

## 使用方式

1. 首页点击“注册账号”，输入用户名、密码和确认密码；注册成功返回登录页。用户名为3～40位英文字母、数字或下划线，新密码为8～16个字符。历史长密码账号仍可按原8～128字符范围登录。
2. 登录后创建问卷，在草稿中添加题目和校验设置，按需配置跳转、匿名、重复填写和截止时间，再发布问卷。
3. 复制填写链接。填写者登录后回答并提交；创建者从管理页查看答卷、整卷统计及单题结果。只在成功提交后保存答卷，刷新未提交页面可能丢失填写内容。
4. 在“题库与共享”创建题库。“从我的问卷选择题目”复制已有题目；“加入已有题库题目”增加归属；“创建新题目”用于编写新内容。共享题目在共享列表选择。
5. 草稿管理页选择题库中的指定版本。题库修改会创建新版本；草稿须显式换版，已发布或关闭问卷不能换版。恢复旧版同样生成新版本，不覆盖旧记录。
6. 在题目页面查看版本、分享及使用问卷。跨问卷统计只计算当前用户自己的问卷，并按版本分别显示。

## 账号与题库操作细节

登录页和注册页互相切换，点击“返回登录”不提交注册。注册成功保留用户名、清空密码且不自动登录；确认密码只用于页面校验，不传给服务端。分享地址上的注册和登录保持原问卷路径，登录后继续填写；退出删除服务端会话和浏览器凭据。已有有效会话可直接进入相应页面。

密码字符数按Unicode码点计算，包含emoji；新注册8～16字符，登录保留8～128字符，既有账号无需改密。前端不按UTF-16长度截断密码。

题库候选只列出尚未加入当前题库的自有可复用题目。列表为空可能表示尚未保存可复用题目，或已有题目均在当前库；可从自己的问卷复制或创建新题。没有可复制题目时，可返回“我的问卷”添加题目。自己的草稿、已发布和已关闭问卷均可作为复制来源；原问卷与答卷不变。共享题目仍在共享列表中查看和复用。

## 自动测试

测试库始终使用`survey_system_test_<32位UUID>`，不继承应用的`MONGODB_DATABASE`；每个用例仅清理自己的UUID库。为了与开发进程完全分离，可在另一个终端启动独立MongoDB：

```powershell
New-Item -ItemType Directory -Path test-results/local-mongo -Force | Out-Null
mongod --dbpath (Resolve-Path test-results/local-mongo).Path --bind_ip 127.0.0.1 --port 27018
```

测试终端执行：

```powershell
$env:TEST_MONGODB_URI='mongodb://127.0.0.1:27018'
$env:TEST_ARTIFACT_DIR='test-results/local-run'
.\.venv\Scripts\python.exe -m pip install -r requirements-browser.txt
.\.venv\Scripts\python.exe -m pytest -q --junitxml=test-results/local-run/full.xml --audit-report=test-results/local-run/full.json
.\.venv\Scripts\python.exe -m tests.browser_demo
```

完整pytest中包含Edge浏览器测试；缺少Playwright时相关用例会跳过，完整验证须检查跳过数量。浏览器使用已安装的Microsoft Edge，不要求下载另一份Chromium。独立`browser_demo`不计入pytest实例数。省略`TEST_MONGODB_URI`时，测试默认连接27017的MongoDB服务，但数据库名仍为UUID测试库。

无需MongoDB的文档回归命令：

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_block9.py::test_documentation_present -q
```

最近保存的完整测试结果及其范围见[第二阶段测试记录](docs/TEST_RESULTS_PHASE2.md)。自动化测试、独立浏览器流程与项目作者报告的人工检查分别记录，不相加。六项可选人工演示计划的状态见[人工检查记录](docs/MANUAL_TESTS.md)。

## 文档索引与阶段范围

第一阶段文档保留基础系统的历史设计和验证记录；第二阶段文档说明新增功能及行为变更。阅读当前实现时，两组文档配合使用：现行注册密码规则、题库接口、扩展集合与版本逻辑分别见API_PHASE2、DATABASE_PHASE2和LOGIC_PHASE2，不能仅按历史原稿判断当前行为。

### 第一阶段原始文稿

| 文档 | 原始范围 |
|---|---|
| [AI_USAGE_LOG.md](docs/AI_USAGE_LOG.md) | 第一阶段AI使用过程原始记录 |
| [REPORT.md](docs/REPORT.md) | 第一阶段实验报告及原有日期、参与和测试记录 |
| [API.md](docs/API.md) | 第一阶段问卷、题目、跳转、填写及统计接口 |
| [DATABASE.md](docs/DATABASE.md) | 第一阶段四集合、字段、索引和匿名设计 |
| [LOGIC.md](docs/LOGIC.md) | 第一阶段生命周期、校验、路径、提交及适用边界 |
| [TEST_CASES.md](docs/TEST_CASES.md) | 第一阶段114项历史运行的逐项用例及结果 |
| [TEST_COVERAGE_AUDIT.md](docs/TEST_COVERAGE_AUDIT.md) | 第一阶段六类课程要求的覆盖审计 |
| [TEST_RESULTS.md](docs/TEST_RESULTS.md) | 第一阶段原始执行结果及失败修正记录 |

### 第二阶段及后续完善

| 文档 | 新增或变更范围 |
|---|---|
| [REPORT_PHASE2.md](docs/REPORT_PHASE2.md) | 题库、版本、共享、复用、跨问卷统计的完整实验报告 |
| [API_PHASE2.md](docs/API_PHASE2.md) | 新增题库接口及认证、错误响应等接口变更 |
| [DATABASE_PHASE2.md](docs/DATABASE_PHASE2.md) | 三个新增集合、source快照、版本及账号维护边界 |
| [LOGIC_PHASE2.md](docs/LOGIC_PHASE2.md) | 版本、草稿换版、共享、复制与跨问卷计数的扩展逻辑 |
| [MIGRATION_PHASE2.md](docs/MIGRATION_PHASE2.md) | 新增结构初始化、幂等执行、失败重试和兼容性 |
| [TEST_CASES_PHASE2.md](docs/TEST_CASES_PHASE2.md) | 最近保存的175项完整运行记录，包含基础功能回归 |
| [TEST_RESULTS_PHASE2.md](docs/TEST_RESULTS_PHASE2.md) | 第二阶段及后续专项、全量和文档检查记录，区分运行时间和范围 |
| [AI_USAGE_PHASE2.md](docs/AI_USAGE_PHASE2.md) | 第二阶段实际工具、任务摘要、产物、修改与验证 |
| [MANUAL_TESTS.md](docs/MANUAL_TESTS.md) | 项目作者报告完成的五项检查及六项未执行的可选演示计划 |

第一阶段原始证据位于test-results/coverage-audit和test-results/pytest.xml；第二阶段各次结果及其运行范围集中见TEST_RESULTS_PHASE2.md。

## 常见问题

- **启动失败或无法连接MongoDB**：确认MongoDB进程已启动、地址与端口正确；对照当前终端的服务日志检查，不以网页错误推断数据库原因。更改后端代码或配置后应重启服务，页面脚本更新后刷新浏览器。
- **历史重复账号导致新注册受限**：程序保留原账号和索引，健康接口会报告注册约束未就绪。只读排查与人工处理边界见[用户名唯一性维护](docs/DATABASE_PHASE2.md#用户名唯一性维护)，不能通过删除用户或关闭唯一索引绕过。
- **题库候选列表为空**：问卷内题目不会自动成为题库题目，可使用“从我的问卷选择题目”；已有题目全部在当前题库时也没有可加入候选，不需要重复录入。
- **无法修改发布后的题目**：这是保护已有答卷的约束。新内容在题库另存版本，供其他草稿问卷选用；原发布问卷保持不变。
- **浏览器测试跳过或Edge启动失败**：安装`requirements-browser.txt`并确认本机Microsoft Edge可用。测试输出的跳过或失败不能记为通过。
- **出现Starlette/httpx弃用警告**：现有证据保留了该依赖警告；它不等于断言失败，判断仍以退出状态及测试报告为准。
