from database.database import list_assessments_for_student

def get_assessments_for_student(student_name):
    return list_assessments_for_student(student_name)


def get_dashboard_data():
    # Placeholder implementation - replace with actual dashboard data retrieval logic
    return {
        "subjects": [],
        "average": 0,
        "highest": None,
        "lowest": None
    }
