import pandas as pd

class AttendanceAnalytics:
    def __init__(self, filepath='attendance.csv'):
        self.filepath = filepath
        self.reload_data()

    def reload_data(self):
        try:
            self.df = pd.read_csv(self.filepath, index_col=0)
            self.df.fillna(0, inplace=True)
        except (FileNotFoundError, pd.errors.EmptyDataError):
            self.df = pd.DataFrame()

    def get_dates_present(self, name):
        if self.df.empty or name not in self.df.index:
            return []
        student_row = self.df.loc[name]
        return student_row[student_row == 1].index.tolist()

    def get_students_present_on_date(self, day):
        if self.df.empty or day not in self.df.columns:
            return []
        day_col = self.df[day]
        return day_col[day_col == 1].index.tolist()

    def calculate_stats(self, name):
        if self.df.empty or name not in self.df.index:
            return 0, 0, 0.0
        total = len(self.df.columns)
        attended = int(self.df.loc[name].sum())
        pct = (attended / total * 100) if total > 0 else 0.0
        return attended, total, pct

    def get_students_above_threshold(self, threshold_percent):
        if self.df.empty:
            return []
        
        qualified_students = []
        total_sessions = len(self.df.columns)
        
        if total_sessions == 0:
            return []

        for name, row in self.df.iterrows():
            attended = row.sum()
            pct = (attended / total_sessions) * 100
            if pct >= threshold_percent:
                qualified_students.append(f"{name} ({pct:.1f}%)")
        
        return qualified_students