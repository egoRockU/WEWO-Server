import sqlite3
DATABASE_PATH = "./db/database.db"

def insert_collected_bottles(small, medium, large, total_liters):
    try:
        with sqlite3.connect(DATABASE_PATH) as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO CollectedBottles (small, medium, large, total_liters) VALUES(?,?,?,?)"
                        , (small, medium, large, total_liters))
            conn.commit()
            print("Bottles Have been saved successfully")
    except:
        conn.rollback()
        print("Error Saving bottles")
    finally:
        conn.close()