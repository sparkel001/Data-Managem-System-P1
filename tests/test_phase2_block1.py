import pytest
from pymongo.errors import WriteError
from app.migrations import migrate
from tests.test_block2 import login
from tests.test_course_requirements import case


@case("第二阶段迁移", "保存旧问卷与答卷；执行迁移两次；读取旧接口并比较原文档。", "无source的旧问卷和答卷", "两次迁移成功；旧文档完全不变；旧接口可读。")
def test_additive_repeat_legacy(client):
    h = login(client)
    sid = client.post('/api/surveys', headers=h, json={'title': 'legacy'}).json()['id']
    d = client.app.state.db
    d.responses.insert_one({'_id': 'legacy', 'survey_id': sid, 'answers': {}})
    before = [list(d[c].find()) for c in ('users', 'sessions', 'surveys', 'responses')]
    assert migrate(d) == migrate(d)
    assert before == [list(d[c].find()) for c in ('users', 'sessions', 'surveys', 'responses')]
    assert client.get('/api/surveys/'+sid, headers=h).status_code == 200


@case("第二阶段迁移", "故障注入使索引创建中断；恢复后重复迁移；尝试非法写入。", "模拟create_index抛出异常；缺少必要字段的版本", "可安全重试；新集合验证拒绝非法文档。")
def test_migration_retry_and_validation(client, monkeypatch):
    from pymongo.synchronous.collection import Collection
    d = client.app.state.db
    original = Collection.create_index
    def fail(self, *args, **kwargs):
        if self.name == 'bank_questions':
            raise RuntimeError('injected interruption')
        return original(self, *args, **kwargs)
    with monkeypatch.context() as m:
        m.setattr(Collection, 'create_index', fail)
        with pytest.raises(RuntimeError): migrate(d)
    migrate(d)
    migrate(d)
    with pytest.raises(WriteError): d.question_versions.insert_one({'_id': 'invalid'})
    assert d.question_versions.count_documents({}) == 0
