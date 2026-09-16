from fastapi import APIRouter, FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dashboard.dashboard import get_assessments_for_student

router = APIRouter()

app = FastAPI()

class Credentials(BaseModel):
    username: str
    password: str

@router.get("/api/assessments/{student_name}")
def get_assessments(student_name: str):
    assessments = get_assessments_for_student(student_name)
    if assessments is not None:
        return JSONResponse(content={"assessments": assessments}, status_code=200)
    else:
        return JSONResponse(content={"message": "Failed to retrieve assessments"}, status_code=400)

@router.get("/api/dashboard")
def get_dashboard():
    from dashboard.dashboard import get_dashboard_data
    dashboard_data = get_dashboard_data()
    if dashboard_data is not None:
        return JSONResponse(content={"dashboard": dashboard_data}, status_code=200)
    else:
        return JSONResponse(content={"message": "Failed to retrieve dashboard data"}, status_code=400)