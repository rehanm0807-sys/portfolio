import sqlite3

conn = sqlite3.connect("database.db")
cur = conn.cursor()

# Table create (safe way)
cur.execute("""
CREATE TABLE IF NOT EXISTS stocks (
    id INTEGER PRIMARY KEY,
    name TEXT,
    price INTEGER,
    status TEXT
)
""")

# Data insert (FIXED)
cur.execute("""
INSERT INTO stocks (name, price, status) VALUES
('TCS', 3500, 'profit'),
('Infosys', 1450, 'loss'),
('Reliance', 2800, 'profit'),
('HDFC Bank', 1600, 'profit'),
('ICICI Bank', 950, 'loss'),
('GOOGL', 450, 'profit'),
('AMZN', 800, 'loss');
""")

conn.commit()
conn.close()

print("✅ Table & Data Added")