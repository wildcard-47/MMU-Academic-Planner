from auth.auth import login as auth_login
from auth.auth import signup as auth_signup
from fastapi import APIRouter, FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from database.database import get_student_by_id

router = APIRouter()

app = FastAPI()

class Credentials(BaseModel):
    username: str
    password: str


@app.get("/")
def read_root():
    return {"message": "Welcome to the MMU Academic Planner API!"}

@router.post("/api/signup")
def signup(credentials: Credentials):
    success = auth_signup(credentials.username, credentials.password)
    if success:
        return JSONResponse(content={"message": "Signup successful"}, status_code=200)
    else:
        return JSONResponse(content={"message": "Signup failed"}, status_code=400)


@router.post("/api/login")
def login(credentials: Credentials,request: Request):
    stu_id, success = auth_login(credentials.username, credentials.password)
    if success:
        request.session["stu_id"] = stu_id
        return JSONResponse(content={"message": "Login successful"}, status_code=200)
    else:
        return JSONResponse(content={"message": "Login failed"}, status_code=400)

@router.post("/api/logout")
def logout_route(request: Request):
    request.session.clear()
    return {"ok": True}

@router.get("/api/me")
def me_route(request: Request):
    stu_id = request.session.get("stu_id")
    print("session stu_id:", repr(stu_id))
    if stu_id is None:
        raise HTTPException(status_code=401, detail="Not logged in.")
    student = get_student_by_id(stu_id)
    print("student:", student)
    if not student:                       # catches None AND {}
        raise HTTPException(status_code=401, detail="Student not found.")
    return {"id": student["stu_id"], "username": student["stu_name"]}

