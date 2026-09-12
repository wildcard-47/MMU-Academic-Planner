from database.database import add_user, get_user


def login(username, password):
    user = get_user(username)
    if user and user[2] == password:
        return True
    return False