import customtkinter as ctk
from PIL import Image

# =========================
# MAIN WINDOW
# =========================

app = ctk.CTk()
app.geometry("750x500")
app.title("GRADE PLANNER")


# =========================
# SCREEN 1 - HOME
# =========================

home_screen = ctk.CTkFrame(app)
home_screen.pack(fill="both", expand=True)


# BACKGROUND

background_image = ctk.CTkImage(
    light_image=Image.open("background.png"),
    size=(750, 500)
)

background = ctk.CTkLabel(
    home_screen,
    text="",
    image=background_image
)

background.place(
    x=0,
    y=0,
    relwidth=1,
    relheight=1
)

# =========================
# SCREEN 2 - GRADE TARGET
# =========================

target_screen = ctk.CTkFrame(app)
# SCREEN 2 BACKGROUND

target_background_image = ctk.CTkImage(
    light_image=Image.open("background.png"),
    size=(750, 500)
)

target_background = ctk.CTkLabel(
    target_screen,
    text="",
    image=target_background_image
)

target_background.place(
    x=0,
    y=0,
    relwidth=1,
    relheight=1
)


# =========================
# OPEN SCREEN 2
# =========================

def open_image1_screen():
    home_screen.pack_forget()
    target_screen.pack(fill="both", expand=True)


# =========================
# BACK TO HOME
# =========================

def back_to_home():
    target_screen.pack_forget()
    home_screen.pack(fill="both", expand=True)


# =========================
# CALCULATE OVERALL
# =========================

def calculate_overall():

    try:
        quiz_score = float(quiz_entry.get())
        assignment_score = float(assignment_entry.get())
        midterm_score = float(midterm_entry.get())

        # Check scores
        if not 0 <= quiz_score <= 100:
            result_label.configure(text="Quiz score must be 0-100")
            return

        if not 0 <= assignment_score <= 100:
            result_label.configure(text="Assignment score must be 0-100")
            return

        if not 0 <= midterm_score <= 100:
            result_label.configure(text="Midterm score must be 0-100")
            return

        # Assessment weights
        quiz_weight = 20
        assignment_weight = 20
        midterm_weight = 20

        # Calculate earned marks
        quiz_earned = quiz_score * quiz_weight / 100
        assignment_earned = assignment_score * assignment_weight / 100
        midterm_earned = midterm_score * midterm_weight / 100

        # Current earned
        current_earned = (
            quiz_earned
            + assignment_earned
            + midterm_earned
        )

        # Completed weight
        completed_weight = (
            quiz_weight
            + assignment_weight
            + midterm_weight
        )

        # Remaining weight
        remaining_weight = 100 - completed_weight

        # Current performance
        current_performance = (
            current_earned / completed_weight
        ) * 100

        # Display results
        result_label.configure(
            text=(
                f"Current Earned: {current_earned:.2f}%\n"
                f"Completed Weight: {completed_weight}%\n"
                f"Remaining Weight: {remaining_weight}%\n"
                f"Current Performance: {current_performance:.2f}%"
            )
        )

    except ValueError:
        result_label.configure(
            text="Please enter valid numbers."
        )


# =========================
# TITLE
# =========================

title = ctk.CTkLabel(
    target_screen,
    text="GRADE TARGET & WHAT-IF",
    font=("Arial", 28, "bold")
)

title.pack(pady=15)


# =========================
# QUIZ
# =========================

quiz_label = ctk.CTkLabel(
    target_screen,
    text="Quiz Score (Weight: 20%)"
)

quiz_label.pack()

quiz_entry = ctk.CTkEntry(
    target_screen,
    placeholder_text="Enter score 0-100"
)

quiz_entry.pack(pady=5)


# =========================
# ASSIGNMENT
# =========================

assignment_label = ctk.CTkLabel(
    target_screen,
    text="Assignment Score (Weight: 20%)"
)

assignment_label.pack()

assignment_entry = ctk.CTkEntry(
    target_screen,
    placeholder_text="Enter score 0-100"
)

assignment_entry.pack(pady=5)


# =========================
# MIDTERM
# =========================

midterm_label = ctk.CTkLabel(
    target_screen,
    text="Midterm Score (Weight: 20%)"
)

midterm_label.pack()

midterm_entry = ctk.CTkEntry(
    target_screen,
    placeholder_text="Enter score 0-100"
)

midterm_entry.pack(pady=5)


# =========================
# CALCULATE BUTTON
# =========================

calculate_button = ctk.CTkButton(
    target_screen,
    text="CALCULATE OVERALL",
    command=calculate_overall
)

calculate_button.pack(pady=10)


# =========================
# RESULT
# =========================

result_label = ctk.CTkLabel(
    target_screen,
    text="Enter your scores and click Calculate Overall",
    font=("Arial", 15)
)

result_label.pack(pady=5)


# =========================
# BACK BUTTON
# =========================

back_button = ctk.CTkButton(
    target_screen,
    text="BACK",
    command=back_to_home
)

back_button.pack(pady=10)


# =========================
# IMAGE 1 - CENTER
# =========================

image1 = ctk.CTkImage(
    light_image=Image.open("image 1.png"),
    size=(150, 150)
)

image1_button = ctk.CTkButton(
    home_screen,
    text="",
    image=image1,
    width=150,
    height=150,
    fg_color="pink",
    hover_color="yellow",
    command=open_image1_screen
)

image1_button.place(
    relx=0.5,
    rely=0.5,
    anchor="center"
)


# =========================
# IMAGE 2 - TOP
# =========================

image2 = ctk.CTkImage(
    light_image=Image.open("image 2.png"),
    size=(160, 100)
)

image2_button = ctk.CTkButton(
    home_screen,
    text="",
    image=image2,
    width=160,
    height=100,
    fg_color="pink",
    hover_color="yellow"
)

image2_button.place(
    relx=0.5,
    rely=0.18,
    anchor="center"
)


# =========================
# IMAGE 3 - LEFT
# =========================

image3 = ctk.CTkImage(
    light_image=Image.open("image 3.png"),
    size=(160, 100)
)

image3_button = ctk.CTkButton(
    home_screen,
    text="",
    image=image3,
    width=160,
    height=100,
    fg_color="pink",
    hover_color="yellow"
)

image3_button.place(
    relx=0.18,
    rely=0.5,
    anchor="center"
)


# =========================
# IMAGE 4 - RIGHT
# =========================

image4 = ctk.CTkImage(
    light_image=Image.open("image 4.png"),
    size=(160, 100)
)

image4_button = ctk.CTkButton(
    home_screen,
    text="",
    image=image4,
    width=160,
    height=100,
    fg_color="pink",
    hover_color="yellow"
)

image4_button.place(
    relx=0.82,
    rely=0.5,
    anchor="center"
)


# =========================
# IMAGE 5 - BOTTOM
# =========================

image5 = ctk.CTkImage(
    light_image=Image.open("image 5.png"),
    size=(160, 100)
)

image5_button = ctk.CTkButton(
    home_screen,
    text="",
    image=image5,
    width=160,
    height=100,
    fg_color="pink",
    hover_color="yellow"
)

image5_button.place(
    relx=0.5,
    rely=0.82,
    anchor="center"
)


# =========================
# START
# =========================

app.mainloop()