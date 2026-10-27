"""Question libraries. Survey ownership remains independent from library access."""
import hashlib
import json
from uuid import uuid4, uuid5, NAMESPACE_URL
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict, Field, field_validator
from pymongo.errors import DuplicateKeyError
from .auth import db, current_user, now, owned
from .questions import QuestionInput

router = APIRouter(prefix='/api')


class Strict(BaseModel):
    model_config = ConfigDict(extra='forbid')


class BankInput(Strict):
    name: str = Field(min_length=1, max_length=200)
    description: str = Field(default='', max_length=3000)

    @field_validator('name')
    @classmethod
    def nonblank(cls, value):
        if not value.strip(): raise ValueError('题库名称不能为空')
        return value.strip()


class SaveQuestion(Strict):
    content: QuestionInput
    request_key: str = Field(min_length=1, max_length=100)


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                     separators=(',', ':'), allow_nan=False).encode()).hexdigest()


def public(document):
    return {('id' if k == '_id' else k): v for k, v in document.items()
            if k not in ('request_hash', 'request_key')}


def bank_owned(database, bid, user):
    bank = database.question_banks.find_one({'_id': bid, 'owner_id': user['_id']})
    if bank is None: raise HTTPException(404, '题库不存在，或您没有管理权限。')
    return bank


def family_access(database, qid, user, *, write=False):
    query = {'_id': qid}
    if write: query['owner_id'] = user['_id']
    else: query['$or'] = [{'owner_id': user['_id']}, {'shared_with': user['_id']}]
    family = database.bank_questions.find_one(query)
    if family is None: raise HTTPException(404, '题目不存在，或您没有查看权限。')
    return family


def version_get(database, qid, vid):
    version = database.question_versions.find_one({'_id': vid, 'question_id': qid})
    if version is None: raise HTTPException(404, '没有找到所选版本，请刷新后重新选择。')
    return version


def append_version(database, qid, content, request_key, parent=None, restored=None):
    """Insert-only versions; unique request and sequence indexes arbitrate races.

    No mutable default pointer/counter is needed. A failed acknowledgement can
    be retried with the same key and payload, returning the persisted version.
    """
    fingerprint = digest({'content': content, 'parent': parent, 'restored': restored})
    for _ in range(30):
        previous = database.question_versions.find_one({'question_id': qid, 'request_key': request_key})
        if previous:
            if previous['request_hash'] != fingerprint:
                raise HTTPException(409, '本次提交与上次提交的内容不同，请返回后重新发起操作。')
            return previous
        latest = database.question_versions.find_one({'question_id': qid}, sort=[('version_no', -1)])
        item = {'_id': str(uuid4()), 'question_id': qid, 'version_no': latest['version_no'] + 1 if latest else 1,
                'parent_version_id': parent, 'restored_from_version_id': restored,
                'content': content, 'content_hash': digest(content), 'created_at': now(),
                'request_key': request_key, 'request_hash': fingerprint}
        try:
            database.question_versions.insert_one(item)
            return item
        except DuplicateKeyError:
            continue
    raise HTTPException(409, '题目正在被更新，请稍后再次保存。')


def family_public(database, family, user):
    latest = database.question_versions.find_one({'question_id': family['_id']}, sort=[('version_no', -1)])
    # Do not disclose sharing recipients or private bank membership to readers.
    return {'id': family['_id'], 'owned': family['owner_id'] == user['_id'],
            'bank_ids': family['bank_ids'] if family['owner_id'] == user['_id'] else [],
            'latest_version': public(latest) if latest else None}


@router.post('/question-banks', status_code=201)
def create_bank(data: BankInput, database=Depends(db), user=Depends(current_user)):
    item = {'_id': str(uuid4()), 'owner_id': user['_id'], **data.model_dump(), 'created_at': now()}
    database.question_banks.insert_one(item)
    return public(item)


@router.get('/question-banks')
def list_banks(database=Depends(db), user=Depends(current_user)):
    return [public(b) for b in database.question_banks.find({'owner_id': user['_id']})]


@router.put('/question-banks/{bid}')
def edit_bank(bid: str, data: BankInput, database=Depends(db), user=Depends(current_user)):
    bank_owned(database, bid, user)
    database.question_banks.update_one({'_id': bid, 'owner_id': user['_id']}, {'$set': data.model_dump()})
    return public(bank_owned(database, bid, user))


