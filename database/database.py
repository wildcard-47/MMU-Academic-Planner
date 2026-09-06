import sqlite3

def create_database_tables():
    try:
        with sqlite3.connect("database/mmu_academic_planner.db") as conn:
            cursor = conn.cursor()
            #Create student table
            cursor.execute("create table if not exists students (stu_id integer primary key, stu_name text not null);")
            conn.commit()
            print("Students table created successfully.")
            #Create subject table
            cursor.execute("create table if not exists subjects (sub_id integer primary key, sub_code text not null, sub_name text not   null);")
            conn.commit()
            print("Subjects table created successfully.")

            #Create assessment table
            cursor.execute("create table if not exists assessments (assessment_id integer primary key, sub_code text not null, assessment_name text not null, weight integer , foreign key (sub_code) references subjects(sub_code));")
            conn.commit()
            print("Assessments table created successfully.")

            #Create score table
            cursor.execute("create table if not exists scores (score_id integer primary key, stu_id integer not null, assessment_id integer not null, score real not null, foreign key (stu_id) references students(stu_id), foreign key (assessment_id) references assessments(assessment_id));")
            conn.commit()
            print("Scores table created successfully.")

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

def add_assessment(subject_code, assessment_name, weight):
    try:
        with sqlite3.connect("database/mmu_academic_planner.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO assessments (sub_code, assessment_name, weight) VALUES (?, ?, ?)", (subject_code, assessment_name, weight))
            conn.commit()
            print(f"Assessment '{assessment_name}' added successfully.")
    except sqlite3.Error as e:
        print("Failed to add assessment:", e)

def add_score(student_id, assessment_id, score):
    try:
        with sqlite3.connect("database/mmu_academic_planner.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO scores (stu_id, assessment_id, score) VALUES (?, ?, ?)", (student_id, assessment_id, score))
            conn.commit()
            print(f"Score for student ID '{student_id}' in assessment ID '{assessment_id}' added successfully.")
    except sqlite3.Error as e:
        print("Failed to add score:", e)


def clean_database():
    try:
        with sqlite3.connect("database/mmu_academic_planner.db") as conn:
            cursor = conn.cursor()
            cursor.execute("drop table if exists students;")
            cursor.execute("drop table if exists subjects;")
            cursor.execute("drop table if exists assessments;")
            cursor.execute("drop table if exists scores;")
            conn.commit()
            print("Database cleaned successfully.")
    except sqlite3.Error as e:
        print("Failed to clean database:", e)


def init_data():
    clean_database()
    create_database_tables()
    add_student("Mayada")
    add_student("Mohammad")
    add_student("Rin")

    add_subject("MATH101", "Mathematics")
    add_subject("CS101", "Programming")
    add_subject("PHYS101", "Physics")


    add_assessment("MATH101", "Midterm Exam", 30)
    add_assessment("MATH101", "Final Exam", 70)
    add_assessment("CS101", "Midterm Exam", 30)
    add_assessment("CS101", "Final Exam", 70)
    add_assessment("PHYS101", "Midterm Exam", 30)
    add_assessment("PHYS101", "Final Exam", 70)

    add_score(1, 1, 85.0)
    add_score(1, 2, 90.0)
    add_score(1, 3, 78.0)