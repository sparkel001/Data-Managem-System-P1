"""Actual headless Edge UI flow against the UUID database from conftest."""
import socket
import threading
import time
from pathlib import Path
import pytest
import uvicorn
from app.config import Settings
from tests.mongo_config import MONGO_URI, ARTIFACT_DIR
from app.main import create_app
from tests.test_block2 import login
from tests.test_course_requirements import case


@case('第二阶段浏览器自动化', 'Edge中创建题库/题目、分支/恢复、分享/撤销；选题加入问卷、换版、发布填写、查使用及统计。', '数字题年龄、答案16，reader共享账号，390px视窗', '页面流程完成；三版本；快照换版成功；统计16；使用清单可见；无JS异常和横向溢出。')
def test_library_browser_flow(client):
    playwright = pytest.importorskip('playwright.sync_api')
    login(client,'reader')
    sock=socket.socket();sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
    settings=Settings(mongo_uri=MONGO_URI,database=client.app.state.db.name)
    server=uvicorn.Server(uvicorn.Config(create_app(settings),log_level='error'))
    thread=threading.Thread(target=server.run,kwargs={'sockets':[sock]},daemon=True);thread.start()
    try:
        for _ in range(100):
            if server.started: break
            time.sleep(.1)
        assert server.started
        with playwright.sync_playwright() as p:
            browser=p.chromium.launch(channel='msedge',headless=True)
            page=browser.new_page(viewport={'width':1280,'height':900})
            errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
            page.goto(f'http://127.0.0.1:{port}')
            page.locator('#register').click()
            page.locator('#username').fill('browser_phase2');page.locator('#password').fill('password123')
            page.locator('#confirmPassword').fill('password123');page.locator('#submitRegistration').click();playwright.expect(page.locator('#notice')).to_contain_text('注册成功')
            page.locator('#password').fill('password123')
            page.get_by_role('button',name='登录',exact=True).click()
            page.locator('#banks').click();page.locator('#newBank').click()
            page.locator('#bankName').fill('课堂题库');page.get_by_role('button',name='保存题库').click()
            page.locator('[data-bank]').click();page.locator('#newBankQuestion').click()
            page.locator('#qt').fill('年龄');page.locator('#kind').select_option('number')
            page.locator('#integer').check();page.get_by_role('button',name='保存题目').click()
            page.locator('[data-family]').click();page.locator('[data-branch]').first.click()
            page.locator('#qt').fill('年龄第二版');page.get_by_role('button',name='保存题目').click()
            playwright.expect(page.locator('[data-version-row]')).to_have_count(2)
            page.locator('[data-restore]').first.click()
            playwright.expect(page.locator('[data-version-row]')).to_have_count(3)
            page.locator('#shareUsername').fill('reader');page.get_by_role('button',name='分享题目',exact=True).click()
            playwright.expect(page.locator('[data-revoke]')).to_have_count(1)
            page.locator('[data-revoke]').click();playwright.expect(page.locator('[data-revoke]')).to_have_count(0)
            page.locator('#back').click();page.locator('#back').click()
            page.locator('#new').click();page.locator('#title').fill('题库复用演示')
            page.locator('#anonymous').check();page.get_by_role('button',name='保存',exact=True).click()
            page.locator('#importLibrary').click();page.locator('[data-family]').click();page.locator('[data-pick]').first.click()
            page.locator('[data-switch]').click();page.locator('[data-family]').click();page.locator('[data-pick]').last.click()
            page.locator('#publish').click();playwright.expect(page.locator('#notice')).to_contain_text('已发布')
            share=page.locator('a[href^="/survey/"]').get_attribute('href')
            page.goto(f'http://127.0.0.1:{port}'+share);page.locator('#answer').fill('16')
            page.get_by_role('button',name='下一步').click();page.locator('#submit').click()
            playwright.expect(page.get_by_role('heading',name='提交成功')).to_be_visible()
            page.goto(f'http://127.0.0.1:{port}');page.locator('[data-open]').click();page.locator('[data-cross]').click()
            playwright.expect(page.locator('#app')).to_contain_text('平均值：16')
            page.locator('#versionFilter').select_option(index=3)
            playwright.expect(page.locator('#app')).to_contain_text('平均值：16')
            ARTIFACT_DIR.mkdir(parents=True,exist_ok=True)
            page.screenshot(path=str(ARTIFACT_DIR / 'browser-library-stats.png'),full_page=True)
            page.set_viewport_size({'width':390,'height':844})
            assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth')
            page.locator('#back').click();page.locator('#banks').click();page.locator('[data-family]').first.click();page.locator('#usages').click()
            playwright.expect(page.locator('#app')).to_contain_text('题库复用演示')
            assert errors==[],errors
            browser.close()
    finally:
        server.should_exit=True;thread.join(timeout=10);sock.close()
        assert not thread.is_alive()
