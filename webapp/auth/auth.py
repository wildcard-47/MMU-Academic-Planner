from database.database import add_student, get_student

def login(username, password):
    student = get_student(username)
    if student and student[2] == password:
         return student[0], student
    return None, None

def signup(username, password):
    existing_student = get_student(username)
    if existing_student:
        return False  # Student already exists
    add_student(username, password)
    return True

