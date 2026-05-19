import sqlite3

conn = sqlite3.connect("database.db")
cur = conn.cursor()

# 🔴 OLD TABLE DELETE
cur.execute("DROP TABLE IF EXISTS users")

# 🆕 NEW TABLE WITH ROLE
cur.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    email TEXT,
    password TEXT,
    role TEXT DEFAULT 'user'
)
""")

# 🔥 OPTIONAL: DEFAULT ADMIN CREATE
cur.execute("""
INSERT INTO users (username, email, password, role)
VALUES (?, ?, ?, ?)
""", ("admin", "admin@gmail.com", "admin123", "admin"))

conn.commit()
conn.close()

print("Database ready with admin ✅")