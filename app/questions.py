import math
from typing import Literal, Any
from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict, Field, model_validator
from .auth import db, current_user, owned
from .surveys import draft, update_draft

router = APIRouter(prefix="/api/surveys")
class Option(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str = Field(pattern=r"^[a-zA-Z0-9_-]{1,64}$")
    label: str = Field(min_length=1, max_length=200)

class QuestionInput(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)
    title: str = Field(min_length=1, max_length=500)
    type: Literal["single", "multiple", "text", "number"]
    required: bool = True
    options: list[Option] = Field(default_factory=list, max_length=100)
    min_choices: int = Field(default=0, ge=0)
    max_choices: int | None = Field(default=None, ge=0)
    min_length: int = Field(default=0, ge=0, le=10000)
    max_length: int = Field(default=1000, ge=0, le=10000)
    min_value: float | None = None
    max_value: float | None = None
    integer: bool = False
    @model_validator(mode="after")
    def coherent(self):
        if not self.title.strip():
            raise ValueError("题目标题不能为空")
        ids = [o.id for o in self.options]
        if len(set(ids)) != len(ids):
            raise ValueError("选项编号不能重复，请为每个选项设置不同的编号。")
        if self.type in ("single", "multiple") and len(ids) < 2:
            raise ValueError("选择题至少需要两个选项。")
        if self.type not in ("single", "multiple") and ids:
            raise ValueError("填空题无需选项，请清空选项后保存。")
        if self.type == "multiple":
            maximum = self.max_choices if self.max_choices is not None else len(ids)
            if maximum > len(ids) or self.min_choices > maximum:
                raise ValueError("最少选择数量不能超过最多选择数量，最多数量不能超过选项总数。")
        if self.min_length > self.max_length:
            raise ValueError("最短文本长度不能超过最长文本长度。")
        if self.min_value is not None and self.max_value is not None and self.min_value > self.max_value:
            raise ValueError("数字下限不能超过数字上限。")
        return self

def validate_answer(q, value):
    def fail(message):
        raise HTTPException(422, {"question_id":q["id"], "message":message})
    missing = value is None or value == "" or value == []
    if missing:
        if q["required"]:
            fail("请先回答这道必答题。")
        return None
    kind = q["type"]
    options = {o["id"] for o in q["options"]}
    if kind == "single":
        if not isinstance(value, str) or value not in options:
            fail("请从本题提供的选项中选择。")
    elif kind == "multiple":
        if not isinstance(value, list) or any(not isinstance(v,str) for v in value):
            fail("请勾选本题提供的选项。")
        if len(set(value)) != len(value) or not set(value) <= options:
            fail("所选选项重复或已不存在，请重新选择。")
        maximum = q["max_choices"] if q["max_choices"] is not None else len(options)
        if not q["min_choices"] <= len(value) <= maximum:
            fail("所选数量不符合本题要求，请查看最少和最多选择数量。")
    elif kind == "text":
        if not isinstance(value,str) or not value.strip() or not q["min_length"] <= len(value) <= q["max_length"]:
            fail("请填写实际内容，并将文字长度控制在本题要求的范围内。")
    else:
        if type(value) not in (int,float) or not math.isfinite(value):
            fail("请输入有效的数字。")
        if q["integer"] and value != int(value):
            fail("请输入整数，不要包含小数。")
        if q["min_value"] is not None and value < q["min_value"]:
            fail("输入的数字不能低于最小值。")
        if q["max_value"] is not None and value > q["max_value"]:
            fail("输入的数字不能超过最大值。")
    return value

@router.post("/{sid}/questions", status_code=201)
def add(sid: str, data: QuestionInput, database=Depends(db), user=Depends(current_user)):
    s = owned(database,sid,user)
    draft(s)
    if len(s["questions"]) >= 100:
        raise HTTPException(422,"每份问卷最多可添加100道题。")
    q = {"id":str(uuid4()), **data.model_dump(), "rules":[]}
    return update_draft(database,s,{"questions":[*s["questions"], q]})

@router.put("/{sid}/questions/{qid}")
def edit(sid: str, qid: str, data: QuestionInput, database=Depends(db), user=Depends(current_user)):
    s = owned(database,sid,user)
    draft(s)
    old = next((q for q in s["questions"] if q["id"] == qid), None)
    if old is None:
        raise HTTPException(404,"没有找到这道题，请刷新后重新选择。")
    if old.get("source"):
        raise HTTPException(409,"请先在题库中保存新版本，再点击“更换题库版本”更新草稿中的题目。")
    questions = [{"id":qid, **data.model_dump(), "rules":old["rules"]} if q["id"] == qid else q for q in s["questions"]]
    from .logic import validate_rules
    validate_rules(questions)
    return update_draft(database,s,{"questions":questions})
