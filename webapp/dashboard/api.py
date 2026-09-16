from fastapi import APIRouter, FastAPI, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dashboard.dashboard import get_assessments_for_student, calculate_average, find_highest, find_lowest
from dashboard.grading import percent_to_letter
from auth.api import get_current_student

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

def load_subject_scores(stu_name):
    subjects = []
    for subject in get_assessments_for_student(stu_name):
        subjects.append(
            {"name": subject["sub_name"], "code": subject["sub_code"],"score" : subject["total_score"]}
        )
    return subjects

@router.get("/api/dashboard")
def get_dashboard(student=Depends(get_current_student)):
    subjects = load_subject_scores(student["stu_name"])
    rows = [{**s, "letter": percent_to_letter(s["score"])} for s in subjects]
    return {
        "subjects": rows,
        "average": calculate_average(subjects),
        "highest": find_highest(subjects),
        "lowest": find_lowest(subjects),
    }