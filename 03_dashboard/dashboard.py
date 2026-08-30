import customtkinter

##function to get the grade letter from the score
def percent_to_letter(score):
    if score < 0 or score > 100:
        return "Invalid score"
    if score >= 90:
        return "A+"
    elif score >= 80:
        return "A"
    elif score >= 75:
        return "A-"
    elif score >= 70:
        return "B+"
    elif score >= 65:
        return "B"
    elif score >= 60:
        return "B-"
    elif score >= 55:
        return "C+"
    elif score >= 50:
        return "C"
    elif score >= 47:
        return "C-"
    elif score >= 44:
        return "D+"
    elif score >= 40:
        return "D"
    else:
        return "F"


#defined subjects with their scores
subjects = [
    {"id":1, "code" : "CSP1114", "name": "Programming", "score": 76},
    {"id":2, "code" : "CMT1134", "name": "Mathematics", "score": 82},
    {"id":3, "code" : "CPP1113", "name": "Physics", "score": 68},
]


class Dashboard(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("MMU Academic Planner")
        self.geometry("900x450")

        for subject in subjects:
            row_text = f'{subject["code"]} - {subject["name"]}: ({subject["score"]}%) - Grade: ({percent_to_letter(subject["score"])})'
            row = customtkinter.CTkLabel(self, text=row_text, font=customtkinter.CTkFont(size=20))
            row.pack(pady=10)

        average = sum(subject["score"] for subject in subjects) / len(subjects)
        average_label = customtkinter.CTkLabel(self, text=f"Average score: ({average:.2f}%) - Grade: ({percent_to_letter(average)})", font=customtkinter.CTkFont(size=20))
        average_label.pack(pady=10)


app = Dashboard()
app.mainloop()
