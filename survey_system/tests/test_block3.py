from tests.test_block2 import login

def test_management(client):
    a, b = login(client), login(client,"bobby")
    s = client.post("/api/surveys", headers=a, json={"title":"课堂调查"})
    assert s.status_code == 201
    sid = s.json()["id"]
    url = "/api/surveys/" + sid
    assert s.json()["share_url"] == "/survey/" + sid
    assert client.get(url,headers=b).status_code == 404
    assert client.get("/api/surveys",headers=b).json() == []
    assert client.put(url,headers=a,json={"title":"修改标题"}).json()["title"] == "修改标题"
    assert client.post(url+"/publish",headers=a).status_code == 422
    client.app.state.db.surveys.update_one({"_id":sid},{"$set":{"questions":[{"id":"q1"}]}})
    assert client.post(url+"/publish",headers=a).json()["status"] == "published"
    assert client.put(url,headers=a,json={"title":"不能改"}).status_code == 409
    assert client.post(url+"/close",headers=b).status_code == 404
    assert client.post(url+"/close",headers=a).json()["status"] == "closed"

def test_deadline(client):
    h=login(client)
    assert client.post("/api/surveys",headers=h,json={"title":"t","deadline":"2020-01-01T12:00:00"}).status_code == 422
    s=client.post("/api/surveys",headers=h,json={"title":"t","deadline":"2020-01-01T12:00:00Z"}).json()
    client.app.state.db.surveys.update_one({"_id":s["id"]},{"$set":{"questions":[{"id":"q"}]}})
    assert client.post("/api/surveys/"+s["id"]+"/publish",headers=h).status_code == 422
