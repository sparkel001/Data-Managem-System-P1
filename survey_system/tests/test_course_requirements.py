"""Course requirement gaps: real HTTP APIs and isolated MongoDB assertions.

Every parametrized input is a separate case in the generated audit document.
No business modules are patched or mocked.
"""
from datetime import datetime
from uuid import UUID

import pytest

from tests.test_block2 import login


OPTIONS = [{"id": key, "label": key.upper()} for key in ("a", "b", "c")]


def case(category, steps, inputs, expected):
    def decorate(function):
        function.audit_case = {
            "category": category,
            "preconditions": "本机真实 MongoDB 可用；每用例新建 UUID 测试库；通过 API 注册登录，业务数据从空库开始。",
            "steps": steps,
            "inputs": inputs,
            "expected": expected,
        }
        return function
    return decorate


@pytest.fixture
def owner(client):
    return login(client, "course_owner")


def question_input(kind, **changes):
    data = {"title": "课程测试题", "type": kind}
    if kind in ("single", "multiple"):
        data["options"] = OPTIONS
    return {**data, **changes}


def survey_with_questions(client, owner, questions, *, publish=True, **settings):
    response = client.post("/api/surveys", headers=owner, json={"title": "课程核对", **settings})
    assert response.status_code == 201, response.text
    sid = response.json()["id"]
    stored_questions = []
    for data in questions:
        response = client.post(f"/api/surveys/{sid}/questions", headers=owner, json=data)
        assert response.status_code == 201, response.text
        stored_questions = response.json()["questions"]
    if publish:
        response = client.post(f"/api/surveys/{sid}/publish", headers=owner)
        assert response.status_code == 200, response.text
    return sid, stored_questions


def observed(request, **values):
    """Evidence records contain no passwords, bearer tokens or user documents."""
    request.node.audit_observations.append(values)


@case("创建问卷", "登录；POST 创建；查询 MongoDB；GET 详情和列表对照。",
      '{"title":"  课程问卷  "}，其余设置省略。',
      "201；稳定 UUID；标题去空白；draft、非匿名、每人一次、无截止、无题目；创建者正确；时间按BSON毫秒精度与落库一致；详情/列表与落库一致。")