@router.get('/question-banks/{bid}/questions')
def bank_questions(bid: str, database=Depends(db), user=Depends(current_user)):
    bank_owned(database, bid, user)
    return [family_public(database, q, user) for q in database.bank_questions.find({'bank_ids': bid, 'owner_id': user['_id']})]


@router.post('/question-banks/{bid}/questions', status_code=201)
def save_question(bid: str, data: SaveQuestion, database=Depends(db), user=Depends(current_user)):
    bank_owned(database, bid, user)
    # Stable identity lets a retry finish after an interrupted family/version write.
    qid = str(uuid5(NAMESPACE_URL, json.dumps([user['_id'], bid, data.request_key])))
    database.bank_questions.update_one({'_id': qid}, {'$setOnInsert': {
        'owner_id': user['_id'], 'bank_ids': [bid], 'shared_with': [], 'created_at': now()}}, upsert=True)
    append_version(database, qid, data.content.model_dump(), 'create:'+data.request_key)
    return family_public(database, family_access(database, qid, user, write=True), user)


@router.get('/bank-questions')
def list_questions(exclude_bank_id: str | None = None, database=Depends(db), user=Depends(current_user)):
    query = {'owner_id': user['_id']}
    if exclude_bank_id:
        bank_owned(database, exclude_bank_id, user)
        query['bank_ids'] = {'$ne': exclude_bank_id}
    rows = [family_public(database, q, user) for q in database.bank_questions.find(query)]
    return [q for q in rows if q['latest_version'] is not None]


@router.get('/bank-questions/{qid}')
def get_question(qid: str, database=Depends(db), user=Depends(current_user)):
    return family_public(database, family_access(database, qid, user), user)


@router.put('/question-banks/{bid}/questions/{qid}')
def add_membership(bid: str, qid: str, database=Depends(db), user=Depends(current_user)):
    bank_owned(database, bid, user)
    family_access(database, qid, user, write=True)
    result = database.bank_questions.update_one({'_id': qid}, {'$addToSet': {'bank_ids': bid}})
    return {'ok': True, 'added': bool(result.modified_count),
            'message': '题目已加入此题库。' if result.modified_count else '此题目已在当前题库中，无需重复加入。'}


class CopySurveyQuestion(Strict):
    survey_id: str
    instance_id: str


@router.post('/question-banks/{bid}/from-survey')
def copy_survey_question(bid: str, data: CopySurveyQuestion, database=Depends(db), user=Depends(current_user)):
    bank_owned(database, bid, user)
    survey = owned(database, data.survey_id, user)
    question = next((q for q in survey['questions'] if q['id'] == data.instance_id), None)
    if question is None:
        raise HTTPException(404, '问卷中没有找到这道题，请刷新后重新选择。')
    # Only question content is portable; IDs, source and jumps belong to the survey.
    content = QuestionInput.model_validate({k: question[k] for k in QuestionInput.model_fields if k in question}).model_dump()
    content_hash = digest(content)
    source = question.get('source', {})
    family = database.bank_questions.find_one({'_id': source.get('question_id'), 'owner_id': user['_id']})
    source_version = database.question_versions.find_one({'_id': source.get('version_id'), 'question_id': source.get('question_id')}) if family else None
    if family and source_version and source_version['content'] == content:
        qid = family['_id']
    else:
        # Same snapshot copied again (or into another bank) reuses one owned family.
        qid = str(uuid5(NAMESPACE_URL, json.dumps(['survey-copy', user['_id'], data.survey_id, data.instance_id, content_hash])))
        database.bank_questions.update_one({'_id': qid}, {'$setOnInsert': {
            'owner_id': user['_id'], 'bank_ids': [], 'shared_with': [], 'created_at': now(),
            'copied_from': {'survey_id': data.survey_id, 'instance_id': data.instance_id, 'content_hash': content_hash}}}, upsert=True)
        append_version(database, qid, content, 'survey-copy')
    result = database.bank_questions.update_one({'_id': qid, 'owner_id': user['_id']}, {'$addToSet': {'bank_ids': bid}})
    return {'question': family_public(database, family_access(database, qid, user, write=True), user),
            'added': bool(result.modified_count),
            'message': '题目已保存到题库，原问卷保持不变。' if result.modified_count else '此题目已在当前题库中，无需重复保存。'}


