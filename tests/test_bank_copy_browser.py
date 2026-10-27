import json
import re
import socket
import threading
import time
import pytest
import uvicorn
from app.config import Settings
from tests.mongo_config import MONGO_URI
from app.main import create_app
from tests.test_block2 import login
from tests.test_course_requirements import case, question_input, survey_with_questions


@case('题库与提示浏览器验证', '浏览器模拟非JSON/网络错误；创建空题库，从自己的问卷复制题目，重复保存，加入另一题库。',
      '数字题年龄；他人私有问卷；纯文本/HTML/无效JSON/英文错误和断网响应',
      '提示全中文且无状态码或原始异常；空状态有引导；不显示私有问卷；复制保留内容，重复不新增；候选过滤正确。')
def test_bank_copy_and_readable_errors(client):
    pw=pytest.importorskip('playwright.sync_api')
    h=login(client);sid,qs=survey_with_questions(client,h,[question_input('number',title='问卷中的年龄',min_value=0,max_value=120)])
    other=login(client,'other');survey_with_questions(client,other,[question_input('text',title='他人的私有题目')])
    token=h['Authorization'].removeprefix('Bearer ')
    sock=socket.socket();sock.bind(('127.0.0.1',0));origin=f'http://127.0.0.1:{sock.getsockname()[1]}'
    server=uvicorn.Server(uvicorn.Config(create_app(Settings(mongo_uri=MONGO_URI,database=client.app.state.db.name)),log_level='error'))
    thread=threading.Thread(target=server.run,kwargs={'sockets':[sock]},daemon=True);thread.start()
    try:
        for _ in range(100):
            if server.started: break
            time.sleep(.1)
        assert server.started
        with pw.sync_playwright() as p:
            browser=p.chromium.launch(channel='msedge',headless=True);page=browser.new_page()
            page.add_init_script('sessionStorage.setItem("survey_token",'+json.dumps(token)+')')
            errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
            page.goto(origin);pw.expect(page.locator('#banks')).to_be_visible()
            for status,ctype,body in [(500,'text/plain','Internal Server Error'),(503,'text/html','<html>Unavailable</html>'),
                (500,'application/json','Invalid JSON'),(422,'application/json','{"detail":[{"msg":"Field required","loc":["body","title"]}]}'),
                (400,'application/json','{"detail":"Traceback internal_error"}')]:
                page.route('**/api/question-banks',lambda route,request,status=status,ctype=ctype,body=body:route.fulfill(status=status,content_type=ctype,body=body))
                page.locator('#notice').evaluate('(el)=>el.textContent=""')
                page.locator('#banks').click();pw.expect(page.locator('#notice')).not_to_be_empty()
                message=page.locator('#notice').inner_text()
                assert re.search('[\u3400-\u9fff]',message) and not re.search(r'[A-Za-z_{}\[\]0-9]',message)
                page.unroute('**/api/question-banks')
            page.route('**/api/question-banks',lambda route:route.abort())
            page.locator('#banks').click();pw.expect(page.locator('#notice')).to_contain_text('无法连接')
            page.unroute('**/api/question-banks')
            page.locator('#banks').click();page.locator('#newBank').click();page.locator('#bankName').fill('第一个库')
            page.get_by_role('button',name='保存题库').click();page.locator('[data-bank]').click()
            pw.expect(page.locator('#noCandidates')).to_contain_text('从我的问卷选择题目')
            assert page.locator('#existingFamily').count()==0
            page.locator('#copyFromSurvey').click()
            pw.expect(page.locator('#sourceSurvey option')).to_have_count(2)
            page.locator('#sourceSurvey').select_option(sid)
            pw.expect(page.locator('#sourceQuestions')).to_contain_text('数字范围：0～120')
            page.locator('[data-copy-question]').click()
            pw.expect(page.locator('#notice')).to_contain_text('原问卷保持不变')
            pw.expect(page.locator('[data-family]')).to_have_count(1)
            page.locator('#copyFromSurvey').click();page.locator('#sourceSurvey').select_option(sid);page.locator('[data-copy-question]').click()
            pw.expect(page.locator('#notice')).to_contain_text('无需重复保存')
            page.locator('#back').click();page.locator('#newBank').click();page.locator('#bankName').fill('第二个库')
            page.get_by_role('button',name='保存题库').click();page.locator('[data-bank]').last.click()
            pw.expect(page.locator('#existingFamily option')).to_have_count(1)
            page.get_by_role('button',name='加入当前题库',exact=True).click()
            pw.expect(page.locator('#notice')).to_contain_text('已加入')
            assert page.locator('#existingFamily').count()==0
            assert client.app.state.db.bank_questions.count_documents({})==1
            assert client.app.state.db.question_versions.count_documents({})==1
            assert client.app.state.db.surveys.find_one({'_id':sid})['questions']==qs
            empty=login(client,'empty_owner')
            empty_bank=client.post('/api/question-banks',headers=empty,json={'name':'空题库'}).json()['id']
            blank=browser.new_page()
            blank.add_init_script('sessionStorage.setItem("survey_token",'+json.dumps(empty['Authorization'].removeprefix('Bearer '))+')')
            blank.goto(origin);blank.locator('#banks').click();blank.locator('[data-bank]').click()
            blank.locator('#copyFromSurvey').click()
            pw.expect(blank.locator('#app')).to_contain_text('您的问卷中还没有可复制的题目')
            pw.expect(blank.locator('#mySurveys')).to_be_visible()
            assert blank.locator('#sourceSurvey').count()==0
            assert errors==[],errors
            browser.close()
    finally:
        server.should_exit=True;thread.join(timeout=10);sock.close()
        assert not thread.is_alive()
