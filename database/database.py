import sqlite3

create_table = 'create table if not exists students (id integer primary key, name text not null);'
insert_data= "insert into students (name) values ('Mayada');"

try:
    with  sqlite3.connect("database/mmu_academic_planner.db") as conn:
    # interact with database
        print(f"Opened SQLite database with version {sqlite3.sqlite_version} successfully.")
        cursor = conn.cursor()
        cursor.execute(create_table)
        conn.commit()
        print("Table created successfully.")
        cursor.execute(insert_data)
        conn.commit()
        print("Data inserted successfully.")
except sqlite3.OperationalError as e:
    print("Failed to open database:", e)
