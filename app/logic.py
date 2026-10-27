import math
from typing import Any, Literal
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict, Field
from .auth import db, current_user, owned
from .surveys import draft, update_draft
from .questions import validate_answer

router = APIRouter(prefix="/api/surveys")
class Rule(BaseModel):
    model_config = ConfigDict(extra="forbid")
    op: Literal["eq", "contains_any", "contains_all", "gt", "gte", "lt", "lte"]
    value: Any
    target: str
class RulesInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    rules: list[Rule] = Field(max_length=50)

def validate_rules(questions):
    positions = {q["id"]:i for i,q in enumerate(questions)}
    if len(positions) != len(questions):
        raise HTTPException(422,"问卷中存在重复的题目，请联系创建者检查。")
    for i,q in enumerate(questions):
        for rule in q.get("rules",[]):
            target, op, value = rule["target"], rule["op"], rule["value"]
            if target != "END" and (target not in positions or positions[target] <= i):
                raise HTTPException(422,"请选择后面的题目或结束问卷作为跳转目标，不能跳回前面的题目。")
            options = {o["id"] for o in q["options"]}
            valid = False
            if q["type"] == "single":
                valid = op == "eq" and isinstance(value,str) and value in options
            elif q["type"] == "multiple":
                valid = op in ("contains_any","contains_all") and isinstance(value,list) and bool(value) and all(isinstance(v,str) and v in options for v in value)
            elif q["type"] == "number":
                valid = op in ("eq","gt","gte","lt","lte") and type(value) in (int,float) and math.isfinite(value)
            if not valid:
                raise HTTPException(422,"跳转条件不适用于这道题，请检查题型、条件值和选项。")

def matches(rule, value):
    if value is None:
        return False
    op, expected = rule["op"], rule["value"]
    if op == "eq": return value == expected
    if op == "contains_any": return bool(set(value) & set(expected))
    if op == "contains_all": return set(expected) <= set(value)
    if op == "gt": return value > expected
    if op == "gte": return value >= expected
    if op == "lt": return value < expected
    if op == "lte": return value <= expected
    return False

def next_id(questions, index, value):
    for rule in questions[index].get("rules",[]):
        if matches(rule,value):
            return rule["target"]
    return questions[index+1]["id"] if index+1 < len(questions) else "END"

def walk(questions, answers, partial=False):
    positions = {q["id"]:i for i,q in enumerate(questions)}
    if set(answers) - positions.keys():
        raise HTTPException(422,"填写内容包含已不存在的题目，请刷新问卷后重新填写。")
    current = questions[0]["id"] if questions else "END"
    visited, cleaned = [], {}
    while current != "END":
        if current in visited or current not in positions:
            raise HTTPException(422,"问卷的跳转设置有误，请联系创建者检查。")
        if partial and current not in answers:
            break
        visited.append(current)
        q = questions[positions[current]]
        value = validate_answer(q, answers.get(current))
        if value is not None:
            cleaned[current] = value
        current = next_id(questions,positions[current],value)
    if set(answers) - set(visited):
        raise HTTPException(422,"请只填写本次作答过程中显示的题目。")
    return {"path":visited,"answers":cleaned,"next_question_id":current}

@router.put("/{sid}/questions/{qid}/rules")
def configure(sid: str, qid: str, data: RulesInput, database=Depends(db), user=Depends(current_user)):
    s = owned(database,sid,user)
    draft(s)
    if not any(q["id"] == qid for q in s["questions"]):
        raise HTTPException(404,"没有找到这道题，请刷新后重新选择。")
    questions = [{**q,"rules":[r.model_dump() for r in data.rules]} if q["id"] == qid else q for q in s["questions"]]
    validate_rules(questions)
    return update_draft(database,s,{"questions":questions})
