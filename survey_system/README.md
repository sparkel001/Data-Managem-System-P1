# 基于 MongoDB 的问卷系统

基于 Python、FastAPI、PyMongo、MongoDB 和原生 HTML/CSS/JavaScript 实现的简化问卷系统。所有业务数据存储在 MongoDB 中，不使用关系数据库或现成问卷系统框架。

## 1. 环境要求

- Windows + PowerShell（下文命令按 Windows 编写）
- Python 3.11 或更高版本；项目已有测试记录使用 Python 3.14.4
- 本机 MongoDB 服务，默认连接 `mongodb://127.0.0.1:27017`
- Git 非必需

项目不需要 Docker 或互联网服务运行；但首次安装 Python 依赖时通常需要网络，除非已提前准备好依赖包。

## 2. 首次安装与启动

在 PowerShell 中进入解压后的项目根目录（即包含 `requirements.txt` 的 `survey_system` 目录），执行：

```powershell
# 1. 创建项目独立虚拟环境
python -m venv .venv

# 2. 安装依赖
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

# 3. 创建本地环境配置文件
Copy-Item .env.example .env

# 4. 启动服务（启动前请确认本机 MongoDB 已运行）
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

浏览器打开：

- 首页：<http://127.0.0.1:8000>
- API 文档：<http://127.0.0.1:8000/docs>
- 健康检查：<http://127.0.0.1:8000/api/health>

如果 `.env` 中的 MongoDB 地址或数据库名需要自定义，请按 `.env.example` 中的变量配置。默认数据库为 `survey_system`，连接地址为 `mongodb://127.0.0.1:27017`。MongoDB 必须先启动；服务会在启动过程中创建所需索引。

## 3. 运行测试

先确保 MongoDB 服务可连接，再在项目根目录执行：

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

测试使用带 UUID 后缀的独立 `survey_system_test_*` 数据库，不应清理或替代开发数据库 `survey_system`。测试完成后仅清理本次测试创建的数据库。

可选：运行真实浏览器端到端测试（需要本机 Microsoft Edge，并先安装浏览器测试依赖）：

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-browser.txt
.\.venv\Scripts\python.exe -m tests.browser_demo
```

浏览器测试会使用独立测试库与随机本机端口，完成后关闭服务并清理测试库。测试截图和结果位置以测试脚本及 `docs/TEST_RESULTS.md` 的实际记录为准。

如需重新生成逐项测试报告：

```powershell
.\.venv\Scripts\python.exe -m pytest -q --junitxml=test-results/coverage-audit/pytest.xml --audit-report=test-results/coverage-audit/cases.json
.\.venv\Scripts\python.exe scripts/build_test_audit_docs.py
```

以上命令会重新运行测试并生成审计记录；运行前应确认 MongoDB 可用。已有测试记录见 [测试结果](docs/TEST_RESULTS.md)。

## 4. 基本使用流程

注册账号 → 登录 → 新建问卷 → 添加题目 → 配置跳转规则 → 发布 → 复制分享链接 → 填写者登录后填写 → 创建者查看答卷与统计。

系统支持单选、多选、文本填空和数字填空。跳转规则由问卷配置，不写死在程序中。填写者需要登录；匿名问卷对创建者隐藏填写者身份，但数据库内部仍保留关联以支持重复填写限制。

## 5. 目录结构与文档

- `app/`：应用配置、认证、问卷、题目、跳转、答卷、统计与静态网页
- `tests/`：自动化测试与浏览器流程测试
- `scripts/`：测试审计文档生成等辅助脚本
- `docs/DATABASE.md`：MongoDB 集合、字段、索引及建模理由
- `docs/API.md`：API 路径、请求格式、状态码和返回字段
- `docs/LOGIC.md`：问卷生命周期、跳转、校验、并发及已知限制
- `docs/TEST_COVERAGE_AUDIT.md`：六类课程测试覆盖核对
- `docs/TEST_CASES.md`：自动化测试用例与执行结果
- `docs/TEST_RESULTS.md`：已有测试执行记录
- `docs/REPORT.md`：第一阶段项目完成报告
- `docs/AI_USAGE_LOG.md`：AI 使用过程日志


## 6. 已知范围与限制

- 只有成功提交后才会保存整份答卷；未提交内容不会自动保存，刷新可能丢失。
- 跳转只支持向后，不支持回跳。
- 问卷关闭后不能重新开启。
- 统计逻辑将答卷载入内存，适用于课堂规模数据，尚未实现分页。
- 关闭问卷与答卷写入不是跨文档事务，已经通过检查的提交可能在关闭后完成写入。
- 项目面向本机课堂演示，没有邮件通知、找回密码、互联网部署、答卷导出等功能。

详细限制和设计理由见 [关键逻辑说明](docs/LOGIC.md)。
