
import os
os.environ['TF_ENABLE_ONEDNN_OPTS']='0'
import tensorflow as tf
tf.get_logger().setLevel('ERROR')
import tkinter as tk
import sqlite3
import cv2
from deepface import DeepFace
from datetime import datetime
from threading import Thread
import matplotlib.pyplot as plt

# Database setup
def create_database():
    conn = sqlite3.connect("emotions.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS emotions (
                    id INTEGER PRIMARY KEY,
                    timestamp TEXT,
                    emotion TEXT
                )''')
    conn.commit()
    conn.close()

def insert_emotion(emotion):
    conn = sqlite3.connect("emotions.db")
    c = conn.cursor()
    c.execute("INSERT INTO emotions (timestamp, emotion) VALUES (?, ?)",
              (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), emotion))
    conn.commit()
    conn.close()

def view_database():
    conn = sqlite3.connect("emotions.db")
    c = conn.cursor()
    c.execute("SELECT * FROM emotions")
    data = c.fetchall()
    conn.close()
    return data

def plot_emotions():
    conn = sqlite3.connect("emotions.db")
    c = conn.cursor()
    c.execute("SELECT emotion, COUNT(*) FROM emotions GROUP BY emotion")
    data = c.fetchall()
    conn.close()

    if data:
        labels, counts = zip(*data)
        plt.pie(counts, labels=labels, autopct='%1.1f%%')
        plt.title("Emotion Distribution")
        plt.show()

# Emotion Detection
def detect_emotion_for_10_seconds():
    cap = cv2.VideoCapture(0)
    start_time = datetime.now()
    while (datetime.now() - start_time).seconds < 10:
        ret, frame = cap.read()
        if ret:
            try:
                result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
                dominant_emotion = result[0]['dominant_emotion']
                insert_emotion(dominant_emotion)
                print("Detected:", dominant_emotion)
            except Exception as e:
                print("Error:", e)
    cap.release()
    cv2.destroyAllWindows()

# UI
class EmotionApp:
    def _init_(self, root):
        self.root = root
        self.root.title("Emotion Detector")

        tk.Button(root, text="Start Detection", command=self.start_detection).pack(pady=10)
        tk.Button(root, text="Show Database", command=self.show_database).pack(pady=10)
        tk.Button(root, text="Show Charts", command=plot_emotions).pack(pady=10)

        self.output = tk.Text(root, height=10, width=50)
        self.output.pack()

    def start_detection(self):
        self.output.insert(tk.END, "Starting emotion detection...\n")
        Thread(target=detect_emotion_for_10_seconds).start()

    def show_database(self):
        records = view_database()
        self.output.delete("1.0", tk.END)
        for row in records:
            self.output.insert(tk.END, str(row) + "\n")

# Run
if __name__ == "_main_":
    create_database()
    root = tk.Tk()
    app = EmotionApp(root)
    root.mainloop()