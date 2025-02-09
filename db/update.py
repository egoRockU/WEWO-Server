import sqlite3

conn = sqlite3.connect('database.db')

conn.execute("ALTER TABLE PumperValues ADD ml INTEGER DEFAULT 0")
