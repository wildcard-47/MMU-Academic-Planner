from random import random
import sqlite3
import os

DB_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(DB_DIR, "mmu_academic_planner.db")

def create_database_tables():
    try:
        with sqlite3.connect(os.path.join(DB_DIR, "mmu_academic_planner.db")) as conn:
            cursor = conn.cursor()
            cursor.execute("create table if not exists students (stu_id integer primary key, stu_name text not null, stu_password text not null);")
            conn.commit()
            print("Students table created successfully.")
            cursor.execute("create table if not exists subjects (sub_id integer primary key, sub_code text not null, sub_name text not   null);")
            conn.commit()
            print("Subjects table created successfully.")
            cursor.execute("create table if not exists assessments (assessment_id integer primary key, sub_code text not null, assessment_name text not null, weight integer , foreign key (sub_code) references subjects(sub_code));")
            conn.commit()
            print("Assessments table created successfully.")
            cursor.execute("create table if not exists scores (score_id integer primary key, stu_id integer not null, assessment_id integer not null, score real not null, foreign key (stu_id) references students(stu_id), foreign key (assessment_id) references assessments(assessment_id));")
            conn.commit()
            print("Scores table created successfully.")

    except sqlite3.Error as e:
        print("Failed to create database:", e)


def add_student(name, password):
    try:
        with sqlite3.connect(os.path.join(DB_DIR, "mmu_academic_planner.db")) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO students (stu_name, stu_password) VALUES (?, ?)", (name, password))
            conn.commit()
            print(f"Student '{name}' added successfully.")
    except sqlite3.Error as e:
        print("Failed to add student:", e)


def get_student_by_id(student_id):
    try:
        with sqlite3.connect(os.path.join(DB_DIR, "mmu_academic_planner.db")) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            row = cursor.execute(
                "SELECT * FROM students WHERE stu_id = ?",(student_id,),).fetchone()
            if row is None:
                return None
            return dict(row) 
    except sqlite3.Error as e:
        print("Failed to get student by ID:", e)
        return None

def get_student(username):
    try:
        with sqlite3.connect(os.path.join(DB_DIR, "mmu_academic_planner.db")) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM students WHERE stu_name = ?", (username,))
            student = cursor.fetchone()
            return student
    except sqlite3.Error as e:
        print("Failed to get student:", e)
        return None


def add_subject(code, name):
    try:
        with sqlite3.connect(os.path.join(DB_DIR, "mmu_academic_planner.db")) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO subjects (sub_code, sub_name) VALUES (?, ?)", (code, name))
            conn.commit()
            print(f"Subject '{name}' added successfully.")
    except sqlite3.Error as e:
        print("Failed to add subject:", e)

def add_assessment(subject_code, assessment_name, weight):
    try:
        with sqlite3.connect(os.path.join(DB_DIR, "mmu_academic_planner.db")) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO assessments (sub_code, assessment_name, weight) VALUES (?, ?, ?)", (subject_code, assessment_name, weight))
            conn.commit()
            print(f"Assessment '{assessment_name}' added successfully.")
    except sqlite3.Error as e:
        print("Failed to add assessment:", e)

def add_score(student_id, assessment_id, score):
    try:
        with sqlite3.connect(os.path.join(DB_DIR, "mmu_academic_planner.db")) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO scores (stu_id, assessment_id, score) VALUES (?, ?, ?)", (student_id, assessment_id, score))
            conn.commit()
            print(f"Score for student ID '{student_id}' in assessment ID '{assessment_id}' added successfully.")
    except sqlite3.Error as e:
        print("Failed to add score:", e)


def clean_database():
    try:
        with sqlite3.connect(os.path.join(DB_DIR, "mmu_academic_planner.db")) as conn:
            cursor = conn.cursor()
            cursor.execute("drop table if exists students;")
            cursor.execute("drop table if exists subjects;")
            cursor.execute("drop table if exists assessments;")
            cursor.execute("drop table if exists scores;")
            conn.commit()
            print("Database cleaned successfully.")
    except sqlite3.Error as e:
        print("Failed to clean database:", e)

def list_students():
    try:
        with sqlite3.connect(os.path.join(DB_DIR, "mmu_academic_planner.db")) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM students")
            students = cursor.fetchall()
            return students
    except sqlite3.Error as e:
        print("Failed to list students:", e)
        return []

def list_assessments_for_student(student_name):
    try:
        with sqlite3.connect(os.path.join(DB_DIR, "mmu_academic_planner.db")) as conn:
            conn.row_factory = sqlite3.Row 
            cursor = conn.cursor()
            cursor.execute("SELECT j.sub_name, j.sub_code, round(sum((a.weight) * (s.score)/100)) total_score FROM scores s JOIN assessments a ON s.assessment_id = a.assessment_id JOIN subjects j ON j.sub_code = a.sub_code JOIN students st ON st.stu_id = s.stu_id WHERE st.stu_name = ? group by j.sub_name, j.sub_code", (student_name,)) 
            rows = cursor.fetchall()
            return [dict(r) for r in rows]
    except sqlite3.Error as e:
        print("Failed to list assessments for student:", e)
        return []


