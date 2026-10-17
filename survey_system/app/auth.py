import hashlib
import hmac
import secrets
from datetime import datetime, timedelta, timezone
from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field
from pymongo.errors import DuplicateKeyError

router = APIRouter(prefix="/api")
def now():
    return datetime.now(timezone.utc)
def db(request: Request):
    return request.app.state.db

def current_user(request: Request, database=Depends(db)):
    token = request.headers.get("Authorization", "").removeprefix("Bearer ")
    session = database.sessions.find_one({"_id": hashlib.sha256(token.encode()).hexdigest(), "expires_at": {"$gt": now()}})
    if not session:
        raise HTTPException(401, "请先登录")
    user = database.users.find_one({"_id": session["user_id"]})
    if not user:
        raise HTTPException(401, "用户不存在")
    return user

def owned(database, survey_id, user):
    survey = database.surveys.find_one({"_id": survey_id, "owner_id": user["_id"]})
    if not survey:
        raise HTTPException(404, "问卷不存在")
    return survey

class Credentials(BaseModel):
    username: str = Field(min_length=3, max_length=40, pattern=r"^[a-zA-Z0-9_]+$")
    password: str = Field(min_length=8, max_length=128)

def digest(password, salt):
    return hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt), 600000).hex()

@router.post("/auth/register", status_code=201)
def register(data: Credentials, database=Depends(db)):
    salt = secrets.token_hex(16)
    user = {"_id": str(uuid4()), "username": data.username.lower(), "salt": salt,
            "password_hash": digest(data.password, salt), "created_at": now()}
    try:
        database.users.insert_one(user)
    except DuplicateKeyError:
        raise HTTPException(409, "用户名已存在")
    return {"id": user["_id"], "username": user["username"]}

@router.post("/auth/login")
def login(data: Credentials, database=Depends(db)):
    user = database.users.find_one({"username": data.username.lower()})
    if not user or not hmac.compare_digest(digest(data.password, user["salt"]), user["password_hash"]):
        raise HTTPException(401, "用户名或密码错误")
    token = secrets.token_urlsafe(32)
    database.sessions.insert_one({"_id": hashlib.sha256(token.encode()).hexdigest(), "user_id": user["_id"], "expires_at": now() + timedelta(hours=12)})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/auth/me")
def me(user=Depends(current_user)):
    return {"id": user["_id"], "username": user["username"]}

@router.post("/auth/logout")
def logout(request: Request, user=Depends(current_user), database=Depends(db)):
    token = request.headers.get("Authorization", "").removeprefix("Bearer ")
    database.sessions.delete_one({"_id": hashlib.sha256(token.encode()).hexdigest()})
    return {"ok": True}
