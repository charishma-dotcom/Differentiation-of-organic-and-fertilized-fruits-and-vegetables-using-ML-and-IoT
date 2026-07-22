import tkinter as tk
from PIL import Image, ImageTk
import serial
import subprocess
import sys
import time
import json 
import os 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def launch_screen(script_name):
    subprocess.Popen([sys.executable, os.path.join(BASE_DIR, script_name)], cwd=BASE_DIR)

# --- SERIAL SETUP ---
try:
    # Adjust 'COM3' to your actual ESP32 port
    ser = serial.Serial('COM3', 115200, timeout=1)
    time.sleep(2) 
except Exception as e:
    print(f"Serial Connection Error: {e}")
    ser = None

class RealTimeResultWindow:
    def __init__(self, parent_window):
        self.top = tk.Toplevel(parent_window)
        self.top.title("Live Metrics Display")
        self.top.geometry("400x300")
        self.top.configure(bg="#1e293b")
        
        tk.Label(self.top, text="LIVE SENSOR RESULTS", font=("Times New Roman", 18, "bold"), bg="#1e293b", fg="#facc15").pack(pady=20)
        self.accuracy_label = tk.Label(self.top, text="Sensor Accuracy: 0.0%", font=("Times New Roman", 16), bg="#1e293b", fg="#38bdf8")
        self.accuracy_label.pack(pady=15)
        self.status_label = tk.Label(self.top, text="Status: WAITING", font=("Times New Roman", 18, "bold"), bg="#1e293b", fg="#94a3b8")
        self.status_label.pack(pady=15)
        
    def update_metrics(self, accuracy, status, status_color):
        if self.top.winfo_exists():
            self.accuracy_label.config(text=f"Sensor Accuracy: {accuracy:.1f}%")
            self.status_label.config(text=f"Status: {status}", fg=status_color)

