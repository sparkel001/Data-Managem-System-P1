from fastapi import APIRouter, Depends, HTTPException
from .auth import db, current_user, owned

router = APIRouter(prefix="/api/surveys")
def summarize(q, rows):
    values = [r["answers"][q["id"]] for r in rows if q["id"] in r["answers"]]
    item = {"question_id":q["id"],"title":q["title"],"type":q["type"],"answer_count":len(values)}
    if q["type"] in ("single","multiple"):
        item["options"] = [{**o,"count":sum(v == o["id"] if q["type"] == "single" else o["id"] in v for v in values)} for o in q["options"]]
    else:
        item["values"] = values
        if q["type"] == "number":
            item["average"] = sum(v / len(values) for v in values) if values else None
    return item

@router.get("/{sid}/stats")
def stats(sid: str, database=Depends(db), user=Depends(current_user)):
    s = owned(database,sid,user)
    rows = list(database.responses.find({"survey_id":sid},{"answers":1}))
    return {"survey_id":sid,"total_responses":len(rows),"questions":[summarize(q,rows) for q in s["questions"]]}

@router.get("/{sid}/stats/{qid}")
def question_stats(sid: str, qid: str, database=Depends(db), user=Depends(current_user)):
    s = owned(database,sid,user)
    q = next((q for q in s["questions"] if q["id"] == qid),None)
    if q is None:
        raise HTTPException(404,"没有找到这道题，请刷新后重新选择。")
    rows = list(database.responses.find({"survey_id":sid},{"answers":1}))
    return {"survey_id":sid,"total_responses":len(rows),**summarize(q,rows)}
