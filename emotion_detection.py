import sys
user_name=sys.argv[1] if len(sys.argv)>1 else "Unknown"
import sqlite3
from deepface import DeepFace
import cv2
import tkinter as tk
from tkinter import simpledialog
#Function to get the user's name
def get_user_name():
    root=tk.Tk()
    root.withdraw()
    user_name=simpledialog.askstring("User Name","Enter your name:")
    return user_name

user_name=get_user_name()
if not user_name:
    print("no name entered");


# Open webcam
cap = cv2.VideoCapture(0)

# Connect to SQLite database
conn = sqlite3.connect("emotions.db")
cursor = conn.cursor()

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    try:
        # Analyze emotions
        result = DeepFace.analyze(frame, actions=['emotion'])
        emotion = result[0]['dominant_emotion']
        print("Detected Emotion:", emotion)
        # Store detected emotion in database
        from datetime import datetime
        cursor.execute("INSERT INTO emotions (name,emotion,timestamp) VALUES (?, ?, ?)", (user_name,emotion,datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()  # Save changes

        # Display emotion on frame
        cv2.putText(frame, f"Emotion: {emotion}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    except:
        pass

    # Show the frame
    cv2.imshow("Emotion Detection", frame)

    # Exit when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
conn.close()  # Close database connection