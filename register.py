# =========================================================
# register.py
# =========================================================

import customtkinter as ctk
from PIL import Image
import json
import subprocess
import sys
from pathlib import Path

# =========================================================
# SETTINGS
# =========================================================

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

# =========================================================
# BASE PATH
# =========================================================

BASE_DIR = Path(__file__).resolve().parent
USER_DATA_FILE = BASE_DIR / "user_data.json"


def launch_script(script_name):

    subprocess.Popen([sys.executable, str(BASE_DIR / script_name)], cwd=BASE_DIR)


# =========================================================
# CREATE JSON FILE IF NOT EXISTS
# =========================================================

if not USER_DATA_FILE.exists():

    with open(USER_DATA_FILE, "w") as file:

        json.dump([], file)

# =========================================================
# MAIN WINDOW
# =========================================================

app = ctk.CTk()

app.title("Fruit Classifier - Register")

screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

app.geometry(f"{screen_width}x{screen_height}+0+0")

# =========================================================
# FUNCTIONS
# =========================================================

def open_login():

    app.destroy()

    launch_script("login.py")

# =========================================================
# REGISTER USER
# =========================================================

def register_user():

    name = fullname.get()
    mail = email.get()
    pwd = password.get()
    confirm_pwd = confirm_password.get()

    # =====================================================
    # VALIDATIONS
    # =====================================================

    if name == "" or mail == "" or pwd == "" or confirm_pwd == "":

        print("Please fill all fields")
        return

    if pwd != confirm_pwd:

        print("Passwords do not match")
        return

    # =====================================================
    # USER DATA
    # =====================================================

    user = {
        "fullname": name,
        "email": mail,
        "password": pwd
    }

    # =====================================================
    # LOAD EXISTING USERS
    # =====================================================

    try:

        with open(USER_DATA_FILE, "r") as file:

            data = json.load(file)

            if not isinstance(data, list):

                data = []

    except:

        data = []

    # =====================================================
    # APPEND USER
    # =====================================================

    data.append(user)

    # =====================================================
    # SAVE DATA
    # =====================================================

    with open(USER_DATA_FILE, "w") as file:

        json.dump(data, file, indent=4)

    print("Registration Successful")

    app.destroy()

    launch_script("login.py")

# =========================================================
# SHOW / HIDE PASSWORD
# =========================================================

def toggle_password(entry):

    if entry.cget("show") == "*":

        entry.configure(show="")

    else:

        entry.configure(show="*")

# =========================================================
# BACKGROUND IMAGE
# =========================================================

bg_image = ctk.CTkImage(
    Image.open(BASE_DIR / "static/images/registerimage.jpeg"),
    size=(screen_width, screen_height)
)

# =========================================================
# MAIN FRAME
# =========================================================

