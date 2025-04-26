import sqlite3

# Connect to database
conn = sqlite3.connect("emotions.db")
cursor = conn.cursor()

# Create a new table with correct column order
cursor.execute("""
    CREATE TABLE IF NOT EXISTS emotions_new(
        Name TEXT,
        Id INTEGER PRIMARY KEY,
        Emotion TEXT,
        Timestamp TEXT
    )
""")

# Copy data from old table to new table
cursor.execute("""
    INSERT INTO emotions_new(Name, Id, Emotion, Timestamp)
    SELECT Name, Id, Emotion, Timestamp FROM emotions
""")

# Drop old table and rename new table
cursor.execute("DROP TABLE emotions")
cursor.execute("ALTER TABLE emotions_new RENAME TO emotions")

# Commit and close connection
conn.commit()
conn.close()

print("Column order updated successfully!")