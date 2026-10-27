import pytest
from tests.test_phase2_block2 import library
from tests.test_phase2_block3 import version
from tests.test_course_requirements import case


def import_into(client,h,q,sid=None,vid=None):
    if sid is None:
        sid=client.post('/api/surveys',headers=h,json={'title':'复用','anonymous':True,'allow_multiple':True}).json()['id']
    r=client.post(f'/api/surveys/{sid}/library-questions',headers=h,json={
        'question_id':q['id'],'version_id':vid or q['latest_version']['id']})
    assert r.status_code == 201,r.text
    return sid,r.json()['questions'][-1]


@case('复用快照', '同版本加入两次；创建新版本；显式换版；发布、提交后尝试换版。', '数字题V1、V2；答案键为实例ID', '实例ID不同；原快照不自动更新；换版保持ID；发布后拒绝；答卷不变。')
def test_snapshots_and_published_freeze(client):
    h,b,q=library(client)
    sid,a=import_into(client,h,q)
    _,bq=import_into(client,h,q,sid)
    assert len({a['id'],bq['id'],q['id'],q['latest_version']['id']}) == 4
    v=version(client,h,q).json()
    base=f'/api/surveys/{sid}'
    assert client.get(base,headers=h).json()['questions'][0] == a
    path=base+f'/questions/{a["id"]}/version'
    body={'question_id':q['id'],'version_id':v['id']}
    changed=client.put(path,headers=h,json=body).json()['questions'][0]
    assert changed['id']==a['id'] and changed['source']['version_id']==v['id']
    assert client.put(base+f'/questions/{a["id"]}',headers=h,json=v['content']).status_code == 409
    assert client.post(base+'/publish',headers=h).status_code == 200
    assert client.post(f'/api/fill/{sid}/submit',headers=h,json={'answers':{a['id']:10,bq['id']:20}}).status_code == 201
    d=client.app.state.db
    before=d.surveys.find_one({'_id':sid}); response=d.responses.find_one()
    assert client.put(path,headers=h,json=body).status_code == 409
    version(client,h,q,title='第三版',key='third')
    assert d.surveys.find_one({'_id':sid})==before and d.responses.find_one()==response


@case('换版规则完整性', '配置规则后换成不兼容版本，或模拟损坏目标；比较完整问卷。', '数字gt规则改文本；单选移除条件选项；无效跳转目标', '422且问卷快照、规则、revision完全不变。')
@pytest.mark.parametrize('scenario',['type','option','target'])
def test_replacement_atomic_rule_rejection(client,scenario):
    h,b,q=library(client,'single' if scenario=='option' else 'number')
    sid,a=import_into(client,h,q)
    base=f'/api/surveys/{sid}'
    rule={'op':'eq' if scenario=='option' else 'gt','value':'a' if scenario=='option' else 0,'target':'END'}
    assert client.put(base+f'/questions/{a["id"]}/rules',headers=h,json={'rules':[rule]}).status_code==200
    changes={'type':'text'} if scenario=='type' else {'options':[{'id':'b','label':'B'},{'id':'c','label':'C'}]} if scenario=='option' else {}
    v=version(client,h,q,**changes).json()
    d=client.app.state.db
    if scenario=='target':
        d.surveys.update_one({'_id':sid},{'$set':{'questions.0.rules.0.target':'missing'}})
    before=d.surveys.find_one({'_id':sid})
    r=client.put(base+f'/questions/{a["id"]}/version',headers=h,json={'question_id':q['id'],'version_id':v['id']})
    assert r.status_code==422,r.text
    assert d.surveys.find_one({'_id':sid})==before
