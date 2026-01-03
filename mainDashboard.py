import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
from attendanceViewer import AttendanceApp

class MasterDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Attendance System Launcher")
        self.root.geometry("400x300")
        
        self.center_window(400, 300)

        lbl_title = tk.Label(root, text="Classroom Attendance\nMaster Control", font=("Helvetica", 16, "bold"))
        lbl_title.pack(pady=30)

        btn_frame = ttk.Frame(root)
        btn_frame.pack(expand=True, fill='both', padx=50)

        self.btn_camera = ttk.Button(btn_frame, text="📷 Start Camera Mode", command=self.launch_camera)
        self.btn_camera.pack(fill='x', ipady=10, pady=10)

        self.btn_viewer = ttk.Button(btn_frame, text="📊 View Attendance Dashboard", command=self.launch_viewer)
        self.btn_viewer.pack(fill='x', ipady=10, pady=10)

        lbl_footer = tk.Label(root, text="Press 'q' in Camera Mode to save & quit", font=("Arial", 8), fg="gray")
        lbl_footer.pack(side='bottom', pady=10)

    def launch_camera(self):
        try:
            if getattr(sys, 'frozen', False):
                subprocess.Popen(["faceMedia.exe"])
            else:
                subprocess.Popen([sys.executable, "faceMedia.py"])
        except Exception as e:
            tk.messagebox.showerror("Error", f"Could not launch camera:\n{e}")

    def launch_viewer(self):
        viewer_window = tk.Toplevel(self.root)
        app = AttendanceApp(viewer_window)

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

if __name__ == "__main__":
    root = tk.Tk()
    app = MasterDashboard(root)
    root.mainloop()