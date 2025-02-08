import sqlite3

conn = sqlite3.connect('database.db')

conn.execute('DELETE FROM TurbidityValue')
conn.commit()