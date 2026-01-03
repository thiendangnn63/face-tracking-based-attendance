import cv2
import mediapipe as mp
import time
import numpy as np
import face_recognition
import tkinter as tk
from tkinter import simpledialog
import json
import os
import pandas as pd
import math

class FaceDetector:
    def __init__(self, min_detection_confidence=0.7):
        self.mp_face_detection = mp.solutions.face_detection
        self.face_detection = self.mp_face_detection.FaceDetection(min_detection_confidence=min_detection_confidence)
        
        self.known_people = {}
        self.present_people = set()
        self.unknown = None
        
        self.frame_count = 0
        self.process_interval = 30
        self.face_tracker = []

        self.root = tk.Tk()
        self.root.withdraw()
        self.display_message = ""
        self.message_timer = 0

    def find_faces(self, img, draw=True):
        self.frame_count += 1
        
        height, width, _ = img.shape
        small_frame = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
        imgRGB = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        
        results = self.face_detection.process(imgRGB)
        self.unknown = None
        
        current_frame_faces = []

        if results.detections:
            for detection in results.detections:
                bbox = detection.location_data.relative_bounding_box
                x = int(bbox.xmin * width)
                y = int(bbox.ymin * height)
                w = int(bbox.width * width)
                h = int(bbox.height * height)

                x, y = max(0, x), max(0, y)
                w, h = min(w, width - x), min(h, height - y)
                
                center_x, center_y = x + w//2, y + h//2

                name = "Verifying..."
                color = (0, 255, 255)

                if self.frame_count % self.process_interval == 0:
                    face_crop = np.ascontiguousarray(img[y:y+h, x:x+w])
                    
                    if face_crop.shape[0] > 200:
                        scale = 200 / face_crop.shape[0]
                        face_crop = cv2.resize(face_crop, (0, 0), fx=scale, fy=scale)
                    
                    face_crop_rgb = cv2.cvtColor(face_crop, cv2.COLOR_BGR2RGB)

                    try:
                        encodings = face_recognition.face_encodings(face_crop_rgb, known_face_locations=[(0, face_crop.shape[1], face_crop.shape[0], 0)])
                        if encodings:
                            encoding = encodings[0]
                            match_found = False
                            for p_name, p_encodings in self.known_people.items():
                                matches = face_recognition.compare_faces(p_encodings, encoding, tolerance=0.6)
                                if True in matches:
                                    name = p_name
                                    color = (0, 255, 0)
                                    if name not in self.present_people:
                                        self.present_people.add(name)
                                        self.set_message(f"Marked: {name}")
                                    match_found = True
                                    break
                            
                            if not match_found:
                                name = "Unknown"
                                color = (0, 0, 255)
                                self.unknown = encoding
                        else:
                            name = "No Eyes"
                    except Exception:
                        pass
                else:
                    closest_dist = float('inf')
                    best_match = None
                    
                    for tracked_face in self.face_tracker:
                        old_x, old_y = tracked_face['center']
                        dist = math.hypot(center_x - old_x, center_y - old_y)
                        if dist < closest_dist:
                            closest_dist = dist
                            best_match = tracked_face
                    
                    if best_match and closest_dist < 100:
                        name = best_match['name']
                        color = best_match['color']
                    else:
                        name = "Scanning..."
                        color = (192, 192, 192)

                current_frame_faces.append({'center': (center_x, center_y), 'name': name, 'color': color})

                if draw:
                    cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                    cv2.rectangle(img, (x, y - 30), (x + w, y), color, cv2.FILLED)
                    cv2.putText(img, name, (x + 6, y - 6), cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)

        self.face_tracker = current_frame_faces

        if time.time() < self.message_timer:
            cv2.putText(img, self.display_message, (10, img.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
        return img

    def set_message(self, text, duration=1):
        self.display_message = text
        self.message_timer = time.time() + duration

    def add_unknown_face(self, root_window):
        if self.unknown is not None:
            new_name = simpledialog.askstring("Add Face", "Enter name:", parent=root_window)
            if new_name:
                if new_name not in self.known_people:
                    self.known_people[new_name] = []
                self.known_people[new_name].append(self.unknown)
                self.present_people.add(new_name)
                self.set_message(f"Added: {new_name}")
                self.frame_count = self.process_interval 
                return True
        return False

    def load_data(self):
        if os.path.exists("known_faces.json"):
            with open("known_faces.json", 'r') as f:
                data = json.load(f)
                self.known_people = {k: [np.array(e) for e in v] for k, v in data.items()}

    def save_data(self, day):
        serializable = {k: [e.tolist() for e in v] for k, v in self.known_people.items()}
        with open("known_faces.json", 'w') as f:
            json.dump(serializable, f)

        try:
            df = pd.read_csv("attendance.csv", index_col=0)
        except (FileNotFoundError, pd.errors.EmptyDataError):
            df = pd.DataFrame()

        if day not in df.columns: df[day] = 0
        all_names = list(self.known_people.keys())
        df = df.reindex(all_names, fill_value=0)
        for p in self.present_people:
            df.at[p, day] = 1
        df.fillna(0, inplace=True)
        df.astype(int).to_csv("attendance.csv")

def main():
    detector = FaceDetector()
    detector.load_data()
    day = time.strftime("%Y-%m-%d")
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret: break
        frame = detector.find_faces(frame)
        cv2.imshow("Attendance Cam", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            detector.save_data(day)
            break
        elif key == ord('a'):
            detector.add_unknown_face(detector.root)
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()