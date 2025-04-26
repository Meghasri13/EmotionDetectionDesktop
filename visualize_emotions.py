import sqlite3
import matplotlib.pyplot as plt

# Connect to SQLite database
conn = sqlite3.connect("emotions.db")
cursor = conn.cursor()

# Fetch all stored emotions
cursor.execute("SELECT emotion FROM emotions")
rows = cursor.fetchall()

# Count occurrences of each emotion
emotion_counts = {}
total_entries = len(rows)

for row in rows:
    emotion = row[0]
    if emotion in emotion_counts:
        emotion_counts[emotion] += 1
    else:
        emotion_counts[emotion] = 1

# Prepare data for the pie chart
labels = list(emotion_counts.keys())
sizes = [count / total_entries * 100 for count in emotion_counts.values()]

# Create the pie chart
plt.figure(figsize=(8, 6))
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=['red', 'blue', 'green', 'yellow', 'purple', 'orange'])
plt.title("Emotion Percentage Distribution")

# Show the pie chart
plt.show()

# Close the connection
conn.close()