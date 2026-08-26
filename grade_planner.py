import customtkinter as ctk
from PIL import Image

app = ctk.CTk()
app.geometry("750x500")
app.title("GRADE PLANNER")

# BACKGROUND
background_image = ctk.CTkImage(
    light_image=Image.open("background.png"),
    size=(750, 500)
)

background = ctk.CTkLabel(
    app,
    text="",
    image=background_image
)

background.place(
    x=0,
    y=0,
    relwidth=1,
    relheight=1
)

image1 = ctk.CTkImage(
    light_image=Image.open("image 1.png"),
    size=(150, 150)
)
image1_button = ctk.CTkButton(
    app,
    text="",
    image=image1,
    width=150,
    height=150,
    fg_color="pink",
    hover_color="yellow",
    command=lambda: print("image 1 CLICKED")
)
image1_button.place(
    relx=0.5,
    rely=0.5,
    anchor="center"
)


# IMAGE 2 - TOP
image2 = ctk.CTkImage(
    light_image=Image.open("image 2.png"),
    size=(160, 100)
)

image2_button = ctk.CTkButton(
    app,
    text="",
    image=image2,
    width=160,
    height=100,
    fg_color="pink",
    hover_color="yellow",
    command=lambda: print("image 2 CLICKED")
)

image2_button.place(
    relx=0.5,
    rely=0.18,
    anchor="center"
)


# IMAGE 3 - LEFT
image3 = ctk.CTkImage(
    light_image=Image.open("image 3.png"),
    size=(160, 100)
)

image3_button = ctk.CTkButton(
    app,
    text="",
    image=image3,
    width=160,
    height=100,
    fg_color="pink",
    hover_color="yellow",
    command=lambda: print("image 3 CLICKED")
)

image3_button.place(
    relx=0.18,
    rely=0.5,
    anchor="center"
)


# IMAGE 4 - RIGHT
image4 = ctk.CTkImage(
    light_image=Image.open("image 4.png"),
    size=(160, 100)
)

image4_button = ctk.CTkButton(
    app,
    text="",
    image=image4,
    width=160,
    height=100,
    fg_color="pink",
    hover_color="yellow",
    command=lambda: print("image 4 CLICKED")
)

image4_button.place(
    relx=0.82,
    rely=0.5,
    anchor="center"
)


# IMAGE 5 - BOTTOM
image5 = ctk.CTkImage(
    light_image=Image.open("image 5.png"),
    size=(160, 100)
)

image5_button = ctk.CTkButton(
    app,
    text="",
    image=image5,
    width=160,
    height=100,
    fg_color="pink",
    hover_color="yellow",
    command=lambda: print("image 5 CLICKED")
)

image5_button.place(
    relx=0.5,
    rely=0.82,
    anchor="center"
)

app.mainloop()