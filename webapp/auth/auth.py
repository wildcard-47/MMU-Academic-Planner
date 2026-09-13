from database.database import add_student, get_student, list_assessments_for_student

def login(username, password):
    student = get_student(username)
    if student and student[2] == password:
        return True
    return False

def signup(username, password):
    existing_student = get_student(username)
    if existing_student:
        return False  # Student already exists
    add_student(username, password)
    return True

def get_assessments_for_student(student_name):
    return list_assessments_for_student(student_name)