import sqlite3

conn = sqlite3.connect('database.db')

with conn:
    conn.row_factory = sqlite3.Row
    curs = conn.cursor()
    curs.execute("SELECT * FROM PumperValues")
    rows = curs.fetchall()
    for row in rows:
        print(f"{row['name']}: {row['value']}")