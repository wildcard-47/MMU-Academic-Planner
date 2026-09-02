import customtkinter as ctk

subjects = []
assessments = []
_next_subject_id = 1
_next_assessment_id = 1


def calculate_subject_performance(subject_assessments):
    completed = [a for a in subject_assessments if a["score"] is not None]
    remaining = [a for a in subject_assessments if a["score"] is None]
    earned = sum(a["weight"] * a["score"] / 100 for a in completed)
    return {
        "earned": earned,
        "completed_weight": sum(a["weight"] for a in completed),
        "remaining_weight": sum(a["weight"] for a in remaining),
    }


def validate_weight(value):
    try:
        weight = float(value)
    except ValueError:
        return None, "Weight must be a number."
    if not 0 <= weight <= 100:
        return None, "Weight must be between 0 and 100."
    return weight, None


def validate_score(value):
    if value == "":
        return None, None
    try:
        score = float(value)
    except ValueError:
        return None, "Score must be a number."
    if not 0 <= score <= 100:
        return None, "Score must be between 0 and 100."
    return score, None


class SubjectManagerFrame(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)
        self.selected_subject_id = None
        self._build_layout()
        self.refresh_subjects()

    def _build_layout(self):
        ctk.CTkLabel(
            self, text="Subject & Assessment Manager", font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=(15, 10))

        top = ctk.CTkFrame(self)
        top.pack(fill="x", padx=15)
        self.name_entry = ctk.CTkEntry(top, placeholder_text="Subject name")
        self.name_entry.pack(side="left", padx=5, pady=10)
        self.code_entry = ctk.CTkEntry(top, placeholder_text="Subject code")
        self.code_entry.pack(side="left", padx=5, pady=10)
        ctk.CTkButton(top, text="Add Subject", command=self.add_subject).pack(side="left", padx=5)

        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=15, pady=10)

        self.subjects_frame = ctk.CTkScrollableFrame(body, width=260, label_text="Subjects")
        self.subjects_frame.pack(side="left", fill="y", padx=(0, 10))

        right = ctk.CTkFrame(body, fg_color="transparent")
        right.pack(side="left", fill="both", expand=True)

        form = ctk.CTkFrame(right)
        form.pack(fill="x", pady=(0, 10))
        self.assess_name = ctk.CTkEntry(form, placeholder_text="Assessment name")
        self.assess_name.grid(row=0, column=0, padx=5, pady=10)
        self.assess_weight = ctk.CTkEntry(form, placeholder_text="Weight %")
        self.assess_weight.grid(row=0, column=1, padx=5, pady=10)
        self.assess_score = ctk.CTkEntry(form, placeholder_text="Score % (blank if not taken)")
        self.assess_score.grid(row=0, column=2, padx=5, pady=10)
        ctk.CTkButton(form, text="Add Assessment", command=self.add_assessment).grid(
            row=0, column=3, padx=5
        )

        self.assessments_frame = ctk.CTkScrollableFrame(right, label_text="Assessments")
        self.assessments_frame.pack(fill="both", expand=True)

        self.summary_label = ctk.CTkLabel(right, text="", font=ctk.CTkFont(size=14, weight="bold"))
        self.summary_label.pack(pady=10)

        self.error_label = ctk.CTkLabel(self, text="", text_color="red")
        self.error_label.pack(pady=(0, 10))

    def show_error(self, message):
        self.error_label.configure(text=message)

    def add_subject(self):
        global _next_subject_id
        name = self.name_entry.get().strip()
        code = self.code_entry.get().strip()
        if not name or not code:
            self.show_error("Subject name and code are required.")
            return
        subjects.append({"id": _next_subject_id, "name": name, "code": code})
        _next_subject_id += 1
        self.name_entry.delete(0, "end")
        self.code_entry.delete(0, "end")
        self.show_error("")
        self.refresh_subjects()

    def refresh_subjects(self):
        for widget in self.subjects_frame.winfo_children():
            widget.destroy()
        for subject in subjects:
            row = ctk.CTkFrame(self.subjects_frame)
            row.pack(fill="x", pady=4)
            ctk.CTkButton(
                row,
                text=f'{subject["name"]} ({subject["code"]})',
                command=lambda s=subject: self.select_subject(s["id"]),
            ).pack(side="left", padx=(0, 5), fill="x", expand=True)
            ctk.CTkButton(
                row, text="Delete", width=60, fg_color="darkred",
                command=lambda s=subject: self.remove_subject(s["id"]),
            ).pack(side="left")
        if self.selected_subject_id is not None and not any(
            s["id"] == self.selected_subject_id for s in subjects
        ):
            self.selected_subject_id = None
        self.refresh_assessments()

    def remove_subject(self, subject_id):
        subjects[:] = [s for s in subjects if s["id"] != subject_id]
        assessments[:] = [a for a in assessments if a["subject_id"] != subject_id]
        if self.selected_subject_id == subject_id:
            self.selected_subject_id = None
        self.refresh_subjects()

    def select_subject(self, subject_id):
        self.selected_subject_id = subject_id
        self.refresh_assessments()


if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    root = ctk.CTk()
    root.title("Subject Manager (prototype)")
    root.geometry("500x450")
    SubjectManagerFrame(root).pack(fill="both", expand=True)
    root.mainloop()