from tests.test_phase2_block2 import library
from tests.test_phase2_block3 import version
from tests.test_phase2_block4 import import_into
from tests.test_block2 import login
from tests.test_course_requirements import case


@case('题目分享权限', '分享给另一账号；复用；尝试编辑、查看问卷答卷；撤销后再访问。', 'owner/alice、reader、stranger', '共享仅查看复用；撤销阻止新复用；已有快照仍可发布填写；使用清单不泄露他人问卷。')
def test_share_revoke_snapshot_and_usage_isolation(client):
    h,b,q=library(client)
    reader=login(client,'reader'); stranger=login(client,'stranger')
    owner_sid,_=import_into(client,h,q)
    base='/api/bank-questions/'+q['id']
    assert client.post(base+'/shares',headers=h,json={'username':'reader'}).status_code==200
    assert len(client.get('/api/shared-questions',headers=reader).json())==1
    shared=client.get(base,headers=reader).json()
    assert shared['bank_ids']==[] and 'shared_with' not in shared
    assert client.get(base+'/versions',headers=reader).status_code==200
    sid,instance=import_into(client,reader,q)
    before=client.app.state.db.surveys.find_one({'_id':sid})
    assert version(client,reader,q).status_code==404
    assert client.post(base+'/shares',headers=reader,json={'username':'stranger'}).status_code==404
    for suffix in ('','/responses','/stats'):
        assert client.get('/api/surveys/'+sid+suffix,headers=h).status_code==404
        assert client.get('/api/surveys/'+owner_sid+suffix,headers=reader).status_code==404
    assert [s['survey_id'] for s in client.get(base+'/usages',headers=h).json()]==[owner_sid]
    assert [s['survey_id'] for s in client.get(base+'/usages',headers=reader).json()]==[sid]
    assert client.get(base+'/usages',headers=stranger).status_code==404
    assert client.delete(base+'/shares/reader',headers=h).status_code==200
    assert client.get(base,headers=reader).status_code==404
    assert client.get('/api/shared-questions',headers=reader).json()==[]
    assert client.post(f'/api/surveys/{sid}/library-questions',headers=reader,json={'question_id':q['id'],'version_id':q['latest_version']['id']}).status_code==404
    assert client.app.state.db.surveys.find_one({'_id':sid})==before
    assert client.get(base+'/usages',headers=reader).status_code==200
    assert client.post(f'/api/surveys/{sid}/publish',headers=reader).status_code==200
    assert client.post(f'/api/fill/{sid}/submit',headers=reader,json={'answers':{instance['id']:12}}).status_code==201


@case('共享授权校验', '无权限账号撤销、分享不存在账号、重复分享和撤销。', 'missing用户名、reader、匿名请求', '401/404；重复操作幂等，不重复存储共享对象。')
def test_share_validation_idempotency(client):
    h,b,q=library(client); reader=login(client,'reader')
    base='/api/bank-questions/'+q['id']+'/shares'
    assert client.post(base,json={'username':'reader'}).status_code==401
    assert client.post(base,headers=h,json={'username':'missing'}).status_code==404
    for _ in range(2): assert client.post(base,headers=h,json={'username':'reader'}).status_code==200
    assert client.get(base,headers=h).json()==[{'username':'reader'}]
    assert client.delete(base+'/reader',headers=reader).status_code==404
    for _ in range(2): assert client.delete(base+'/reader',headers=h).status_code==200
    assert client.get(base,headers=h).json()==[]
