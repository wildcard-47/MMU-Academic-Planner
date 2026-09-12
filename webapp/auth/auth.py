from database.database import add_user, get_user

def login(username, password):
    user = get_user(username)
    if user and user[2] == password:
        return True
    return False

def signup(username, password):
    existing_user = get_user(username)
    if existing_user:
        return False  # User already exists
    add_user(username, password)
    return True