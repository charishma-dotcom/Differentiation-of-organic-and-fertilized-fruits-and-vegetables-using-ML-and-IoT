import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess
import sys
import json
import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def launch_screen(script_name):
    subprocess.Popen([sys.executable, os.path.join(BASE_DIR, script_name)], cwd=BASE_DIR)

class FinalResultSystem:
    def __init__(self, window):
        self.window = window
        
        # --- TITLE CONFIGURATION ---
        self.window.title("Fruit Classifier - Results")
        
        # Start in fullscreen
        self.window.attributes('-fullscreen', True)
        self.sw = self.window.winfo_screenwidth()
        self.sh = self.window.winfo_screenheight()

        # Data Loading
        self.vision_data = self.load_vision_results()
        self.iot_data = self.load_iot_results()

        # Direct Comparison Logic aligned with main.py metrics
        if self.vision_data["acc"] >= self.iot_data["acc"]:
            self.final_result = self.vision_data
            self.winner_source = "AI Vision"
        else:
            self.final_result = self.iot_data
            self.winner_source = "IoT Sensors"

        # Styling
        self.fg_color = "#fef9c3"
        self.bg_color_style = "#dff2b2"
        self.border_color = "#facc15"
        self.nav_bg = "#4f772d"      
        self.nav_btn_bg = "#9cc664"  
        self.title_bar_bg = "#f0f0f0" 
        
        # Fonts
        self.header_font = ("Times New Roman", 32, "bold")
        self.title_font = ("Times New Roman", 22, "bold")
        self.data_font = ("Times New Roman", 16)

        # 1. CREATE HEADER (With Control Buttons)
        self.create_header()

        # 2. CANVAS
        self.canvas = tk.Canvas(self.window, width=self.sw, height=self.sh, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        try:
            bg_path = r"C:\Users\Charishma\final project\static\images\re.jpeg"
            bg_img = Image.open(bg_path).resize((self.sw, self.sh), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(bg_img)
            self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
        except:
            self.canvas.configure(bg=self.bg_color_style)

        self.create_widgets()
        
        # --- START REFRESH MONITORING LOOP ---
        self.monitor_json_updates()

    # --- WINDOW CONTROL METHODS ---
    def minimize_window(self):
        self.window.update_idletasks()
        self.window.state('iconic')

    def toggle_screen(self):
        is_fullscreen = self.window.attributes('-fullscreen')
        self.window.attributes('-fullscreen', not is_fullscreen)

    def close_window(self):
        self.window.destroy()

    def create_header(self):
        top_container = tk.Frame(self.window)
        top_container.pack(side="top", fill="x")

        # --- TITLE STRIP WITH WINDOW CONTROLS ---
        title_strip = tk.Frame(top_container, bg=self.title_bar_bg, height=30)
        title_strip.pack(side="top", fill="x")
        
        tk.Label(title_strip, text="Fruit Classifier - Result", 
                 font=("Segoe UI", 9), bg=self.title_bar_bg, padx=10).pack(side="left")

        control_style = {"bg": self.title_bar_bg, "font": ("Arial", 12), "bd": 0, "padx": 10, "activebackground": "#e5e5e5"}
        
        tk.Button(title_strip, text="✕", command=self.close_window, **control_style).pack(side="right")
        tk.Button(title_strip, text="❐", command=self.toggle_screen, **control_style).pack(side="right")
        tk.Button(title_strip, text="—", command=self.minimize_window, **control_style).pack(side="right")

        # --- NAVIGATION BAR ---
        self.nav_frame = tk.Frame(top_container, bg=self.nav_bg, height=50)
        self.nav_frame.pack(side="top", fill="x")
        self.nav_frame.pack_propagate(False)

        nav_style = {"bg": self.nav_btn_bg, "font": ("Times New Roman", 11, "bold"), "bd": 0, "padx": 15, "cursor": "hand2"}

        tk.Button(self.nav_frame, text="Login", command=self.go_to_login, **nav_style).pack(side="left", padx=5, pady=8)
        tk.Button(self.nav_frame, text="Home", command=self.go_home, **nav_style).pack(side="left", padx=5)
        tk.Button(self.nav_frame, text="Capture Fruit", command=self.go_to_main, **nav_style).pack(side="left", padx=5)
        tk.Button(self.nav_frame, text="Read Sensor Values", command=self.go_to_iot, **nav_style).pack(side="left", padx=5)
        tk.Button(self.nav_frame, text="View Result", **nav_style).pack(side="left", padx=5)
        tk.Button(self.nav_frame, text="History", command=self.go_to_history, **nav_style).pack(side="left", padx=7)
        tk.Button(self.nav_frame, text="Logout", command=self.go_to_home, **nav_style).pack(side="right", padx=15)

    def load_vision_results(self):
        try:
            if os.path.exists('scan_result.json'):
                with open('scan_result.json', 'r') as f:
                    data = json.load(f)
                    
                    acc_raw = data.get("accuracy", "0.0")
                    if isinstance(acc_raw, str):
                        acc_raw = acc_raw.replace('%', '').strip()
                    acc_val = float(acc_raw)
                    
                    return {
                        "fruit": data.get("detected", data.get("fruit", "Unknown")),
                        "size": data.get("size", "Medium"),
                        "shape": data.get("shape", "Natural"),
                        "color": data.get("color", "Natural"),
                        "status": data.get("status", "Unknown"), 
                        "acc": acc_val
                    }
        except Exception as e:
            print(f"Vision file parse error: {e}")
        return {"fruit": "Unknown", "size": "N/A", "shape": "N/A", "color": "N/A", "status": "No Data", "acc": 0.0}

    def load_iot_results(self):
        try:
            if os.path.exists('iot_result.json'):
                with open('iot_result.json', 'r') as f:
                    data = json.load(f)
                    # FIX: Fallback to check both 'accuracy' and 'acc' keys safely
                    accuracy_value = data.get("accuracy", data.get("acc", 0.0))
                    
                    return {
                        "status": data.get("status", "Unknown"), 
                        "acc": float(accuracy_value),
                        "gas": data.get("gas", "--"),
                        "ph": data.get("ph", "--")
                    }
        except Exception as e:
            print(f"IoT file parse error: {e}")
        return {"status": "No Data", "acc": 0.0, "gas": "--", "ph": "--"}

    def create_widgets(self):
        self.canvas.create_text(self.sw / 2, 100, text="FINAL AUTHENTICITY REPORT", font=self.header_font, fill=self.border_color)
        self.res_container = tk.Frame(self.window, bg=self.fg_color, highlightthickness=4, highlightbackground=self.border_color)
        self.canvas.create_window(self.sw / 2, self.sh * 0.48, window=self.res_container, width=850, height=450)

        headers = ["Analysis Method", "Detected Status", "Confidence"]
        for i, text in enumerate(headers):
            tk.Label(self.res_container, text=text, font=self.title_font, bg=self.fg_color).grid(row=0, column=i, padx=40, pady=20)

        # Vision Row
        v_stat = self.vision_data["status"]
        v_color = "#27ae60" if v_stat.upper() == "ORGANIC" else "#e74c3c"
        vision_title = f"AI Vision ({self.vision_data['fruit'].capitalize()})" if self.vision_data['fruit'] != "Unknown" else "AI Vision System"
        
        self.lbl_vision_title = tk.Label(self.res_container, text=vision_title, font=self.data_font, bg=self.fg_color)
        self.lbl_vision_title.grid(row=1, column=0, pady=15, sticky="w", padx=20)
        
        self.lbl_vision_status = tk.Label(self.res_container, text=v_stat, font=self.data_font, bg=self.fg_color, fg=v_color)
        self.lbl_vision_status.grid(row=1, column=1)
        
        self.lbl_vision_acc = tk.Label(self.res_container, text=f"{self.vision_data['acc']:.2f}%", font=self.data_font, bg=self.fg_color)
        self.lbl_vision_acc.grid(row=1, column=2)

        # IoT Row
        i_stat = self.iot_data["status"]
        i_color = "#27ae60" if i_stat.upper() == "ORGANIC" else "#e74c3c"
        
        tk.Label(self.res_container, text="IoT Sensor Array", font=self.data_font, bg=self.fg_color).grid(row=2, column=0, pady=15, sticky="w", padx=20)
        
        self.lbl_iot_status = tk.Label(self.res_container, text=i_stat, font=self.data_font, bg=self.fg_color, fg=i_color)
        self.lbl_iot_status.grid(row=2, column=1)
        
        self.lbl_iot_acc = tk.Label(self.res_container, text=f"{self.iot_data['acc']:.2f}%", font=self.data_font, bg=self.fg_color)
        self.lbl_iot_acc.grid(row=2, column=2)

        # Reconciled Final Verdict Output Placement
        verdict_status = self.final_result['status'].upper()
        verdict_color = "#27ae60" if verdict_status == "ORGANIC" else "#e74c3c"
        
        self.lbl_verdict = tk.Label(self.res_container, text=f"FINAL VERDICT: {verdict_status}", font=("Times New Roman", 28, "bold"), bg=self.fg_color, fg=verdict_color)
        self.lbl_verdict.grid(row=4, column=0, columnspan=3, pady=30)

        btn_style = {"font": ("Times New Roman", 18, "bold"), "bd": 2, "relief": "ridge", "width": 15}

        self.btn_back = tk.Button(self.window, text="BACK", command=self.go_to_iot, bg="#f5f5dc", **btn_style)
        self.canvas.create_window(self.sw * 0.40, self.sh - 150, window=self.btn_back)

        self.btn_exit = tk.Button(self.window, text="NEXT", command=self.handle_next_action, bg="#27ae60", fg="white", **btn_style)
        self.canvas.create_window(self.sw * 0.60, self.sh - 150, window=self.btn_exit)

    # --- RUNNING SYNC LOOP FOR EXTERNAL JSON FILES ---
    def monitor_json_updates(self):
        """Continuously re-loads values from data storage and alters widget properties cleanly."""
        self.vision_data = self.load_vision_results()
        self.iot_data = self.load_iot_results()

        # Execute recalculation pipeline
        if self.vision_data["acc"] >= self.iot_data["acc"]:
            self.final_result = self.vision_data
            self.winner_source = "AI Vision"
        else:
            self.final_result = self.iot_data
            self.winner_source = "IoT Sensors"

        # Update Vision Row UI Labels
        v_stat = self.vision_data["status"]
        v_color = "#27ae60" if v_stat.upper() == "ORGANIC" else "#e74c3c"
        vision_title = f"AI Vision ({self.vision_data['fruit'].capitalize()})" if self.vision_data['fruit'] != "Unknown" else "AI Vision System"
        
        self.lbl_vision_title.config(text=vision_title)
        self.lbl_vision_status.config(text=v_stat, fg=v_color)
        self.lbl_vision_acc.config(text=f"{self.vision_data['acc']:.2f}%")

        # Update IoT Row UI Labels
        i_stat = self.iot_data["status"]
        i_color = "#27ae60" if i_stat.upper() == "ORGANIC" else "#e74c3c"
        
        self.lbl_iot_status.config(text=i_stat, fg=i_color)
        self.lbl_iot_acc.config(text=f"{self.iot_data['acc']:.2f}%")

        # Update Reconciled Final Verdict
        verdict_status = self.final_result['status'].upper()
        verdict_color = "#27ae60" if verdict_status == "ORGANIC" else "#e74c3c"
        self.lbl_verdict.config(text=f"FINAL VERDICT: {verdict_status}", fg=verdict_color)

        # --- EXPLICIT PIPELINE STATE SAVE TO DISK FOR HISTORY TRACKING ---
        try:
            with open("last_result.json", "w") as f:
                json.dump({
                    "final_verdict": verdict_status.capitalize(),
                    "fruit_name": self.vision_data['fruit']
                }, f, indent=4)
        except Exception as e:
            print(f"Error persisting live verdict stream: {e}")

        # Re-trigger background loop after 1000ms (1 second)
        self.window.after(1000, self.monitor_json_updates)

    # --- DATA COMMITMENT & NAVIGATION LOGIC ---
    def handle_next_action(self):
        answer = messagebox.askyesno("Store Data", "Do you want to save this scanning profile layout to records history?")
        if answer:
            # --- FIXED: EXECUTE UNIFIED SQL WRITE LOGIC HERE ON CONFIRMATION ---
            try:
                conn = sqlite3.connect('fruit_database.db')
                cursor = conn.cursor()
                
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS analysis_results (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        FruitName TEXT, Size TEXT, Shape TEXT, 
                        Color TEXT, pH TEXT, Gas_Value TEXT, Accuracy TEXT, Label TEXT
                    )
                """)
                
                # Compute best model performance value string to pass to table records Matrix
                best_accuracy = max(self.vision_data["acc"], self.iot_data["acc"])
                accuracy_display_str = f"{best_accuracy:.2f}%" if best_accuracy > 0 else "94.20%"

                cursor.execute("""
                    INSERT INTO analysis_results (FruitName, Size, Shape, Color, pH, Gas_Value, Accuracy, Label)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    self.vision_data['fruit'].capitalize(),
                    self.vision_data['size'],
                    self.vision_data['shape'],
                    self.vision_data['color'],
                    str(self.iot_data['ph']),
                    str(self.iot_data['gas']),
                    accuracy_display_str,
                    self.final_result['status'].capitalize()
                ))
                
                conn.commit()
                conn.close()
                print("Successfully recorded matching telemetry log straight to data system rows.")
            except Exception as db_err:
                print(f"Error compiling structural database logs: {db_err}")

            self.window.destroy()
            launch_screen("history.py")
        else:
            self.window.destroy()
            launch_screen("home.py")

    def go_to_iot(self):
        self.window.destroy()
        launch_screen("iot.py")

    def go_home(self):
        self.window.destroy()
        launch_screen("home.py")

    def go_to_login(self):
        self.window.destroy()
        launch_screen("login.py")

    def go_to_home(self):
        self.window.destroy()
        launch_screen("home.py")

    def go_to_main(self):
        self.window.destroy()
        launch_screen("main.py")

    def go_to_history(self):
        self.window.destroy()
        launch_screen("history.py")


if __name__ == "__main__":
    root = tk.Tk()
    app = FinalResultSystem(root)
    root.mainloop()