from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException
from .auth import db, current_user, owned
from .banks import Strict, family_access, version_get
from .surveys import draft, update_draft
from .logic import validate_rules

router = APIRouter(prefix='/api/surveys')


class ReuseInput(Strict):
    question_id: str
    version_id: str


def snapshot(version, instance_id, rules):
    return {**version['content'], 'id': instance_id, 'rules': rules,
            'source': {'question_id': version['question_id'], 'version_id': version['_id'],
                       'content_hash': version['content_hash']}}


@router.post('/{sid}/library-questions', status_code=201)
def import_question(sid: str, data: ReuseInput, database=Depends(db), user=Depends(current_user)):
    survey = owned(database, sid, user)
    draft(survey)
    if len(survey['questions']) >= 100: raise HTTPException(422, '每份问卷最多可添加100道题。')
    family_access(database, data.question_id, user)
    version = version_get(database, data.question_id, data.version_id)
    questions = [*survey['questions'], snapshot(version, str(uuid4()), [])]
    validate_rules(questions)
    return update_draft(database, survey, {'questions': questions})


@router.put('/{sid}/questions/{instance_id}/version')
def replace_version(sid: str, instance_id: str, data: ReuseInput, database=Depends(db), user=Depends(current_user)):
    survey = owned(database, sid, user)
    draft(survey)
    old = next((q for q in survey['questions'] if q['id'] == instance_id), None)
    if old is None: raise HTTPException(404, '没有找到这道题，请刷新后重新选择。')
    if old.get('source', {}).get('question_id') != data.question_id:
        raise HTTPException(422, '只能选择这道题自己的历史版本，不能替换为另一道题。')
    family_access(database, data.question_id, user)
    version = version_get(database, data.question_id, data.version_id)
    questions = [snapshot(version, instance_id, q['rules']) if q['id'] == instance_id else q
                 for q in survey['questions']]
    validate_rules(questions)
    return update_draft(database, survey, {'questions': questions})
