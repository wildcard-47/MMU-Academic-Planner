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


# The subject where the student stands best, compared by position in the class
# (a smaller share = better, e.g. #1 of 5 beats #1 of 1 and #2 of 10).
# Subjects nobody else takes are skipped.
def position_share(subject):
    return subject["rank"] / subject["class_size"]


def find_best_subject_rank(subjects):
    ranked = [s for s in subjects if s["class_size"] > 1]
    if not ranked:
        return None
    best = ranked[0]
    for s in ranked:
        if position_share(s) < position_share(best):
            best = s
        elif position_share(s) == position_share(best) and s["class_size"] > best["class_size"]:
            best = s
    return best


def get_insight_message(subjects):
    ranked = [s for s in subjects if s["class_size"] > 1]
    if not ranked:
        return "No classmates are taking your subjects this trimester yet — subject ranks will appear once they do."

    firsts = [s["code"] for s in ranked if s["rank"] == 1]
    if len(firsts) == len(ranked):
        return f"🏆 You're ranked #1 in every subject you share with classmates ({', '.join(firsts)}) — amazing work!"
    if firsts:
        return f"🎉 You're ranked #1 in {', '.join(firsts)}. Keep it up!"

    best = find_best_subject_rank(ranked)
    worst = ranked[0]
    for s in ranked:
        if position_share(s) > position_share(worst):
            worst = s
    if best is worst:
        return f"💪 You're rank {best['rank']} of {best['class_size']} in {best['code']}. Check the Grade Planner to see what you need next."
    return (f"👍 Your strongest subject is {best['code']} (rank {best['rank']} of {best['class_size']}). "
            f"{worst['code']} (rank {worst['rank']} of {worst['class_size']}) needs the most attention.")


# Whether the student is still on course for the target they set in the Grade Planner.
def get_target_status(subject, assessments):
    if not subject["target_grade"]:
        return None
    overall = calculate_overall(assessments)
    result = calculate_required_score(
        letter_to_minimum(subject["target_grade"]), overall["current_earned"], overall["remaining_weight"]
    )
    return {"grade": subject["target_grade"], "status": result["status"], "score": result["score"]}


# GPA for every trimester the student has, plus the CGPA across all of them.
# Uses the current % of each subject, so it is a projection until every
# assessment is marked.
def get_gpa_history(stu_id):
    by_trimester = {}
    for subject in list_all_subjects_for_student(stu_id):
        score, completed = subject_current_score(list_assessments_for_subject(subject["sub_id"]))
        if score is None:
            continue
        if subject["trimester"] not in by_trimester:
            by_trimester[subject["trimester"]] = []
        by_trimester[subject["trimester"]].append(
            {"points": percent_to_points(score), "credit_hours": subject["credit_hours"]}
        )

    history = []
    all_subjects = []
    for trimester in sorted(by_trimester):
        rows = by_trimester[trimester]
        all_subjects.extend(rows)
        history.append({
            "trimester": trimester,
            "gpa": calculate_gpa(rows),
            "credits": sum(r["credit_hours"] for r in rows),
            "subjects": len(rows),
        })
    return history, calculate_gpa(all_subjects)


def get_dashboard_data(student):
    stu_id = student["stu_id"]
    trimester = student["active_trimester"]

    subjects = []
    attention = []
    setup_warnings = []
    for subject in list_subjects(stu_id, trimester):
        assessments = list_assessments_for_subject(subject["sub_id"])
        total_weight = sum(a["weight"] for a in assessments)
        if total_weight < 100:
            setup_warnings.append({"code": subject["sub_code"], "name": subject["sub_name"], "total_weight": total_weight})

        for a in assessments:
            if a["score"] is None:
                attention.append({
                    "assessment_name": a["assessment_name"], "weight": a["weight"],
                    "sub_name": subject["sub_name"], "sub_code": subject["sub_code"],
                })

        score, completed_weight = subject_current_score(assessments)
        if score is None:
            continue

        classmates = [
            row["total_score"] for row in get_class_scores(trimester, subject["sub_code"])
            if row["stu_id"] != stu_id
        ]
        rank, class_size = calculate_subject_rank(score, classmates)
        subjects.append({
            "id": subject["sub_id"],
            "name": subject["sub_name"],
            "code": subject["sub_code"],
            "credit_hours": subject["credit_hours"],
            "score": score,
            "completed_weight": completed_weight,
            "letter": percent_to_letter(score),
            "points": percent_to_points(score),
            "higher_than_percent": calculate_percentile(score, classmates),
            "classmates": len(classmates),
            "rank": rank,
            "class_size": class_size,
            "target": get_target_status(subject, assessments),
        })

    average = calculate_average(subjects)
    history, cgpa = get_gpa_history(stu_id)

    attention.sort(key=lambda a: a["weight"], reverse=True)

    return {
        "trimester": trimester,
        "subjects": subjects,
        "average": average,
        "gpa": calculate_gpa(subjects),
        "cgpa": cgpa,
        "history": history,
        "highest": find_highest(subjects),
        "lowest": find_lowest(subjects),
        "best_rank": find_best_subject_rank(subjects),
        "insight": get_insight_message(subjects),
        "attention": attention,
        "setup_warnings": setup_warnings,
    }
