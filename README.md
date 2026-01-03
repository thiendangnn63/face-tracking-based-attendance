```markdown
# Face Tracking Attendance System

An open-source application for automating attendance tracking using real-time face recognition. This system uses computer vision to identify students from a live camera feed, logs their attendance to a CSV file, and provides a graphical dashboard for teachers to view statistics and reports.

## Features

* **Real-Time Recognition:** Detects and identifies registered faces instantly using MediaPipe and dlib.
* **Dynamic Registration:** Add new students/faces directly from the camera interface without stopping the program.
* **Attendance Dashboard:** A GUI interface to view student attendance history, daily registers, and participation statistics.
* **Threshold Reporting:** Filter students based on attendance percentage to identify those falling below a certain requirement.
* **Data Export:** All attendance data is automatically saved to standard CSV files for easy integration with other tools.

## Installation

1. Clone this repository.
2. Install the required dependencies. Note that this project requires a specific version of OpenCV and NumPy to ensure compatibility with dlib.

```bash
pip install numpy<2
pip install opencv-python<=4.11.0.86
pip install dlib-bin face_recognition --no-deps
pip install pillow mediapipe pandas

```

## Usage

Run the main launcher script to start the application:

```bash
python main_dashboard.py

```

### 1. Camera Mode

* Select **Start Camera Mode** from the main menu.
* The camera will scan for faces. Recognized students are marked present automatically once per session.
* **Controls:**
* Press `a` to register an unknown face (enter the student's name when prompted).
* Press `q` to save the attendance log and quit camera mode.



### 2. Dashboard Mode

* Select **View Attendance Dashboard** from the main menu.
* Use the tabs to navigate between:
* **Student History:** View all dates a specific student was present.
* **Daily Register:** View all students present on a specific date.
* **Statistics:** View total sessions attended and percentage for a student.
* **Threshold Report:** Generate a list of students whose attendance is above or below a specific percentage.



## File Structure

* `main_dashboard.py`: The entry point for the application. Launches the camera or the viewer.
* `faceMedia.py`: Handles video capture, face detection, and recognition logic.
* `attendanceViewer.py`: Contains the GUI code for the analytics dashboard (Tkinter).
* `attendanceAnalytics.py`: Handles data processing and CSV reading/writing.
* `known_faces.json`: Stores the facial encodings for registered users.
* `attendance.csv`: Stores the daily attendance records.

Google Drive link for executable files:
https://drive.google.com/drive/folders/1VQ9xTLoXgP_HQeNZPuQxiqStWjgt-ivu?usp=drive_link
