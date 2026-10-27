from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from .config import Settings
from .statistics import router as stats_router
from .responses import router as response_router
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from .logic import router as logic_router
from .questions import router as question_router
from .surveys import router as survey_router
from .auth import router as auth_router
from .migrations import migrate
from .banks import router as bank_router
from .reuse import router as reuse_router
from .cross_statistics import router as cross_router
from .user_indexes import ensure_username_index, username_index_ready
from .errors import install_error_handlers


def create_app(settings=None):
    settings = settings or Settings()
    @asynccontextmanager
    async def lifespan(app):
        client = MongoClient(settings.mongo_uri, serverSelectionTimeoutMS=3000, tz_aware=True)
        app.state.db = client[settings.database]
        ensure_username_index(app.state.db)
        app.state.db.sessions.create_index("expires_at", expireAfterSeconds=0)
        app.state.db.surveys.create_index("owner_id")
        app.state.db.responses.create_index("survey_id")
        app.state.db.responses.create_index("once_key", unique=True, partialFilterExpression={"once_key":{"$type":"string"}})
        migrate(app.state.db)
        yield
        client.close()
    app = FastAPI(title="MongoDB 问卷系统", lifespan=lifespan, docs_url=None, redoc_url=None)
    install_error_handlers(app)
    app.include_router(question_router)
    app.include_router(logic_router)
    app.include_router(response_router)
    app.include_router(stats_router)
    app.include_router(auth_router)
    app.include_router(survey_router)
    app.include_router(bank_router)
    app.include_router(reuse_router)
    app.include_router(cross_router)
    @app.get("/api/health")
    def health():
        try:
            app.state.db.command("ping")
            if not username_index_ready(app.state.db):
                return JSONResponse(status_code=503, content={"status": "degraded", "registration": "blocked",
                    "detail": "用户名唯一索引未就绪，请人工检查重复账号或索引配置"})
            return {"status": "ok", "database": settings.database}
        except PyMongoError:
            return JSONResponse(status_code=503, content={"status": "unavailable"})
    static = Path(__file__).parent / "static"
    app.mount("/static", StaticFiles(directory=static), name="static")
    @app.get("/docs", include_in_schema=False)
    def offline_docs():
        return FileResponse(static / "docs.html")
    @app.get("/", include_in_schema=False)
    @app.get("/survey/{sid}", include_in_schema=False)
    def page(sid: str = ""):
        return FileResponse(static / "index.html")
    return app

app = create_app()
