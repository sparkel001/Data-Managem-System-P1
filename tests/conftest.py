import re
import uuid
import pytest
from fastapi.testclient import TestClient
from pymongo import MongoClient
from app.config import Settings
from tests.mongo_config import MONGO_URI
from app.main import create_app

pytest_plugins = ["tests.audit_plugin"]

@pytest.fixture
def client(request):
    name = "survey_system_test_" + uuid.uuid4().hex
    # Never inherit MONGODB_DATABASE, including when a developer's .env is set.
    assert re.fullmatch(r"survey_system_test_[0-9a-f]{32}", name)
    settings = Settings(mongo_uri=MONGO_URI, database=name)
    request.node.audit_database = name

    def cleanup():
        assert re.fullmatch(r"survey_system_test_[0-9a-f]{32}", name)
        assert name != "survey_system"
        with MongoClient(settings.mongo_uri, serverSelectionTimeoutMS=3000) as connection:
            connection.drop_database(name)

    # Finalizer also runs after assertions/setup failures; it only drops this UUID.
    request.addfinalizer(cleanup)
    app = create_app(settings)
    with TestClient(app) as client:
        assert app.state.db.name == name
        app.state.db.command("ping")
        yield client
