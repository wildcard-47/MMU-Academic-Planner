from fastapi import APIRouter, FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

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
    from auth.auth import signup as auth_signup
    success = auth_signup(credentials.username, credentials.password)
    if success:
        return JSONResponse(content={"message": "Signup successful"}, status_code=200)
    else:
        return JSONResponse(content={"message": "Signup failed"}, status_code=400)


@router.post("/api/login")
def login(credentials: Credentials):
    from auth.auth import login as auth_login
    success = auth_login(credentials.username, credentials.password)
    if success:
        return JSONResponse(content={"message": "Login successful"}, status_code=200)
    else:
        return JSONResponse(content={"message": "Login failed"}, status_code=400)


@router.get("/api/assessments/{student_name}")
def get_assessments(student_name: str):
    from auth.auth import get_assessments_for_student
    assessments = get_assessments_for_student(student_name)
    if assessments is not None:
        return JSONResponse(content={"assessments": assessments}, status_code=200)
    else:
        return JSONResponse(content={"message": "Failed to retrieve assessments"}, status_code=400)

