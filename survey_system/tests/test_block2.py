from app.auth import owned
from fastapi import HTTPException
import pytest

def login(client, name="alice"):
    credentials = {"username": name, "password": "password123"}
    client.post("/api/auth/register", json=credentials)
    token = client.post("/api/auth/login", json=credentials).json()["access_token"]
    return {"Authorization": "Bearer " + token}

def test_auth(client):
    h = login(client)
    assert client.get("/api/auth/me", headers=h).status_code == 200
    assert client.get("/api/auth/me").status_code == 401
    assert client.post("/api/auth/login", json={"username":"alice", "password":"incorrect"}).status_code == 401
    assert client.post("/api/auth/register", json={"username":"alice", "password":"password123"}).status_code == 409
    user = client.app.state.db.users.find_one()
    assert user["password_hash"] != "password123"
    assert "password" not in user
    assert client.post("/api/auth/logout", headers=h).status_code == 200
    assert client.get("/api/auth/me", headers=h).status_code == 401

def test_ownership(client):
    database = client.app.state.db
    database.surveys.insert_one({"_id":"s", "owner_id":"a"})
    assert owned(database,"s",{"_id":"a"})["_id"] == "s"
    with pytest.raises(HTTPException) as e:
        owned(database,"s",{"_id":"b"})
    assert e.value.status_code == 404
