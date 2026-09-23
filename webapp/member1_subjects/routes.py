from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from auth.api import get_current_student
from database.database import add_subject, list_subjects, list_assessments_for_subject, add_assessment
from member1_subjects.logic import validate_weight

router = APIRouter()


class SubjectIn(BaseModel):
    code: str
    name: str

class AssessmentIn(BaseModel):
    name: str
    weight: float

@router.get("/api/subjects")
def get_subjects(student=Depends(get_current_student)):
    return list_subjects()


@router.post("/api/subjects")
def create_subject(body: SubjectIn, student=Depends(get_current_student)):
    code = body.code.strip()
    name = body.name.strip()
    if not code or not name:
        raise HTTPException(status_code=400, detail="Subject code and name are required.")
    add_subject(code, name)
    return {"code": code, "name": name}

@router.get("/api/subjects/{sub_code}/assessments")
def get_assessments(sub_code: str, student=Depends(get_current_student)):
    return list_assessments_for_subject(sub_code)


@router.post("/api/subjects/{sub_code}/assessments")
def create_assessment(sub_code: str, body: AssessmentIn, student=Depends(get_current_student)):
    weight, error = validate_weight(body.weight)
    if error:
        raise HTTPException(status_code=400, detail=error)

    existing = list_assessments_for_subject(sub_code)
    total_weight = 0
    for a in existing:
        total_weight = total_weight + a["weight"]

    if total_weight + weight > 100:
        raise HTTPException(status_code=400, detail="Total weight for this subject would exceed 100%.")

    add_assessment(sub_code, body.name.strip(), weight)
    return {"message": "Assessment added"}