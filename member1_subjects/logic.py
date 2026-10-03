def calculate_subject_performance(assessments):
    completed = []
    remaining = []

    for a in assessments:
        if a["score"] is not None:
            completed.append(a)
        else:
            remaining.append(a)

    earned = 0
    for a in completed:
        earned = earned + (a["weight"] * a["score"] / 100)

    completed_weight = 0
    for a in completed:
        completed_weight = completed_weight + a["weight"]

    remaining_weight = 0
    for a in remaining:
        remaining_weight = remaining_weight + a["weight"]

    return {
        "earned": earned,
        "completed_weight": completed_weight,
        "remaining_weight": remaining_weight,
    }

def validate_weight(value):
    try:
        weight = float(value)
    except ValueError:
        return None, "Weight must be a number."

    if not 0 <= weight <= 100:
        return None, "Weight must be between 0 and 100."

    return weight, None

def validate_score(value):
    if value == "" or value is None:
        return None, None

    try:
        score = float(value)
    except ValueError:
        return None, "Score must be a number."

    if not 0 <= score <= 100:
        return None, "Score must be between 0 and 100."

    return score, None

# A trimester is written as "YYYY/YYYY Tn", for example "2026/2027 T1".
# Everyone must use the same format, otherwise classmates in the same
# trimester would not be matched when a subject is copied.

def validate_trimester(value):
    value = (value or "").strip()
    parts = value.split(" ")
    if len(parts) != 2:
        return None, "Trimester must look like 2026/2027 T1."

    years, term = parts
    year_parts = years.split("/")
    if len(year_parts) != 2:
        return None, "Trimester must look like 2026/2027 T1."
    for y in year_parts:
        if not y.isdigit() or len(y) != 4:
            return None, "Trimester must look like 2026/2027 T1."
    if int(year_parts[1]) != int(year_parts[0]) + 1:
        return None, "The second year must follow the first, e.g. 2026/2027."
    if term not in ("T1", "T2", "T3"):
        return None, "Trimester must be T1, T2 or T3."

    return value, None