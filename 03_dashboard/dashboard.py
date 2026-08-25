import customtkinter

#Define sample subjects and their scores
subjects = ["Programming","Mathematics","Physics"]
score = [76, 82, 68]

class Dashboard(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("900x450")
        self.title("MMU Academic Planner")

        self.textbox = customtkinter.CTkTextbox(self, width=300, height=200)
        self.textbox.pack(pady=20)
        array_string = "\n".join(subjects)
        self.textbox.insert("0.0", array_string)


app = Dashboard()
app.mainloop()