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