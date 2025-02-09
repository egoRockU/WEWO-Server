import sqlite3
DATABASE_PATH = "./db/database.db"

def get_collected_bottles(date_filter='all'):
    query_condition = query_by(date_filter)
    query = f"SELECT * FROM CollectedBottles WHERE {query_condition};"
    if 'Invalid date filter.' in query_condition:
        return query_condition
    try:
        with sqlite3.connect(DATABASE_PATH) as conn:
            cur = conn.cursor()
            cur.execute(query)
            rows = cur.fetchall()
            return rows
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return "Collected Bottles Error: Database Error"
    except Exception as e:
        print(f"Unexpected error: {e}")
        return "Collected Bottles Error: Unexpected Error"
    


def query_by(date_filter='all'):
    query_conditions = {
        "today": "DATE(date) = DATE('now')",
        "this_week": "STRFTIME('%Y-%W', date) = STRFTIME('%Y-%W', 'now')",
        "this_month": "STRFTIME('%Y-%m', date) = STRFTIME('%Y-%m', 'now')",
        "all": "1=1"  # No filter, selects all records, sql trick to always true
    }

    if date_filter not in query_conditions:
        #raise ValueError("Invalid date filter. Use 'today', 'this_week', 'this_month', or 'all'.")
        return "Invalid date filter. Use 'today', 'this_week', 'this_month', or 'all'."

    return query_conditions[date_filter]