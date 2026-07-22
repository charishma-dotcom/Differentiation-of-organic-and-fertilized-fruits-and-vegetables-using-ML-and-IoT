import tkinter as tk
from PIL import Image, ImageTk
import subprocess
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def launch_screen(script_name):
    subprocess.Popen([sys.executable, os.path.join(BASE_DIR, script_name)], cwd=BASE_DIR)

class HomeSystem:
    def __init__(self, window):
        self.window = window
        self.window.title("Fruit Authenticity System")
        self.window.attributes('-fullscreen', True)
        self.sw = self.window.winfo_screenwidth()
        self.sh = self.window.winfo_screenheight()

        # 1. CANVAS FOR FULLSCREEN BACKGROUND
        self.canvas = tk.Canvas(self.window, width=self.sw, height=self.sh, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        try:
            # Using the established leaf background image
            bg_path = r"C:\Users\Charishma\final project\static\images\cha.png"
            bg_img = Image.open(bg_path).resize((self.sw, self.sh), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(bg_img)
            self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
        except:
            self.canvas.configure(bg="#dff2b2") # Fallback light green

        self.create_widgets()

    def create_widgets(self):
        
        # 3. NAVIGATION FUNCTIONS
        def start_app():
            self.window.destroy()
            launch_screen("register.py")

        def close_app():
            self.window.destroy()

        # 4. START AND CLOSE BUTTONS
        btn_style = {
            "font": ("Times New Roman", 20, "bold"),
            "width": 15,
            "bd": 3,
            "relief": "ridge"
        }

        # START Button (Success Green)
        self.btn_start = tk.Button(self.window, text="START", command=start_app, 
                                   bg="#008000", fg="white", activebackground="#2ecc71", **btn_style)
        
        # CLOSE Button (Alert Red)
        self.btn_close = tk.Button(self.window, text="CLOSE", command=close_app, 
                                   bg="#ff0000", fg="white", activebackground="#e74c3c", **btn_style)

        # Centering the buttons at the bottom
        self.canvas.create_window(self.sw * 0.45, self.sh * 0.75, window=self.btn_start)
        self.canvas.create_window(self.sw * 0.62, self.sh * 0.75, window=self.btn_close)

if __name__ == "__main__":
    root = tk.Tk()
    app = HomeSystem(root)
    root.mainloop()