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
            raise ValueError("选项 ID 重复")
        if self.type in ("single", "multiple") and len(ids) < 2:
            raise ValueError("选择题至少两个选项")
        if self.type not in ("single", "multiple") and ids:
            raise ValueError("填空题不能有选项")
        if self.type == "multiple":
            maximum = self.max_choices if self.max_choices is not None else len(ids)
            if maximum > len(ids) or self.min_choices > maximum:
                raise ValueError("选择数量上下限不合法")
        if self.min_length > self.max_length:
            raise ValueError("文本长度上下限不合法")
        if self.min_value is not None and self.max_value is not None and self.min_value > self.max_value:
            raise ValueError("数字上下限不合法")
        return self

def validate_answer(q, value):
    def fail(message):
        raise HTTPException(422, {"question_id":q["id"], "message":message})
    missing = value is None or value == "" or value == []
    if missing:
        if q["required"]:
            fail("此题必答")
        return None
    kind = q["type"]
    options = {o["id"] for o in q["options"]}
    if kind == "single":
        if not isinstance(value, str) or value not in options:
            fail("请选择合法选项")
    elif kind == "multiple":
        if not isinstance(value, list) or any(not isinstance(v,str) for v in value):
            fail("多选答案必须是选项 ID 数组")
        if len(set(value)) != len(value) or not set(value) <= options:
            fail("选项重复或不存在")
        maximum = q["max_choices"] if q["max_choices"] is not None else len(options)
        if not q["min_choices"] <= len(value) <= maximum:
            fail("选择数量不符合限制")
    elif kind == "text":
        if not isinstance(value,str) or not value.strip() or not q["min_length"] <= len(value) <= q["max_length"]:
            fail("文本长度不符合限制或仅包含空白")
    else:
        if type(value) not in (int,float) or not math.isfinite(value):
            fail("请输入有限数字")
        if q["integer"] and value != int(value):
            fail("必须为整数")
        if q["min_value"] is not None and value < q["min_value"]:
            fail("数字小于最小值")
        if q["max_value"] is not None and value > q["max_value"]:
            fail("数字大于最大值")
    return value

@router.post("/{sid}/questions", status_code=201)
def add(sid: str, data: QuestionInput, database=Depends(db), user=Depends(current_user)):
    s = owned(database,sid,user)
    draft(s)
    if len(s["questions"]) >= 100:
        raise HTTPException(422,"最多100题")
    q = {"id":str(uuid4()), **data.model_dump(), "rules":[]}
    return update_draft(database,s,{"questions":[*s["questions"], q]})

@router.put("/{sid}/questions/{qid}")
def edit(sid: str, qid: str, data: QuestionInput, database=Depends(db), user=Depends(current_user)):
    s = owned(database,sid,user)
    draft(s)
    old = next((q for q in s["questions"] if q["id"] == qid), None)
    if old is None:
        raise HTTPException(404,"题目不存在")
    questions = [{"id":qid, **data.model_dump(), "rules":old["rules"]} if q["id"] == qid else q for q in s["questions"]]
    from .logic import validate_rules
    validate_rules(questions)
    return update_draft(database,s,{"questions":questions})
