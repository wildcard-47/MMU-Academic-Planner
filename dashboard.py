import customtkinter

class Dashboard(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("400x150")
        self.title("MMU Academic Planner")

        self.button = customtkinter.CTkButton(self, text="my button", command=self.button_callbck)
        self.button.pack(padx=20, pady=20)

    def button_callbck(self):
        print("button clicked")

app = Dashboard()
app.mainloop()