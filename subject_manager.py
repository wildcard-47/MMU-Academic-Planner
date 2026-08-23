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


if __name__ == "__main__":
    add_assessment(subject, "Assignment 1", 20, 80)
    add_assessment(subject, "Quiz 1", 10, -5)   # should fail
    print(subject)