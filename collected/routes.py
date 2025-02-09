from flask import Blueprint, request
from collected.collected_queries import get_collected_bottles

collected = Blueprint('collected', __name__, url_prefix='/collected')

@collected.route('/get_collected_bottles', methods=["POST"])
def get_collected():
    date_filter = request.form["date_filter"]
    rows = get_collected_bottles(date_filter)
    
    if isinstance(rows, str):
        return rows, 403
    else:
        parsed_rows = {
            item[0]: {"large": item[1], "medium": item[2], "small": item[3], "total_liters": item[4], "date": item[5]}
            for item in rows
        }
        return parsed_rows