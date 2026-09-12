import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import auth.auth as auth
import database.database as db

#db.clean_database()
db.create_database_tables()

##testing signup
auth.signup("Mayada", "testpassword")

#testing signup with existing username
auth.signup("Mayada1", "testpassword123")


if auth.login("Mayada", "testpassword123"):
    print("Login successful.")
else:
    print("Login failed.")