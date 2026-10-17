from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta
import pytest
from tests.test_block2 import login
from tests.test_block6 import setup_survey
from app.auth import now
from app.questions import QuestionInput
from app.logic import walk
from fastapi import HTTPException
from tests.test_block4 import question


def test_concurrent_submit(client):
    h,sid,qid=setup_survey(client)
    def submit(_):
        return client.post("/api/fill/"+sid+"/submit",headers=h,json={"answers":{qid:30}}).status_code
    with ThreadPoolExecutor(max_workers=4) as pool:
        statuses=list(pool.map(submit,range(4)))
    assert sorted(statuses) == [201,409,409,409]
    assert client.app.state.db.responses.count_documents({"survey_id":sid}) == 1


def test_expired(client):
    h,sid,qid=setup_survey(client)
    client.app.state.db.surveys.update_one({"_id":sid},{"$set":{"deadline":now()-timedelta(seconds=1)}})
    assert client.get("/api/fill/"+sid,headers=h).status_code == 410
    assert client.post("/api/fill/"+sid+"/submit",headers=h,json={"answers":{qid:10}}).status_code == 410
    assert client.app.state.db.responses.count_documents({}) == 0


def test_full_jump_workflow(client):
    owner=login(client)
    filler=login(client,"student")
    sid=client.post("/api/surveys",headers=owner,json={"title":"分支问卷","anonymous":True}).json()["id"]
    base="/api/surveys/"+sid
    for title,kind in [("年龄","number"),("职业","text"),("反馈","text")]:
        client.post(base+"/questions",headers=owner,json={"title":title,"type":kind})
    qs=client.get(base,headers=owner).json()["questions"]
    a,b,c=[q["id"] for q in qs]
    rule={"rules":[{"op":"lt","value":18,"target":c}]}
    assert client.put(base+"/questions/"+a+"/rules",headers=owner,json=rule).status_code == 200
    assert client.post(base+"/publish",headers=owner).status_code == 200
    assert client.put(base+"/questions/"+a+"/rules",headers=owner,json=rule).status_code == 409
    assert client.post("/api/fill/"+sid+"/next",headers=filler,json={"answers":{a:16}}).json()["next_question_id"] == c
    assert client.post("/api/fill/"+sid+"/submit",headers=filler,json={"answers":{a:16,c:"很好"}}).status_code == 201
    saved=client.app.state.db.responses.find_one({"survey_id":sid})
    assert saved["answers"] == {a:16,c:"很好"} and saved["path"] == [a,c]
    stats=client.get(base+"/stats",headers=owner).json()
    assert stats["questions"][1]["answer_count"] == 0
    assert stats["questions"][2]["values"] == ["很好"]


def test_edit_invalidates_rule(client):
    h=login(client)
    sid=client.post("/api/surveys",headers=h,json={"title":"规则验证"}).json()["id"]
    base="/api/surveys/"+sid
    qid=client.post(base+"/questions",headers=h,json={"title":"年龄","type":"number"}).json()["questions"][0]["id"]
    client.put(base+"/questions/"+qid+"/rules",headers=h,json={"rules":[{"op":"gt","value":10,"target":"END"}]})
    assert client.put(base+"/questions/"+qid,headers=h,json={"title":"文本","type":"text"}).status_code == 422
    assert client.get(base,headers=h).json()["questions"][0]["type"] == "number"

@pytest.mark.parametrize("kwargs",[
    {"min_length":3,"max_length":2},
    {"type":"number","min_value":10,"max_value":1},
    {"type":"single","options":[{"id":"a","label":"A"},{"id":"a","label":"B"}]},
    {"type":"multiple","options":[{"id":"a","label":"A"},{"id":"b","label":"B"}],"min_choices":3},
])
def test_schema_rejects(kwargs):
    with pytest.raises(ValueError): QuestionInput(**{"title":"t","type":"text",**kwargs})

def test_missing_unknown_and_priority():
    q=question("number")
    q["rules"]=[{"op":"gt","value":0,"target":"END"},{"op":"gt","value":0,"target":"later"}]
    qs=[q,{**question(),"id":"later"}]
    assert walk(qs,{"q":1})["path"] == ["q"]
    with pytest.raises(HTTPException): walk(qs,{"unknown":1})
    with pytest.raises(HTTPException): walk(qs,{"q":0})


def test_real_name_details(client):
    h,sid,qid=setup_survey(client,anonymous=False)
    f=login(client,"filler")
    client.post("/api/fill/"+sid+"/submit",headers=f,json={"answers":{qid:22}})
    row=client.get("/api/surveys/"+sid+"/responses",headers=h).json()[0]
    assert row["respondent"]["username"] == "filler"
