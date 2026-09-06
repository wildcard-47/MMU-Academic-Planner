import customtkinter
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import database as db
from grading import percent_to_letter

# Initialize the database with sample data
#db.init_data()

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

#main dashboard class
class Dashboard(customtkinter.CTk):
    def display_assessments(self):
        # Clear existing data
        for widget in self.data_frame.winfo_children():
            widget.destroy()
        
        student_name = self.combobox.get()
        if student_name == "Select a Student" or not student_name:
            error_label = customtkinter.CTkLabel(
                self.data_frame, 
                text="Please select a valid student.", 
                font=customtkinter.CTkFont(size=20)
            )
            error_label.pack(pady=10)
            return
        
        assessments = db.list_assessments_for_student(student_name)
        if not assessments:
            no_data_label = customtkinter.CTkLabel(
                self.data_frame, 
                text="No assessments found for this student.", 
                font=customtkinter.CTkFont(size=20)
            )
            no_data_label.pack(pady=10)
            return

        # Display each assessment - ALL code inside the loop
        for assessment in assessments:
            row_frame = customtkinter.CTkFrame(self.data_frame)
            row_frame.pack(pady=10, fill="x", padx=20)

            # FIXED: assessment_label inside loop, uses row_frame as parent
            assessment_label = customtkinter.CTkLabel(
                row_frame,  # Changed from 'self' to 'row_frame'
                text=f"Subject: {assessment[2]} - Assessment: {assessment[1]} - Score: {assessment[4]}% - Grade: ({percent_to_letter(assessment[4])})", 
                font=customtkinter.CTkFont(size=20)
            )
            assessment_label.pack(pady=5)

            # FIXED: Use .pack() instead of .grid()
            progress = customtkinter.CTkProgressBar(row_frame, width=180)
            progress.pack(pady=5)
            progress.set(assessment[4] / 100)
            
            # Color coding for the progress bar based on the score
            if assessment[4] >= 70:
                progress.configure(progress_color="green")
            elif assessment[4] >= 50:
                progress.configure(progress_color="yellow")
            else:
                progress.configure(progress_color="red")

        # MOVED OUTSIDE the for loop - calculate and display averages once
        try:
            average = sum(assessment[4] for assessment in assessments) / len(assessments)
            average_label = customtkinter.CTkLabel(
                self.data_frame,  # Changed from 'self' to 'self.data_frame'
                text=f"Average score: ({average:.2f}%) - Grade: ({percent_to_letter(average)})", 
                font=customtkinter.CTkFont(size=20, weight="bold")
            )
            average_label.pack(pady=10)
        except ZeroDivisionError:
            pass

        # Find and display highest assessment
        highest_subject = find_highest_assessment(assessments)
        if highest_subject:
            highest_label = customtkinter.CTkLabel(
                self.data_frame,  # Changed from 'self' to 'self.data_frame'
                text=f"Highest Subject: {highest_subject[2]} - {highest_subject[1]}: ({highest_subject[4]}%) - Grade: ({percent_to_letter(highest_subject[4])})", 
                font=customtkinter.CTkFont(size=20)
            )
            highest_label.pack(pady=5)

        # Find and display lowest assessment
        lowest_subject = find_lowest_assessment(assessments)
        if lowest_subject:
            lowest_label = customtkinter.CTkLabel(
                self.data_frame,  # Changed from 'self' to 'self.data_frame'
                text=f"Lowest Subject: {lowest_subject[2]} - {lowest_subject[1]}: ({lowest_subject[4]}%) - Grade: ({percent_to_letter(lowest_subject[4])})", 
                font=customtkinter.CTkFont(size=20)
            )
            lowest_label.pack(pady=5)

    def __init__(self):
        super().__init__()
        self.title("MMU Academic Planner")
        self.geometry("900x600")  # Increased height for better display

        # Header Title
        self.title_label = customtkinter.CTkLabel(
            self, text="Academic Dashboard", font=customtkinter.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack(pady=20)

        # Student Selection Combobox
        self.combobox = customtkinter.CTkComboBox(
            master=self,
            values=[student[1] for student in db.list_students()]
        )
        self.combobox.pack(pady=20)
        self.combobox.set("Select a Student")

        # Display Button
        self.button = customtkinter.CTkButton(
            self, 
            text="Display Assessments", 
            command=self.display_assessments
        )
        self.button.pack(padx=20, pady=20)

        # Frame to hold assessment data
        self.data_frame = customtkinter.CTkFrame(self)
        self.data_frame.pack(pady=10, fill="both", expand=True, padx=20)

if __name__ == "__main__":
    app = Dashboard()
    app.mainloop()