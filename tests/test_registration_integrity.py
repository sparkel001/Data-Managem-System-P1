from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from fastapi.testclient import TestClient
from app.config import Settings
from tests.mongo_config import MONGO_URI
from app.main import create_app
from app.user_indexes import username_index_ready
from tests.test_course_requirements import case

BODY = {'username': 'same_user', 'password': 'password123'}


@case('注册唯一性', '首次注册，再同名及大小写变体注册；检查用户数。', 'same_user、SAME_USER', '201、409、409；只有一条用户；唯一索引存在。')
def test_register_duplicate(client):
    assert client.post('/api/auth/register', json=BODY).status_code == 201
    for name in ('same_user', 'SAME_USER'):
        r = client.post('/api/auth/register', json={**BODY, 'username': name})
        assert r.status_code == 409 and r.json()['detail'] == '用户名已存在'
    assert client.app.state.db.users.count_documents({}) == 1
    assert username_index_ready(client.app.state.db)


@case('注册并发唯一性', '8个请求在密码哈希前汇合，确保均通过预查询后竞争插入。', '8次相同用户名', '只有1个201、7个409；MongoDB只有1条用户。')
def test_concurrent_duplicate(client, monkeypatch):
    from app import auth
    barrier = Barrier(8)
    original = auth.digest
    def synchronize(password, salt):
        barrier.wait(timeout=20)
        return original(password, salt)
    monkeypatch.setattr(auth, 'digest', synchronize)
    with ThreadPoolExecutor(max_workers=8) as pool:
        responses = list(pool.map(lambda _: client.post('/api/auth/register', json=BODY), range(8)))
    assert sorted(r.status_code for r in responses) == [201] + [409]*7
    assert all(r.json()['detail'] == '用户名已存在' for r in responses if r.status_code == 409)
    assert client.app.state.db.users.count_documents({}) == 1


@case('历史重复用户保护', '隔离库删除测试索引并植入重复用户；重新启动应用；注册、登录及健康检查。', '两条同名历史记录；一个新用户名', '启动可用；同名409、新账号503、重复登录409；健康降级；所有历史记录保持不变。')
def test_existing_duplicates_safe_startup(client):
    database = client.app.state.db
    database.users.drop_index('username_1')
    database.users.insert_many([{'_id': 'old1', 'username': 'same_user'},
                                {'_id': 'old2', 'username': 'same_user'}])
    before = list(database.users.find())
    app = create_app(Settings(mongo_uri=MONGO_URI, database=database.name))
    with TestClient(app) as restarted:
        assert restarted.get('/').status_code == 200
        assert restarted.post('/api/auth/register', json=BODY).status_code == 409
        r = restarted.post('/api/auth/register', json={**BODY, 'username': 'new_user'})
        assert r.status_code == 503 and '注册设置' in r.json()['detail']
        assert restarted.post('/api/auth/login', json=BODY).status_code == 409
        assert restarted.get('/api/health').json()['registration'] == 'blocked'
    assert list(database.users.find()) == before


@case('缺失索引修复', '在隔离库移除索引后注册；重复请求；检查索引。', '空用户集合、缺失索引', '注册前重建唯一索引，201后409。')
def test_missing_index_rebuilt(client):
    client.app.state.db.users.drop_index('username_1')
    assert client.post('/api/auth/register', json=BODY).status_code == 201
    assert username_index_ready(client.app.state.db)
    assert client.post('/api/auth/register', json=BODY).status_code == 409


@case('冲突索引保护', '隔离库用非唯一同名索引代替唯一索引；尝试注册。', 'username_1非唯一', '503；不删除索引、不写用户。')
def test_nonunique_index_blocks_without_replacement(client):
    d = client.app.state.db
    d.users.drop_index('username_1'); d.users.create_index('username')
    before = d.users.index_information()
    assert client.post('/api/auth/register', json=BODY).status_code == 503
    assert d.users.count_documents({}) == 0
    assert d.users.index_information() == before