@router.delete('/question-banks/{bid}/questions/{qid}')
def remove_membership(bid: str, qid: str, database=Depends(db), user=Depends(current_user)):
    bank_owned(database, bid, user)
    family_access(database, qid, user, write=True)
    database.bank_questions.update_one({'_id': qid}, {'$pull': {'bank_ids': bid}})
    return {'ok': True}


class NewVersion(SaveQuestion):
    parent_version_id: str


class RestoreVersion(Strict):
    request_key: str = Field(min_length=1, max_length=100)
    parent_version_id: str


@router.get('/bank-questions/{qid}/versions')
def history(qid: str, database=Depends(db), user=Depends(current_user)):
    family_access(database, qid, user)
    return [public(v) for v in database.question_versions.find({'question_id': qid}).sort('version_no', 1)]


@router.get('/bank-questions/{qid}/versions/{vid}')
def version_detail(qid: str, vid: str, database=Depends(db), user=Depends(current_user)):
    family_access(database, qid, user)
    return public(version_get(database, qid, vid))


@router.post('/bank-questions/{qid}/versions', status_code=201)
def new_version(qid: str, data: NewVersion, database=Depends(db), user=Depends(current_user)):
    family_access(database, qid, user, write=True)
    version_get(database, qid, data.parent_version_id)
    return public(append_version(database, qid, data.content.model_dump(), data.request_key, data.parent_version_id))


@router.post('/bank-questions/{qid}/versions/{vid}/restore', status_code=201)
def restore_version(qid: str, vid: str, data: RestoreVersion, database=Depends(db), user=Depends(current_user)):
    family_access(database, qid, user, write=True)
    target = version_get(database, qid, vid)
    version_get(database, qid, data.parent_version_id)
    return public(append_version(database, qid, target['content'], data.request_key, data.parent_version_id, vid))


class ShareInput(Strict):
    username: str = Field(min_length=3, max_length=40)


@router.get('/shared-questions')
def shared_questions(database=Depends(db), user=Depends(current_user)):
    return [family_public(database, q, user) for q in database.bank_questions.find({'shared_with': user['_id']})]


@router.get('/bank-questions/{qid}/shares')
def shares(qid: str, database=Depends(db), user=Depends(current_user)):
    q = family_access(database, qid, user, write=True)
    return [{'username': u['username']} for u in database.users.find({'_id': {'$in': q['shared_with']}})]


@router.post('/bank-questions/{qid}/shares')
def share(qid: str, data: ShareInput, database=Depends(db), user=Depends(current_user)):
    family_access(database, qid, user, write=True)
    recipient = database.users.find_one({'username': data.username.lower()})
    if not recipient: raise HTTPException(404, '没有找到该用户名，请确认对方已注册并检查拼写。')
    if recipient['_id'] == user['_id']: raise HTTPException(422, '这道题已属于您，无需再分享给自己。')
    database.bank_questions.update_one({'_id': qid}, {'$addToSet': {'shared_with': recipient['_id']}})
    return {'ok': True}


@router.delete('/bank-questions/{qid}/shares/{username}')
def revoke(qid: str, username: str, database=Depends(db), user=Depends(current_user)):
    family_access(database, qid, user, write=True)
    recipient = database.users.find_one({'username': username.lower()})
    if recipient:
        database.bank_questions.update_one({'_id': qid}, {'$pull': {'shared_with': recipient['_id']}})
    return {'ok': True}


def accessible_surveys(database, qid, user):
    """Revocation denies library reads but never revokes owners' snapshot access."""
    surveys = list(database.surveys.find({'owner_id': user['_id'], 'questions.source.question_id': qid}))
    if not surveys: family_access(database, qid, user)
    return surveys


@router.get('/bank-questions/{qid}/usages')
def usages(qid: str, database=Depends(db), user=Depends(current_user)):
    return [{'survey_id': s['_id'], 'title': s['title'], 'status': s['status'],
             'instances': [{'instance_id': q['id'], 'version_id': q['source']['version_id']}
                           for q in s['questions'] if q.get('source', {}).get('question_id') == qid]}
            for s in accessible_surveys(database, qid, user)]
