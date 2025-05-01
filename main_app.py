
import tkinter as tk
from tkinter import messagebox
from threading import Thread
from datetime import datetime
import sqlite3
import cv2
from deepface import DeepFace
import matplotlib.pyplot as plt
import time 

# Create or connect to database
def create_database():
    conn = sqlite3.connect("emotions.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS emotions_new (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        emotion TEXT,
                        timestamp TEXT)''')
    conn.commit()
    conn.close()

# Insert data into database with retry
def insert_emotion(name, emotion):
    for attempt in range(5):
        try:
            conn = sqlite3.connect("emotions.db")
            cursor = conn.cursor()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("INSERT INTO emotions_new (name, emotion, timestamp) VALUES (?, ?, ?)", (name, emotion, timestamp))
            conn.commit()
            conn.close()
            break
        except sqlite3.OperationalError:
            print("Database is locked, retrying...")
            time.sleep(1.5)

# View database records
def view_database():
    conn = sqlite3.connect("emotions.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM emotions_new")
    rows = cursor.fetchall()
    conn.close()
    return rows

# Plot pie chart of emotions
def plot_emotions():
    conn = sqlite3.connect("emotions.db")
    cursor = conn.cursor()
    cursor.execute("SELECT emotion, COUNT(*) FROM emotions_new GROUP BY emotion")
    data = cursor.fetchall()
    conn.close()

    if data:
        labels, values = zip(*data)
        plt.pie(values, labels=labels, autopct='%1.1f%%')
        plt.title("Detected Emotions")
        plt.show()
    else:
        messagebox.showinfo("No Data", "No emotions to display.")

# Clear all data from the database
def clear_database():
    confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete all emotion records?")
    if confirm:
        conn = sqlite3.connect("emotions.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM emotions_new")
        conn.commit()
        conn.close()
        messagebox.showinfo("Deleted", "All emotion records have been deleted.")

# Detect emotions from webcam
def detect_emotion(name):
    cap = cv2.VideoCapture(0)
    start_time = time.time()
    while time.time() - start_time < 10:
        ret, frame = cap.read()
        if not ret:
            break

        try:
            result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)[0]
            emotion = result['dominant_emotion']
            insert_emotion(name, emotion)
            cv2.putText(frame, f"{emotion}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        except Exception as e:
            print("Detection Error:", e)

        cv2.imshow("Emotion Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# GUI Application
class EmotionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Emotion Detection App")
        self.root.geometry("700x600")
        self.root.configure(bg='lightblue')  # Light blue background

        self.name_label = tk.Label(root, text="Enter Your Name:", bg='lightblue', font=("Arial", 14))
        self.name_label.pack(pady=10)

        self.name_entry = tk.Entry(root, font=("Arial", 12))
        self.name_entry.pack(pady=5)

        tk.Button(root, text="Start Detection", command=self.start_detection, width=20, font=("Arial", 12)).pack(pady=8)
        tk.Button(root, text="Show Database", command=self.show_database, width=20, font=("Arial", 12)).pack(pady=8)
        tk.Button(root, text="Show Charts", command=plot_emotions, width=20, font=("Arial", 12)).pack(pady=8)
        tk.Button(root, text="Clear Data", command=clear_database, width=20, font=("Arial", 12)).pack(pady=8)

        self.output = tk.Text(root, height=12, width=80, font=("Arial", 10))
        self.output.pack(pady=10)

        

    def start_detection(self):
        name = self.name_entry.get()
        if not name:
            messagebox.showerror("Input Error", "Please enter your name.")
            return
        Thread(target=detect_emotion, args=(name,), daemon=True).start()

    def show_database(self):
        self.output.delete("1.0", tk.END)
        records = view_database()
        for row in records:
            self.output.insert(tk.END, str(row) + "\n")

# Main
if __name__ == "__main__":
    create_database()
    root = tk.Tk()
    app = EmotionApp(root)
    root.mainloop()
