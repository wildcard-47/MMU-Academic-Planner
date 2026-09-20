from database.database import list_assessments_for_student
from database.database import list_assessments_for_student, list_students

def calculate_average(subjects):
    if not subjects:
        return 0
    return sum(s["score"] for s in subjects) / len(subjects)

def find_highest(subjects):
    return max(subjects, key=lambda s: s["score"]) if subjects else None

def find_lowest(subjects):
    return min(subjects, key=lambda s: s["score"]) if subjects else None

def get_assessments_for_student(student_name):
    return list_assessments_for_student(student_name)

def get_dashboard_data():
    return {
        "subjects": [],
        "average": 0,
        "highest": None,
        "lowest": None
    }
def calculate_percentile(my_score, other_scores):
    if not other_scores:
        return None
    higher_than_count = sum(1 for score in other_scores if score < my_score)
    return round((higher_than_count / len(other_scores)) * 100)

def get_all_students_overall_averages():
    results = []
    for student in list_students():
        stu_id, stu_name = student[0], student[1]
        subjects = get_assessments_for_student(stu_name)
        if subjects:
            average = calculate_average([{"score": s["total_score"]} for s in subjects])
            results.append({"stu_id": stu_id, "average": average})
    return results

def calculate_rank(my_average, other_averages):
    if not other_averages:
        return 1, 1
    rank = 1 + sum(1 for avg in other_averages if avg > my_average)
    total = len(other_averages) + 1
    return rank, total

def get_insight_message(rank, total):
    if total <= 1:
        return "Add more subjects and scores to see how you compare with classmates!"
    share = rank / total
    if rank == 1:
        return "🏆 You're currently ranked #1 in your class overall — amazing work!"
    if share <= 0.34:
        return f"🎉 Great job! You're in the top third of your class (rank {rank} of {total})."
    if share <= 0.67:
        return f"👍 You're holding steady in the middle of the pack (rank {rank} of {total}). A little more effort could push you higher!"
    return f"💪 You're currently rank {rank} of {total}. Check the Grade Planner to see what you need for your target grade."


def find_next_rank_average(my_average, other_averages):
    higher = [avg for avg in other_averages if avg > my_average]
    return min(higher) if higher else None