# 实际测试执行记录

执行日期：2026-10-16（Asia/Shanghai）

环境：Windows、Python 3.14.4、真实本机 MongoDB（127.0.0.1:27017）、项目独立虚拟环境。运行命令 `.venv/Scripts/python -m pytest -q`，数据库均为 UUID 后缀的 survey_system_test_*，未访问或清理开发业务记录。

| 阶段完成时 | 累计通过 | 失败 | 跳过 | 说明 |
| --- | ---: | ---: | ---: | --- |
| BLOCK 1 | 1 | 0 | 0 | 配置、健康检查、测试库隔离 |
| BLOCK 2 | 3 | 0 | 0 | 注册登录、哈希、注销、所有权 |
| BLOCK 3 | 5 | 0 | 0 | 管理、发布关闭、截止、分享 |
| BLOCK 4 | 19 | 0 | 0 | 建题、稳定 ID、四题型和校验 |
| BLOCK 5 | 26 | 0 | 0 | 数据规则、跳转与非法目标 |
| BLOCK 6 | 30 | 0 | 0 | 填写保存、重复、匿名、网页路由 |
| BLOCK 7 | 31 | 0 | 0 | 全卷及单题统计 |
| BLOCK 8 | 41 | 0 | 0 | 端到端、并发、防越权、截止 |

BLOCK 8 另外运行 `.venv/Scripts/python -m tests.browser_demo`：真实无界面 Microsoft Edge 场景 **1通过、0失败**。覆盖注册登录、建问卷、加题、配置数字跳转、发布、数字校验提示、跳过必答题、提交、匿名统计及390px宽度检查。未捕获到页面 JavaScript 异常。截图 test-results/browser-stats.png 已检查，无明显截断或重叠。

JavaScript 运行 `node --check app/static/app.js` 通过。pytest 有一条依赖弃用警告：Starlette 的 httpx 测试客户端后续建议迁移到 httpx2；当前所有测试正常运行，没有隐藏警告或伪造结果。

BLOCK 9 最终回归：**43通过、0失败、0跳过**，JUnit 原始结果保存在 test-results/pytest.xml。离线接口文档、OpenAPI结构和文档完整性检查通过；docs.js语法检查通过。各块要求均已实现，范围取舍详见 LOGIC.md。

## 本轮课程六类测试逐项审计

执行时间：2026-10-16T19:30:09.657881+08:00（UTC+08:00）。

原有实例：43通过 / 0失败 / 0跳过 / 0未执行。
新增实例：71通过 / 0失败 / 0跳过 / 0未执行。
全套唯一实例：**114通过 / 0失败 / 0跳过 / 0未执行**。

逐类覆盖和名称见 TEST_COVERAGE_AUDIT.md；每个实例的前置、步骤、输入、预期、实际与通过情况见 TEST_CASES.md；原始证据为 test-results/coverage-audit/cases.json 和 pytest.xml，保留旧test-results/pytest.xml作为历史记录。

业务文件SHA-256核对：app下Python/JavaScript/CSS/HTML与审计前完全一致，未修改业务代码。

失败原因：本轮没有失败。
pytest仍有原有Starlette/httpx弃用警告，不属于测试失败。

首轮结果：113通过 / 1失败 / 0跳过 / 0未执行。唯一失败是新增用例将微秒创建响应与毫秒落库读取响应直接比较。已说明原因后仅修正测试的时间精度预期，业务代码未修改。修正后单用例1通过0失败，再运行全套得上述最终结果。保留 first-run-* 与 timestamp-recheck.*，不隐藏首轮失败。

本轮浏览器自动化：1通过、0失败。证据 browser.json；不计入114个pytest实例，也不属于手工测试。
