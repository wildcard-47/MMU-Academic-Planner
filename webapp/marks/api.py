from typing import Optional

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from auth.api import get_current_student
from database.database import list_assessments_with_scores, get_assessment_by_id, save_score
from member1_subjects.logic import calculate_subject_performance, validate_score
from dashboard.grading import percent_to_letter

router = APIRouter()

class MarkIn(BaseModel):
    score: Optional[float] = None

@router.get("/api/marks")
def get_marks(student=Depends(get_current_student)):
    subjects = {}
    for row in list_assessments_with_scores(student["stu_id"]):
        code = row["sub_code"]
        if code not in subjects:
            subjects[code] = {"code": code, "name": row["sub_name"], "assessments": []}
        subjects[code]["assessments"].append({
            "id": row["assessment_id"],
            "name": row["assessment_name"],
            "weight": row["weight"],
            "score": row["score"],
        })

    for subject in subjects.values():
        performance = calculate_subject_performance(subject["assessments"])
        completed_weight = performance["completed_weight"]
        current = performance["earned"] / completed_weight * 100 if completed_weight > 0 else None
        subject["summary"] = {
            **performance,
            "current": current,
            "letter": percent_to_letter(current) if current is not None else None,
        }

    return list(subjects.values())


@router.put("/api/marks/{assessment_id}")
def update_mark(assessment_id: int, body: MarkIn, student=Depends(get_current_student)):
    if not get_assessment_by_id(assessment_id):
        raise HTTPException(status_code=404, detail="Assessment not found.")
    score, error = validate_score(body.score)
    if error:
        raise HTTPException(status_code=400, detail=error)
    save_score(student["stu_id"], assessment_id, score)
    return {"message": "Mark saved"}