def test_create_defaults_persisted(client, owner, request):
    response = client.post("/api/surveys", headers=owner, json={"title": "  课程问卷  "})
    observed(request, status=response.status_code)
    assert response.status_code == 201
    body = response.json()
    assert str(UUID(body["id"])) == body["id"]
    stored = client.app.state.db.surveys.find_one({"_id": body["id"]})
    assert stored["title"] == "课程问卷"
    assert stored["status"] == "draft" and stored["questions"] == []
    assert stored["anonymous"] is False and stored["allow_multiple"] is False
    assert stored["deadline"] is None and stored["description"] == ""
    assert stored["created_at"].tzinfo is not None
    assert stored["owner_id"] == client.get("/api/auth/me", headers=owner).json()["id"]
    detail = client.get(f'/api/surveys/{body["id"]}', headers=owner).json()
    # BSON Date stores milliseconds; the immediate creation response contains
    # Python microseconds. Compare the actual documented storage precision.
    created = datetime.fromisoformat(body["created_at"])
    stored_precision = created.replace(microsecond=(created.microsecond // 1000) * 1000)
    assert datetime.fromisoformat(detail["created_at"]) == stored["created_at"] == stored_precision
    assert 0 <= (created - stored["created_at"]).total_seconds() < 0.001
    assert {k: v for k, v in detail.items() if k != "created_at"} == {k: v for k, v in body.items() if k != "created_at"}
    assert client.get("/api/surveys", headers=owner).json() == [detail]
    observed(request, creation_time=body["created_at"], read_time=detail["created_at"], bson_precision="milliseconds")
    observed(request, stored_defaults={k: stored[k] for k in ("title", "status", "anonymous", "allow_multiple", "deadline", "questions")})


@case("创建问卷", "登录；POST 非法问卷；查询测试库问卷数量。", "payload 参数。",
      "422；surveys 集合仍为 0 条。")
@pytest.mark.parametrize("payload", [{}, {"title": ""}, {"title": "   "}, {"title": "长" * 201}],
                         ids=["missing-title", "empty-title", "blank-title", "too-long-title"])
def test_create_rejects_invalid_without_write(client, owner, request, payload):
    response = client.post("/api/surveys", headers=owner, json=payload)
    count = client.app.state.db.surveys.count_documents({})
    observed(request, status=response.status_code, surveys=count)
    assert response.status_code == 422
    assert count == 0


@case("创建问卷", "不登录；POST 合法问卷；检查库中数量。", '{"title":"未登录创建"}。',
      "401；surveys 集合无写入。")
def test_create_requires_login(client, request):
    response = client.post("/api/surveys", json={"title": "未登录创建"})
    count = client.app.state.db.surveys.count_documents({})
    observed(request, status=response.status_code, surveys=count)
    assert response.status_code == 401 and count == 0


@case("添加题目", "创建草稿；分别 POST 四类题目；再次添加另一题；检查 API 与 MongoDB 中 ID/配置。",
      "kind 参数；选择题 a/b/c；文本2～4字；数字0～120整数。",
      "两次添加均201；题型和配置落库一致；两道题 UUID 不同，后续添加不改变已有 ID。")
@pytest.mark.parametrize("kind", ["single", "multiple", "text", "number"])
def test_add_each_type_persists_with_stable_ids(client, owner, request, kind):
    configs = {"single": {}, "multiple": {"min_choices": 2, "max_choices": 2},
               "text": {"min_length": 2, "max_length": 4},
               "number": {"min_value": 0, "max_value": 120, "integer": True}}
    data = question_input(kind, **configs[kind])
    sid, questions = survey_with_questions(client, owner, [data], publish=False)
    first = questions[0]
    assert str(UUID(first["id"])) == first["id"]
    for key, value in data.items():
        assert first[key] == value
    response = client.post(f"/api/surveys/{sid}/questions", headers=owner, json=question_input("text"))
    assert response.status_code == 201
    stored = client.app.state.db.surveys.find_one({"_id": sid})["questions"]
    assert stored == response.json()["questions"]
    assert stored[0] == first and stored[0]["id"] != stored[1]["id"]
    observed(request, add_status=201, second_status=response.status_code, kind=kind, stored_questions=len(stored), first_id_stable=True)


@case("添加题目", "创建草稿；保存文档快照；POST 非法题目；重新读取文档比较。",
      "payload 参数。", "422；整个问卷文档（包括 revision 和 questions）不变。")
@pytest.mark.parametrize("payload", [
    question_input("single", options=[]),
    question_input("multiple", min_choices=3, max_choices=2),
    question_input("text", min_length=5, max_length=2),
    question_input("number", min_value=10, max_value=0),
], ids=["single-no-options", "multiple-invalid-limits", "text-invalid-limits", "number-invalid-limits"])
def test_invalid_question_does_not_mutate_survey(client, owner, request, payload):
    sid, _ = survey_with_questions(client, owner, [], publish=False)
    before = client.app.state.db.surveys.find_one({"_id": sid})
    response = client.post(f"/api/surveys/{sid}/questions", headers=owner, json=payload)
    after = client.app.state.db.surveys.find_one({"_id": sid})
    observed(request, status=response.status_code, document_unchanged=before == after)
    assert response.status_code == 422 and before == after


@case("添加题目", "准备草稿或已发布问卷；以指定身份 POST 新题；比较前后文档。",
      "actor 参数：未登录、其他用户、已发布问卷的创建者。",
      "分别401、404、409；问卷文档不变。")
@pytest.mark.parametrize("actor,expected", [("anonymous", 401), ("other", 404), ("published_owner", 409)])
def test_add_question_authorization_and_state(client, owner, request, actor, expected):
    sid, _ = survey_with_questions(client, owner, [question_input("text")], publish=actor == "published_owner")
    headers = {} if actor == "anonymous" else login(client, "other_user") if actor == "other" else owner
    before = client.app.state.db.surveys.find_one({"_id": sid})
    response = client.post(f"/api/surveys/{sid}/questions", headers=headers, json=question_input("number"))
    after = client.app.state.db.surveys.find_one({"_id": sid})
    observed(request, status=response.status_code, document_unchanged=before == after)
    assert response.status_code == expected and before == after


@case("跳转逻辑", "API 创建数字题和后续文本题；设置数字规则到 END；发布；调用 next。",
      "比较阈值18，op/answer/matched 参数。",
      "匹配时 next_question_id=END，否则进入后续文本题；规则从 MongoDB 读取。")
@pytest.mark.parametrize("op,answer,matched", [
    ("eq", 18, True), ("eq", 19, False),
    ("gt", 18, False), ("gt", 19, True),
    ("gte", 18, True), ("gte", 17, False),
    ("lt", 18, False), ("lt", 17, True),
    ("lte", 18, True), ("lte", 19, False),
])
def test_numeric_jump_operator_boundaries_api(client, owner, request, op, answer, matched):
    sid, qs = survey_with_questions(client, owner, [question_input("number"), question_input("text")], publish=False)
    first, second = [q["id"] for q in qs]
    rule = {"op": op, "value": 18, "target": "END"}
    configured = client.put(f"/api/surveys/{sid}/questions/{first}/rules", headers=owner, json={"rules": [rule]})
    assert configured.status_code == 200
    assert client.app.state.db.surveys.find_one({"_id": sid})["questions"][0]["rules"] == [rule]
    assert client.post(f"/api/surveys/{sid}/publish", headers=owner).status_code == 200
    response = client.post(f"/api/fill/{sid}/next", headers=owner, json={"answers": {first: answer}})
    observed(request, status=response.status_code, next_is_end=response.json().get("next_question_id") == "END", matched=matched)
    assert response.status_code == 200
    assert response.json()["next_question_id"] == ("END" if matched else second)


@case("跳转逻辑", "创建选择题+后续文本题；配置跳转规则；发布；使用指定答案调用 next。",
      "kind、op、condition、answer、matched 参数，选项 a/b/c。",
      "匹配则 END；不匹配则按顺序进入后续题；contains_all 允许额外选项但必须包含全部条件。")
@pytest.mark.parametrize("kind,op,condition,answer,matched", [
    ("single", "eq", "a", "a", True), ("single", "eq", "a", "b", False),
    ("multiple", "contains_any", ["a", "b"], ["b"], True),
    ("multiple", "contains_any", ["a", "b"], ["c"], False),
    ("multiple", "contains_all", ["a", "b"], ["a", "b", "c"], True),
    ("multiple", "contains_all", ["a", "b"], ["a"], False),
])
def test_choice_jump_and_fallback_api(client, owner, request, kind, op, condition, answer, matched):
    sid, qs = survey_with_questions(client, owner, [question_input(kind), question_input("text")], publish=False)
    first, second = [q["id"] for q in qs]
    response = client.put(f"/api/surveys/{sid}/questions/{first}/rules", headers=owner,
                          json={"rules": [{"op": op, "value": condition, "target": "END"}]})
    assert response.status_code == 200
    assert client.post(f"/api/surveys/{sid}/publish", headers=owner).status_code == 200
    response = client.post(f"/api/fill/{sid}/next", headers=owner, json={"answers": {first: answer}})
    observed(request, status=response.status_code, next_is_end=response.json().get("next_question_id") == "END", matched=matched)
    assert response.status_code == 200
    assert response.json()["next_question_id"] == ("END" if matched else second)


@case("跳转逻辑", "创建两道数字题草稿；向第二题 PUT 非法规则；比较 MongoDB 文档。",
      "invalid 参数：自跳、回跳第一题、不存在的目标、数字题使用 contains_any。",
      "422；规则和 revision 均不变。")
@pytest.mark.parametrize("invalid", ["self", "backward", "missing", "wrong-operator"])
def test_invalid_jump_api_does_not_mutate(client, owner, request, invalid):
    sid, qs = survey_with_questions(client, owner, [question_input("number"), question_input("number")], publish=False)
    first, second = [q["id"] for q in qs]
    rule = {"op": "gt", "value": 0, "target": {"self": second, "backward": first, "missing": "missing", "wrong-operator": "END"}[invalid]}
    if invalid == "wrong-operator":
        rule.update(op="contains_any", value=["a"])
    before = client.app.state.db.surveys.find_one({"_id": sid})
    response = client.put(f"/api/surveys/{sid}/questions/{second}/rules", headers=owner, json={"rules": [rule]})
    after = client.app.state.db.surveys.find_one({"_id": sid})
    observed(request, status=response.status_code, document_unchanged=before == after)
    assert response.status_code == 422 and before == after


@case("答案校验", "创建并发布指定题型；按 required 配置留空提交；检查 responses。",
      "kind×required；answers={}。",
      "必答422且不保存；选答201，answers={}，path 包含该题。")
@pytest.mark.parametrize("kind", ["single", "multiple", "text", "number"])
@pytest.mark.parametrize("required", [True, False], ids=["required", "optional"])
def test_required_and_optional_all_types_api(client, owner, request, kind, required):
    sid, qs = survey_with_questions(client, owner, [question_input(kind, required=required)])
    response = client.post(f"/api/fill/{sid}/submit", headers=owner, json={"answers": {}})
    saved = list(client.app.state.db.responses.find({"survey_id": sid}))
    observed(request, status=response.status_code, saved_count=len(saved), stored_answers=[r["answers"] for r in saved])
    assert response.status_code == (422 if required else 201)
    if required:
        assert saved == []
    else:
        assert len(saved) == 1 and saved[0]["answers"] == {} and saved[0]["path"] == [qs[0]["id"]]


@case("答案校验", "按配置创建发布单题问卷；提交参数答案；同时核对 HTTP 与 MongoDB。",
      "kind、constraints、answer、expected 参数；选项 a/b/c。",
      "合法边界201且原值保存；非法422且零答卷。多选精确2项、文本2～4字符、数字0～120整数。")
@pytest.mark.parametrize("kind,constraints,answer,expected", [
    ("multiple", {"min_choices": 2, "max_choices": 2}, ["a"], 422),
    ("multiple", {"min_choices": 2, "max_choices": 2}, ["a", "b"], 201),
    ("multiple", {"min_choices": 2, "max_choices": 2}, ["a", "b", "c"], 422),
    ("multiple", {}, ["a", "a"], 422),
    ("multiple", {}, ["a", "missing"], 422),
    ("single", {}, "a", 201), ("single", {}, "missing", 422),
    ("text", {"min_length": 2, "max_length": 4}, "中", 422),
    ("text", {"min_length": 2, "max_length": 4}, "中文", 201),
    ("text", {"min_length": 2, "max_length": 4}, "中文反馈", 201),
    ("text", {"min_length": 2, "max_length": 4}, "中文反馈好", 422),
    ("number", {"min_value": 0, "max_value": 120, "integer": True}, -1, 422),
    ("number", {"min_value": 0, "max_value": 120, "integer": True}, 0, 201),
    ("number", {"min_value": 0, "max_value": 120, "integer": True}, 120, 201),
    ("number", {"min_value": 0, "max_value": 120, "integer": True}, 121, 422),
    ("number", {"integer": True}, 1.5, 422),
    ("number", {"integer": False}, 1.5, 201),
    ("number", {}, True, 422), ("number", {}, "12", 422),
], ids=["multi-below", "multi-exact", "multi-above", "multi-duplicate", "multi-unknown",
        "single-valid", "single-unknown", "text-below", "text-min", "text-max", "text-above",
        "number-below", "number-min", "number-max", "number-above", "integer-fraction",
        "decimal-valid", "number-bool", "number-string"])
def test_answer_validation_submission_boundaries(client, owner, request, kind, constraints, answer, expected):
    sid, qs = survey_with_questions(client, owner, [question_input(kind, **constraints)])
    answers = {qs[0]["id"]: answer}
    response = client.post(f"/api/fill/{sid}/submit", headers=owner, json={"answers": answers})
    saved = list(client.app.state.db.responses.find({"survey_id": sid}))
    observed(request, status=response.status_code, saved_count=len(saved), stored_values=[list(r["answers"].values()) for r in saved])
    assert response.status_code == expected
    if expected == 201:
        assert len(saved) == 1 and saved[0]["answers"] == answers
    else:
        assert saved == []


@case("提交问卷", "准备问卷；按 failure 场景调用 submit；检查零答卷。",
      "未登录、草稿、包含未知题目、包含被跳过题目的额外答案。",
      "分别401、404、422、422；responses 不新增记录。")
@pytest.mark.parametrize("failure,expected", [("unauthenticated", 401), ("draft", 404), ("unknown-answer", 422), ("skipped-answer", 422)])
def test_submit_rejects_invalid_context_without_save(client, owner, request, failure, expected):
    sid, qs = survey_with_questions(client, owner, [question_input("number"), question_input("text")], publish=False)
    first, second = [q["id"] for q in qs]
    answers = {first: 20, second: "反馈"}
    if failure == "unknown-answer":
        answers["unknown"] = "非法答案"
    if failure == "skipped-answer":
        response = client.put(f"/api/surveys/{sid}/questions/{first}/rules", headers=owner,
                              json={"rules": [{"op": "gte", "value": 18, "target": "END"}]})
        assert response.status_code == 200
    if failure != "draft":
        assert client.post(f"/api/surveys/{sid}/publish", headers=owner).status_code == 200
    response = client.post(f"/api/fill/{sid}/submit", headers={} if failure == "unauthenticated" else owner, json={"answers": answers})
    count = client.app.state.db.responses.count_documents({"survey_id": sid})
    observed(request, status=response.status_code, responses=count)
    assert response.status_code == expected and count == 0


@case("提交问卷", "创建每人一次问卷；两位不同用户分别提交；读取数据库。",
      "第一用户数字10，第二用户数字30。",
      "两次201，答卷ID不同，survey_id一致、respondent_id不同，各自答案与路径保存准确。")
def test_distinct_users_can_each_submit_and_persist(client, owner, request):
    sid, qs = survey_with_questions(client, owner, [question_input("number")])
    qid = qs[0]["id"]
    other = login(client, "course_student")
    ids = []
    for headers, value in [(owner, 10), (other, 30)]:
        response = client.post(f"/api/fill/{sid}/submit", headers=headers, json={"answers": {qid: value}})
        assert response.status_code == 201
        ids.append(response.json()["id"])
        saved = client.app.state.db.responses.find_one({"_id": ids[-1]})
        assert saved["survey_id"] == sid and saved["answers"] == {qid: value} and saved["path"] == [qid]
    rows = list(client.app.state.db.responses.find({"survey_id": sid}))
    observed(request, statuses=[201, 201], responses=len(rows), distinct_response_ids=len(set(ids)), distinct_users=len({r["respondent_id"] for r in rows}))
    assert len(set(ids)) == 2 and len(rows) == 2
    assert len({r["respondent_id"] for r in rows}) == 2


@case("统计结果", "创建四类选答题并发布，允许多次；先读空统计；提交完整答卷和全空答卷；逐题与整卷比较；再提交并检查统计更新。",
      "完整答案 single=a、multiple=[a,b]、text=反馈、number=10；第二份为空；第三份数字30。",
      "总答卷数0→2→3；四类单题结果与整卷一致；未选c=0；空答案不计有效回答；数字均值10→20。")
def test_all_question_stats_zero_optional_and_refresh(client, owner, request):
    kinds = ["single", "multiple", "text", "number"]
    sid, qs = survey_with_questions(client, owner, [question_input(k, required=False) for k in kinds], allow_multiple=True, anonymous=True)
    base = f"/api/surveys/{sid}"
    empty = client.get(base + "/stats", headers=owner).json()
    assert empty["total_responses"] == 0
    assert all(q["answer_count"] == 0 for q in empty["questions"])
    for q in empty["questions"][:2]:
        assert [o["count"] for o in q["options"]] == [0, 0, 0]
    assert empty["questions"][2]["values"] == []
    assert empty["questions"][3]["average"] is None
    answers = {q["id"]: value for q, value in zip(qs, ["a", ["a", "b"], "反馈", 10])}
    for values in (answers, {}):
        assert client.post(f"/api/fill/{sid}/submit", headers=owner, json={"answers": values}).status_code == 201
    stats = client.get(base + "/stats", headers=owner).json()
    assert stats["total_responses"] == 2
    assert [q["answer_count"] for q in stats["questions"]] == [1, 1, 1, 1]
    assert [o["count"] for o in stats["questions"][0]["options"]] == [1, 0, 0]
    assert [o["count"] for o in stats["questions"][1]["options"]] == [1, 1, 0]
    assert stats["questions"][2]["values"] == ["反馈"]
    assert stats["questions"][3]["values"] == [10] and stats["questions"][3]["average"] == 10
    for q in stats["questions"]:
        response = client.get(base + "/stats/" + q["question_id"], headers=owner)
        assert response.status_code == 200
        single = response.json()
        assert {k: v for k, v in single.items() if k not in ("survey_id", "total_responses")} == q
        assert single["total_responses"] == 2
    number_id = qs[-1]["id"]
    assert client.post(f"/api/fill/{sid}/submit", headers=owner, json={"answers": {number_id: 30}}).status_code == 201
    refreshed = client.get(base + "/stats/" + number_id, headers=owner).json()
    observed(request, first_total=stats["total_responses"], answer_counts=[q["answer_count"] for q in stats["questions"]], single_question_types_checked=kinds, refreshed=refreshed)
    assert refreshed["total_responses"] == 3 and refreshed["answer_count"] == 2 and refreshed["average"] == 20


@case("统计结果", "同一创建者建立两份问卷并各提交；查询整卷、其他问卷题ID、不存在题ID。",
      "问卷A答案10，问卷B答案1000。",
      "各自总数1、均值10和1000；A的单题接口使用B的题ID或未知ID返回404。")
def test_stats_isolate_surveys_and_reject_foreign_questions(client, owner, request):
    surveys = []
    for value in (10, 1000):
        sid, qs = survey_with_questions(client, owner, [question_input("number")])
        assert client.post(f"/api/fill/{sid}/submit", headers=owner, json={"answers": {qs[0]["id"]: value}}).status_code == 201
        surveys.append((sid, qs[0]["id"]))
    for (sid, _), expected in zip(surveys, (10, 1000)):
        stats = client.get(f"/api/surveys/{sid}/stats", headers=owner).json()
        assert stats["total_responses"] == 1 and stats["questions"][0]["average"] == expected
    first, second = surveys
    statuses = [client.get(f"/api/surveys/{first[0]}/stats/{qid}", headers=owner).status_code for qid in (second[1], "missing")]
    observed(request, survey_averages=[10, 1000], invalid_question_statuses=statuses)
    assert statuses == [404, 404]
