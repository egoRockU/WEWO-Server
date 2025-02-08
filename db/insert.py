import sqlite3

conn = sqlite3.connect('database.db')

# res1 = conn.execute("INSERT INTO CollectedBottles (small, medium, large, total_liters) VALUES(1,2,3,14)")
# res2 = conn.execute("INSERT INTO CollectedBottles (small, medium, large, total_liters) VALUES(1,1,1,6)")
# res3 = conn.execute("INSERT INTO CollectedBottles (small, medium, large, total_liters) VALUES(0,0,1,3)")


# res1 = conn.execute("INSERT INTO PumperValues (name, value) VALUES('small', 1)")
# res2 = conn.execute("INSERT INTO PumperValues (name, value) VALUES('medium', 2)")
# res3 = conn.execute("INSERT INTO PumperValues (name, value) VALUES('large', 3)")

res1 = conn.execute("INSERT INTO TurbidityValue (turbidity) VALUES (5)")

conn.commit()
print(res1)