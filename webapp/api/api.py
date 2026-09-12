from fastapi import APIRouter, FastAPI
from fastapi.responses import JSONResponse


router = APIRouter()

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the MMU Academic Planner API!"}

@router.post("/api/signup")
def signup(username: str, password: str):
    from auth.auth import signup as auth_signup
    success = auth_signup(username, password)
    if success:
        return JSONResponse(content={"message": "Signup successful"}, status_code=200)
    else:
        return JSONResponse(content={"message": "Signup failed"}, status_code=400)

@router.post("/api/login")
def login(username: str, password: str):
    from auth.auth import login as auth_login
    success = auth_login(username, password)
    if success:
        return JSONResponse(content={"message": "Login successful"}, status_code=200)
    else:
        return JSONResponse(content={"message": "Login failed"}, status_code=400)

