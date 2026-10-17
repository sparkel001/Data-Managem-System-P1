"""Optional per-case evidence: pytest --audit-report test-results/.../cases.json."""
import inspect
import json
from datetime import datetime
from pathlib import Path

import pytest

from tests.audit_catalog import LEGACY


def pytest_addoption(parser):
    parser.addoption("--audit-report", default=None, help="Write per-case inputs, assertion outcomes and observations as JSON")


def pytest_collection_modifyitems(items):
    for index, item in enumerate(items, 1):
        metadata = getattr(item.obj, "audit_case", None)
        if metadata is None:
            categories, steps, inputs, expected = LEGACY.get(item.originalname, (
                ["待归类"], "执行测试函数，断言见源代码。", "见实例参数与源代码。", "见测试函数的显式断言；尚未人工编目。"
            ))
            metadata = {
                "categories": categories, "steps": steps, "inputs": inputs, "expected": expected,
                "preconditions": "本机MongoDB可用；每实例独立UUID测试库。" if "client" in item.fixturenames else "纯函数/本地文件自动测试；无需MongoDB业务数据。",
            }
        else:
            metadata = dict(metadata)
            metadata["categories"] = [metadata.pop("category")]
        item.audit_metadata = {
            "id": f"AUTO-{index:03d}", "nodeid": item.nodeid,
            "origin": "新增" if "test_course_requirements.py" in item.nodeid else "已有",
            "type": ("自动化数据库集成测试（直接调用权限函数）" if item.originalname == "test_ownership" else
                     "自动化API集成测试（真实MongoDB）" if "client" in item.fixturenames else "自动化单元/文件检查"),
            **metadata,
            "parameters": getattr(getattr(item, "callspec", None), "params", {}),
            "source": inspect.getsource(item.obj),
        }
        item.audit_observations = []
        item.audit_phases = []


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    item.audit_phases.append({
        "phase": report.when, "outcome": report.outcome,
        "duration": report.duration,
        "failure": report.longreprtext if report.failed else None,
    })


def pytest_sessionfinish(session, exitstatus):
    destination = session.config.getoption("--audit-report")
    if not destination:
        return
    # Use an explicit UTC+8 offset: Windows Python installations may lack tzdata.
    from datetime import timezone, timedelta
    result = {"executed_at": datetime.now(timezone(timedelta(hours=8))).isoformat(),
              "exitstatus": int(exitstatus), "cases": []}
    for item in session.items:
        phases = getattr(item, "audit_phases", [])
        status = "failed" if any(p["outcome"] == "failed" for p in phases) else "skipped" if any(p["outcome"] == "skipped" for p in phases) else "passed" if any(p["phase"] == "call" and p["outcome"] == "passed" for p in phases) else "not_run"
        result["cases"].append({
            **item.audit_metadata, "status": status,
            "phases": phases, "observations": item.audit_observations,
            "database": getattr(item, "audit_database", None),
        })
    path = Path(destination)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
