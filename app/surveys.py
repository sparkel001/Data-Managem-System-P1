from datetime import datetime
from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field, ConfigDict, field_validator
from .auth import db, current_user, owned, now

router = APIRouter(prefix="/api/surveys")
class SurveyInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=3000)
    anonymous: bool = False
    allow_multiple: bool = False
    deadline: datetime | None = None
    @field_validator("title")
    @classmethod
    def title_valid(cls, v):
        if not v.strip():
            raise ValueError("标题不能为空")
        return v.strip()
    @field_validator("deadline")
    @classmethod
    def timezone_required(cls, v):
        if v and v.tzinfo is None:
            raise ValueError("请选择有效的截止日期和时间。")
        return v

def public(s):
    return {**{k:v for k,v in s.items() if k != "_id"}, "id":s["_id"], "share_url":"/survey/" + s["_id"]}

def draft(s):
    if s["status"] != "draft":
        raise HTTPException(409, "只有草稿问卷可以编辑，发布后的题目和跳转规则不能修改。")

@router.post("", status_code=201)
def create(data: SurveyInput, database=Depends(db), user=Depends(current_user)):
    s = {"_id": str(uuid4()), **data.model_dump(), "owner_id": user["_id"], "status":"draft", "questions":[], "created_at":now(), "revision":0, "schema_version":1}
    database.surveys.insert_one(s)
    return public(s)

@router.get("")
def listing(database=Depends(db), user=Depends(current_user)):
    return [public(s) for s in database.surveys.find({"owner_id":user["_id"]}).sort("created_at", -1)]

@router.get("/{sid}")
def detail(sid: str, database=Depends(db), user=Depends(current_user)):
    return public(owned(database, sid, user))

def update_draft(database, s, changes):
    result = database.surveys.update_one({"_id":s["_id"], "status":"draft", "revision":s["revision"]}, {"$set":changes, "$inc":{"revision":1}})
    if result.modified_count != 1:
        raise HTTPException(409, "问卷已被更新，请刷新后再保存。")
    return public(database.surveys.find_one({"_id":s["_id"]}))

@router.put("/{sid}")
def edit(sid: str, data: SurveyInput, database=Depends(db), user=Depends(current_user)):
    s = owned(database, sid, user)
    draft(s)
    return update_draft(database, s, data.model_dump())

@router.post("/{sid}/publish")
def publish(sid: str, database=Depends(db), user=Depends(current_user)):
    s = owned(database, sid, user)
    draft(s)
    if not s["questions"]:
        raise HTTPException(422, "请至少添加一道题")
    if s["deadline"] and s["deadline"] <= now():
        raise HTTPException(422, "截止时间必须晚于现在")
    from .logic import validate_rules
    validate_rules(s["questions"])
    return update_draft(database, s, {"status":"published"})

@router.post("/{sid}/close")
def close(sid: str, database=Depends(db), user=Depends(current_user)):
    s = owned(database, sid, user)
    if s["status"] != "published":
        raise HTTPException(409, "只有正在收集答卷的已发布问卷可以关闭。")
    database.surveys.update_one({"_id":sid, "status":"published"}, {"$set":{"status":"closed"}})
    return public(database.surveys.find_one({"_id":sid}))
