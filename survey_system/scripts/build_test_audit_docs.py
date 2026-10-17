"""Build reviewable test documents from actual pytest phase results.

Run only after pytest --audit-report=...; never converts not-run into passed.
"""
import hashlib
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "test-results" / "coverage-audit"
CATEGORIES = ["创建问卷", "添加题目", "跳转逻辑", "答案校验", "提交问卷", "统计结果"]
LABELS = {"passed": "通过", "failed": "失败", "skipped": "跳过", "not_run": "未执行"}


def counts(cases):
    counter = Counter(c["status"] for c in cases)
    return f'{counter["passed"]}通过 / {counter["failed"]}失败 / {counter["skipped"]}跳过 / {counter["not_run"]}未执行'


def code_json(value):
    return "```json\n" + json.dumps(value, ensure_ascii=False, indent=2, default=str) + "\n```"


def business_unchanged():
    original = json.loads((EVIDENCE / "business-files-before.json").read_text(encoding="utf-8-sig"))
    differences = []
    for record in original:
        path = Path(record["Path"])
        if not path.exists() or hashlib.sha256(path.read_bytes()).hexdigest().upper() != record["Hash"]:
            differences.append(str(path))
    previous_paths = {str(Path(r["Path"])) for r in original}
    for path in (ROOT / "app").rglob("*"):
        if path.is_file() and path.suffix in (".py", ".js", ".css", ".html") and str(path) not in previous_paths:
            differences.append(str(path))
    return differences


def build_inventory(cases):
    lines = ["# 课程六类测试覆盖核对", "",
             "本清单逐项阅读原有断言后建立，不能用旧总数43推断覆盖完整。已有与新增指本次核对之前和之后。参数化实例逐一执行，跨类别的同一实例只执行一次。", "",
             "## 原有测试文件与名称", "",
             "| 课程类别 | 原有文件和函数 | 原有覆盖与不足 |", "| --- | --- | --- |"]
    gaps = {
        "创建问卷": "已有创建/分享/所有权/截止；缺默认值与落库、非法标题及未登录零写入断言。",
        "添加题目": "已有文本添加、ID稳定和部分非法配置单元检查；缺四类API落库、非法配置无副作用、权限与发布状态检查。",
        "跳转逻辑": "已有END、规则持久化、数字跳后题、自跳/未知目标和首匹配；缺数字各运算边界、选择不匹配回退、真正回跳第一题的API拒绝。",
        "答案校验": "已有部分必答、文本/数字/选项边界单元检查；缺四类必答/选答、最多/精确数量以及API合法与非法输入的落库验证。",
        "提交问卷": "已有保存、重复/并发、匿名/实名、过期/关闭；缺提交本身未登录、草稿和路径外输入拒绝、不同用户分别保存。",
        "统计结果": "已有四类整卷、数字单题、跳过题不计数；缺四类单题一致性、零选项、选答空值、跨问卷隔离和后续提交刷新。",
    }
    for category in CATEGORIES:
        nodes = sorted({c["nodeid"].split("[")[0] for c in cases if c["origin"] == "已有" and category in c["categories"]})
        lines.append(f'| {category} | ' + "<br>".join(f"`{n}`" for n in nodes) + f' | {gaps[category]} |')
    lines += ["", "原有 test_management/test_deadline 曾直接向测试库插入占位题；不能用它们替代添加题目API测试。原有部分 raises 断言只检查异常类型，不能推断具体422或无写入；新增接口用例已补充。", "",
              "## 本次逐类结果", "",
              "| 类别 | 原有实例 | 新增实例 | 关联实例实际结果 | 新增函数 |", "| --- | ---: | ---: | --- | --- |"]
    for category in CATEGORIES:
        related = [c for c in cases if category in c["categories"]]
        old = [c for c in related if c["origin"] == "已有"]
        new = [c for c in related if c["origin"] == "新增"]
        functions = sorted({c["nodeid"].split("::")[-1].split("[")[0] for c in new})
        lines.append(f'| {category} | {len(old)} | {len(new)} | {counts(related)} | ' + "<br>".join(f"`{n}`" for n in functions) + " |")
    lines += ["", "类别间有交叉，不要相加得到总测试数。全套唯一实例结果：" + counts(cases) + "。", "",
              "以上覆盖结论限定于文档中列出的实际断言，不声称穷尽所有输入、负载或安全情形。已有其他类别测试（健康检查、认证、静态资源、文档）仍保留运行。", "",
              "## 数据隔离与证据", "",
              "conftest.py 显式连接本机 MongoDB，每用例使用 survey_system_test_<32位UUID>，不继承 MONGODB_DATABASE。创建之前和清理之前都校验名称；finalizer 在用例失败时仍仅清理自己的数据库。未扫描、删除、读取或写入开发库业务记录。", "",
              "逐项用例见 [TEST_CASES.md](TEST_CASES.md)，原始结果见 test-results/coverage-audit/cases.json 与 pytest.xml。原始 JSON 同时保存每个用例的 setup/call/teardown 结果、测试库名和新增用例采集的实际观察值。", "",
              "浏览器脚本是自动化测试；没有实际执行的人工验收计划不计入已执行手工测试。"]
    return "\n".join(lines) + "\n"