class IOTAuthenticitySystem:
    def __init__(self, window):
        self.window = window
        self.window.title("Fruit Authenticity - IoT Sensor Mode")
        self.window.attributes('-fullscreen', True)
        self.sw = self.window.winfo_screenwidth()
        self.sh = self.window.winfo_screenheight()

        self.fg_color = "#fef9c3"      
        self.bg_color_style = "#dff2b2" 
        self.border_color = "#facc15"   
        self.nav_bg_color = "#558833"  
        self.btn_bg_color = "#90C850"  
        
        self.nav_font = ("Times New Roman", 11, "bold")
        self.header_font = ("Times New Roman", 32, "bold")
        self.title_font = ("Times New Roman", 18, "bold")
        self.data_font = ("Times New Roman", 15)

        self.canvas = tk.Canvas(self.window, width=self.sw, height=self.sh, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        try:
            bg_path = r"C:\Users\Charishma\final project\static\images\resultimage.jpeg"
            bg_img = Image.open(bg_path).resize((self.sw, self.sh), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(bg_img)
            self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
        except Exception:
            self.canvas.configure(bg=self.bg_color_style)

        self.create_system_bar()   
        self.create_nav_bar()      
        self.create_widgets()      
        
        self.result_popup = RealTimeResultWindow(self.window)
        self.check_sensors()

    def create_system_bar(self):
        self.system_bar = tk.Frame(self.window, bg="#f0f0f0", height=30)
        self.canvas.create_window(self.sw/2, 15, window=self.system_bar, width=self.sw)
        tk.Label(self.system_bar, text="   Fruit Classifier - IoT Sensor Mode", font=("Segoe UI", 10), bg="#f0f0f0", fg="black").pack(side="left")
        controls_frame = tk.Frame(self.system_bar, bg="#f0f0f0")
        controls_frame.pack(side="right", fill="y")
        ctrl_style = {"font": ("Segoe UI", 10), "relief": "flat", "width": 4, "bd": 0, "bg": "#f0f0f0"}
        tk.Button(controls_frame, text="—", command=lambda: self.window.iconify(), **ctrl_style).pack(side="left")
        tk.Button(controls_frame, text="❐", command=self.toggle_screen, **ctrl_style).pack(side="left")
        tk.Button(controls_frame, text="✕", command=self.exit_app, activebackground="#e81123", activeforeground="white", **ctrl_style).pack(side="left")

    def create_nav_bar(self):
        self.nav_frame = tk.Frame(self.window, bg=self.nav_bg_color, height=60)
        self.canvas.create_window(self.sw/2, 60, window=self.nav_frame, width=self.sw)

        def nav_btn(text, command):
            return tk.Button(self.nav_frame, text=text, command=command, font=self.nav_font, bg=self.btn_bg_color, fg="black", activebackground="#7bad42", relief="flat", padx=15, pady=5, bd=0)

        nav_btn("Home", self.open_home).pack(side="left", padx=15, pady=10)
        nav_btn("Capture Fruit", self.open_capture).pack(side="left", padx=15)
        nav_btn("Read Sensor Values", self.open_sensor).pack(side="left", padx=15)
        nav_btn("View Result", self.open_result).pack(side="left", padx=15)
        nav_btn("History", self.open_history).pack(side="left", padx=15)
        nav_btn("Logout", self.logout).pack(side="right", padx=15)

    def create_widgets(self):
        self.header_frame = tk.Frame(self.window, bg="#1b813e", bd=2, relief="flat")
        self.canvas.create_window(self.sw/2, 170, window=self.header_frame)
        tk.Label(self.header_frame, text="SENSOR ANALYSIS REPORT", font=self.header_font, bg="#1b813e", fg="white", pady=10).pack(padx=60)

        self.res_container = tk.Frame(self.window, bg=self.fg_color, highlightthickness=3, highlightbackground=self.border_color)
        self.canvas.create_window(self.sw / 2, self.sh / 2 + 80, window=self.res_container, anchor="center", width=550, height=450)

        self.gas_lbl = tk.Label(self.res_container, text="Gas Level: Scanning...", font=self.data_font, bg=self.fg_color)
        self.ph_lbl = tk.Label(self.res_container, text="pH Value: Scanning...", font=self.data_font, bg=self.fg_color)
        self.acc_lbl = tk.Label(self.res_container, text="Sensor Accuracy: --", font=self.data_font, bg=self.fg_color, fg="blue")
        self.status_lbl = tk.Label(self.res_container, text="Status: WAITING", font=self.title_font, bg=self.fg_color)
        self.reason_lbl = tk.Label(self.res_container, text="Reason: Please wait for sensor stabilization.", font=("Times New Roman", 13, "italic"), bg=self.fg_color, wraplength=480, justify="center")

        self.gas_lbl.pack(pady=10)
        self.ph_lbl.pack(pady=10)
        self.acc_lbl.pack(pady=10)
        self.status_lbl.pack(pady=15)
        self.reason_lbl.pack(side="bottom", pady=20)

        btn_style = {"font": self.title_font, "bd": 3, "relief": "ridge", "width": 15}
        self.btn_back = tk.Button(self.window, text="BACK TO VISION", command=self.open_capture, bg="#f5f5dc", **btn_style)
        self.canvas.create_window(self.sw * 0.40, self.sh - 80, window=self.btn_back)

        self.btn_next = tk.Button(self.window, text="NEXT", command=self.go_to_result, bg="#008000", fg="white", **btn_style)
        self.canvas.create_window(self.sw * 0.60, self.sh - 80, window=self.btn_next)

    def toggle_screen(self): self.window.attributes('-fullscreen', not self.window.attributes('-fullscreen'))
    def exit_app(self):
        if ser: ser.close()
        self.window.destroy()
    def safe_exit(self, script_name):
        if ser: ser.close()
        self.window.destroy()
        launch_screen(script_name)

    def open_home(self): self.safe_exit("home.py")
    def open_capture(self): self.safe_exit("main.py")
    def open_sensor(self): print("Refreshed Sensor View")
    def open_result(self): self.safe_exit("result.py")
    def open_history(self): self.safe_exit("history.py")
    def logout(self): self.safe_exit("login.py")
    def go_to_result(self): self.open_result()

    def check_sensors(self):
        """Reads Serial data and writes straight to telemetry json cache"""
        if ser and ser.in_waiting > 0:
            try:
                line = ser.readline().decode('utf-8').strip()
                data = line.split(',')
                if len(data) == 3:
                    gas, ph, status = data
                    gas_val, ph_val = float(gas), float(ph)
                    
                    calc_acc = min(99.9, 85 + (gas_val / 50)) if status.upper() == "FERTILIZED" else min(99.9, 90 + (10 / (gas_val + 1)))
                    status_color = "#e74c3c" if status.upper() == "FERTILIZED" else "#27ae60"

                    self.gas_lbl.config(text=f"Gas Level: {gas_val} PPM")
                    self.ph_lbl.config(text=f"pH Value: {ph_val}")
                    self.status_lbl.config(text=f"Status: {status}", fg=status_color)
                    self.acc_lbl.config(text=f"Detection Accuracy: {calc_acc:.1f}%")

                    # Export parameters cleanly to the pipeline exchange layer
                    iot_data = {
                        "status": status.capitalize(), 
                        "accuracy": round(float(calc_acc), 2), # Keep this as 'accuracy'
                        "gas": f"{gas_val} PPM", 
                        "ph": str(ph_val)
                    }
                    with open('iot_result.json', 'w') as f:
                        json.dump(iot_data, f, indent=4)

                    self.result_popup.update_metrics(calc_acc, status.upper(), status_color)
            except Exception as e:
                print(f"Serial Error: {e}")

        self.window.after(100, self.check_sensors)

if __name__ == "__main__":
    root = tk.Tk()
    app = IOTAuthenticitySystem(root)
    root.mainloop()