import customtkinter as ctk

#prototype: in-memory only, no SQLite yet, no assessments yet.
# Just proves the subject list can be created/viewed.
subjects = []


class SubjectManagerFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self._build_layout()
        self.refresh_subjects()

    def _build_layout(self):
        ctk.CTkLabel(
            self, text="Subject Manager (prototype)", font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=(15, 10))

        form = ctk.CTkFrame(self)
        form.pack(pady=10)
        self.name_entry = ctk.CTkEntry(form, placeholder_text="Subject name")
        self.name_entry.pack(side="left", padx=5)
        self.code_entry = ctk.CTkEntry(form, placeholder_text="Subject code")
        self.code_entry.pack(side="left", padx=5)
        ctk.CTkButton(form, text="Add Subject", command=self.add_subject).pack(side="left", padx=5)

        self.subjects_frame = ctk.CTkScrollableFrame(self, width=400, height=250)
        self.subjects_frame.pack(padx=15, pady=15, fill="both", expand=True)

    def add_subject(self):
        name = self.name_entry.get().strip()
        code = self.code_entry.get().strip()
        if not name or not code:
            return
        subjects.append({"name": name, "code": code})
        self.name_entry.delete(0, "end")
        self.code_entry.delete(0, "end")
        self.refresh_subjects()

    def refresh_subjects(self):
        for widget in self.subjects_frame.winfo_children():
            widget.destroy()
        for subject in subjects:
            ctk.CTkLabel(self.subjects_frame, text=f'{subject["name"]} ({subject["code"]})').pack(
                anchor="w", padx=10, pady=4
            )


if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    root = ctk.CTk()
    root.title("Subject Manager (Week 1 prototype)")
    root.geometry("500x450")
    SubjectManagerFrame(root).pack(fill="both", expand=True)
    root.mainloop()
