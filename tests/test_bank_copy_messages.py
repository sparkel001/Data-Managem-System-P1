from concurrent.futures import ThreadPoolExecutor
import logging
import pytest
from fastapi.testclient import TestClient
from pymongo.errors import ServerSelectionTimeoutError
from pymongo.synchronous.collection import Collection
from tests.test_block2 import login
from tests.test_course_requirements import case, question_input, survey_with_questions
from tests.test_phase2_block2 import library
from tests.test_phase2_block4 import import_into


@case('从问卷保存题目', '创建并发布问卷、提交答卷；复制至题库；重复复制；比较原数据。', '四种题型及相应答案、完整校验配置', '内容完整，复制初版无规则和实例ID；重复不新增族或版本；问卷、答卷不变。')
@pytest.mark.parametrize('kind,value', [('single','a'),('multiple',['a','b']),('text','课程评价'),('number',18)])
def test_copy_snapshot_preserves_data(client, kind, value):
    h=login(client)
    data=question_input(kind,min_value=0,max_value=120,integer=True,min_length=2,max_length=100)
    sid,qs=survey_with_questions(client,h,[data])
    assert client.post(f'/api/fill/{sid}/submit',headers=h,json={'answers':{qs[0]['id']:value}}).status_code==201
    bid=client.post('/api/question-banks',headers=h,json={'name':'复用库'}).json()['id']
    d=client.app.state.db;before=[list(d[c].find()) for c in ('users','surveys','responses')]
    body={'survey_id':sid,'instance_id':qs[0]['id']};url=f'/api/question-banks/{bid}/from-survey'
    r=client.post(url,headers=h,json=body);assert r.status_code==200,r.text
    v=r.json()['question']['latest_version']
    assert v['content']=={k:v for k,v in qs[0].items() if k not in ('id','rules','source')}
    again=client.post(url,headers=h,json=body).json()
    assert again['added'] is False and '无需重复' in again['message']
    assert d.bank_questions.count_documents({})==d.question_versions.count_documents({})==1
    assert before==[list(d[c].find()) for c in ('users','surveys','responses')]


@case('已有题目加入和权限', '排除当前题库后查询；加入另一题库、重复加入；尝试跨用户操作。', '两个题库、一个自有题目、另一用户', '候选只含未加入的自有题目；重复明确提示，无新增版本；跨用户404。')
def test_candidates_membership_and_permissions(client):
    h,b,q=library(client);other=login(client,'other')
    b2=client.post('/api/question-banks',headers=h,json={'name':'另一个库'}).json()['id']
    assert client.get('/api/bank-questions',params={'exclude_bank_id':b},headers=h).json()==[]
    assert [x['id'] for x in client.get('/api/bank-questions',params={'exclude_bank_id':b2},headers=h).json()]==[q['id']]
    url=f'/api/question-banks/{b2}/questions/{q["id"]}'
    assert client.put(url,headers=other).status_code==404
    assert client.put(url,headers=h).json()['added'] is True
    assert client.put(url,headers=h).json()['added'] is False
    assert client.get('/api/bank-questions',params={'exclude_bank_id':b2},headers=h).json()==[]
    assert client.get('/api/bank-questions',params={'exclude_bank_id':b2},headers=other).status_code==404
    assert client.app.state.db.question_versions.count_documents({})==1


@case('复制权限和共享边界', '自有来源题复用；他人尝试复制；共享接收人复制自己问卷中的快照。', '所有者、共享接收人、两个题库', '自有来源不新建版本；不读取他人问卷；共享快照复制为接收人自有题，不改原题。')
def test_copy_source_and_shared_ownership(client):
    h,b,q=library(client);sid,instance=import_into(client,h,q)
    b2=client.post('/api/question-banks',headers=h,json={'name':'目标'}).json()['id']
    payload={'survey_id':sid,'instance_id':instance['id']}
    r=client.post(f'/api/question-banks/{b2}/from-survey',headers=h,json=payload)
    assert r.json()['question']['id']==q['id']
    reader=login(client,'reader');rb=client.post('/api/question-banks',headers=reader,json={'name':'读者题库'}).json()['id']
    assert client.post(f'/api/question-banks/{rb}/from-survey',headers=reader,json=payload).status_code==404
    assert client.post(f'/api/question-banks/{b2}/from-survey',headers=reader,json=payload).status_code==404
    client.post(f'/api/bank-questions/{q["id"]}/shares',headers=h,json={'username':'reader'})
    rsid,ri=import_into(client,reader,q)
    client.delete(f'/api/bank-questions/{q["id"]}/shares/reader',headers=h)
    copied=client.post(f'/api/question-banks/{rb}/from-survey',headers=reader,json={'survey_id':rsid,'instance_id':ri['id']}).json()['question']
    assert copied['id']!=q['id'] and copied['owned']
    assert copied['latest_version']['content']==q['latest_version']['content']
    assert client.app.state.db.question_versions.count_documents({'question_id':q['id']})==1


