"""Optional real browser regression: python -m tests.browser_demo (requires Edge)."""
import socket
import threading
import time
from uuid import uuid4
from pathlib import Path
import uvicorn
from pymongo import MongoClient
from playwright.sync_api import sync_playwright, expect
from app.main import create_app
from app.config import Settings

name="survey_system_test_"+uuid4().hex
settings=Settings(database=name)
sock=socket.socket()
sock.bind(("127.0.0.1",0))
port=sock.getsockname()[1]
server=uvicorn.Server(uvicorn.Config(create_app(settings),log_level="error"))
thread=threading.Thread(target=server.run,kwargs={"sockets":[sock]},daemon=True)
thread.start()
try:
    for _ in range(100):
        if server.started: break
        time.sleep(.1)
    assert server.started
    with sync_playwright() as p:
        browser=p.chromium.launch(channel="msedge",headless=True)
        page=browser.new_page(viewport={"width":1280,"height":900})
        errors=[]
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.goto(f"http://127.0.0.1:{port}")
        page.locator("#username").fill("browser_user")
        page.locator("#password").fill("password123")
        page.locator("#register").click()
        expect(page.locator("#notice")).to_contain_text("注册成功")
        page.get_by_role("button",name="登录",exact=True).click()
        page.locator("#new").click()
        page.locator("#title").fill("浏览器演示问卷")
        page.locator("#anonymous").check()
        page.get_by_role("button",name="保存",exact=True).click()
        page.locator("#add").click()
        page.locator("#qt").fill("年龄")
        page.locator("#kind").select_option("number")
        page.locator("#minValue").fill("0")
        page.locator("#maxValue").fill("120")
        page.locator("#integer").check()
        page.get_by_role("button",name="保存题目").click()
        page.locator("#add").click()
        page.locator("#qt").fill("成人反馈")
        page.locator("#kind").select_option("text")
        page.get_by_role("button",name="保存题目").click()
        page.locator("[data-rule]").first.click()
        page.locator("#op").select_option("lt")
        page.locator("#value").fill("18")
        page.get_by_role("button",name="添加规则到列表").click()
        page.locator("#save").click()
        page.locator("#publish").click()
        expect(page.locator("#notice")).to_contain_text("已发布")
        share=page.locator('a[href^="/survey/"]').get_attribute("href")
        page.goto(f"http://127.0.0.1:{port}"+share)
        page.locator("#answer").fill("200")
        page.get_by_role("button",name="下一步").click()
        expect(page.locator("#notice")).to_contain_text("最大值")
        page.locator("#answer").fill("16")
        page.get_by_role("button",name="下一步").click()
        expect(page.get_by_role("heading",name="填写完成")).to_be_visible()
        page.locator("#submit").click()
        expect(page.get_by_role("heading",name="提交成功")).to_be_visible()
        page.goto(f"http://127.0.0.1:{port}")
        page.get_by_role("button",name="管理问卷").click()
        page.locator("#stats").click()
        expect(page.get_by_role("heading",name="总答卷数：1")).to_be_visible()
        expect(page.locator("#app")).to_contain_text("平均值：16")
        expect(page.locator("#app")).to_contain_text("不显示填写者身份")
        Path("test-results").mkdir(exist_ok=True)
        page.screenshot(path="test-results/browser-stats.png",full_page=True)
        page.set_viewport_size({"width":390,"height":844})
        assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth")
        assert errors == [], errors
        browser.close()
        print("Browser scenario: 1 passed, 0 failed (register/create/questions/rules/publish/validate/jump/submit/statistics/mobile width)")
finally:
    server.should_exit=True
    thread.join(timeout=10)
    sock.close()
    assert name.startswith("survey_system_test_") and name != "survey_system"
    with MongoClient(settings.mongo_uri) as client:
        client.drop_database(name)