def build_cases(report):
    cases = report["cases"]
    lines = ["# 自动化测试用例与实际结果", "",
             f'执行时间：{report["executed_at"]}（UTC+08:00）。执行者：Codex代理。', "",
             "执行命令：", "", "```powershell",
             ".venv/Scripts/python -m pytest -q --junitxml=test-results/coverage-audit/pytest.xml --audit-report=test-results/coverage-audit/cases.json",
             "```", "",
             "这些全部是自动化测试。每个参数化输入单独编号；测试通过以 setup、call、teardown 全部成功为准，失败/跳过/未执行不会记为通过。", "",
             "公共输入约定：新增题目默认 title=课程测试题，required=true；选择题选项为 a/A、b/B、c/C。问卷默认 title=课程核对、draft、非匿名、每人一次。新用例的准备动作通过注册/登录/建卷/加题/发布API执行。UUID在运行时生成，参数中的题目位置在步骤中映射为对应UUID；密码与令牌不写入证据。", "",
             "已有用例未采集原始HTTP响应时，实际结果仅记为pytest断言通过，不编造具体响应值。新增用例另外列出实际采集的状态码、数量或统计值；预期结果同时包含数据库、ID或路径等额外断言。", "",
             "| 分类 | 结果 |", "| --- | --- |"]
    for origin in ("已有", "新增"):
        lines.append(f'| {origin} | {counts([c for c in cases if c["origin"] == origin])} |')
    for c in cases:
        case_type = "自动化数据库集成测试（直接调用权限函数）" if c["nodeid"].endswith("::test_ownership") else c["type"]
        lines += ["", f'## {c["id"]} {c["nodeid"]}', "",
                  f'- 测试编号：{c["id"]}',
                  f'- 测试类型：{case_type}；{c["origin"]}；课程类别：{"、".join(c["categories"])}。',
                  f'- 前置条件：{c["preconditions"]}',
                  f'- 操作步骤：{c["steps"]}',
                  f'- 输入数据：{c["inputs"]}',
                  f'- 预期结果：{c["expected"]}',
                  f'- 实际结果：pytest {LABELS[c["status"]]}；阶段结果为 ' + "、".join(f'{p["phase"]}={p["outcome"]}' for p in c["phases"]) + "。",
                  '- 测试是否通过：' + ("是" if c["status"] == "passed" else "否" if c["status"] == "failed" else "未判定") + "。"]
        if c["database"]:
            lines.append(f'- 本实例独立数据库：`{c["database"]}`。')
        if c["parameters"]:
            lines += ["", "本实例精确参数：", "", code_json(c["parameters"])]
        if c["observations"]:
            lines += ["", "本次实际采集结果：", "", code_json(c["observations"])]
        failures = [p["failure"] for p in c["phases"] if p["failure"]]
        if failures:
            lines += ["", "失败原因与原始断言：", "", "```text", "\n".join(failures), "```"]
        lines += ["", "对应测试源代码：`" + c["nodeid"].split("[")[0] + "`。完整断言源保存在原始 cases.json 的 source 字段，便于核查文档与执行是否一致。"]
    browser_path = EVIDENCE / "browser.json"
    lines += ["", "## BROWSER-001 浏览器自动化场景", "",
              "- 测试编号：BROWSER-001", "- 测试类型：浏览器自动化端到端测试，不是手工测试。",
              "- 前置条件：本机MongoDB、Microsoft Edge、Playwright；脚本创建独立UUID测试库和临时本机服务。",
              "- 操作步骤：自动注册登录→建问卷→添加年龄/反馈题→配置未成年人END→发布→输入200触发错误→改16→跳转结束→提交→查看匿名统计→检查390px宽度。",
              "- 输入数据：browser_user、匿名问卷、年龄0～120整数、lt18→END、无效200、有效16。",
              "- 预期结果：能完成流程；200显示最大值错误；16跳过反馈；总答卷数1、平均16、不显示身份；无页面JS异常、窄屏不横向溢出。"]
    if browser_path.exists():
        browser = json.loads(browser_path.read_text(encoding="utf-8"))
        lines += [f'- 实际结果：进程退出码 {browser["returncode"]}；输出见下。',
                  '- 测试是否通过：' + ("是。" if browser["returncode"] == 0 else "否。"), "", "```text", browser["output"].strip(), "```"]
    else:
        lines += ["- 实际结果：本轮未执行；历史结果见旧测试记录。", "- 测试是否通过：本轮未判定。"]
    lines += ["", "## 人工验收", "",
              "本轮未实际手动操作测试，已执行手工测试数量为0。待执行计划单列于 MANUAL_TESTS.md，不能当作已执行的手工测试结果。"]
    first_run = EVIDENCE / "first-run-cases.json"
    if first_run.exists():
        initial = json.loads(first_run.read_text(encoding="utf-8"))
        lines += ["", "## 首轮失败与测试修正记录", "",
                  "首轮结果：" + counts(initial["cases"]) + "。原始结果保留为 first-run-cases.json / first-run-pytest.xml。", "",
                  "失败用例：test_create_defaults_persisted。创建响应 created_at 保留 Python 微秒，读取响应经过 BSON Date 毫秒存储，直接全对象相等断言错误。涉及测试文件 tests/test_course_requirements.py 与业务响应位置 app/surveys.py；已在修正前向用户说明。", "",
                  "仅修正测试：将创建时间向下截断到毫秒，严格比较读取时间与数据库时间；原始创建时间差还必须小于1毫秒；其他字段仍完全相等。不改业务代码、不放宽其他断言。单用例重跑1通过0失败，证据 timestamp-recheck.json/xml；随后重新执行全部用例，结果见上文。"]
    return "\n".join(lines) + "\n"


