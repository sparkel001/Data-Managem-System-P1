from concurrent.futures import ThreadPoolExecutor
import pytest
from tests.test_phase2_block2 import library
from tests.test_block2 import login
from tests.test_course_requirements import case


def version(client, h, q, title='第二版', key='version2', parent=None, **changes):
    return client.post(f'/api/bank-questions/{q["id"]}/versions', headers=h, json={
        'request_key':key, 'parent_version_id':parent or q['latest_version']['id'],
        'content':{**q['latest_version']['content'], 'title':title, **changes}})


@case('版本历史', '创建新版本、从初版分支、恢复初版；比较历史文档并重复恢复。', 'V1→V2，V1→V3，恢复V1生成V4', '父版本与恢复来源正确；V1未变；重复请求返回同一V4。')
def test_branch_restore_immutable(client):
    h, b, q = library(client)
    d = client.app.state.db
    initial = d.question_versions.find_one()
    v2 = version(client,h,q).json()
    v3 = version(client,h,q,title='分支',key='branch').json()
    assert v2['parent_version_id'] == v3['parent_version_id'] == initial['_id']
    path = f'/api/bank-questions/{q["id"]}/versions/{initial["_id"]}/restore'
    body = {'request_key':'restore','parent_version_id':v2['id']}
    v4 = client.post(path,headers=h,json=body).json()
    assert v4['version_no'] == 4 and v4['restored_from_version_id'] == initial['_id']
    assert v4['parent_version_id'] == v2['id'] and v4['content'] == initial['content']
    assert client.post(path,headers=h,json=body).json()['id'] == v4['id']
    assert d.question_versions.find_one({'_id':initial['_id']}) == initial
    assert len(client.get(f'/api/bank-questions/{q["id"]}/versions',headers=h).json()) == 4


@case('版本幂等并发', '并发发送相同请求；再并发发送不同请求；复用键改变内容。', '4个相同请求、4个不同键、冲突内容', '相同请求仅一版本；不同请求序号唯一；冲突409。')
def test_version_concurrent_idempotency(client):
    h,b,q = library(client)
    with ThreadPoolExecutor(max_workers=4) as pool:
        same = list(pool.map(lambda _:version(client,h,q), range(4)))
    assert all(r.status_code == 201 for r in same)
    assert len({r.json()['id'] for r in same}) == 1
    with ThreadPoolExecutor(max_workers=4) as pool:
        different = list(pool.map(lambda i:version(client,h,q,key='key'+str(i)), range(4)))
    assert sorted(r.json()['version_no'] for r in different) == [3,4,5,6]
    assert version(client,h,q,title='冲突').status_code == 409
    assert client.app.state.db.question_versions.count_documents({}) == 6


@case('版本失败重试', '模拟版本写入成功但响应丢失；相同键重试；检查数量。', 'insert_one完成后抛出RuntimeError', '异常后恢复同一已提交版本；不重复插入。')
def test_version_retry_after_lost_ack(client, monkeypatch):
    from pymongo.synchronous.collection import Collection
    h,b,q=library(client)
    original=Collection.insert_one
    def lost(self,*args,**kwargs):
        result=original(self,*args,**kwargs)
        if self.name=='question_versions': raise RuntimeError('lost acknowledgement')
        return result
    with monkeypatch.context() as m:
        m.setattr(Collection,'insert_one',lost)
        with pytest.raises(RuntimeError): version(client,h,q)
    assert version(client,h,q).status_code == 201
    assert client.app.state.db.question_versions.count_documents({}) == 2


@case('版本权限', '他人创建/恢复；不存在或其他题目版本作为父版本；尝试覆盖版本。', '其他账号、错误parent、PUT版本', '404/405；历史内容不变。')
def test_version_invalid_parent_and_permissions(client):
    h,b,q=library(client)
    other=login(client,'other')
    assert version(client,other,q).status_code == 404
    assert version(client,h,q,parent='missing').status_code == 404
    assert client.get(f'/api/bank-questions/{q["id"]}/versions',headers=other).status_code == 404
    path=f'/api/bank-questions/{q["id"]}/versions/{q["latest_version"]["id"]}'
    assert client.put(path,headers=h,json={}).status_code == 405
    assert client.post(path+'/restore',headers=other,json={'request_key':'r','parent_version_id':q['latest_version']['id']}).status_code == 404
    assert client.app.state.db.question_versions.count_documents({}) == 1
