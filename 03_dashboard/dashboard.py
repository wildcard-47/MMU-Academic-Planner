import customtkinter

subjects = [
    {"id":1, "code" : "CS101", "name": "Programming", "score": 76},
    {"id":2, "code" : "MATH201", "name": "Mathematics", "score": 82},
    {"id":3, "code" : "PHYS201", "name": "Physics", "score": 68},
]


class Dashboard(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("MMU Academic Planner")
        self.geometry("900x450")


        for subject in subjects:
            row_text = f'{subject["id"]} - {subject["code"]} - {subject["name"]}: {subject["score"]}%'
            row = customtkinter.CTkLabel(self, text=row_text, font=customtkinter.CTkFont(size=20))
            row.pack(pady=10)


app = Dashboard()
app.mainloop()
