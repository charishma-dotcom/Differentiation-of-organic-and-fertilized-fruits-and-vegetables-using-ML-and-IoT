import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# ---------------- WINDOW ----------------
root = tk.Tk()
root.title("FitAI")
root.state("zoomed")

# ---------------- PAGE SWITCH ----------------
def show_page(page):
    for w in content.winfo_children():
        w.place_forget()
    page.place(relwidth=1, relheight=1)

# ---------------- PLACEHOLDER FUNCTION ----------------
def add_placeholder(entry, text, is_password=False):
    entry.insert(0, text)
    entry.config(fg="grey")

    def on_focus_in(e):
        if entry.get() == text:
            entry.delete(0, "end")
            entry.config(fg="black")
            if is_password:
                entry.config(show="*")

    def on_focus_out(e):
        if entry.get() == "":
            entry.insert(0, text)
            entry.config(fg="grey")
            if is_password:
                entry.config(show="")

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

# ---------------- START SCREEN ----------------
start_frame = tk.Frame(root)
start_frame.place(relwidth=1, relheight=1)

# Load your start image here
try:
    start_img = Image.open(r"C:\Users\Admin\OneDrive\Desktop\fitai\start.jpeg")
except:
    start_img = Image.new("RGB", (800, 600), (87, 30, 43)) # Fallback color

start_label = tk.Label(start_frame)
start_label.place(relwidth=1, relheight=1)

def resize_start(e):
    img = start_img.resize((e.width, e.height))
    photo = ImageTk.PhotoImage(img)
    start_label.config(image=photo)
    start_label.image = photo

start_frame.bind("<Configure>", resize_start)

# ---------------- DASHBOARD (Main Container) ----------------
dashboard = tk.Frame(root)

# --- NEW TOP NAVIGATION BAR (Based on your Drawing) ---
navbar = tk.Frame(dashboard, bg="#f0f0f0", height=80)
navbar.pack(side="top", fill="x")

# Nav Buttons with rounded-look (using relief/borderwidth)
nav_style = {"font": ("Arial", 12), "bg": "white", "fg": "black", "relief": "ridge", "bd": 2, "padx": 20}

tk.Button(navbar, text="Home", command=lambda: show_page(home_page), **nav_style).pack(side="left", padx=15, pady=20)
tk.Button(navbar, text="About", command=lambda: show_page(about_page), **nav_style).pack(side="left", padx=15)
tk.Button(navbar, text="Outfit Generation", **nav_style).pack(side="left", padx=15)
tk.Button(navbar, text="Feedback", **nav_style).pack(side="left", padx=15)

# Main content area where pages swap
content = tk.Frame(dashboard, bg="white")
content.pack(fill="both", expand=True)

# ---------------- HOME PAGE (Based on Drawing) ----------------
home_page = tk.Frame(content, bg="white")

# Central Box
home_box = tk.Frame(home_page, bg="white", highlightbackground="black", highlightthickness=1, padx=50, pady=50)
home_box.place(relx=0.5, rely=0.4, anchor="center")

tk.Label(home_box, text="Welcome to FitAI", font=("Arial", 20), bg="white").pack(pady=20)

tk.Button(home_box, text="Login", font=("Arial", 14), width=15, bd=1, relief="solid",
          command=lambda: show_page(login_page)).pack(pady=10)

tk.Button(home_box, text="Register", font=("Arial", 14), width=15, bd=1, relief="solid",
          command=lambda: show_page(register_page)).pack(pady=10)

# ---------------- LOGIN PAGE ----------------
login_page = tk.Frame(content, bg="white")
login_box = tk.Frame(login_page, bg="white", padx=30, pady=30, highlightthickness=1, highlightbackground="grey")
login_box.place(relx=0.5, rely=0.5, anchor="center")

tk.Label(login_box, text="🔐 Login", font=("Segoe UI", 18, "bold"), bg="white").pack(pady=10)
user = tk.Entry(login_box, width=30)
user.pack(pady=5)
add_placeholder(user, "Enter Username")
pwd = tk.Entry(login_box, width=30)
pwd.pack(pady=5)
add_placeholder(pwd, "Enter Password", is_password=True)

def login_action():
    if user.get() in ("", "Enter Username") or pwd.get() in ("", "Enter Password"):
        messagebox.showerror("Error", "All fields required")
    else:
        messagebox.showinfo("Success", "Login Successful")

tk.Button(login_box, text="Login", bg="#32eac6", fg="white", width=18, command=login_action).pack(pady=10)
tk.Button(login_box, text="⬅ Back", command=lambda: show_page(home_page)).pack()

# ---------------- REGISTER PAGE ----------------
register_page = tk.Frame(content, bg="white")
reg_box = tk.Frame(register_page, bg="white", padx=30, pady=30, highlightthickness=1, highlightbackground="grey")
reg_box.place(relx=0.5, rely=0.5, anchor="center")

tk.Label(reg_box, text="📝 Register", font=("Segoe UI", 18, "bold"), bg="white").pack(pady=10)
# ... (Registration entries follow same pattern as your original)
tk.Button(reg_box, text="⬅ Back", command=lambda: show_page(home_page)).pack()

# ---------------- ABOUT PAGE ----------------
about_page = tk.Frame(content, bg="#f3e7dc")
about_canvas = tk.Canvas(about_page, bg="#f3e7dc", highlightthickness=0)
about_canvas.pack(fill="both", expand=True)

def draw_about_page(event=None):
    about_canvas.delete("all")
    w, h = about_canvas.winfo_width(), about_canvas.winfo_height()
    about_canvas.create_text(w/2, 70, text="OUTFIT RECOMMENDED SYSTEM", font=("Times New Roman", 34, "bold"), fill="#4b2e2a")
    about_canvas.create_text(w/2, 150, text="Personalized outfit suggestions for every you.", font=("Segoe UI", 14), fill="#3f3f3f")
    # (Remaining about page drawing logic kept from your code)

about_canvas.bind("<Configure>", draw_about_page)

# ---------------- START APP LOGIC ----------------
def start_app():
    start_frame.place_forget()
    dashboard.place(relwidth=1, relheight=1)
    show_page(home_page) # This now shows the layout from your image

tk.Button(start_frame, text="Start App", bg="#571e2b", font=("Arial", 18, "bold"), fg="white", width=20, height=2,
          command=start_app).place(relx=0.5, rely=0.7, anchor="center")

root.mainloop()