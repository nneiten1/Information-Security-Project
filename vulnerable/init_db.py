import sqlite3

# create or connect to a database file
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# creating table for storing user data
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT NOT NULL       
);
''')

conn.commit()
conn.close()