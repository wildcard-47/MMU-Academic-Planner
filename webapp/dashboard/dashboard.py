from database.database import list_assessments_for_student

def calculate_average(subjects):
    if not subjects:
        return 0
    return sum(s["score"] for s in subjects) / len(subjects)

def find_highest(subjects):
    return max(subjects, key=lambda s: s["score"]) if subjects else None

def find_lowest(subjects):
    return min(subjects, key=lambda s: s["score"]) if subjects else None

def get_assessments_for_student(student_name):
    return list_assessments_for_student(student_name)

def get_dashboard_data():
    return {
        "subjects": [],
        "average": 0,
        "highest": None,
        "lowest": None
    }
