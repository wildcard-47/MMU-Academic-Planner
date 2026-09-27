import hashlib
import os
from datetime import date
from database.database import add_student, get_student


def hash_password(password):
    salt = os.urandom(16).hex()
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt), 100_000).hex()
    return f"{salt}${digest}"

def default_trimester(today=None):
    today = today or date.today()
    start_year = today.year if today.month >= 7 else today.year - 1
    return f"{start_year}/{start_year + 1} T1"


def login(username, password):
    student = get_student(username)
    if student and check_password(password, student["stu_password"]):
        return student["stu_id"], True
    return None, False


def signup(username, password):
    if get_student(username):
        return False  # Student already exists
    return add_student(username, hash_password(password), default_trimester())

