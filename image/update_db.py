import sqlite3

conn = sqlite3.connect("database.db")
cur = conn.cursor()

# 🔥 role column add
cur.execute("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'user'")

conn.commit()
conn.close()

print("Role column added successfully ✅")