import customtkinter
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import database as db
from grading import percent_to_letter

# Initialize the database with sample data
db.init_data()

#find the highest assessment for a student
def find_highest_assessment(assessments):
    if not assessments:
        return None  # Handles empty list scenario safely
    return max(assessments, key=lambda x: x[4])  # Assuming the score is at index 4

#find the lowest assessment for a student
def find_lowest_assessment(assessments):
    if not assessments:
        return None  # Handles empty list scenario safely
    return min(assessments, key=lambda x: x[4])  # Assuming the score is at index 4

#define combobox callback function
def combobox_callback(choice):
    print(f"Combobox selection: {choice}")

#main dashboard class
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
            row_frame = customtkinter.CTkFrame(self)
            row_frame.pack(pady=10, fill="x", padx=20)

            assessment_label = customtkinter.CTkLabel(self, text=f"Subject: {assessment[2]} - Assessment: {assessment[1]} - Score: {assessment[4]}% - Grade: ({percent_to_letter(assessment[4])})", font=customtkinter.CTkFont(size=20))
            assessment_label.pack(pady=10)
   
            #score progress bar
            progress = customtkinter.CTkProgressBar(row_frame, width=180)
            progress.grid(row=0, column=3, padx=(5, 10), pady=8)
            progress.set(assessment[4] / 100)
            #color coding for the progress bar based on the score
            if assessment[4] >= 70:
                progress.configure(progress_color="green")
            elif assessment[4] >= 50:
                progress.configure(progress_color="yellow")
            else:
                progress.configure(progress_color="red")


        #calculate and display average score
        average = sum(assessment[4] for assessment in assessments) / len(assessments)
        average_label = customtkinter.CTkLabel(self, text=f"Average score: ({average:.2f}%) - Grade: ({percent_to_letter(average)})", font=customtkinter.CTkFont(size=20))
        average_label.pack(pady=10)

        #find and display highest assessments
        highest_subject = find_highest_assessment(assessments)
        if highest_subject:
            highest_label = customtkinter.CTkLabel(self, text=f"Highest Subject: {highest_subject[2]} - {highest_subject[1]}: ({highest_subject[4]}%) - Grade: ({percent_to_letter(highest_subject[4])})", font=customtkinter.CTkFont(size=20))
            highest_label.pack(pady=10)
        #find and display lowest assessments
        lowest_subject = find_lowest_assessment(assessments)
        if lowest_subject:
            lowest_label = customtkinter.CTkLabel(self, text=f"Lowest Subject: {lowest_subject[2]} - {lowest_subject[1]}: ({lowest_subject[4]}%) - Grade: ({percent_to_letter(lowest_subject[4])})", font=customtkinter.CTkFont(size=20))
            lowest_label.pack(pady=10)

app = Dashboard()
app.mainloop()