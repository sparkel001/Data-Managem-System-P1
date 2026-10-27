import pytest
from fastapi import HTTPException
from app.questions import QuestionInput, validate_answer
from tests.test_block2 import login

def question(kind="text", **kw):
    return {"id":"q", **QuestionInput(title="问题",type=kind,**kw).model_dump(), "rules":[]}

def test_add_edit(client):
    h=login(client)
    s=client.post("/api/surveys",headers=h,json={"title":"问卷"}).json()
    url="/api/surveys/"+s["id"]+"/questions"
    q=client.post(url,headers=h,json={"title":"姓名","type":"text"})
    assert q.status_code == 201
    qid=q.json()["questions"][0]["id"]
    changed=client.put(url+"/"+qid,headers=h,json={"title":"年龄","type":"number","integer":True})
    assert changed.json()["questions"][0]["id"] == qid
    assert client.post(url,headers=h,json={"title":"错误","type":"single"}).status_code == 422

@pytest.mark.parametrize("q,value",[
    (question(),None), (question(min_length=2),"a"), (question(max_length=2),"abc"),
    (question(),"  "), (question("number",integer=True),1.5),
    (question("number",min_value=0),-1), (question("number",max_value=120),121),
    (question("number"),True), (question("number"),"12"),
    (question("single",options=[{"id":"a","label":"A"},{"id":"b","label":"B"}]),"c"),
    (question("multiple",options=[{"id":"a","label":"A"},{"id":"b","label":"B"}],min_choices=2),["a"]),
    (question("multiple",options=[{"id":"a","label":"A"},{"id":"b","label":"B"}]),["a","a"]),
])
def test_invalid(q,value):
    with pytest.raises(HTTPException): validate_answer(q,value)

def test_valid():
    assert validate_answer(question(required=False),None) is None
    assert validate_answer(question("number",integer=True,min_value=0,max_value=120),120) == 120
    assert validate_answer(question(min_length=2,max_length=2),"中文") == "中文"
