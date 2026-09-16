from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from auth.api import get_current_student
from database.database import add_subject, list_subjects

router = APIRouter()


class SubjectIn(BaseModel):
    code: str
    name: str


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