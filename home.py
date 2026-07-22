# =========================================================
# home.py
# =========================================================

import customtkinter as ctk
from PIL import Image
import os
import subprocess
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def launch_screen(script_name):
    subprocess.Popen([sys.executable, os.path.join(BASE_DIR, script_name)], cwd=BASE_DIR)

# =========================================================
# SETTINGS
# =========================================================

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

# =========================================================
# MAIN WINDOW
# =========================================================

app = ctk.CTk()
app.title("Fruit Classifier - Home")

screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
app.geometry(f"{screen_width}x{screen_height}+0+0")


# =========================================================
# FUNCTIONS
# =========================================================

def open_login():
    app.destroy()
    launch_screen("login.py")


def open_home():
    app.destroy()
    launch_screen("home.py")


def open_history():
    app.destroy()
    launch_screen("history.py")


def open_capture():
    app.destroy()
    launch_screen("main.py")


def open_sensor():
    app.destroy()
    launch_screen("iot.py")


def open_result():
    app.destroy()
    launch_screen("result.py")


def logout():
    app.destroy()
    launch_screen("login.py")

# =========================================================
# BACKGROUND IMAGE
# =========================================================

bg_image = ctk.CTkImage(
    Image.open("static/images/homebackground.jpeg"),
    size=(screen_width, screen_height)
)

# =========================================================
# MAIN FRAME
# =========================================================

main_frame = ctk.CTkFrame(
    app,
    fg_color="#dff2b2",
    corner_radius=0
)
main_frame.pack(fill="both", expand=True)

# =========================================================
# BACKGROUND LABEL
# =========================================================

bg_label = ctk.CTkLabel(
    main_frame,
    image=bg_image,
    text=""
)
bg_label.place(relwidth=1, relheight=1)

# =========================================================
# COLLEGE HEADER
# =========================================================

header = ctk.CTkFrame(
    main_frame,
    height=130,
    fg_color="white",
    corner_radius=0
)
header.pack(fill="x")

# =========================================================
# LEFT LOGO
# =========================================================

left_logo_img = ctk.CTkImage(
    Image.open("static/images/download.jpeg"),
    size=(100, 100)
)
left_logo = ctk.CTkLabel(header, image=left_logo_img, text="")
left_logo.place(x=30, y=15)

# =========================================================
# RIGHT LOGO
# =========================================================

right_logo_img = ctk.CTkImage(
    Image.open("static/images/logo2.jpeg"),
    size=(100, 100)
)
right_logo = ctk.CTkLabel(header, image=right_logo_img, text="")
right_logo.place(relx=0.92, y=15)

# =========================================================
# COLLEGE TITLE
# =========================================================

title = ctk.CTkLabel(
    header,
    text="GAYATRI VIDYA PARISHAD\nCOLLEGE FOR DEGREE AND PG COURSES (A)",
    text_color="black",
    font=("Times New Roman", 30, "bold")
)
title.place(relx=0.5, rely=0.5, anchor="center")

# =========================================================
# NAVIGATION BAR
# =========================================================

navbar = ctk.CTkFrame(
    main_frame,
    height=65,
    fg_color="#558B2f",
    corner_radius=0
)
navbar.pack(fill="x")

# =========================================================
# NAVIGATION BUTTONS
# =========================================================

nav_font = ("Arial", 17, "bold")

buttons = [
    ("Login", open_login),
    ("Home", open_home),
    ("Capture Fruit", open_capture),
    ("Read Sensor Values", open_sensor),
    ("View Result", open_result),
    ("Logout", logout)
]

for text, cmd in buttons:
    btn = ctk.CTkButton(
        navbar,
        text=text,
        fg_color="#8BC34A",
        hover_color="#C5E1A5",
        text_color="black",
        font=nav_font,
        corner_radius=18,
        height=45,
        border_width=1,
        border_color="#689F38",
        command=cmd
    )
    btn.pack(side="left", expand=True, padx=12, pady=10)

# =========================================================
# FEATURE BOX FUNCTION
# =========================================================

def create_feature_box(x_pos, title_text, desc_text, button_text, command):
    box = ctk.CTkFrame(
        main_frame,
        width=320,
        height=260,
        fg_color="#fef9c3",
        bg_color="#dff2b2",
        corner_radius=25,
        border_width=3,
        border_color="#facc15"
    )
    box.place(relx=x_pos, rely=0.48, anchor="center")
    box.pack_propagate(False)

    heading = ctk.CTkLabel(
        box,
        text=title_text,
        text_color="black",
        font=("Arial", 26, "bold")
    )
    heading.pack(pady=(35, 15))

    description = ctk.CTkLabel(
        box,
        text=desc_text,
        text_color="#374151",
        font=("Arial", 16),
        wraplength=240,
        justify="center"
    )
    description.pack(pady=10)

    open_btn = ctk.CTkButton(
        box,
        text=button_text,
        width=180,
        height=50,
        fg_color="#eab308",
        hover_color="#ca8a04",
        text_color="black",
        font=("Arial", 18, "bold"),
        corner_radius=14,
        command=command
    )
    open_btn.pack(pady=25)

# =========================================================
# FEATURE BOXES
# =========================================================

create_feature_box(0.22, "Capture Fruit Image", "Upload or capture fruit image for analysis.", "Open", open_capture)
create_feature_box(0.50, "Read Sensor Values", "View sensor readings and collected values.", "Open", open_sensor)
create_feature_box(0.78, "View Result", "Check whether fruit is Organic/Inorganic.", "Open", open_result)

# =========================================================
# RUN APPLICATION
# =========================================================

app.mainloop()