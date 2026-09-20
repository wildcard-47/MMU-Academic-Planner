from fastapi import APIRouter, Depends
from dashboard.dashboard import (
    get_assessments_for_student, calculate_average, find_highest, find_lowest,
    calculate_percentile, get_all_students_overall_averages, calculate_rank,
    get_insight_message, find_next_rank_average,
)
from dashboard.grading import percent_to_letter
from database.database import (
    get_all_scores_for_subject, get_unscored_assessments_for_student,
)
from auth.api import get_current_student


router = APIRouter()

def build_quick_win(student, rows, average, other_averages):
    if not rows:
        return None

    target_average = find_next_rank_average(average, other_averages)
    if target_average is None:
        return {"status": "already_first"}

    weakest = min(rows, key=lambda s: s["score"])
    performance = get_subject_performance(student["stu_id"], weakest["code"])
    if performance["remaining_weight"] <= 0:
        return {"status": "no_remaining_assessments", "subject_name": weakest["name"]}

    # Overall average is a plain mean of subject scores, so raising one
    # subject's score by delta raises the average by delta / num_subjects.
    # Solve for the subject score that would just clear the next rank up.
    num_subjects = len(rows)
    target_subject_score = weakest["score"] + num_subjects * (target_average - average)

    required = required_score_for_target(
        performance["earned"], performance["remaining_weight"], target_subject_score
    )
    if required > 100:
        return {"status": "not_achievable", "subject_name": weakest["name"]}
    return {
        "status": "ok",
        "subject_name": weakest["name"],
        "required_score": max(0, required),
    }



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
    rows = []
    for s in subjects:
        others = [
            row["total_score"] for row in get_all_scores_for_subject(s["code"])
            if row["stu_id"] != student["stu_id"]
        ]
        rows.append({
            **s,
            "letter": percent_to_letter(s["score"]),
            "higher_than_percent": calculate_percentile(s["score"], others),
        })

    average = calculate_average(subjects)

    all_averages = get_all_students_overall_averages()
    other_averages = [a["average"] for a in all_averages if a["stu_id"] != student["stu_id"]]
    rank, total = calculate_rank(average, other_averages)

    return {
        "subjects": rows,
        "average": average,
        "highest": find_highest(subjects),
        "lowest": find_lowest(subjects),
        "rank": rank,
        "class_size": total,
        "insight": get_insight_message(rank, total),
        "attention": get_unscored_assessments_for_student(student["stu_id"]),
        "quick_win": build_quick_win(student, rows, average, other_averages),
    }