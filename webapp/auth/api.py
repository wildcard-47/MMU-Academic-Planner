from auth.auth import login as auth_login
from auth.auth import signup as auth_signup
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from database.database import get_student_by_id

router = APIRouter()


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
    stu_id, success = auth_login(credentials.username.strip(), credentials.password)
    if success:
        request.session["stu_id"] = stu_id
        return JSONResponse(content={"message": "Login successful"}, status_code=200)
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
