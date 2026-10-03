from fastapi import APIRouter, Depends

from auth.api import get_current_student
from dashboard.dashboard import get_dashboard_data

router = APIRouter()


# Dashboard for the logged-in student's active trimester. Comparisons
# (rank and percentile) are per subject: only classmates who take the same
# subject code in the same trimester are compared. There is no overall rank.
@router.get("/api/dashboard")
def get_dashboard(student=Depends(get_current_student)):
    return get_dashboard_data(student)