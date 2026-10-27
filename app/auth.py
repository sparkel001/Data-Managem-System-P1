import hashlib
import hmac
import secrets
from datetime import datetime, timedelta, timezone
from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field
from pymongo.errors import DuplicateKeyError, PyMongoError
from .user_indexes import ensure_username_index

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
        raise HTTPException(401, "当前账号已不可用，请重新登录或联系管理员。")
    return user

def owned(database, survey_id, user):
    survey = database.surveys.find_one({"_id": survey_id, "owner_id": user["_id"]})
    if not survey:
        raise HTTPException(404, "问卷不存在，或您没有管理权限。")
    return survey

class Credentials(BaseModel):
    username: str = Field(min_length=3, max_length=40, pattern=r"^[a-zA-Z0-9_]+$")
    password: str = Field(min_length=8, max_length=128)

class RegistrationCredentials(Credentials):
    password: str = Field(min_length=8, max_length=16)

def digest(password, salt):
    return hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt), 600000).hex()

@router.post("/auth/register", status_code=201)
def register(data: RegistrationCredentials, database=Depends(db)):
    username = data.username.lower()
    if database.users.find_one({"username": username}, {"_id": 1}):
        raise HTTPException(409, "用户名已存在")
    # A preflight query alone cannot arbitrate concurrent registrations.
    # Recheck the DB constraint even if startup was skipped or an index removed.
    try:
        ready = ensure_username_index(database)
    except PyMongoError:
        ready = False
    if not ready:
        raise HTTPException(503, "暂时无法注册，请联系管理员检查重复账号及注册设置。")
    salt = secrets.token_hex(16)
    user = {"_id": str(uuid4()), "username": username, "salt": salt,
            "password_hash": digest(data.password, salt), "created_at": now()}
    try:
        database.users.insert_one(user)
    except DuplicateKeyError:
        raise HTTPException(409, "用户名已存在")
    return {"id": user["_id"], "username": user["username"]}

@router.post("/auth/login")
def login(data: Credentials, database=Depends(db)):
    matches = list(database.users.find({"username": data.username.lower()}).limit(2))
    if len(matches) > 1:
        raise HTTPException(409, "这个用户名对应多个历史账号，请联系管理员确认后再登录。")
    user = matches[0] if matches else None
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
