import sqlite3

# Connect to SQLite database (it will create a new one if not exists)
conn = sqlite3.connect("emotions.db")

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create a table to store detected emotions
cursor.execute("""
CREATE TABLE IF NOT EXISTS emotions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    emotion TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

# Commit and close the connection
conn.commit()
conn.close()

print("Database and table created successfully.")