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


def launch_screen(script_name):
    subprocess.Popen([sys.executable, str(BASE_DIR / script_name)], cwd=BASE_DIR)

# =========================================================
# MAIN WINDOW
# =========================================================

app = ctk.CTk()

app.title("Fruit Classifier - Login")

screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

app.geometry(f"{screen_width}x{screen_height}+0+0")

# =========================================================
# FUNCTIONS
# =========================================================

def open_register():
    app.destroy()
    launch_screen("register.py")

# =========================================================
# LOGIN FUNCTION
# =========================================================

def login_user():

    mail = email.get()
    pwd = password.get()

    if mail == "" or pwd == "":

        print("Please fill all fields")
        return

    try:

        with open(USER_DATA_FILE, "r") as file:

            users = json.load(file)

            if not isinstance(users, list):

                users = []

    except:

        users = []

    for user in users:

        try:

            if user["email"] == mail and user["password"] == pwd:

                print("Login Successful")

                app.destroy()
                launch_screen("home.py")
                return

        except:

            pass

    print("Invalid Email or Password")

# =========================================================
# SHOW / HIDE PASSWORD
# =========================================================

def toggle_password(entry):

    if entry.cget("show") == "*":

        entry.configure(show="")

    else:

        entry.configure(show="*")

# =========================================================
# BACKGROUND
# =========================================================

bg_image = ctk.CTkImage(
    Image.open(BASE_DIR / "static/images/loginimage.jpeg"),
    size=(screen_width, screen_height)
)

main_frame = ctk.CTkFrame(app, fg_color="white")

main_frame.pack(fill="both", expand=True)

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

title = ctk.CTkLabel(
    navbar,
    text="Fruit Classifier",
    text_color="white",
    font=("Arial", 38, "bold")
)

title.pack(pady=18)

# =========================================================
# LOGIN CARD
# =========================================================

login_card = ctk.CTkFrame(
    main_frame,
    width=500,
    height=500,
    fg_color="#f8f8f8",
    corner_radius=0,
    border_width=2,
    border_color="#d1d5db"
)

login_card.place(
    relx=0.78,
    rely=0.50,
    anchor="center"
)

login_card.pack_propagate(False)

# =========================================================
# HEADING
# =========================================================

heading = ctk.CTkLabel(
    login_card,
    text="Welcome Back",
    text_color="#166534",
    font=("Arial", 36, "bold")
)

heading.pack(pady=(35, 10))

line = ctk.CTkFrame(
    login_card,
    width=170,
    height=4,
    fg_color="#22c55e"
)

line.pack()

# =========================================================
# EMAIL
# =========================================================

email = ctk.CTkEntry(
    login_card,
    width=380,
    height=55,
    placeholder_text="Enter Email",
    corner_radius=14,
    border_width=2,
    border_color="#22c55e",
    font=("Arial", 16)
)

email.pack(pady=(40, 15))

# =========================================================
# PASSWORD
# =========================================================

password_frame = ctk.CTkFrame(
    login_card,
    fg_color="transparent"
)

password_frame.pack(pady=15)

password = ctk.CTkEntry(
    password_frame,
    width=310,
    height=55,
    placeholder_text="Enter Password",
    show="*",
    corner_radius=14,
    border_width=2,
    border_color="#22c55e",
    font=("Arial", 16)
)

password.pack(side="left")

eye_btn = ctk.CTkButton(
    password_frame,
    text="👁",
    width=55,
    height=55,
    fg_color="#22c55e",
    hover_color="#15803d",
    corner_radius=14,
    command=lambda: toggle_password(password)
)

eye_btn.pack(side="left", padx=(8, 0))

# =========================================================
# LOGIN BUTTON
# =========================================================

login_btn = ctk.CTkButton(
    login_card,
    text="Login",
    width=380,
    height=55,
    fg_color="#15803d",
    hover_color="#166534",
    font=("Arial", 20, "bold"),
    corner_radius=14,
    command=login_user
)

login_btn.pack(pady=(30, 15))

# =========================================================
# CREATE ACCOUNT
# =========================================================

bottom_frame = ctk.CTkFrame(
    login_card,
    fg_color="transparent"
)

bottom_frame.pack(pady=(15, 0))

bottom_text = ctk.CTkLabel(
    bottom_frame,
    text="Don't have an account?",
    text_color="#374151",
    font=("Arial", 16)
)

bottom_text.pack(side="left")

create_btn = ctk.CTkButton(
    bottom_frame,
    text=" Create Account",
    fg_color="transparent",
    hover=False,
    text_color="#15803d",
    font=("Arial", 16, "bold"),
    width=20,
    command=open_register
)

create_btn.pack(side="left")

# =========================================================
# RUN APP
# =========================================================

if __name__ == "__main__":

    app.mainloop()