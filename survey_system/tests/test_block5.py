import pytest
from fastapi import HTTPException
from app.logic import validate_rules, walk
from tests.test_block4 import question
from tests.test_block2 import login

@pytest.mark.parametrize("kind,op,value,answer",[
    ("single","eq","a","a"),
    ("multiple","contains_any",["a"],["a","b"]),
    ("multiple","contains_all",["a","b"],["a","b"]),
    ("number","gte",18,20),
])
def test_jump(kind,op,value,answer):
    opts={"options":[{"id":"a","label":"A"},{"id":"b","label":"B"}]} if kind != "number" else {}
    q=question(kind,**opts)
    q["rules"]=[{"op":op,"value":value,"target":"END"}]
    qs=[q,{**question(),"id":"skip"}]
    validate_rules(qs)
    assert walk(qs,{"q":answer})["path"] == ["q"]
    with pytest.raises(HTTPException): walk(qs,{"q":answer,"skip":"非法额外答案"})

@pytest.mark.parametrize("target",["q","missing"])
def test_bad_target(target):
    q=question("number")
    q["rules"]=[{"op":"gt","value":0,"target":target}]
    with pytest.raises(HTTPException): validate_rules([q])

def test_rule_persistence(client):
    h=login(client)
    sid=client.post("/api/surveys",headers=h,json={"title":"规则"}).json()["id"]
    url="/api/surveys/"+sid
    qid=client.post(url+"/questions",headers=h,json={"title":"年龄","type":"number"}).json()["questions"][0]["id"]
    rules=[{"op":"lt","value":18,"target":"END"}]
    assert client.put(url+"/questions/"+qid+"/rules",headers=h,json={"rules":rules}).status_code == 200
    assert client.app.state.db.surveys.find_one({"_id":sid})["questions"][0]["rules"] == rules
