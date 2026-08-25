import customtkinter

subjects = [
    {"name": "Programming", "score": 76},
    {"name": "Mathematics", "score": 82},
    {"name": "Physics", "score": 68},
]


class Dashboard(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("MMU Academic Planner")
        self.geometry("900x450")


        for subject in subjects:
            row_text = f'{subject["name"]}: {subject["score"]}%'
            row = customtkinter.CTkLabel(self, text=row_text, font=customtkinter.CTkFont(size=20))
            row.pack(pady=10)


app = Dashboard()
app.mainloop()
