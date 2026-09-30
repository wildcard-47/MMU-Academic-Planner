# Member 2 - Grade Planner calculations.
# These are the same formulas as the original stand-alone grade planner
# (overall performance, target grade, minimum score required, what-if),
# but they now work on the student's real marks from the main database
# instead of numbers typed in by hand.

from dashboard.grading import GRADE_SCALE, percent_to_letter, percent_to_points, round_mark, current_percentage


# 1 - CALCULATE OVERALL PERFORMANCE
# assessments: list of {"weight": float, "score": float or None}
def calculate_overall(assessments):
    current_earned = 0
    completed_weight = 0
    setup_weight = 0

    for a in assessments:
        setup_weight = setup_weight + a["weight"]
        if a["score"] is not None:
            current_earned = current_earned + a["score"] * a["weight"] / 100
            completed_weight = completed_weight + a["weight"]

    # Only assessments that exist and are not marked yet can still add marks.
    # If the subject is not fully set up (setup_weight < 100), the missing part
    # is not counted, and the page shows a warning.
    remaining_weight = setup_weight - completed_weight

    current_performance = current_percentage(assessments)
    highest_possible = min(100, current_earned + remaining_weight)

    return {
        "current_earned": current_earned,
        "completed_weight": completed_weight,
        "remaining_weight": remaining_weight,
        "setup_weight": setup_weight,
        "current_performance": current_performance,
        "current_letter": percent_to_letter(current_performance),
        "highest_possible": round_mark(highest_possible),
        "highest_letter": percent_to_letter(round_mark(highest_possible)),
        "lowest_possible": round_mark(current_earned),
        "lowest_letter": percent_to_letter(round_mark(current_earned)),
    }


# 2 - CONVERT TO PERCENTAGE / GRADE
def convert_percentage(percentage):
    percentage = round_mark(percentage)
    return {
        "percentage": percentage,
        "letter": percent_to_letter(percentage),
        "points": percent_to_points(percentage),
    }


# 3 - MINIMUM SCORE REQUIRED
# The average mark needed on everything that is not marked yet to finish
# with at least minimum_mark overall.
def calculate_required_score(minimum_mark, current_earned, remaining_weight):
    if remaining_weight <= 0:
        if round_mark(current_earned) >= minimum_mark:
            return {"status": "achieved", "score": None}
        return {"status": "impossible", "score": None}

    required_score = (minimum_mark - current_earned) / remaining_weight * 100

    if required_score <= 0:
        return {"status": "achieved", "score": None}
    if required_score > 100:
        return {"status": "impossible", "score": None}
    return {"status": "needed", "score": round(required_score, 2)}


# The minimum-score table for every grade (A+ down to D).
def calculate_minimum_scores(current_earned, remaining_weight):
    table = []
    for minimum, letter, points in GRADE_SCALE:
        if letter == "F":
            continue
        required = calculate_required_score(minimum, current_earned, remaining_weight)
        table.append({
            "letter": letter,
            "minimum_mark": minimum,
            "points": points,
            "status": required["status"],
            "score": required["score"],
        })
    return table


# 4 - WHAT-IF CALCULATOR
# hypothetical: {assessment_id: score} for the assessments not marked yet.
def calculate_what_if(assessments, hypothetical):
    projected = 0
    for a in assessments:
        score = a["score"]
        if score is None:
            score = hypothetical.get(a["assessment_id"], 0)
        projected = projected + score * a["weight"] / 100

    projected = round_mark(projected)
    return {
        "projected_score": projected,
        "letter": percent_to_letter(projected),
        "points": percent_to_points(projected),
    }
