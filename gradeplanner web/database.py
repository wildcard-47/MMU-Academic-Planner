import sqlite3
import os

DB_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(DB_DIR, "mmu_academic_planner.db")


# Opens a connection with foreign keys switched on, so deleting a subject
# also deletes its assessments (ON DELETE CASCADE). Rows come back as dicts.
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# Tables:
#   students    - one row per account, remembers which trimester is active
#   subjects    - belongs to ONE student and ONE trimester (e.g. "2026/2027 T1"),
#                 so every student has their own subject list per trimester
#   assessments - belongs to one subject; score is NULL until it is marked
def create_database_tables():
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS students ("
                "stu_id INTEGER PRIMARY KEY, "
                "stu_name TEXT NOT NULL UNIQUE, "
                "stu_password TEXT NOT NULL, "
                "active_trimester TEXT)"
            )
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS subjects ("
                "sub_id INTEGER PRIMARY KEY, "
                "stu_id INTEGER NOT NULL, "
                "trimester TEXT NOT NULL, "
                "sub_code TEXT NOT NULL, "
                "sub_name TEXT NOT NULL, "
                "credit_hours INTEGER NOT NULL DEFAULT 3, "
                "target_grade TEXT, "
                "UNIQUE (stu_id, trimester, sub_code), "
                "FOREIGN KEY (stu_id) REFERENCES students(stu_id) ON DELETE CASCADE)"
            )
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS assessments ("
                "assessment_id INTEGER PRIMARY KEY, "
                "sub_id INTEGER NOT NULL, "
                "assessment_name TEXT NOT NULL, "
                "weight REAL NOT NULL, "
                "score REAL, "
                "FOREIGN KEY (sub_id) REFERENCES subjects(sub_id) ON DELETE CASCADE)"
            )
            conn.commit()
            print("Database tables ready.")
    except sqlite3.Error as e:
        print("Failed to create database:", e)


# Called on startup. Creates missing tables but keeps existing data.
def init_data():
    create_database_tables()


# ---------- Students ----------

def add_student(name, password_hash, trimester):
    try:
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO students (stu_name, stu_password, active_trimester) VALUES (?, ?, ?)",
                (name, password_hash, trimester),
            )
            conn.commit()
            return True
    except sqlite3.Error as e:
        print("Failed to add student:", e)
        return False


def get_student(username):
    try:
        with get_connection() as conn:
            row = conn.execute("SELECT * FROM students WHERE stu_name = ?", (username,)).fetchone()
            return dict(row) if row else None
    except sqlite3.Error as e:
        print("Failed to get student:", e)
        return None


def get_student_by_id(student_id):
    try:
        with get_connection() as conn:
            row = conn.execute("SELECT * FROM students WHERE stu_id = ?", (student_id,)).fetchone()
            return dict(row) if row else None
    except sqlite3.Error as e:
        print("Failed to get student by ID:", e)
        return None


def set_active_trimester(stu_id, trimester):
    try:
        with get_connection() as conn:
            conn.execute("UPDATE students SET active_trimester = ? WHERE stu_id = ?", (trimester, stu_id))
            conn.commit()
    except sqlite3.Error as e:
        print("Failed to set trimester:", e)


def list_trimesters_for_student(stu_id):
    try:
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT DISTINCT trimester FROM subjects WHERE stu_id = ? ORDER BY trimester",
                (stu_id,),
            ).fetchall()
            return [r["trimester"] for r in rows]
    except sqlite3.Error as e:
        print("Failed to list trimesters:", e)
        return []


# ---------- Subjects (always scoped to one student) ----------

def add_subject(stu_id, trimester, code, name, credit_hours):
    try:
        with get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO subjects (stu_id, trimester, sub_code, sub_name, credit_hours) "
                "VALUES (?, ?, ?, ?, ?)",
                (stu_id, trimester, code, name, credit_hours),
            )
            conn.commit()
            return cursor.lastrowid
    except sqlite3.Error as e:
        print("Failed to add subject:", e)
        return None


def list_subjects(stu_id, trimester):
    try:
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM subjects WHERE stu_id = ? AND trimester = ? ORDER BY sub_code",
                (stu_id, trimester),
            ).fetchall()
            return [dict(r) for r in rows]
    except sqlite3.Error as e:
        print("Failed to list subjects:", e)
        return []


def list_all_subjects_for_student(stu_id):
    try:
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM subjects WHERE stu_id = ? ORDER BY trimester, sub_code", (stu_id,)
            ).fetchall()
            return [dict(r) for r in rows]
    except sqlite3.Error as e:
        print("Failed to list subjects:", e)
        return []


# Returns the subject only if it belongs to this student, otherwise None.
def get_subject(stu_id, sub_id):
    try:
        with get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM subjects WHERE sub_id = ? AND stu_id = ?", (sub_id, stu_id)
            ).fetchone()
            return dict(row) if row else None
    except sqlite3.Error as e:
        print("Failed to get subject:", e)
        return None


