from typing import Dict, Optional

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from auth.api import get_current_student
from database.database import get_subject, list_assessments_for_subject, set_target_grade
from dashboard.grading import letter_to_minimum
from member1_subjects.logic import validate_score
from member2_grades.logic import (
    calculate_overall, convert_percentage, calculate_required_score,
    calculate_minimum_scores, calculate_what_if,
)

router = APIRouter()


class TargetIn(BaseModel):
    grade: Optional[str] = None

class WhatIfIn(BaseModel):
    scores: Dict[int, float]


def own_subject(student, sub_id):
    subject = get_subject(student["stu_id"], sub_id)
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found.")
    return subject


# Everything the Grade Planner page shows for one subject, calculated from
# the marks the student entered on the Marks page.
@router.get("/api/planner/{sub_id}")
def get_planner(sub_id: int, student=Depends(get_current_student)):
    subject = own_subject(student, sub_id)
    assessments = list_assessments_for_subject(sub_id)
    overall = calculate_overall(assessments)

    target = None
    if subject["target_grade"]:
        minimum_mark = letter_to_minimum(subject["target_grade"])
        required = calculate_required_score(minimum_mark, overall["current_earned"], overall["remaining_weight"])
        target = {
            "grade": subject["target_grade"],
            "minimum_mark": minimum_mark,
            "status": required["status"],
            "score": required["score"],
        }

    return {
        "subject": {
            "id": subject["sub_id"], "code": subject["sub_code"],
            "name": subject["sub_name"], "credit_hours": subject["credit_hours"],
        },
        "assessments": [
            {"id": a["assessment_id"], "name": a["assessment_name"], "weight": a["weight"], "score": a["score"]}
            for a in assessments
        ],
        "overall": overall,
        "target": target,
        "minimum_scores": calculate_minimum_scores(overall["current_earned"], overall["remaining_weight"]),
    }


@router.put("/api/planner/{sub_id}/target")
def save_target(sub_id: int, body: TargetIn, student=Depends(get_current_student)):
    own_subject(student, sub_id)
    if body.grade is not None and (body.grade == "F" or letter_to_minimum(body.grade) is None):
        raise HTTPException(status_code=400, detail="Pick a grade from A+ to D.")
    set_target_grade(sub_id, body.grade)
    return {"message": "Target saved"}


@router.post("/api/planner/{sub_id}/what-if")
def what_if(sub_id: int, body: WhatIfIn, student=Depends(get_current_student)):
    own_subject(student, sub_id)
    assessments = list_assessments_for_subject(sub_id)
    remaining_ids = []
    for a in assessments:
        if a["score"] is None:
            remaining_ids.append(a["assessment_id"])

    hypothetical = {}
    for assessment_id, value in body.scores.items():
        if assessment_id not in remaining_ids:
            continue
        score, error = validate_score(value)
        if error:
            raise HTTPException(status_code=400, detail=error)
        hypothetical[assessment_id] = score or 0

    return calculate_what_if(assessments, hypothetical)


@router.get("/api/planner-convert")
def convert(percentage: float, student=Depends(get_current_student)):
    if not 0 <= percentage <= 100:
        raise HTTPException(status_code=400, detail="Percentage must be between 0 and 100.")
    return convert_percentage(percentage)
