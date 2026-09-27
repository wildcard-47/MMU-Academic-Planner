#MMU grading scale: (minimum %, letter, grade point).
#Used everywhere in the app so the letter, the GPA and the grade planner agree.
GRADE_SCALE = [
    (90, "A+", 4.00),
    (80, "A", 4.00),
    (75, "A-", 3.67),
    (70, "B+", 3.33),
    (65, "B", 3.00),
    (60, "B-", 2.67),
    (55, "C+", 2.33),
    (50, "C", 2.00),
    (47, "C-", 1.67),
    (44, "D+", 1.33),
    (40, "D", 1.00),
    (0, "F", 0.00),
]


#Rounds a mark to 1 decimal. Every page uses this one function, so the same
#marks always give the same % and the same letter everywhere in the app.
def round_mark(value):
    if value is None:
        return None
    return round(value, 1)


#Current % of a subject = weighted average of the assessments marked so far,
#rounded with round_mark. Returns None when nothing is marked.
#assessments: list of {"weight": float, "score": float or None}
def current_percentage(assessments):
    total = 0
    completed_weight = 0
    for a in assessments:
        if a["score"] is not None:
            total = total + a["weight"] * a["score"]
            completed_weight = completed_weight + a["weight"]
    if completed_weight == 0:
        return None
    return round_mark(total / completed_weight)


#function to get the grade letter from the score
def percent_to_letter(score):
    if score is None:
        return None
    if score < 0 or score > 100:
        return "Invalid score"
    for minimum, letter, points in GRADE_SCALE:
        if score >= minimum:
            return letter
    return "F"


#function to get the grade point (0.00 - 4.00) from the score
def percent_to_points(score):
    if score is None:
        return None
    for minimum, letter, points in GRADE_SCALE:
        if score >= minimum:
            return points
    return 0.0


#function to get the minimum % needed for a letter grade, e.g. "B+" -> 70
def letter_to_minimum(letter):
    for minimum, grade, points in GRADE_SCALE:
        if grade == letter:
            return minimum
    return None


#GPA = sum(grade point x credit hours) / sum(credit hours)
#subjects: list of {"points": float, "credit_hours": int}
def calculate_gpa(subjects):
    total_credits = 0
    total_points = 0
    for s in subjects:
        if s["points"] is None:
            continue
        total_credits = total_credits + s["credit_hours"]
        total_points = total_points + s["points"] * s["credit_hours"]
    if total_credits == 0:
        return None
    return round(total_points / total_credits, 2)