def get_all_scores_for_subject(sub_code):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                "SELECT st.stu_id, st.stu_name, round(sum(a.weight * s.score / 100)) total_score "
                "FROM scores s "
                "JOIN assessments a ON s.assessment_id = a.assessment_id "
                "JOIN subjects j ON j.sub_code = a.sub_code "
                "JOIN students st ON st.stu_id = s.stu_id "
                "WHERE j.sub_code = ? "
                "GROUP BY st.stu_id, st.stu_name",
                (sub_code,),
            )
            return [dict(r) for r in cursor.fetchall()]
    except sqlite3.Error as e:
        print("Failed to get scores for subject:", e)
        return []


def get_unscored_assessments_for_student(stu_id):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                "SELECT a.assessment_name, a.weight, j.sub_name, j.sub_code "
                "FROM assessments a "
                "JOIN subjects j ON j.sub_code = a.sub_code "
                "LEFT JOIN scores s ON s.assessment_id = a.assessment_id AND s.stu_id = ? "
                "WHERE s.score IS NULL "
                "ORDER BY a.weight DESC",
                (stu_id,),
            )
            return [dict(r) for r in cursor.fetchall()]
    except sqlite3.Error as e:
        print("Failed to get unscored assessments:", e)
        return []


def fill_assessments_for_all_students():
    try:
        with sqlite3.connect(os.path.join(DB_DIR, "mmu_academic_planner.db")) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT stu_id FROM students")
            students = cursor.fetchall()
            cursor.execute("SELECT assessment_id FROM assessments")
            assessments = cursor.fetchall()

            for student in students:
                for assessment in assessments:
                    cursor.execute("INSERT INTO scores (stu_id, assessment_id, score) VALUES (?, ?, ?)", (student[0], assessment[0], random() * 100))
            conn.commit()
            print("Filled assessments for all students successfully.")
    except sqlite3.Error as e:
        print("Failed to fill assessments for all students:", e)


def init_data():
    clean_database()
    create_database_tables()
    add_student("Mayada","password1")
    add_student("Mohammad","password2")
    add_student("Rin","password3")

    add_subject("MATH101", "Mathematics")
    add_subject("CS101", "Programming")
    add_subject("PHYS101", "Physics")

    add_assessment("MATH101", "Midterm Exam", 30)
    add_assessment("MATH101", "Final Exam", 70)
    add_assessment("CS101", "Midterm Exam", 30)
    add_assessment("CS101", "Final Exam", 70)
    add_assessment("PHYS101", "Midterm Exam", 30)
    add_assessment("PHYS101", "Final Exam", 70)

    fill_assessments_for_all_students()


def list_subjects():
    try:
        with sqlite3.connect(os.path.join(DB_DIR, "mmu_academic_planner.db")) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            rows = cursor.execute("SELECT * FROM subjects").fetchall()
            return [dict(r) for r in rows]
    except sqlite3.Error as e:
        print("Failed to list subjects:", e)
        return []


def list_assessments_for_subject(sub_code):
    try:
        with sqlite3.connect(os.path.join(DB_DIR, "mmu_academic_planner.db")) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            rows = cursor.execute(
                "SELECT * FROM assessments WHERE sub_code = ?", (sub_code,)
            ).fetchall()
            return [dict(r) for r in rows]
    except sqlite3.Error as e:
        print("Failed to list assessments:", e)
        return []


def get_subject_by_code(code):
    try:
        with sqlite3.connect(os.path.join(DB_DIR, "mmu_academic_planner.db")) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            row = cursor.execute("SELECT * FROM subjects WHERE sub_code = ?", (code,)).fetchone()
            return dict(row) if row else None
    except sqlite3.Error as e:
        print("Failed to get subject:", e)
        return None


def update_subject(code, name):
    try:
        with sqlite3.connect(os.path.join(DB_DIR, "mmu_academic_planner.db")) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE subjects SET sub_name = ? WHERE sub_code = ?", (name, code))
            conn.commit()
    except sqlite3.Error as e:
        print("Failed to update subject:", e)


def delete_subject(code):
    try:
        with sqlite3.connect(os.path.join(DB_DIR, "mmu_academic_planner.db")) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM assessments WHERE sub_code = ?", (code,))
            cursor.execute("DELETE FROM subjects WHERE sub_code = ?", (code,))
            conn.commit()
    except sqlite3.Error as e:
        print("Failed to delete subject:", e)


def update_assessment(assessment_id, name, weight):
    try:
        with sqlite3.connect(os.path.join(DB_DIR, "mmu_academic_planner.db")) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE assessments SET assessment_name = ?, weight = ? WHERE assessment_id = ?",
                (name, weight, assessment_id),
            )
            conn.commit()
    except sqlite3.Error as e:
        print("Failed to update assessment:", e)


def delete_assessment(assessment_id):
    try:
        with sqlite3.connect(os.path.join(DB_DIR, "mmu_academic_planner.db")) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM assessments WHERE assessment_id = ?", (assessment_id,))
            conn.commit()
    except sqlite3.Error as e:
        print("Failed to delete assessment:", e)