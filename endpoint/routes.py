from flask import Blueprint, request
from endpoint.endpoint_queries import get_collected_bottles, get_turbidity_values, update_pumper_values
import json

endpoint = Blueprint('collected', __name__, url_prefix='/api')

@endpoint.route('/get_collected_bottles', methods=["POST"])
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
        collected_bottles = json.dumps(parsed_rows, indent=4)
        return collected_bottles


@endpoint.route('/get_turbidity_values', methods=["POST"])
def get_turbidity():
    date_filter = request.form["date_filter"]
    rows = get_turbidity_values(date_filter)

    if isinstance(rows, str):
        return rows, 403
    else:
        parsed_rows = {
            item[0]: {"date": item[1], "value": item[2]}
            for item in rows
        }
        turbidity_values = json.dumps(parsed_rows, indent=4)
        return turbidity_values
    

@endpoint.route('/update_pumper_values', methods=["POST"])
def update_pumper():
    smallV = request.form["small_sec"]
    smallML = request.form["small_ml"]
    mediumV = request.form["medium_sec"]
    mediumML = request.form["medium_ml"]
    largeV = request.form["large_sec"]
    largeML = request.form["large_ml"]

    result = update_pumper_values(smallV, smallML, mediumV, mediumML, largeV, largeML)
    if 'Pumper Values Error' in result:
        return result, 403
    else:
        return result