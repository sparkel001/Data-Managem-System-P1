from tests.test_block2 import login

def test_statistics(client):
    h=login(client)
    sid=client.post("/api/surveys",headers=h,json={"title":"统计","allow_multiple":True,"anonymous":True}).json()["id"]
    base="/api/surveys/"+sid
    opts=[{"id":"a","label":"A"},{"id":"b","label":"B"}]
    for kind in ("single","multiple","text","number"):
        body={"title":kind,"type":kind}
        if kind in ("single","multiple"): body["options"]=opts
        client.post(base+"/questions",headers=h,json=body)
    qs=client.get(base,headers=h).json()["questions"]
    client.post(base+"/publish",headers=h)
    empty=client.get(base+"/stats",headers=h).json()
    assert empty["total_responses"] == 0 and empty["questions"][3]["average"] is None
    for values in (["a",["a","b"],"甲",10],["b",["b"],"乙",20]):
        answers={q["id"]:v for q,v in zip(qs,values)}
        assert client.post("/api/fill/"+sid+"/submit",headers=h,json={"answers":answers}).status_code == 201
    stats=client.get(base+"/stats",headers=h).json()
    assert stats["total_responses"] == 2
    assert [o["count"] for o in stats["questions"][0]["options"]] == [1,1]
    assert [o["count"] for o in stats["questions"][1]["options"]] == [1,2]
    assert stats["questions"][2]["values"] == ["甲","乙"]
    assert stats["questions"][3]["average"] == 15
    single=client.get(base+"/stats/"+qs[3]["id"],headers=h).json()
    assert single["average"] == 15 and single["answer_count"] == 2
    other=login(client,"other")
    assert client.get(base+"/stats",headers=other).status_code == 404
    assert client.get(base+"/stats/"+qs[3]["id"],headers=other).status_code == 404
