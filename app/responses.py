from uuid import uuid4
from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict, Field
from pymongo.errors import DuplicateKeyError
from .auth import db, current_user, now, owned
from .logic import walk

router = APIRouter(prefix="/api")
class Answers(BaseModel):
    model_config = ConfigDict(extra="forbid")
    answers: dict[str, Any] = Field(default_factory=dict, max_length=100)

def available(database,sid):
    s = database.surveys.find_one({"_id":sid})
    if not s or s["status"] != "published":
        raise HTTPException(404,"这份问卷尚未开放填写或已经关闭。")
    if s["deadline"] and s["deadline"] <= now():
        raise HTTPException(410,"这份问卷已超过截止时间，不能继续提交。")
    return s

@router.get("/fill/{sid}")
def form(sid: str, database=Depends(db), user=Depends(current_user)):
    s = available(database,sid)
    return {"id":sid, **{k:s[k] for k in ("title","description","anonymous","allow_multiple","deadline","questions")}}

@router.post("/fill/{sid}/next")
def next_question(sid: str, data: Answers, database=Depends(db), user=Depends(current_user)):
    s = available(database,sid)
    return walk(s["questions"], data.answers, partial=True)

@router.post("/fill/{sid}/submit", status_code=201)
def submit(sid: str, data: Answers, database=Depends(db), user=Depends(current_user)):
    s = available(database,sid)
    result = walk(s["questions"],data.answers)
    rid = str(uuid4())
    response = {"_id":rid,"survey_id":sid,"respondent_id":user["_id"],"answers":result["answers"],"path":result["path"],"created_at":now(),"schema_version":1}
    if not s["allow_multiple"]:
        response["once_key"] = sid + ":" + user["_id"]
    try:
        database.responses.insert_one(response)
    except DuplicateKeyError:
        raise HTTPException(409,"您已提交过这份问卷，每个账号只能提交一次。")
    return {"id":rid,"message":"提交成功"}

@router.get("/surveys/{sid}/responses")
def responses(sid: str, database=Depends(db), user=Depends(current_user)):
    s = owned(database,sid,user)
    result = []
    for r in database.responses.find({"survey_id":sid}).sort("created_at",1):
        item = {"id":r["_id"],"survey_id":sid,"answers":r["answers"],"path":r["path"],"created_at":r["created_at"]}
        if not s["anonymous"]:
            respondent = database.users.find_one({"_id":r["respondent_id"]})
            item["respondent"] = {"id":r["respondent_id"],"username":respondent["username"] if respondent else "已删除用户"}
        result.append(item)
    return result
