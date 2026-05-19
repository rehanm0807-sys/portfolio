import sqlite3

conn = sqlite3.connect("database.db")
cur = conn.cursor()

cur.execute("UPDATE users SET role='admin' WHERE email=?", ("admin@gmail.com",))

conn.commit()
conn.close()

print("Admin set successfully ✅")