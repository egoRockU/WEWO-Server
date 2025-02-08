import sqlite3

conn = sqlite3.connect('database.db')
if (conn):
    print("Connected to Database successfully")

conn.execute('''CREATE TABLE CollectedBottles (
             id INTEGER PRIMARY KEY,
             small INTEGER DEFAULT 0,
             medium INTEGER DEFAULT 0,
             large INTEGER DEFAULT 0,
             total_liters INTEGER DEFAULT 0,
             date datetime DEFAULT current_timestamp
             )''')


conn.execute('''CREATE TABLE PumperValues (
             id INTEGER PRIMARY KEY,
             name TEXT NOT NULL,
             value INTEGER DEFAULT 0
             )''')

conn.execute('''CREATE TABLE TurbidityValue (
             id INTEGER PRIMARY KEY,
             date datetime DEFAULT current_timestamp,
             turbidity INTEGER DEFAULT 0
             )''')