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

def insert_turbidity(turbidity):
    try:
        with sqlite3.connect(DATABASE_PATH) as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO TurbidityValue (turbidity) VALUES (?)", (turbidity,))
            conn.commit()
            print("Turbidity Value Has been saved successfully")
    except:
        conn.rollback()
        print("Error Saving Turbidity")
    finally:
        conn.close()

def get_pumper_values():
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        with conn:
            conn.row_factory = sqlite3.Row
            curs = conn.cursor()
            curs.execute("SELECT * FROM PumperValues")
            rows = curs.fetchall()
            return rows
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return "Pumper Values Error: Database Error"
    except Exception as e:
        print(f"Unexpected error: {e}")
        return "Pumper Values Error: Unexpected Error"