@case('复制重试及快照变化', '并发复制同一草稿题；修改草稿后再次复制；比较旧版本。', '4个并发请求，题干修改', '第一次只有一族一版；内容改变生成独立题，旧版本不变。')
def test_copy_concurrent_and_changed_snapshot(client):
    h=login(client);sid,qs=survey_with_questions(client,h,[question_input('number')],publish=False)
    b=client.post('/api/question-banks',headers=h,json={'name':'目标'}).json()['id']
    url=f'/api/question-banks/{b}/from-survey';body={'survey_id':sid,'instance_id':qs[0]['id']}
    with ThreadPoolExecutor(max_workers=4) as pool:
        results=list(pool.map(lambda _:client.post(url,headers=h,json=body),range(4)))
    assert all(r.status_code==200 for r in results)
    assert len({r.json()['question']['id'] for r in results})==1
    old=client.app.state.db.question_versions.find_one()
    assert client.put(f'/api/surveys/{sid}/questions/{qs[0]["id"]}',headers=h,json=question_input('number',title='新题干')).status_code==200
    assert client.post(url,headers=h,json=body).status_code==200
    assert client.app.state.db.question_versions.count_documents({})==2
    assert client.app.state.db.question_versions.find_one({'_id':old['_id']})==old


@case('数字范围中文提示', '发布数字题并提交越界值。', '下限0、上限120；-1和121', '422，分别提示不能低于最小值和不能超过最大值。')
@pytest.mark.parametrize('value,expected',[(-1,'输入的数字不能低于最小值。'),(121,'输入的数字不能超过最大值。')])
def test_number_messages(client,value,expected):
    h=login(client);sid,qs=survey_with_questions(client,h,[question_input('number',min_value=0,max_value=120)])
    r=client.post(f'/api/fill/{sid}/submit',headers=h,json={'answers':{qs[0]['id']:value}})
    assert r.status_code==422 and r.json()['detail']['message']==expected
    assert client.app.state.db.responses.count_documents({})==0


@case('中文校验及系统错误', '提交缺少标题和过长密码；模拟数据库异常与未知路由。', '缺少title、17字符密码、读取异常', '中文JSON错误，不含英文校验结构；故障有日志且返回503。')
def test_validation_and_database_messages(client,monkeypatch,caplog):
    h=login(client)
    r=client.post('/api/surveys',headers=h,json={})
    assert r.status_code==422 and r.json()['detail']=='请填写标题。'
    r=client.post('/api/auth/register',json={'username':'new_user','password':'x'*17})
    assert '密码' in r.json()['detail'] and '16' in r.json()['detail']
    assert client.get('/api/not-found').json()['detail']=='没有找到所需内容，或您没有查看权限。'
    def broken(*args,**kwargs): raise ServerSelectionTimeoutError('injected DB failure')
    monkeypatch.setattr(Collection,'find_one',broken)
    with caplog.at_level(logging.ERROR):
        r=client.post('/api/auth/register',json={'username':'new_user','password':'password123'})
    assert r.status_code==503 and '暂时' in r.json()['detail']
    assert 'injected' not in r.text and any(record.exc_info for record in caplog.records)


@case('关闭问卷复制与规则隔离', '草稿配置数字跳转后发布并关闭；复制题目并尝试不存在题目。', '数字规则跳到结束；不存在的题目编号', '关闭问卷可以复制，规则不进入通用题目；原规则保留，非法请求404无额外版本。')
def test_copy_closed_survey_without_rules(client):
    h=login(client);sid,qs=survey_with_questions(client,h,[question_input('number')],publish=False)
    qid=qs[0]['id'];base=f'/api/surveys/{sid}'
    assert client.put(base+f'/questions/{qid}/rules',headers=h,json={'rules':[{'op':'gt','value':10,'target':'END'}]}).status_code==200
    client.post(base+'/publish',headers=h);client.post(base+'/close',headers=h)
    before=client.app.state.db.surveys.find_one({'_id':sid})
    b=client.post('/api/question-banks',headers=h,json={'name':'关闭问卷题目'}).json()['id']
    url=f'/api/question-banks/{b}/from-survey'
    r=client.post(url,headers=h,json={'survey_id':sid,'instance_id':qid})
    assert r.status_code==200 and 'rules' not in r.json()['question']['latest_version']['content']
    assert client.post(url,headers=h,json={'survey_id':sid,'instance_id':'missing'}).status_code==404
    assert client.app.state.db.question_versions.count_documents({})==1
    assert client.app.state.db.surveys.find_one({'_id':sid})==before


@case('意外异常中文响应', '隔离应用注入未预期的运行异常并发起注册。', '模拟内部异常', '返回中文JSON错误，日志保留traceback；不向用户返回英文或内部细节。')
def test_unexpected_error_message(client,monkeypatch,caplog):
    from app import auth
    def broken(*args): raise RuntimeError('internal diagnostic only')
    monkeypatch.setattr(auth,'digest',broken)
    probe=TestClient(client.app,raise_server_exceptions=False)
    try:
        with caplog.at_level(logging.ERROR):
            r=probe.post('/api/auth/register',json={'username':'new_user','password':'password123'})
        assert r.status_code==500 and '服务暂时' in r.json()['detail']
        assert 'internal' not in r.text and any(record.exc_info for record in caplog.records)
    finally: probe.close()
