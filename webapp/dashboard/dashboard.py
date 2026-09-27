from database.database import (
    list_subjects, list_all_subjects_for_student, list_assessments_for_subject,
    get_class_scores_for_subject,
)
from dashboard.grading import (
    percent_to_letter, percent_to_points, calculate_gpa, letter_to_minimum, current_percentage,
)
from member2_grades.logic import calculate_overall, calculate_required_score


# Current % in one subject (shared current_percentage) plus the weight marked so far.
# Returns (score, completed_weight); score is None when nothing is marked.
def subject_current_score(assessments):
    completed_weight = sum(a["weight"] for a in assessments if a["score"] is not None)
    return current_percentage(assessments), completed_weight


# Every classmate's current % in one subject code and trimester, worked out with
# the same function as the student's own score, so equal marks give equal scores.
def get_class_scores(trimester, code):
    per_student = {}
    for row in get_class_scores_for_subject(trimester, code):
        if row["stu_id"] not in per_student:
            per_student[row["stu_id"]] = []
        per_student[row["stu_id"]].append(row)
    scores = []
    for stu_id, assessments in per_student.items():
        score = current_percentage(assessments)
        if score is not None:
            scores.append({"stu_id": stu_id, "total_score": score})
    return scores


# Average weighted by credit hours, so a 4-credit subject counts more than a 2-credit one.
def calculate_average(subjects):
    total_credits = sum(s["credit_hours"] for s in subjects)
    if total_credits == 0:
        return 0
    return sum(s["score"] * s["credit_hours"] for s in subjects) / total_credits

def find_highest(subjects):
    return max(subjects, key=lambda s: s["score"]) if subjects else None

def find_lowest(subjects):
    return min(subjects, key=lambda s: s["score"]) if subjects else None


def calculate_percentile(my_score, other_scores):
    if not other_scores:
        return None
    higher_than_count = sum(1 for score in other_scores if score < my_score)
    return round((higher_than_count / len(other_scores)) * 100)


# Rank inside one subject: 1 + number of classmates with a higher score.
# Everyone in the subject has the same assessments, so this is a fair comparison.
# (There is no overall class rank: students take different subjects, so their
# averages can't be compared fairly.)
def calculate_subject_rank(my_score, other_scores):
    rank = 1 + sum(1 for score in other_scores if score > my_score)
    return rank, len(other_scores) + 1
