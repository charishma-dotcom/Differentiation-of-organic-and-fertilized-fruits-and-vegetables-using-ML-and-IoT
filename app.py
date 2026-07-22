import cv2
import sys
import json
import subprocess
from pathlib import Path
from PIL import Image
import customtkinter as ctk  # For the RegisterApp integration

# =========================================================
# CONFIGURATIONS & ASSET LOADING
# =========================================================
# Define the path cleanly to avoid f-string backslash errors
image_path = r'C:\Users\Charishma\final project\static\images\the.png'
img = cv2.imread(image_path)

if img is None:
    print(f"Error: Could not load image from path '{image_path}'. Check the filename.")
    sys.exit()

BASE_DIR = Path(__file__).resolve().parent
USER_DATA_FILE = BASE_DIR / "user_data.json"

if not USER_DATA_FILE.exists():
    with open(USER_DATA_FILE, "w") as file:
        json.dump([], file)

def launch_script(script_name):
    subprocess.Popen([sys.executable, str(BASE_DIR / script_name)], cwd=BASE_DIR)

# Global variables to store the current window scale factor
scale_x = 1.0
scale_y = 1.0

# Base Button Coordinates & Dimensions (based on original image scale)
start_btn_base = [50, 450, 140, 50]   
stop_btn_base = [220, 450, 140, 50]   

# =========================================================
# APPLICATION CLASS (Your Register Window)
# =========================================================
class RegisterApp:
    def __init__(self):
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("green")
        
        self.app = ctk.CTk()
        self.app.title("Fruit Classifier - Register")

        self.screen_width = self.app.winfo_screenwidth()
        self.screen_height = self.app.winfo_screenheight()
        self.app.geometry(f"{self.screen_width}x{self.screen_height}+0+0")
        self.setup_ui()

    def open_login(self):
        self.app.destroy()
        launch_script("login.py")

    def register_user(self):
        name = self.fullname.get()
        mail = self.email.get()
        pwd = self.password.get()
        confirm_pwd = self.confirm_password.get()

        if name == "" or mail == "" or pwd == "" or confirm_pwd == "":
            print("Please fill all fields")
            return

        if pwd != confirm_pwd:
            print("Passwords do not match")
            return

        user = {
            "fullname": name,
            "email": mail,
            "password": pwd
        }

        try:
            with open(USER_DATA_FILE, "r") as file:
                data = json.load(file)
                if not isinstance(data, list):
                    data = []
        except:
            data = []

        data.append(user)

        with open(USER_DATA_FILE, "w") as file:
            json.dump(data, file, indent=4)

        print("Registration Successful")
        self.app.destroy()
        launch_script("login.py")

    def toggle_password(self, entry):
        if entry.cget("show") == "*":
            entry.configure(show="")
        else:
            entry.configure(show="*")

    def setup_ui(self):
        bg_image = ctk.CTkImage(
            Image.open(BASE_DIR / "static/images/registerimage.jpeg"),
            size=(self.screen_width, self.screen_height)
        )

        main_frame = ctk.CTkFrame(self.app, fg_color="white")
        main_frame.pack(fill="both", expand=True)

        bg_label = ctk.CTkLabel(main_frame, image=bg_image, text="")
        bg_label.place(relwidth=1, relheight=1)

        navbar = ctk.CTkFrame(main_frame, height=80, fg_color="#14532d", corner_radius=0)
        navbar.pack(fill="x")

        title = ctk.CTkLabel(navbar, text="Fruit Classifier", text_color="white", font=("Arial", 38, "bold"))
        title.pack(pady=18)

        register_card = ctk.CTkFrame(main_frame, width=520, height=620, fg_color="#f8f8f8", corner_radius=20, border_width=2, border_color="#d1d5db")
        register_card.place(relx=0.78, rely=0.50, anchor="center")
        register_card.pack_propagate(False)

        heading = ctk.CTkLabel(register_card, text="Create Account", text_color="#166534", font=("Arial", 36, "bold"))
        heading.pack(pady=(30, 10))

        line = ctk.CTkFrame(register_card, width=180, height=4, fg_color="#22c55e")
        line.pack()

        ENTRY_WIDTH = 390
        ENTRY_HEIGHT = 55

        self.fullname = ctk.CTkEntry(register_card, width=ENTRY_WIDTH, height=ENTRY_HEIGHT, placeholder_text="Full Name", corner_radius=14, border_width=2, border_color="#22c55e", font=("Arial", 16))
        self.fullname.pack(pady=(30, 12))

        self.email = ctk.CTkEntry(register_card, width=ENTRY_WIDTH, height=ENTRY_HEIGHT, placeholder_text="Email", corner_radius=14, border_width=2, border_color="#22c55e", font=("Arial", 16))
        self.email.pack(pady=12)

        password_frame = ctk.CTkFrame(register_card, fg_color="transparent")
        password_frame.pack(pady=12)

        self.password = ctk.CTkEntry(password_frame, width=320, height=ENTRY_HEIGHT, placeholder_text="Password", show="*", corner_radius=14, border_width=2, border_color="#22c55e", font=("Arial", 16))
        self.password.pack(side="left")

        eye_btn = ctk.CTkButton(password_frame, text="👁", width=55, height=ENTRY_HEIGHT, fg_color="#22c55e", hover_color="#15803d", corner_radius=14, command=lambda: self.toggle_password(self.password))
        eye_btn.pack(side="left", padx=(8, 0))

        confirm_frame = ctk.CTkFrame(register_card, fg_color="transparent")
        confirm_frame.pack(pady=12)

        self.confirm_password = ctk.CTkEntry(confirm_frame, width=320, height=ENTRY_HEIGHT, placeholder_text="Confirm Password", show="*", corner_radius=14, border_width=2, border_color="#22c55e", font=("Arial", 16))
        self.confirm_password.pack(side="left")

        confirm_eye = ctk.CTkButton(confirm_frame, text="👁", width=55, height=ENTRY_HEIGHT, fg_color="#22c55e", hover_color="#15803d", corner_radius=14, command=lambda: self.toggle_password(self.confirm_password))
        confirm_eye.pack(side="left", padx=(8, 0))

        register_btn = ctk.CTkButton(register_card, text="Register", width=390, height=55, fg_color="#15803d", hover_color="#166534", text_color="white", font=("Arial", 20, "bold"), corner_radius=14, command=self.register_user)
        register_btn.pack(pady=(25, 15))

        bottom_frame = ctk.CTkFrame(register_card, fg_color="transparent")
        bottom_frame.pack(pady=(10, 0))

        bottom_text = ctk.CTkLabel(bottom_frame, text="Already have an account?", text_color="#374151", font=("Arial", 16))
        bottom_text.pack(side="left")

        signin = ctk.CTkButton(bottom_frame, text=" Sign In", fg_color="transparent", hover=False, text_color="#15803d", font=("Arial", 16, "bold"), width=20, command=self.open_login)
        signin.pack(side="left")

    def run(self):
        self.app.mainloop()

