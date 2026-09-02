import customtkinter as ctk
from PIL import Image


# MAIN WINDOW

app = ctk.CTk()
app.geometry("800x700")
app.title("GRADE PLANNER")



# SCREEN 1 - HOME

home_screen = ctk.CTkFrame(app)
home_screen.pack(fill="both", expand=True)


# BACKGROUND

background_image = ctk.CTkImage(
    light_image=Image.open("background.png"),
    size=(800, 700)
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

# OPEN SCREEN  ( FROM IMAGE 1)

def open_image1_screen():
    home_screen.pack_forget()
    calculate_overall_screen.pack(fill="both", expand=True)

# IMAGE 1 

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

# IMAGE 2 


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

# IMAGE 3

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

# IMAGE 4 

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

# IMAGE 5 


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

# SCREEN 2 - background 2

calculate_overall_screen = ctk.CTkFrame(app)

calculate_overall_background_image = ctk.CTkImage(
    light_image=Image.open("background.png"),
    size=(800, 700)
)

calculate_overall_background = ctk.CTkLabel(
    calculate_overall_screen,
    text="",
    image=calculate_overall_background_image
)

calculate_overall_background.place(
    x=0,
    y=0,
    relwidth=1,
    relheight=1
)


# CALCULATE OVERALL - IMAGE 1

def calculate_overall():

    try:
        quiz_score = float(quiz_entry.get())
        quiz_weight = float(quiz_weight_entry.get())

        assignment_score = float(assignment_entry.get())
        assignment_weight = float(assignment_weight_entry.get())

        midterm_score = float(midterm_entry.get())
        midterm_weight = float(midterm_weight_entry.get())


        # CHECK SCORES

        if not 0 <= quiz_score <= 100:
            result_label.configure(
                text="Quiz score must be 0-100"
            )
            return

        if not 0 <= assignment_score <= 100:
            result_label.configure(
                text="Assignment score must be 0-100"
            )
            return

        if not 0 <= midterm_score <= 100:
            result_label.configure(
                text="Midterm score must be 0-100"
            )
            return


        # CHECK WEIGHTS

        if not 0 <= quiz_weight <= 100:
            result_label.configure(
                text="Quiz weight must be 0-100"
            )
            return

        if not 0 <= assignment_weight <= 100:
            result_label.configure(
                text="Assignment weight must be 0-100"
            )
            return

        if not 0 <= midterm_weight <= 100:
            result_label.configure(
                text="Midterm weight must be 0-100"
            )
            return


        # CALCULATE EARNED MARKS

        quiz_earned = quiz_score * quiz_weight / 100

        assignment_earned = (
            assignment_score * assignment_weight / 100
        )

        midterm_earned = (
            midterm_score * midterm_weight / 100
        )


        # CURRENT EARNED

        current_earned = (
            quiz_earned
            + assignment_earned
            + midterm_earned
        )


        # COMPLETED WEIGHT

        completed_weight = (
            quiz_weight
            + assignment_weight
            + midterm_weight
        )


        # CHECK TOTAL WEIGHT

        if completed_weight > 100:
            result_label.configure(
                text="Total weight cannot be more than 100%"
            )
            return


        # CHECK IF WEIGHT IS 0

        if completed_weight == 0:
            result_label.configure(
                text="Please enter at least one weight."
            )
            return


        # REMAINING WEIGHT

        remaining_weight = 100 - completed_weight


        # CURRENT PERFORMANCE

        current_performance = (
            current_earned / completed_weight
        ) * 100


        # DISPLAY RESULTS

        result_label.configure(
            text=(
                f"Current Earned: {current_earned:.2f}%\n"
                f"Completed Weight: {completed_weight:.2f}%\n"
                f"Remaining Weight: {remaining_weight:.2f}%\n"
                f"Current Performance: {current_performance:.2f}%"
            )
        )


    except ValueError:
        result_label.configure(
            text="Please enter valid numbers."
        )


# TITLE

title = ctk.CTkLabel(
    calculate_overall_screen,
    text="CALCULATE OVERALL PERFORMANCE",
    text_color="#BE165F",
    font=("Arial", 24, "bold"),
    fg_color="#FBDCEE"
)
title.pack(pady=(10, 20))




# QUIZ


quiz_label = ctk.CTkLabel(
   calculate_overall_screen,
    text="Quiz Score (Weight: 20%)",
    text_color= "#1DB51B",
    font=("Arial", 18,),
    fg_color="#F4F1F1"
)


quiz_label.pack()

quiz_entry = ctk.CTkEntry(
   calculate_overall_screen,
    placeholder_text="Enter score 0-100"
)

quiz_entry.pack(pady=5)



# ASSIGNMENT


assignment_label = ctk.CTkLabel(
    calculate_overall_screen,
    text="Assignment Score (Weight: 20%)",
     text_color= "#411BB5",
    font=("Arial", 18,),
    fg_color="#F4F1F1"
)

assignment_label.pack()

assignment_entry = ctk.CTkEntry(
  calculate_overall_screen,
    placeholder_text="Enter score 0-100"
)

assignment_entry.pack(pady=5)



# MIDTERM


midterm_label = ctk.CTkLabel(
   calculate_overall_screen,
    text="Midterm Score (Weight: 20%)",
    text_color= "#98102B",
    font=("Arial", 18,),
    fg_color="#F4F1F1"
)


midterm_label.pack()

midterm_entry = ctk.CTkEntry(
    calculate_overall_screen,
    placeholder_text="Enter score 0-100"
)

midterm_entry.pack(pady=5)
                  



# CALCULATE BUTTON


calculate_button = ctk.CTkButton(
   calculate_overall_screen,
    text="CALCULATE OVERALL",
    command=calculate_overall
)

calculate_button.pack(pady=10)



# RESULT


result_label = ctk.CTkLabel(
   calculate_overall_screen,
    text="Enter your scores and click Calculate Overall",
    font=("Arial", 15)
)

result_label.pack(pady=5)

# BACK TO HOME


def back_to_home():
  calculate_overall_screen.pack_forget()
  home_screen.pack(fill="both", expand=True)


# BACK BUTTON


back_button = ctk.CTkButton(
  calculate_overall_screen,
    text="BACK",
    command=back_to_home
)

back_button.pack(pady=10)




app.mainloop()
