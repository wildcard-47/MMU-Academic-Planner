# Sample data for testing (will later come from SQLite)
subject = {
    "id": 1,
    "name": "Programming",
    "code": "CSP1123",
    "assessments": []
}

def add_assessment(subject, name, weight, score):
    """
    Adds a new assessment to a subject's assessment list.
    Validates that weight and score are within acceptable ranges.
    Returns True if added successfully, False if invalid.
    """
    # Validation
    if not name.strip():
        print("Error: Assessment name cannot be empty.")
        return False

    if not (0 <= weight <= 100):
        print("Error: Weight must be between 0 and 100.")
        return False

    if not (0 <= score <= 100):
        print("Error: Score must be between 0 and 100.")
        return False

    # Create the assessment
    new_assessment = {
        "id": len(subject["assessments"]) + 1,
        "subject_id": subject["id"],
        "name": name,
        "weight": weight,
        "score": score
    }

    subject["assessments"].append(new_assessment)
    print(f"Assessment '{name}' added successfully.")
    return True

def calculate_weighted_contribution(score, weight):
    """
    Calculates how much an assessment contributes to the overall grade.
    Example: score=80, weight=20 -> contribution=16
    """
    return score * weight / 100


def calculate_subject_performance(subject):
    """
    Calculates the subject's current earned percentage
    by summing the weighted contribution of every assessment.
    """
    total = 0
    for assessment in subject["assessments"]:
        contribution = calculate_weighted_contribution(assessment["score"], assessment["weight"])
        total += contribution
    return total

if __name__ == "__main__":
    add_assessment(subject, "Assignment 1", 20, 80)
    add_assessment(subject, "Quiz 1", 10, -5)   # should fail
    print(subject)

    add_assessment(subject, "Quiz 1", 10, 70)  # add a valid second assessment
    performance = calculate_subject_performance(subject)
    print(f"Current subject performance: {performance}%")

    