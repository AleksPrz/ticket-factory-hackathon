from flask import Blueprint, request, jsonify
from .bus_pass import Pass

pass_builder = Pass()

api = Blueprint('api', __name__)

@api.route('/create-class', methods = ['POST'])
def create_class():
    """
    input:
    {
    "issuer_id" : str,
    "class_sufix" : str
    }
    """

    data = request.json
    issuer_id = data.get('issuer_id')
    class_suffix = data.get('class_suffix')

    if issuer_id == None or class_suffix == None:
        print("Missing data")
        return jsonify({'error': 'Missing data'}), 400
    

    try:
        class_id = pass_builder.create_class(issuer_id, class_suffix)
    except Exception as e:
        error_message = e.args[0]
        print(error_message)
        return jsonify({'error': error_message}), 500
    
    return jsonify({"class_id": class_id}), 200


@api.route('/create-pass', methods = ['POST'])
def create_object():
    """
    input:
    {
    "issuer_id" : str
    "class_suffix" : str
    "object_suffix" : str
    "ticket" : {
        "category" : str
        "passenger_name" : str
        "seat_number" : str
        "billing_token" : str,
        "total_payment" : dbl,
        "payment_method" : str,
        "operation_number" : int,
        "service_number" : int,
        "trip": {
            "origin" : str
            "destination" : str
            "date" : str (DD-MM-YY)
            "time" : srr
            "hour" : str (HH:MM)
            "boarding_gate" : str
            }
        }
    }
    """

    data : dict = request.json
    issuer_id = data.get('issuer_id')
    class_suffix = data.get('class_suffix')
    object_suffix = data.get('object_suffix')
    ticket : dict = data.get('ticket')

    if None in [issuer_id, class_suffix, object_suffix, ticket]:
        print("Missing data")
        return jsonify({'error': 'Missing data'}), 400

    try:
        add_to_gw_url = pass_builder.create_object(issuer_id, class_suffix, object_suffix, ticket)
    except Exception as e:
        error_message = e.args[0]
        print(error_message)
        return jsonify({'error': error_message}), 500

    
    return jsonify({'link' : add_to_gw_url})


@api.route('/send-message', methods = ['POST'])
def send_message():
    """
    input:
    {
    issuer_id: str
    object_suffix: str
    header: str
    body: str
    }
    """

    data : dict = request.json
    issuer_id = data.get('issuer_id')
    object_suffix = data.get('object_suffix')
    header = data.get('header')
    body = data.get('body')
    
    #Check that all data is received
    if None in [issuer_id, object_suffix, body, header]:
        print("Missing data")
        return jsonify({'error': 'Missing data'}), 400

    try:
        pass_builder.add_object_message(issuer_id, object_suffix, header, body)
    except Exception as e:
        error_message = e.args[0]
        print(error_message)
        return jsonify({'error': error_message}), 500

    return jsonify({"status" : "message sended!"}), 200


@api.route('/update-hour', methods=['PATCH'])
def update_hour():
    """
    input:
    {
    "issuer_id" : str
    "object_suffix" : str
    "hour" : str
    }
    """

    data : dict = request.json
    issuer_id = data.get("issuer_id")
    object_suffix = data.get("object_suffix")
    new_hour = data.get("hour")


    #Check that all data is received
    if None in [issuer_id, object_suffix, new_hour]:
        print("Missing data")
        return jsonify({'error': 'Missing data'}), 400
    
    try:
        pass_builder.update_hour(issuer_id, object_suffix, new_hour)
    except Exception as e:
        error_message = e.args[0]
        print(error_message)
        return jsonify({'error': error_message}), 500

    return jsonify({"status": "Updated hour"})


@api.route('/update-status', methods=['PATCH'])
def update_status():
    """
    input:
    {
    "issuer_id" : str
    "object_suffix" : str
    "status" : str
    }
    """

    data: dict = request.json
    issuer_id = data.get("issuer_id")
    object_suffix = data.get("object_suffix")
    new_status = data.get("status")

    #Check that all data is received
    if None in [issuer_id, object_suffix, new_status]:
        print("Missing data")
        return jsonify({'error': 'Missing data'}), 400

    try:
        pass_builder.update_status(issuer_id, object_suffix, new_status)
    except Exception as e:
        error_message = e.args[0]
        print(error_message)
        return jsonify({'error': error_message}), 500

    return jsonify({"status": "Updated status"})
