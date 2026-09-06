import sqlite3

def create_database_tables():
    try:
        with sqlite3.connect("database/mmu_academic_planner.db") as conn:
            cursor = conn.cursor()
            #Add student table
            cursor.execute("create table if not exists students (stu_id integer primary key, stu_name text not null);")
            conn.commit()
            print("Students table created successfully.")
            #Add subject table
            cursor.execute("create table if not exists subjects (sub_id integer primary key, sub_code text not null, sub_name text not null);")
            conn.commit()
            print("Subjects table created successfully.")

    except sqlite3.Error as e:
        print("Failed to create database:", e)
        

def add_student(name):
    try:
        with sqlite3.connect("database/mmu_academic_planner.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO students (stu_name) VALUES (?)", (name,))
            conn.commit()
            print(f"Student '{name}' added successfully.")
    except sqlite3.Error as e:
        print("Failed to add student:", e)
insert_data= "insert into students (stu_name) values ('Mayada');"


def add_subject(code, name):
    try:
        with sqlite3.connect("database/mmu_academic_planner.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO subjects (sub_code, sub_name) VALUES (?, ?)", (code, name))
            conn.commit()
            print(f"Subject '{name}' added successfully.")
    except sqlite3.Error as e:
        print("Failed to add subject:", e)


def clean_database():
    try:
        with sqlite3.connect("database/mmu_academic_planner.db") as conn:
            cursor = conn.cursor()
            cursor.execute("drop table if exists students;")
            cursor.execute("drop table if exists subjects;")
            conn.commit()
            print("Database cleaned successfully.")
    except sqlite3.Error as e:
        print("Failed to clean database:", e)


clean_database()
create_database_tables()
add_student("Mayada")
add_student("Mohammad")
add_student("Rin")

add_subject("MATH101", "Mathematics")
add_subject("CS101", "Programming")
add_subject("PHYS101", "Physics")