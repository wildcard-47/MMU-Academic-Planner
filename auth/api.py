from auth.auth import login as auth_login
from auth.auth import signup as auth_signup
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from database.database import get_student_by_id, list_trimesters_for_student, set_active_trimester
router = APIRouter()
from collections import defaultdict
from time import time

# Very simple in-memory brute-force protection: tracks failed login attempts
# per username. Resets on server restart, and won't work across multiple
# server instances - a real production system would use Redis or a shared
# database table instead. Good enough to block naive repeated guessing.
_failed_attempts = defaultdict(list)
MAX_ATTEMPTS = 5
LOCKOUT_SECONDS = 60


def _is_locked_out(username):
    now = time()
    attempts = [t for t in _failed_attempts[username] if now - t < LOCKOUT_SECONDS]
    _failed_attempts[username] = attempts
    return len(attempts) >= MAX_ATTEMPTS


def _record_failed_attempt(username):
    _failed_attempts[username].append(time())


class Credentials(BaseModel):
    username: str
    password: str


def get_current_student(request: Request):
    stu_id = request.session.get("stu_id")
    if stu_id is None:
        raise HTTPException(status_code=401, detail="Not logged in.")
    student = get_student_by_id(stu_id)
    if student is None:
        raise HTTPException(status_code=401, detail="Not logged in.")
    return student


@router.post("/api/signup")
def signup(credentials: Credentials):
    username = credentials.username.strip()
    if not username or not credentials.password:
        return JSONResponse(content={"detail": "Username and password are required."}, status_code=400)
    if len(credentials.password) < 6:
        return JSONResponse(content={"detail": "Password must be at least 6 characters."}, status_code=400)
    if auth_signup(username, credentials.password):
        return JSONResponse(content={"message": "Signup successful"}, status_code=200)
    return JSONResponse(content={"detail": "That username is already taken."}, status_code=400)


@router.post("/api/login")
def login(credentials: Credentials, request: Request):
    username = credentials.username.strip()

    if _is_locked_out(username):
        return JSONResponse(
            content={"detail": "Too many failed attempts. Try again in a minute."},
            status_code=429,
        )

    stu_id, success = auth_login(username, credentials.password)
    if success:
        request.session["stu_id"] = stu_id
        return JSONResponse(content={"message": "Login successful"}, status_code=200)

    _record_failed_attempt(username)
    return JSONResponse(content={"detail": "Wrong username or password."}, status_code=400)


@router.post("/api/logout")
def logout_route(request: Request):
    request.session.clear()
    return {"ok": True}


@router.get("/api/me")
def me_route(request: Request):
    student = get_current_student(request)
    return {
        "id": student["stu_id"],
        "username": student["stu_name"],
        "trimester": student["active_trimester"],
    }

@router.get("/api/trimesters")
def get_trimesters(request: Request):
    student = get_current_student(request)
    trimesters = list_trimesters_for_student(student["stu_id"])
    if student["active_trimester"] and student["active_trimester"] not in trimesters:
        trimesters.append(student["active_trimester"])
    return {"trimesters": trimesters, "active": student["active_trimester"]}


class TrimesterIn(BaseModel):
    trimester: str


@router.put("/api/trimesters")
def switch_trimester(body: TrimesterIn, request: Request):
    student = get_current_student(request)
    set_active_trimester(student["stu_id"], body.trimester.strip())
    return {"message": "Trimester updated"}