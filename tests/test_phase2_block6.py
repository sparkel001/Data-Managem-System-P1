import pytest
from tests.test_phase2_block2 import library
from tests.test_phase2_block3 import version
from tests.test_phase2_block4 import import_into
from tests.test_block2 import login
from tests.test_course_requirements import case


def submit(client,h,sid,answers):
    assert client.post(f'/api/surveys/{sid}/publish',headers=h).status_code==200
    assert client.post(f'/api/fill/{sid}/submit',headers=h,json={'answers':answers}).status_code==201


@case('跨问卷四题型统计', '同一版本加入两个问卷；分别提交；查询跨问卷统计。', '单选a/b，多选[a,b]/[b]，文本甲/乙，数字10/20', '答卷2、实例2、回答2；选项/文本/均值和分布精确。')
@pytest.mark.parametrize('kind,values',[('single',['a','b']),('multiple',[['a','b'],['b']]),('text',['甲','乙']),('number',[10,20])])
def test_cross_four_types(client,kind,values):
    h,b,q=library(client,kind)
    for value in values:
        sid,a=import_into(client,h,q)
        submit(client,h,sid,{a['id']:value})
    data=client.get(f'/api/bank-questions/{q["id"]}/stats',headers=h).json()
    g=data['groups'][0]
    assert data['total_responses']==g['total_responses']==g['answer_count']==g['survey_count']==g['instance_count']==2
    if kind in ('single','multiple'):
        assert [o['count'] for o in g['options']]==([1,1,0] if kind=='single' else [1,2,0])
    else: assert g['values']==values
    if kind=='number': assert g['average']==15 and g['distribution']==[{'value':10,'count':1},{'value':20,'count':1}]


@case('跨问卷空数据', '保存题目但无问卷答卷；查询统计。', '四种题型', '答卷和回答数0；数字平均值null、分布空。')
@pytest.mark.parametrize('kind',['single','multiple','text','number'])
def test_cross_empty(client,kind):
    h,b,q=library(client,kind)
    data=client.get(f'/api/bank-questions/{q["id"]}/stats',headers=h).json()
    g=data['groups'][0]
    assert data['total_responses']==g['answer_count']==0
    if kind=='number': assert g['average'] is None and g['distribution']==[]


@case('跨问卷版本与多实例', '同卷放V1两次和V2一次；提交；查询全部及单版本；恢复V1再查询。', 'V1答案10、20；V2答案100', '总答卷1；V1回答2均值15；V2回答1均值100；恢复版本单独空组。')
def test_versions_multi_instances_restore_and_filter(client):
    h,b,q=library(client)
    sid,a=import_into(client,h,q); _,bq=import_into(client,h,q,sid)
    v2=version(client,h,q).json(); _,c=import_into(client,h,q,sid,v2['id'])
    submit(client,h,sid,{a['id']:10,bq['id']:20,c['id']:100})
    url=f'/api/bank-questions/{q["id"]}/stats'
    data=client.get(url,headers=h).json(); groups={g['version_id']:g for g in data['groups']}
    assert data['total_responses']==1
    g=groups[q['latest_version']['id']]
    assert g['answer_count']==2 and g['average']==15 and g['instance_count']==2 and g['total_responses']==1
    assert groups[v2['id']]['average']==100
    filtered=client.get(url,params={'version_id':v2['id']},headers=h).json()
    assert len(filtered['groups'])==1 and filtered['groups'][0]['average']==100
    restore=client.post(f'/api/bank-questions/{q["id"]}/versions/{q["latest_version"]["id"]}/restore',headers=h,json={'parent_version_id':v2['id'],'request_key':'restore'}).json()
    data=client.get(url,headers=h).json()
    assert len(data['groups'])==3
    assert next(g for g in data['groups'] if g['version_id']==restore['id'])['answer_count']==0
    assert client.get(url,params={'version_id':'missing'},headers=h).status_code==404


@case('跨问卷权限与匿名', '共享题目，双方各收答卷；跨问卷查询；撤销共享后重查自己的统计。', '匿名答卷12和99；第三账号', '各只统计自己问卷；无身份字段；撤销不影响已有快照统计。')
def test_cross_permissions_anonymity_revocation(client):
    h,b,q=library(client); reader=login(client,'reader'); stranger=login(client,'stranger')
    base=f'/api/bank-questions/{q["id"]}'
    client.post(base+'/shares',headers=h,json={'username':'reader'})
    for header,value in ((h,12),(reader,99)):
        sid,a=import_into(client,header,q); submit(client,header,sid,{a['id']:value})
    assert client.get(base+'/stats',headers=h).json()['groups'][0]['average']==12
    r=client.get(base+'/stats',headers=reader)
    assert r.json()['groups'][0]['average']==99
    assert all(field not in r.text for field in ('respondent','username','once_key'))
    assert client.get(base+'/stats',headers=stranger).status_code==404
    client.delete(base+'/shares/reader',headers=h)
    assert client.get(base+'/stats',headers=reader).json()['groups'][0]['average']==99
