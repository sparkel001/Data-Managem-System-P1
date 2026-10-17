import pytest
from tests.test_block2 import login

def setup_survey(client, **settings):
    h=login(client)
    sid=client.post("/api/surveys",headers=h,json={"title":"演示",**settings}).json()["id"]
    url="/api/surveys/"+sid
    s=client.post(url+"/questions",headers=h,json={"title":"年龄","type":"number","integer":True,"min_value":0,"max_value":120}).json()
    qid=s["questions"][0]["id"]
    assert client.post(url+"/publish",headers=h).status_code == 200
    return h,sid,qid

def test_submit(client):
    h,sid,qid=setup_survey(client,anonymous=True)
    f=login(client,"filler")
    url="/api/fill/"+sid
    assert client.get(url).status_code == 401
    assert client.get(url,headers=f).status_code == 200
    assert client.post(url+"/next",headers=f,json={"answers":{}}).json()["next_question_id"] == qid
    assert client.post(url+"/submit",headers=f,json={"answers":{qid:200}}).status_code == 422
    assert client.post(url+"/submit",headers=f,json={"answers":{qid:20}}).status_code == 201
    assert client.post(url+"/submit",headers=f,json={"answers":{qid:21}}).status_code == 409
    rows=client.get("/api/surveys/"+sid+"/responses",headers=h).json()
    assert len(rows) == 1 and "respondent" not in rows[0] and "respondent_id" not in rows[0]
    assert "once_key" not in rows[0]
    assert client.get("/api/surveys/"+sid+"/responses",headers=f).status_code == 404

@pytest.mark.parametrize("multiple,expected",[(True,201),(False,409)])
def test_repeated(client,multiple,expected):
    h,sid,qid=setup_survey(client,allow_multiple=multiple)
    url="/api/fill/"+sid+"/submit"
    assert client.post(url,headers=h,json={"answers":{qid:10}}).status_code == 201
    assert client.post(url,headers=h,json={"answers":{qid:20}}).status_code == expected
    client.post("/api/surveys/"+sid+"/close",headers=h)
    assert client.post(url,headers=h,json={"answers":{qid:30}}).status_code == 404

def test_page(client):
    assert client.get("/").status_code == 200
    assert client.get("/survey/example").status_code == 200
    assert client.get("/static/app.js").status_code == 200
