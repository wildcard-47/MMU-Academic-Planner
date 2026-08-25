import customtkinter

class Dashboard(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("900x450")
        self.title("MMU Academic Planner")

app = Dashboard()
app.mainloop()