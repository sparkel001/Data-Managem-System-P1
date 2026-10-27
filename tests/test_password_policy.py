import secrets
import pytest
from app.auth import digest, now
from tests.test_course_requirements import case


@case('注册密码长度', '用指定长度注册；核对响应与用户数；合法密码再次登录。', '7、8、16、17、128字符及8/16/17个Unicode字符', '仅8～16字符可注册，非法请求422且不写入；合法账号可登录。')
@pytest.mark.parametrize('password,expected', [('a'*7,422),('a'*8,201),('a'*16,201),('a'*17,422),('a'*128,422),('😀'*8,201),('😀'*16,201),('😀'*17,422)])
def test_registration_password_bounds(client,password,expected):
    body={'username':'policy_user','password':password}
    assert client.post('/api/auth/register',json=body).status_code==expected
    assert client.app.state.db.users.count_documents({})==(1 if expected==201 else 0)
    if expected==201:
        assert client.post('/api/auth/login',json=body).status_code==200


@case('历史长密码兼容', '在隔离库按原哈希算法准备历史账号；正确和错误密码登录；比较用户记录。', '17、64、128字符历史密码', '正确密码200，错误密码401；用户记录不变。')
@pytest.mark.parametrize('length',[17,64,128])
def test_legacy_long_password_login(client,length):
    password='x'*length;salt=secrets.token_hex(16)
    client.app.state.db.users.insert_one({'_id':'legacy','username':'legacy_user','salt':salt,
        'password_hash':digest(password,salt),'created_at':now()})
    before=client.app.state.db.users.find_one({'_id':'legacy'})
    assert client.post('/api/auth/login',json={'username':'legacy_user','password':password}).status_code==200
    assert client.post('/api/auth/login',json={'username':'legacy_user','password':'y'*length}).status_code==401
    assert client.app.state.db.users.find_one({'_id':'legacy'})==before
