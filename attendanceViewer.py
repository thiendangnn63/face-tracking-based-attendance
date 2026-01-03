import tkinter as tk
from tkinter import ttk, messagebox
from attendanceAnalytics import AttendanceAnalytics

class AttendanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Attendance Dashboard")
        self.root.geometry("600x500")
        
        self.analytics = AttendanceAnalytics()
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)
        
        self.tab_student = ttk.Frame(self.notebook)
        self.tab_date = ttk.Frame(self.notebook)
        self.tab_stats = ttk.Frame(self.notebook)
        self.tab_thresh = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tab_student, text='Student History')
        self.notebook.add(self.tab_date, text='Daily Register')
        self.notebook.add(self.tab_stats, text='Statistics')
        self.notebook.add(self.tab_thresh, text='Threshold Report')
        
        self.setup_student_tab()
        self.setup_date_tab()
        self.setup_stats_tab()
        self.setup_threshold_tab()
        
        btn_frame = ttk.Frame(root)
        btn_frame.pack(fill='x', padx=10, pady=5)
        ttk.Button(btn_frame, text="Refresh Data", command=self.refresh_data).pack(side='right')

    def setup_student_tab(self):
        frame = ttk.Frame(self.tab_student)
        frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        ttk.Label(frame, text="Enter Student Name:").pack(anchor='w')
        self.ent_student = ttk.Entry(frame)
        self.ent_student.pack(fill='x', pady=5)
        ttk.Button(frame, text="Search Dates", command=self.search_student_history).pack(anchor='e', pady=5)
        
        ttk.Label(frame, text="Present On:").pack(anchor='w', pady=(10, 0))
        self.list_student_dates = tk.Listbox(frame, height=10)
        self.list_student_dates.pack(fill='both', expand=True, pady=5)

    def setup_date_tab(self):
        frame = ttk.Frame(self.tab_date)
        frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        ttk.Label(frame, text="Enter Date (YYYY-MM-DD):").pack(anchor='w')
        self.ent_date = ttk.Entry(frame)
        self.ent_date.pack(fill='x', pady=5)
        ttk.Button(frame, text="Show Present Students", command=self.search_date_register).pack(anchor='e', pady=5)
        
        ttk.Label(frame, text="Students Present:").pack(anchor='w', pady=(10, 0))
        self.list_date_students = tk.Listbox(frame, height=10)
        self.list_date_students.pack(fill='both', expand=True, pady=5)

    def setup_stats_tab(self):
        frame = ttk.Frame(self.tab_stats)
        frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        ttk.Label(frame, text="Enter Student Name:").pack(anchor='w')
        self.ent_stat_name = ttk.Entry(frame)
        self.ent_stat_name.pack(fill='x', pady=5)
        ttk.Button(frame, text="Calculate Stats", command=self.show_stats).pack(anchor='e', pady=5)
        
        self.lbl_stats_result = ttk.Label(frame, text="Results will appear here.", font=('Arial', 12))
        self.lbl_stats_result.pack(pady=40)

    def setup_threshold_tab(self):
        frame = ttk.Frame(self.tab_thresh)
        frame.pack(fill='both', expand=True, padx=20, pady=20)

        ttk.Label(frame, text="Minimum Attendance % (e.g. 75):").pack(anchor='w')
        self.ent_thresh = ttk.Entry(frame)
        self.ent_thresh.pack(fill='x', pady=5)
        self.ent_thresh.insert(0, "75")
        
        ttk.Button(frame, text="Filter Students", command=self.filter_threshold).pack(anchor='e', pady=5)
        
        ttk.Label(frame, text="Students Above Threshold:").pack(anchor='w', pady=(10, 0))
        self.list_thresh = tk.Listbox(frame, height=10)
        self.list_thresh.pack(fill='both', expand=True, pady=5)

    def search_student_history(self):
        name = self.ent_student.get().strip()
        if not name: return
        dates = self.analytics.get_dates_present(name)
        self.list_student_dates.delete(0, tk.END)
        if dates:
            for date in dates:
                self.list_student_dates.insert(tk.END, date)
        else:
            messagebox.showinfo("Result", f"No records found for {name}")

    def search_date_register(self):
        day = self.ent_date.get().strip()
        if not day: return
        students = self.analytics.get_students_present_on_date(day)
        self.list_date_students.delete(0, tk.END)
        if students:
            for student in students:
                self.list_date_students.insert(tk.END, student)
        else:
            messagebox.showinfo("Result", f"No records found for {day}")

    def show_stats(self):
        name = self.ent_stat_name.get().strip()
        if not name: return
        attended, total, pct = self.analytics.calculate_stats(name)
        if total == 0:
            self.lbl_stats_result.config(text=f"No data found for {name}")
        else:
            text = f"Student: {name}\n\nAttended: {attended}\nTotal Sessions: {total}\nAttendance: {pct:.2f}%"
            self.lbl_stats_result.config(text=text)

    def filter_threshold(self):
        try:
            val = float(self.ent_thresh.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Please enter a number (e.g. 75)")
            return

        students = self.analytics.get_students_above_threshold(val)
        self.list_thresh.delete(0, tk.END)
        
        if students:
            for s in students:
                self.list_thresh.insert(tk.END, s)
        else:
            messagebox.showinfo("Result", "No students meet this criteria.")

    def refresh_data(self):
        self.analytics.reload_data()
        messagebox.showinfo("Success", "Data reloaded from CSV.")

if __name__ == "__main__":
    root = tk.Tk()
    app = AttendanceApp(root)
    root.mainloop()