import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import sqlite3
import subprocess
import sys
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def launch_screen(script_name):
    subprocess.Popen([sys.executable, os.path.join(BASE_DIR, script_name)], cwd=BASE_DIR)

class StoredResultsSystem:
    def __init__(self, window):
        self.window = window
        # --- TITLE CONFIGURATION ---
        self.window.title("Fruit Classifier - History")
        self.window.attributes('-fullscreen', True)
        self.sw = self.window.winfo_screenwidth()
        self.sh = self.window.winfo_screenheight()

        # Define Colors for the added Header
        self.nav_bg = "#4A7031"       # Dark green header matching main.py
        self.nav_btn_bg = "#8FBC5A"   # Light green buttons matching main.py
        self.title_bar_bg = "#f0f0f0" # Light gray title strip

        # 1. ADD THE HEADER (Title strip + Nav bar)
        self.create_header()

        # Canvas for the background image/color
        self.canvas = tk.Canvas(self.window, width=self.sw, height=self.sh, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        try:
            bg_img = Image.open("resultimage.jpeg").resize((self.sw, self.sh), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(bg_img)
            self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
        except:
            self.canvas.configure(bg="#dff2b2")

        # --- INSTANTIATE WIDGET CONTEXT IN CORRECT ORDER ---
        self.create_widgets()
        self.load_data() # Populates the tree data grid matrix cleanly

    def create_header(self):
        """Adds the grey title strip and green nav bar to the top"""
        top_container = tk.Frame(self.window)
        top_container.pack(side="top", fill="x")

        # Part A: Grey Title Strip
        title_strip = tk.Frame(top_container, bg=self.title_bar_bg, height=30)
        title_strip.pack(side="top", fill="x")
        
        tk.Label(title_strip, text="Fruit Classifier - History", 
                 font=("Segoe UI", 9), bg=self.title_bar_bg, padx=10).pack(side="left")

        # Window Controls
        control_style = {"bg": self.title_bar_bg, "font": ("Arial", 10), "bd": 0, "padx": 10}
        tk.Button(title_strip, text="✕", command=self.window.destroy, **control_style).pack(side="right")
        tk.Button(title_strip, text="❐", command=lambda: self.window.attributes('-fullscreen', False), **control_style).pack(side="right")
        tk.Button(title_strip, text="—", command=lambda: self.window.state('iconic'), **control_style).pack(side="right")

        # Part B: Green Nav Bar
        self.nav_frame = tk.Frame(top_container, bg=self.nav_bg, height=50)
        self.nav_frame.pack(side="top", fill="x")
        self.nav_frame.pack_propagate(False)

        nav_style = {"bg": self.nav_btn_bg, "font": ("Times New Roman", 11, "bold"), "bd": 0, "padx": 15, "cursor": "hand2"}

        tk.Button(self.nav_frame, text="Home", command=self.go_home_nav, **nav_style).pack(side="left", padx=5, pady=8)
        tk.Button(self.nav_frame, text="Capture Fruit", command=self.go_main_nav, **nav_style).pack(side="left", padx=5)
        tk.Button(self.nav_frame, text="History", command=self.go_history_nav, **nav_style).pack(side="left", padx=5)
        tk.Button(self.nav_frame, text="Logout", command=self.go_home_nav, **nav_style).pack(side="right", padx=15)
        
    def go_home_nav(self):
        self.window.destroy()
        launch_screen("home.py")

    def go_main_nav(self):
        self.window.destroy()
        launch_screen("main.py")

    def go_history_nav(self):
        self.window.destroy()
        launch_screen("history.py")

    def create_widgets(self):
        # --- TITLE SECTION ---
        title_frame = tk.Frame(self.window, bg="#4A7031", bd=2, relief="flat")
        tk.Label(title_frame, text="Stored Fruit Analysis Results", 
                 font=("Times New Roman", 24, "bold"), bg="#4A7031", fg="white", pady=5).pack(padx=60)
        self.canvas.create_window(self.sw/2, 80, window=title_frame)

        # --- TABLE CONTAINER ---
        self.table_container = tk.Frame(self.window, bg="white", bd=1, relief="solid")
        self.canvas.create_window(self.sw/2, self.sh*0.48, window=self.table_container, 
                                  width=self.sw*0.96, height=self.sh*0.68)

        style = ttk.Style()
        style.theme_use('clam') 
        style.configure("Treeview", font=("Times New Roman", 12), rowheight=40, background="white", borderwidth=2)
        style.configure("Treeview.Heading", font=("Times New Roman", 13, "bold"), background="#f4f4f4", relief="solid")

        # --- COLUMNS ---
        columns = ("Detected", "Size", "Shape", "Color", "pH_Value", "Gas_Value", "Accuracy", "Status")
        self.tree = ttk.Treeview(self.table_container, columns=columns, show='headings', style="Treeview")
        
        display_headings = {
            "Detected": "Fruit Name",
            "Size": "Size",
            "Shape": "Shape",
            "Color": "Color",
            "pH_Value": "pH value",
            "Gas_Value": "Gas value",
            "Accuracy": "Accuracy",
            "Status": "Status"
        }

        for col in columns:
            self.tree.heading(col, text=display_headings[col])
            self.tree.column(col, width=120, anchor="center", stretch=True)

        v_scroll = ttk.Scrollbar(self.table_container, orient="vertical", command=self.tree.yview)
        h_scroll = ttk.Scrollbar(self.table_container, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscroll=v_scroll.set, xscroll=h_scroll.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scroll.grid(row=0, column=1, sticky="ns")
        h_scroll.grid(row=1, column=0, sticky="ew")
        
        self.table_container.grid_rowconfigure(0, weight=1)
        self.table_container.grid_columnconfigure(0, weight=1)

        # --- BOTTOM BUTTONS ---
        def go_home():
            self.window.destroy()
            launch_screen("home.py")

        def go_back():
            self.window.destroy()
            launch_screen("main.py")

        btn_style = {"font": ("Times New Roman", 16, "bold"), "width": 14, "bd": 1, "relief": "solid"}
        tk.Button(self.window, text="BACK", command=go_back, bg="#f5f5dc", **btn_style).place(x=self.sw*0.35, y=self.sh-50, anchor="center")
        tk.Button(self.window, text="REFRESH", command=self.load_data, bg="#4A7031", fg="white", **btn_style).place(x=self.sw*0.50, y=self.sh-50, anchor="center")
        tk.Button(self.window, text="EXIT", command=go_home, bg="#ff0000", fg="white", **btn_style).place(x=self.sw*0.65, y=self.sh-50, anchor="center")

    def load_data(self):
        """Pulls clean histories from database - Limited to past 5 entries"""
        # Clear existing table data to prevent duplicate stacks on refresh
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        try:
            conn = sqlite3.connect('fruit_database.db')
            cursor = conn.cursor()
            
            # Ensure table exists structure-wise
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS analysis_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    FruitName TEXT, Size TEXT, Shape TEXT, 
                    Color TEXT, pH TEXT, Gas_Value TEXT, Accuracy TEXT, Label TEXT
                )
            """)
            
            # --- FIXED: Added LIMIT 5 to only fetch the 5 most recent records ---
            cursor.execute("""
                SELECT FruitName, Size, Shape, Color, pH, Gas_Value, Accuracy, Label 
                FROM analysis_results 
                ORDER BY id DESC 
                LIMIT 5
            """)
            rows = cursor.fetchall()
            
            for row in rows:
                self.tree.insert("", "end", values=(
                    row[0] if row[0] else "Unknown",
                    row[1] if row[1] else "N/A",
                    row[2] if row[2] else "N/A",
                    row[3] if row[3] else "N/A",
                    row[4] if row[4] else "--",  # Live pH
                    row[5] if row[5] else "--",  # Live Gas
                    row[6] if row[6] else "--",  # Live Accuracy
                    row[7] if row[7] else "Organic"
                ))
            conn.close()
        except Exception as e:
            print(f"History Load Error: {e}")
if __name__ == "__main__":
    root = tk.Tk()
    app = StoredResultsSystem(root)
    root.mainloop()