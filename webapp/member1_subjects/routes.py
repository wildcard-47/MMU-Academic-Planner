from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from auth.api import get_current_student
from database.database import (
    add_subject, list_subjects, get_subject, update_subject, delete_subject,
    list_assessments_for_subject, add_assessment, get_assessment, update_assessment, delete_assessment,
)
from member1_subjects.logic import validate_weight

router = APIRouter()


class SubjectIn(BaseModel):
    code: str
    name: str
    credit_hours: int = 3


class AssessmentIn(BaseModel):
    name: str
    weight: float


@router.get("/api/subjects")
def get_subjects(student=Depends(get_current_student)):
    return list_subjects(student["stu_id"], student["active_trimester"])


@router.post("/api/subjects")
def create_subject(body: SubjectIn, student=Depends(get_current_student)):
    code = body.code.strip()
    name = body.name.strip()
    if not code or not name:
        raise HTTPException(status_code=400, detail="Subject code and name are required.")

    subject_id = add_subject(student["stu_id"], student["active_trimester"], code, name, body.credit_hours)
    if subject_id is None:
        raise HTTPException(status_code=400, detail="Could not create subject.")
    return {"sub_id": subject_id, "code": code, "name": name}


@router.get("/api/subjects/{sub_id}/assessments")
def get_assessments(sub_id: int, student=Depends(get_current_student)):
    subject = get_subject(student["stu_id"], sub_id)
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found.")
    return list_assessments_for_subject(sub_id)


@router.post("/api/subjects/{sub_id}/assessments")
def create_assessment(sub_id: int, body: AssessmentIn, student=Depends(get_current_student)):
    subject = get_subject(student["stu_id"], sub_id)
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found.")

    weight, error = validate_weight(body.weight)
    if error:
        raise HTTPException(status_code=400, detail=error)

    existing = list_assessments_for_subject(sub_id)
    total_weight = 0
    for a in existing:
        total_weight = total_weight + a["weight"]

    if total_weight + weight > 100:
        raise HTTPException(status_code=400, detail="Total weight for this subject would exceed 100%.")

    add_assessment(sub_id, body.name.strip(), weight)
    return {"message": "Assessment added"}


@router.put("/api/subjects/{sub_id}")
def edit_subject(sub_id: int, body: SubjectIn, student=Depends(get_current_student)):
    subject = get_subject(student["stu_id"], sub_id)
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found.")
    update_subject(sub_id, body.name.strip(), body.credit_hours)
    return {"message": "Subject updated"}


@router.delete("/api/subjects/{sub_id}")
def remove_subject(sub_id: int, student=Depends(get_current_student)):
    subject = get_subject(student["stu_id"], sub_id)
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found.")
    delete_subject(sub_id)
    return {"message": "Subject deleted"}


@router.put("/api/subjects/{sub_id}/assessments/{assessment_id}")
def edit_assessment(sub_id: int, assessment_id: int, body: AssessmentIn, student=Depends(get_current_student)):
    subject = get_subject(student["stu_id"], sub_id)
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found.")

    assessment = get_assessment(student["stu_id"], assessment_id)
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found.")

    weight, error = validate_weight(body.weight)
    if error:
        raise HTTPException(status_code=400, detail=error)

    update_assessment(assessment_id, body.name.strip(), weight)
    return {"message": "Assessment updated"}


@router.delete("/api/subjects/{sub_id}/assessments/{assessment_id}")
def remove_assessment(sub_id: int, assessment_id: int, student=Depends(get_current_student)):
    assessment = get_assessment(student["stu_id"], assessment_id)
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found.")
    delete_assessment(assessment_id)
    return {"message": "Assessment deleted"}