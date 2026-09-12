import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import auth.auth as auth
import database.database as db

db.create_database_tables()

##testing signup
auth.signup("Mayada", "testpassword")

#testing signup with existing username
auth.signup("Mayada", "testpassword123")