def build_manual_plan():
    path = ROOT / "docs" / "MANUAL_TESTS.md"
    old = path.read_text(encoding="utf-8")
    # Preserve the existing sixteen scenarios, but make all required fields explicit.
    rows = []
    for line in old.splitlines():
        if line.startswith("| M"):
            parts = [p.strip() for p in line.strip("|").split("|")]
            rows.append(parts[:3])
    if not rows:
        return  # Already expanded by a previous invocation.
    lines = ["# 待执行人工验收计划", "",
             "这是计划，未实际手动执行；不计入已执行手工测试。只有本人实际操作并填写时间、证据与观察结果后，才可将对应项标为手工测试并判定通过。浏览器自动化不能替代此记录。", "",
             "公共前置条件：本机MongoDB和Web服务可用；仅在专用演示/验收库操作，设置MONGODB_DATABASE=survey_system_manual_<自选唯一后缀>再启动服务，避免改动日常开发数据。使用两个独立浏览器会话，按顺序执行；teacher01创建问卷，student01填写。若重复执行，重新使用独立演示库和账号。", "",
             "默认测试密码password123，仅用于测试账号。前置步骤未通过时，依赖它的计划项不得判定通过。"]
    details = {
        "M01": ("使用尚未注册的teacher01；准备学生独立会话。", "用户名teacher01，密码password123；错误密码incorrect123。"),
        "M02": ("M01教师已登录。", "title=课堂反馈；anonymous=true；allow_multiple=false；deadline留空。"),
        "M03": ("M02草稿已创建，未发布。", "single：title=是否参加，yes/是、no/否，required=true；multiple：title=兴趣，a/A、b/B、c/C，min_choices=max_choices=2。"),
        "M04": ("M03草稿已有两道选择题。", "text：title=建议，min_length=2，max_length=20；number：title=年龄，min_value=0，max_value=120，integer=true。"),
        "M05": ("M04草稿四题齐全，已记录各题UUID。", "第一题规则eq/no→END；多选规则contains_all/[a,b]→年龄题UUID。"),
        "M06": ("M05规则已保存；教师登录；持有草稿题UUID和令牌。", "PUT rules，target依次取当前题UUID、missing-id；条件与原题型一致。"),
        "M07": ("草稿四题和合法规则已保存；学生窗口未登录。", "分享路径/survey/<实际问卷UUID>；student01/password123（未注册时先注册）。"),
        "M08": ("M07学生已登录填写且还未提交。", "单选yes；多选先[a]再[a,b]；数字依次121、1.5。"),
        "M09": ("M08仍在本份问卷填写流程。", "单选yes；多选[a,b]；年龄20；建议题由规则跳过不填。"),
        "M10": ("M09已有student01的一份有效答卷。", "同一学生再次从分享链接进入；重复有效路径yes/[a,b]/20并提交。"),
        "M11": ("M09提交成功；M10未增加答卷；教师会话登录。", "查询该问卷统计与答卷详情；有效输入年龄20，多选a/b。"),
        "M12": ("学生会话已登录，持有其自己的令牌和教师问卷UUID。", "GET /api/surveys/{sid}、/stats、/responses；sid为教师问卷UUID。"),
        "M13": ("教师已登录；建立独立新问卷，发布后填写。", "anonymous=false，allow_multiple=true；一题number；同一学生先10再30。"),
        "M14": ("已有发布问卷及其分享链接；教师和学生两会话都可用。", "教师关闭后，学生用原有效答案再次提交。"),
        "M15": ("使用新的独立草稿，至少有一道可回答题。", "deadline=本次操作时间之后1分钟（带本地时区）；发布并实际等待到期后提交。"),
        "M16": ("新建独立问卷，至少有一道required=false的文本题并发布。", "文本题留空，不输入空格，直接下一步并提交。"),
    }
    for number, steps, expected in rows:
        preconditions, inputs = details[number]
        lines += ["", f"## {number}", "",
                  f"- 测试编号：{number}",
                  "- 测试类型：计划人工验收（未执行，不计入手工测试结果）。",
                  "- 前置条件：满足公共条件；" + preconditions,
                  f"- 操作步骤：{steps}",
                  f"- 输入数据：{inputs}",
                  f"- 预期结果：{expected}",
                  "- 实际结果：未执行；执行人、时间、观察值、截图/证据待实际操作后填写。",
                  "- 测试是否通过：未判定。"]
    lines += ["", "用例完成后，请把输入数据中引用的前序配置补充为本人实际使用值，并记录服务URL、数据库名和问卷ID。不要仅依据自动化运行结果把这里改为通过。"]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    report = json.loads((EVIDENCE / "cases.json").read_text(encoding="utf-8"))
    cases = report["cases"]
    differences = business_unchanged()
    (EVIDENCE / "business-integrity.json").write_text(json.dumps({"unchanged": not differences, "differences": differences}, ensure_ascii=False, indent=2), encoding="utf-8")
    (ROOT / "docs" / "TEST_COVERAGE_AUDIT.md").write_text(build_inventory(cases), encoding="utf-8")
    (ROOT / "docs" / "TEST_CASES.md").write_text(build_cases(report), encoding="utf-8")
    build_manual_plan()
    summary = ["", "## 本轮课程六类测试逐项审计", "",
               f'执行时间：{report["executed_at"]}（UTC+08:00）。', "",
               "原有实例：" + counts([c for c in cases if c["origin"] == "已有"]) + "。",
               "新增实例：" + counts([c for c in cases if c["origin"] == "新增"]) + "。",
               "全套唯一实例：**" + counts(cases) + "**。", "",
               "逐类覆盖和名称见 TEST_COVERAGE_AUDIT.md；每个实例的前置、步骤、输入、预期、实际与通过情况见 TEST_CASES.md；原始证据为 test-results/coverage-audit/cases.json 和 pytest.xml，保留旧test-results/pytest.xml作为历史记录。", "",
               "业务文件SHA-256核对：" + ("app下Python/JavaScript/CSS/HTML与审计前完全一致，未修改业务代码。" if not differences else "存在变更：" + "、".join(differences)), "",
               "失败原因：" + ("本轮没有失败。" if all(c["status"] == "passed" for c in cases) else "见逐项用例的原始异常，不把失败改为通过。"),
               "手工测试：0项已执行。MANUAL_TESTS.md是待执行人工计划。pytest仍有原有Starlette/httpx弃用警告，不属于测试失败。"]
    first_run = EVIDENCE / "first-run-cases.json"
    if first_run.exists():
        initial = json.loads(first_run.read_text(encoding="utf-8"))
        summary += ["", "首轮结果：" + counts(initial["cases"]) + "。唯一失败是新增用例将微秒创建响应与毫秒落库读取响应直接比较。已说明原因后仅修正测试的时间精度预期，业务代码未修改。修正后单用例1通过0失败，再运行全套得上述最终结果。保留 first-run-* 与 timestamp-recheck.*，不隐藏首轮失败。"]
    browser_path = EVIDENCE / "browser.json"
    if browser_path.exists():
        browser = json.loads(browser_path.read_text(encoding="utf-8"))
        summary += ["", "本轮浏览器自动化：" + ("1通过、0失败。" if browser["returncode"] == 0 else "失败，退出码" + str(browser["returncode"]) + "。") + "证据 browser.json；不计入114个pytest实例，也不属于手工测试。"]
    path = ROOT / "docs" / "TEST_RESULTS.md"
    old = path.read_text(encoding="utf-8").split("\n## 本轮课程六类测试逐项审计")[0]
    path.write_text(old.rstrip() + "\n" + "\n".join(summary) + "\n", encoding="utf-8")
    print(counts(cases))
    print("Business files unchanged:", not differences)
    for category in CATEGORIES:
        print(category, counts([c for c in cases if category in c["categories"]]))


if __name__ == "__main__":
    main()
