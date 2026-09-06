import customtkinter
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import database as db
from grading import percent_to_letter

# Initialize the database with sample data
#db.init_data()


def find_highest_assessment(assessments):
    if not assessments:
        return None  # Handles empty list scenario safely
    return max(assessments, key=lambda x: x[4])  # Assuming the score is at index 4

def find_lowest_assessment(assessments):
    if not assessments:
        return None  # Handles empty list scenario safely
    return min(assessments, key=lambda x: x[4])  # Assuming the score is at index 4

def combobox_callback(choice):
    print(f"Combobox selection: {choice}")

class Dashboard(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("MMU Academic Planner")
        self.geometry("900x450")


        # Header Title
        self.title_label = customtkinter.CTkLabel(
            self, text="Academic Dashboard", font=customtkinter.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack(pady=20)

        # Student Selection Combobox
        combobox = customtkinter.CTkComboBox(
            master=self,
            values=[student[1] for student in db.list_students()], 
            command=combobox_callback
        )
        combobox.pack(pady=40)
        combobox.set("Select a Student")

        #list_assessments_for_student
        assessments = db.list_assessments_for_student(1) 
        for assessment in assessments:
            assessment_label = customtkinter.CTkLabel(self, text=f"Subject: {assessment[2]} - Assessment: {assessment[1]} - Score: {assessment[4]}% - Grade: ({percent_to_letter(assessment[4])})", font=customtkinter.CTkFont(size=20))
            assessment_label.pack(pady=10)

        
       

        average = sum(assessment[4] for assessment in assessments) / len(assessments)
        average_label = customtkinter.CTkLabel(self, text=f"Average score: ({average:.2f}%) - Grade: ({percent_to_letter(average)})", font=customtkinter.CTkFont(size=20))
        average_label.pack(pady=10)


        highest_subject = find_highest_assessment(assessments)
        if highest_subject:
            highest_label = customtkinter.CTkLabel(self, text=f"Highest Subject: {highest_subject[2]} - {highest_subject[1]}: ({highest_subject[4]}%) - Grade: ({percent_to_letter(highest_subject[4])})", font=customtkinter.CTkFont(size=20))
            highest_label.pack(pady=10)



        lowest_subject = find_lowest_assessment(assessments)
        if lowest_subject:
            lowest_label = customtkinter.CTkLabel(self, text=f"Lowest Subject: {lowest_subject[2]} - {lowest_subject[1]}: ({lowest_subject[4]}%) - Grade: ({percent_to_letter(lowest_subject[4])})", font=customtkinter.CTkFont(size=20))
            lowest_label.pack(pady=10)

app = Dashboard()
app.mainloop()