main_frame = ctk.CTkFrame(
    app,
    fg_color="white"
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
# NAVBAR
# =========================================================

navbar = ctk.CTkFrame(
    main_frame,

    height=80,

    fg_color="#14532d",

    corner_radius=0
)

navbar.pack(fill="x")

# =========================================================
# TITLE
# =========================================================

title = ctk.CTkLabel(
    navbar,

    text="Fruit Classifier",

    text_color="white",

    font=("Arial", 38, "bold")
)

title.pack(pady=18)

# =========================================================
# REGISTER CARD
# =========================================================

register_card = ctk.CTkFrame(
    main_frame,

    width=520,
    height=620,

    fg_color="#f8f8f8",

    corner_radius=20,

    border_width=2,

    border_color="#d1d5db"
)

register_card.place(
    relx=0.78,
    rely=0.50,
    anchor="center"
)

register_card.pack_propagate(False)

# =========================================================
# HEADING
# =========================================================

heading = ctk.CTkLabel(
    register_card,

    text="Create Account",

    text_color="#166534",

    font=("Arial", 36, "bold")
)

heading.pack(pady=(30,10))

line = ctk.CTkFrame(
    register_card,

    width=180,
    height=4,

    fg_color="#22c55e"
)

line.pack()

# =========================================================
# ENTRY SIZE
# =========================================================

ENTRY_WIDTH = 390
ENTRY_HEIGHT = 55

# =========================================================
# FULL NAME
# =========================================================

fullname = ctk.CTkEntry(
    register_card,

    width=ENTRY_WIDTH,
    height=ENTRY_HEIGHT,

    placeholder_text="Full Name",

    corner_radius=14,

    border_width=2,

    border_color="#22c55e",

    font=("Arial",16)
)

fullname.pack(pady=(30,12))

# =========================================================
# EMAIL
# =========================================================

email = ctk.CTkEntry(
    register_card,

    width=ENTRY_WIDTH,
    height=ENTRY_HEIGHT,

    placeholder_text="Email",

    corner_radius=14,

    border_width=2,

    border_color="#22c55e",

    font=("Arial",16)
)

email.pack(pady=12)

# =========================================================
# PASSWORD FRAME
# =========================================================

password_frame = ctk.CTkFrame(
    register_card,
    fg_color="transparent"
)

password_frame.pack(pady=12)

# =========================================================
# PASSWORD ENTRY
# =========================================================

password = ctk.CTkEntry(
    password_frame,

    width=320,
    height=ENTRY_HEIGHT,

    placeholder_text="Password",

    show="*",

    corner_radius=14,

    border_width=2,

    border_color="#22c55e",

    font=("Arial",16)
)

password.pack(side="left")

# =========================================================
# PASSWORD TOGGLE BUTTON
# =========================================================

eye_btn = ctk.CTkButton(
    password_frame,

    text="👁",

    width=55,
    height=ENTRY_HEIGHT,

    fg_color="#22c55e",

    hover_color="#15803d",

    corner_radius=14,

    command=lambda: toggle_password(password)
)

eye_btn.pack(side="left", padx=(8,0))

# =========================================================
# CONFIRM PASSWORD FRAME
# =========================================================

confirm_frame = ctk.CTkFrame(
    register_card,
    fg_color="transparent"
)

confirm_frame.pack(pady=12)

# =========================================================
# CONFIRM PASSWORD ENTRY
# =========================================================

confirm_password = ctk.CTkEntry(
    confirm_frame,

    width=320,
    height=ENTRY_HEIGHT,

    placeholder_text="Confirm Password",

    show="*",

    corner_radius=14,

    border_width=2,

    border_color="#22c55e",

    font=("Arial",16)
)

confirm_password.pack(side="left")

# =========================================================
# CONFIRM PASSWORD TOGGLE BUTTON
# =========================================================

confirm_eye = ctk.CTkButton(
    confirm_frame,

    text="👁",

    width=55,
    height=ENTRY_HEIGHT,

    fg_color="#22c55e",

    hover_color="#15803d",

    corner_radius=14,

    command=lambda: toggle_password(confirm_password)
)

confirm_eye.pack(side="left", padx=(8,0))

# =========================================================
# REGISTER BUTTON
# =========================================================

register_btn = ctk.CTkButton(
    register_card,

    text="Register",

    width=390,
    height=55,

    fg_color="#15803d",

    hover_color="#166534",

    text_color="white",

    font=("Arial",20,"bold"),

    corner_radius=14,

    command=register_user
)

register_btn.pack(pady=(25,15))

# =========================================================
# BOTTOM FRAME
# =========================================================

bottom_frame = ctk.CTkFrame(
    register_card,
    fg_color="transparent"
)

bottom_frame.pack(pady=(10,0))

# =========================================================
# LOGIN TEXT
# =========================================================

bottom_text = ctk.CTkLabel(
    bottom_frame,

    text="Already have an account?",

    text_color="#374151",

    font=("Arial",16)
)

bottom_text.pack(side="left")

# =========================================================
# SIGN IN BUTTON
# =========================================================

signin = ctk.CTkButton(
    bottom_frame,

    text=" Sign In",

    fg_color="transparent",

    hover=False,

    text_color="#15803d",

    font=("Arial",16,"bold"),

    width=20,

    command=open_login
)

signin.pack(side="left")

# =========================================================
# RUN APP
# =========================================================

app.mainloop()