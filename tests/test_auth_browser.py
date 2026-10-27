"""Separate auth views, form validation, and share-link continuation in Edge."""
import socket
import threading
import time
import pytest
import uvicorn
from app.config import Settings
from tests.mongo_config import MONGO_URI
from app.main import create_app
from tests.test_block6 import setup_survey
from tests.test_course_requirements import case


@case('认证浏览器自动化', '登录页进入注册页并返回；验证必填、格式、密码长度、一致性和重复账号；注册后登录、退出；分享链接上注册登录。',
      'ui_user、password123；空字段、短密码、不一致密码、重复用户名',
      '独立表单；错误提示明确且无无效注册写入；注册成功返回登录且不自动登录；登录进入首页或原问卷；退出会话失效。')
def test_separate_auth_views(client):
    pw = pytest.importorskip('playwright.sync_api')
    _, sid, _ = setup_survey(client)
    sock = socket.socket(); sock.bind(('127.0.0.1', 0))
    origin = f'http://127.0.0.1:{sock.getsockname()[1]}'
    app = create_app(Settings(mongo_uri=MONGO_URI, database=client.app.state.db.name))
    server = uvicorn.Server(uvicorn.Config(app, log_level='error'))
    thread = threading.Thread(target=server.run, kwargs={'sockets': [sock]}, daemon=True)
    thread.start()
    try:
        for _ in range(100):
            if server.started: break
            time.sleep(.1)
        assert server.started
        with pw.sync_playwright() as p:
            browser = p.chromium.launch(channel='msedge', headless=True)
            page = browser.new_page()
            errors = []; requests = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.on('request', lambda r: requests.append(r.url) if r.url.endswith('/api/auth/register') else None)
            page.goto(origin)
            pw.expect(page.locator('#auth')).to_be_visible()
            pw.expect(page.locator('#confirmPassword')).to_have_count(0)
            page.locator('#register').click()
            pw.expect(page.locator('#auth')).to_have_count(0)
            pw.expect(page.locator('#registration')).to_be_visible()
            page.locator('#backToLogin').click()
            pw.expect(page.locator('#auth')).to_be_visible()
            page.locator('#register').click()
            page.locator('#submitRegistration').click()
            pw.expect(page.locator('#notice')).to_contain_text('请填写')
            page.locator('#username').fill('!bad')
            page.locator('#password').fill('password123')
            page.locator('#confirmPassword').fill('password123')
            page.locator('#submitRegistration').click()
            pw.expect(page.locator('#notice')).to_contain_text('用户名须')
            page.locator('#username').fill('ui_user')
            page.locator('#password').fill('short')
            page.locator('#submitRegistration').click()
            pw.expect(page.locator('#notice')).to_contain_text('密码长度')
            page.locator('#password').fill('x'*17)
            page.locator('#confirmPassword').fill('x'*17)
            page.locator('#submitRegistration').click()
            pw.expect(page.locator('#notice')).to_contain_text('8～16个字符')
            page.locator('#password').fill('password123')
            page.locator('#confirmPassword').fill('different')
            page.locator('#submitRegistration').click()
            pw.expect(page.locator('#notice')).to_contain_text('不一致')
            assert requests == []
            page.locator('#confirmPassword').fill('password123')
            page.locator('#submitRegistration').click()
            pw.expect(page.locator('#notice')).to_contain_text('注册成功')
            pw.expect(page.locator('#auth')).to_be_visible()
            pw.expect(page.locator('#password')).to_have_value('')
            assert page.evaluate("sessionStorage.getItem('survey_token')") is None
            page.locator('#register').click()
            page.locator('#username').fill('UI_USER')
            page.locator('#password').fill('password123')
            page.locator('#confirmPassword').fill('password123')
            page.locator('#submitRegistration').click()
            pw.expect(page.locator('#notice')).to_contain_text('用户名已存在')
            assert client.app.state.db.users.count_documents({'username': 'ui_user'}) == 1
            page.locator('#backToLogin').click()
            page.locator('#username').fill('ui_user'); page.locator('#password').fill('incorrect')
            page.get_by_role('button', name='登录', exact=True).click()
            pw.expect(page.locator('#notice')).to_contain_text('用户名或密码错误')
            page.locator('#password').fill('password123')
            page.get_by_role('button', name='登录', exact=True).click()
            pw.expect(page.locator('#new')).to_be_visible()
            old_token = page.evaluate("sessionStorage.getItem('survey_token')")
            page.locator('#logout').click()
            pw.expect(page.locator('#auth')).to_be_visible()
            assert page.evaluate("sessionStorage.getItem('survey_token')") is None
            assert client.get('/api/auth/me', headers={'Authorization':'Bearer '+old_token}).status_code == 401
            page.goto(origin+'/survey/'+sid)
            page.locator('#register').click()
            page.locator('#username').fill('share_reader'); page.locator('#password').fill('password123')
            page.locator('#confirmPassword').fill('password123'); page.locator('#submitRegistration').click()
            pw.expect(page.locator('#notice')).to_contain_text('注册成功')
            assert page.url == origin+'/survey/'+sid
            page.locator('#password').fill('password123')
            page.get_by_role('button', name='登录', exact=True).click()
            pw.expect(page.locator('#answerForm')).to_be_visible()
            from app.auth import digest, now
            import secrets
            salt = secrets.token_hex(16)
            client.app.state.db.users.insert_one({'_id':'browser_legacy','username':'browser_legacy',
                'salt':salt,'password_hash':digest('L'*128,salt),'created_at':now()})
            page.locator('#logout').click()
            pw.expect(page.locator('#auth')).to_be_visible()
            page.locator('#username').fill('browser_legacy')
            page.locator('#password').fill('L'*128)
            page.get_by_role('button',name='登录',exact=True).click()
            pw.expect(page.locator('#answerForm')).to_be_visible()
            assert errors == [], errors
            browser.close()
    finally:
        server.should_exit = True; thread.join(timeout=10); sock.close()
        assert not thread.is_alive()