# =========================================================
# OPENCV DASHBOARD AND INTERACTION
# =========================================================
def draw_buttons(base_img):
    btn_img = base_img.copy()  
    cv2.rectangle(btn_img, (start_btn_base[0], start_btn_base[1]), (start_btn_base[0] + start_btn_base[2], start_btn_base[1] + start_btn_base[3]), (0, 180, 0), -1)
    cv2.putText(btn_img, "START", (start_btn_base[0] + 30, start_btn_base[1] + 33), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.rectangle(btn_img, (stop_btn_base[0], stop_btn_base[1]), (stop_btn_base[0] + stop_btn_base[2], stop_btn_base[1] + stop_btn_base[3]), (0, 0, 200), -1)
    cv2.putText(btn_img, "STOP", (stop_btn_base[0] + 38, stop_btn_base[1] + 33), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)
    return btn_img

def mouse_callback(event, x, y, flags, param):
    global scale_x, scale_y
    if event == cv2.EVENT_LBUTTONDOWN:
        orig_x = int(x / scale_x)
        orig_y = int(y / scale_y)
        
        # Check against original Start Button bounds
        if (start_btn_base[0] <= orig_x <= start_btn_base[0] + start_btn_base[2]) and \
           (start_btn_base[1] <= orig_y <= start_btn_base[1] + start_btn_base[3]):
            print("[ACTION] START Button Clicked! Loading Registration Interface...")
            
            # --- INTEGRATION FIXED HERE ---
            cv2.destroyAllWindows()  # Close the OpenCV presentation window cleanly
            
            # Fire up your CustomTkinter window interface
            registration_window = RegisterApp()
            registration_window.run()
            
            # Completely exit the script execution path once CustomTkinter closes down
            sys.exit(0)
            
        # Check against original Stop Button bounds
        elif (stop_btn_base[0] <= orig_x <= stop_btn_base[0] + stop_btn_base[2]) and \
             (stop_btn_base[1] <= orig_y <= stop_btn_base[1] + stop_btn_base[3]):
            print("\n[ACTION] STOP Button Clicked! Terminating program execution immediately...")
            cv2.destroyAllWindows()
            sys.exit(0)

# Create the interactive dashboard window
window_name = "fruit"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.setMouseCallback(window_name, mouse_callback)

print("Dashboard running. Click 'START' inside the image frame to go to the Registration page.")

while True:
    try:
        visible = cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE)
        if visible < 1:
            print("\n[INFO] Window closed via OS close button. Terminating...")
            break
            
        win_rect = cv2.getWindowImageRect(window_name)
        win_w, win_h = win_rect[2], win_rect[3]
        
        full_res_layout = draw_buttons(img)
        
        if win_w > 0 and win_h > 0:
            scale_x = win_w / img.shape[1]
            scale_y = win_h / img.shape[0]
            display_frame = cv2.resize(full_res_layout, (win_w, win_h), interpolation=cv2.INTER_LINEAR)
        else:
            display_frame = full_res_layout

        cv2.imshow(window_name, display_frame)
        
    except cv2.error:
        break
        
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q') or key == 27:
        print("\n[INFO] Exit requested via keyboard. Terminating program safely...")
        break

cv2.destroyAllWindows()
sys.exit(0)