import pytest
from uuid import uuid4
from tests.test_block2 import login
from tests.test_course_requirements import case, question_input


def library(client, kind='number', **changes):
    h = login(client)
    b = client.post('/api/question-banks', headers=h, json={'name': '题库'}).json()['id']
    r = client.post(f'/api/question-banks/{b}/questions', headers=h,
                    json={'content': question_input(kind, **changes), 'request_key': str(uuid4())})
    assert r.status_code == 201, r.text
    return h, b, r.json()


@case('题库管理', '创建题库与题目；读取、编辑题库；移出再加入；对比MongoDB版本。', '四种题型，题库名称更新', '完整保存内容；稳定题目族；移出不删除版本；可重新加入。')
@pytest.mark.parametrize('kind', ['single', 'multiple', 'text', 'number'])
def test_bank_crud_four_types(client, kind):
    h, b, q = library(client, kind)
    assert q['latest_version']['content']['type'] == kind
    assert client.put('/api/question-banks/'+b, headers=h, json={'name':'更新'}).json()['name'] == '更新'
    assert len(client.get('/api/question-banks', headers=h).json()) == 1
    path = f'/api/question-banks/{b}/questions/{q["id"]}'
    assert client.delete(path, headers=h).status_code == 200
    assert client.get(f'/api/question-banks/{b}/questions', headers=h).json() == []
    assert client.get('/api/bank-questions/'+q['id'], headers=h).status_code == 200
    assert client.put(path, headers=h).status_code == 200
    assert len(client.get(f'/api/question-banks/{b}/questions', headers=h).json()) == 1
    assert client.app.state.db.question_versions.count_documents({}) == 1


@case('题库权限与校验', '尝试额外字段、无效题目和他人访问；检查数据库。', 'source伪造、选项不足、其他用户', '422或404/401；没有无效写入。')
def test_bank_validation_permissions(client):
    h, b, q = library(client)
    other = login(client, 'other')
    for payload in ({'content': question_input('number'), 'request_key':'x', 'source':{}},
                    {'content': {'title':'bad','type':'single'}, 'request_key':'x'}):
        assert client.post(f'/api/question-banks/{b}/questions', headers=h, json=payload).status_code == 422
    assert client.get('/api/question-banks').status_code == 401
    assert client.get(f'/api/question-banks/{b}/questions', headers=other).status_code == 404
    assert client.put(f'/api/question-banks/{b}/questions/{q["id"]}', headers=other).status_code == 404
    assert client.get('/api/bank-questions/'+q['id'], headers=other).status_code == 404
    assert client.app.state.db.bank_questions.count_documents({}) == 1
