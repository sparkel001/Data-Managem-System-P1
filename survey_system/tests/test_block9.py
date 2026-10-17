from pathlib import Path

def test_offline_docs(client):
    assert client.get("/docs").status_code == 200
    schema=client.get("/openapi.json").json()
    assert "/api/surveys/{sid}/stats/{qid}" in schema["paths"]
    assert "QuestionInput" in schema["components"]["schemas"]
    for asset in ("index.html","docs.html","app.js","docs.js","style.css"):
        content=(Path(__file__).parents[1]/"app"/"static"/asset).read_text(encoding="utf-8")
        assert "https://" not in content and "http://" not in content

def test_documentation_present():
    root=Path(__file__).parents[1]
    for name in ("DATABASE.md","API.md","LOGIC.md","MANUAL_TESTS.md","REPORT_TEMPLATE.md","AI_USAGE_LOG.md","TEST_RESULTS.md"):
        assert len((root/"docs"/name).read_text(encoding="utf-8")) > 100
    assert "MONGODB_URI" in (root/".env.example").read_text()
