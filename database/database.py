import sqlite3

try:
    with  sqlite3.connect("database/mmu_academic_planner.db") as conn:
    # interact with database
        print(f"Opened SQLite database with version {sqlite3.sqlite_version} successfully.")
except sqlite3.OperationalError as e:
    print("Failed to open database:", e)
