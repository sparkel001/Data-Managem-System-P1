import pytest
from tests.test_phase2_block2 import library
from tests.test_phase2_block3 import version
from tests.test_phase2_block4 import import_into
from tests.test_block2 import login
from tests.test_course_requirements import case


@case('复用边界与权限', '他人导入自己的问卷、错误版本族、伪造source、未知实例换版；对比原问卷。', '另一账号和不存在的版本/实例', '404或422；没有部分写入。')
def test_import_ownership_and_version_validation(client):
    h,b,q=library(client); other=login(client,'other');sid,a=import_into(client,h,q)
    url=f'/api/surveys/{sid}/library-questions'
    body={'question_id':q['id'],'version_id':q['latest_version']['id']}
    before=client.app.state.db.surveys.find_one({'_id':sid})
    assert client.post(url,headers=other,json=body).status_code==404
    assert client.post(url,headers=h,json={**body,'version_id':'missing'}).status_code==404
    assert client.post(url,headers=h,json={**body,'source':{}}).status_code==422
    assert client.put(f'/api/surveys/{sid}/questions/missing/version',headers=h,json=body).status_code==404
    assert client.app.state.db.surveys.find_one({'_id':sid})==before


@case('跨问卷完整性保护', '在隔离库中模拟快照被直接数据库工具篡改，再统计。', '已关联版本的标题改变，摘要保持原值', '409停止统计，不把篡改内容混入原版本。')
def test_tampered_snapshot_statistics_rejected(client):
    h,b,q=library(client);sid,a=import_into(client,h,q)
    client.app.state.db.surveys.update_one({'_id':sid},{'$set':{'questions.0.title':'tampered'}})
    assert client.get(f'/api/bank-questions/{q["id"]}/stats',headers=h).status_code==409


@case('题目保存故障重试', '中断初始版本插入；用同一题库和请求键重试两次，再更改内容重试。', '固定request_key，第一次版本写入前失败', '只有一个题目族和一个版本；冲突内容409。')
def test_family_creation_retry(client,monkeypatch):
    from pymongo.synchronous.collection import Collection
    h=login(client);bid=client.post('/api/question-banks',headers=h,json={'name':'retry'}).json()['id']
    path=f'/api/question-banks/{bid}/questions';body={'request_key':'fixed','content':{'title':'retry','type':'text'}}
    original=Collection.insert_one
    def failure(self,*args,**kwargs):
        if self.name=='question_versions': raise RuntimeError('interrupted before version insert')
        return original(self,*args,**kwargs)
    with monkeypatch.context() as m:
        m.setattr(Collection,'insert_one',failure)
        with pytest.raises(RuntimeError):client.post(path,headers=h,json=body)
    first=client.post(path,headers=h,json=body)
    assert first.status_code==201
    assert client.post(path,headers=h,json=body).json()['id']==first.json()['id']
    assert client.post(path,headers=h,json={**body,'content':{'title':'changed','type':'text'}}).status_code==409
    assert client.app.state.db.bank_questions.count_documents({})==1
    assert client.app.state.db.question_versions.count_documents({})==1