def find_subject_by_code(stu_id, trimester, code):
    try:
        with get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM subjects WHERE stu_id = ? AND trimester = ? AND sub_code = ?",
                (stu_id, trimester, code),
            ).fetchone()
            return dict(row) if row else None
    except sqlite3.Error as e:
        print("Failed to find subject:", e)
        return None


def update_subject(sub_id, name, credit_hours):
    try:
        with get_connection() as conn:
            conn.execute(
                "UPDATE subjects SET sub_name = ?, credit_hours = ? WHERE sub_id = ?",
                (name, credit_hours, sub_id),
            )
            conn.commit()
    except sqlite3.Error as e:
        print("Failed to update subject:", e)


def set_target_grade(sub_id, target_grade):
    try:
        with get_connection() as conn:
            conn.execute("UPDATE subjects SET target_grade = ? WHERE sub_id = ?", (target_grade, sub_id))
            conn.commit()
    except sqlite3.Error as e:
        print("Failed to set target grade:", e)


def delete_subject(sub_id):
    try:
        with get_connection() as conn:
            conn.execute("DELETE FROM subjects WHERE sub_id = ?", (sub_id,))
            conn.commit()
    except sqlite3.Error as e:
        print("Failed to delete subject:", e)


# Finds a classmate who already set up the same subject code in the same
# trimester and has assessments, so a new student can copy the structure.
def find_classmate_template(stu_id, trimester, code):
    try:
        with get_connection() as conn:
            row = conn.execute(
                "SELECT j.sub_id FROM subjects j "
                "JOIN assessments a ON a.sub_id = j.sub_id "
                "WHERE j.trimester = ? AND j.sub_code = ? AND j.stu_id != ? "
                "GROUP BY j.sub_id ORDER BY count(*) DESC LIMIT 1",
                (trimester, code, stu_id),
            ).fetchone()
            return row["sub_id"] if row else None
    except sqlite3.Error as e:
        print("Failed to find template:", e)
        return None


# ---------- Assessments ----------

def add_assessment(sub_id, assessment_name, weight):
    try:
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO assessments (sub_id, assessment_name, weight) VALUES (?, ?, ?)",
                (sub_id, assessment_name, weight),
            )
            conn.commit()
    except sqlite3.Error as e:
        print("Failed to add assessment:", e)


def list_assessments_for_subject(sub_id):
    try:
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM assessments WHERE sub_id = ? ORDER BY assessment_id", (sub_id,)
            ).fetchall()
            return [dict(r) for r in rows]
    except sqlite3.Error as e:
        print("Failed to list assessments:", e)
        return []


# Returns the assessment (with its subject's stu_id) only if it belongs to
# this student, otherwise None.
def get_assessment(stu_id, assessment_id):
    try:
        with get_connection() as conn:
            row = conn.execute(
                "SELECT a.* FROM assessments a JOIN subjects j ON j.sub_id = a.sub_id "
                "WHERE a.assessment_id = ? AND j.stu_id = ?",
                (assessment_id, stu_id),
            ).fetchone()
            return dict(row) if row else None
    except sqlite3.Error as e:
        print("Failed to get assessment:", e)
        return None


def update_assessment(assessment_id, name, weight):
    try:
        with get_connection() as conn:
            conn.execute(
                "UPDATE assessments SET assessment_name = ?, weight = ? WHERE assessment_id = ?",
                (name, weight, assessment_id),
            )
            conn.commit()
    except sqlite3.Error as e:
        print("Failed to update assessment:", e)


def delete_assessment(assessment_id):
    try:
        with get_connection() as conn:
            conn.execute("DELETE FROM assessments WHERE assessment_id = ?", (assessment_id,))
            conn.commit()
    except sqlite3.Error as e:
        print("Failed to delete assessment:", e)


# Saves the mark for one assessment. A score of None removes the mark.
def save_score(assessment_id, score):
    try:
        with get_connection() as conn:
            conn.execute("UPDATE assessments SET score = ? WHERE assessment_id = ?", (score, assessment_id))
            conn.commit()
    except sqlite3.Error as e:
        print("Failed to save score:", e)


# ---------- Comparison queries (used by the dashboard) ----------

# Every student's assessments (weight and score) in one subject code for one
# trimester. The dashboard turns these into each student's current percentage.
def get_class_scores_for_subject(trimester, code):
    try:
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT j.stu_id, a.weight, a.score "
                "FROM subjects j JOIN assessments a ON a.sub_id = j.sub_id "
                "WHERE j.trimester = ? AND j.sub_code = ?",
                (trimester, code),
            ).fetchall()
            return [dict(r) for r in rows]
    except sqlite3.Error as e:
        print("Failed to get class scores:", e)
        return []
