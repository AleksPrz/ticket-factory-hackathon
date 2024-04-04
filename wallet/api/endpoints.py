from flask import Blueprint, request, jsonify
from .bus_pass import Pass

gw = Blueprint('gw', __name__)
g_wallet = Pass()

@gw.route('/create-class', methods = ['POST'])
def create_class():
    """
    input:
    {
    "issuer_id" : str,
    "class_sufix" : str
    }
    """

    data = request.json
    class_id = g_wallet.create_class(data.get("issuer_id"), data.get("class_suffix"))
    
    if not class_id:
        return jsonify({'error' : "class could not be created"})
    
    return jsonify({"class_id": class_id}), 200


@gw.route('/create-pass', methods = ['POST'])
def create_object():
    """
    input:
    {
    "issuer_id" : str
    "class_sufix"
    "object_suffix" : str
    "ticket" : {
        "category" : str
        "passenger_name" : str
        "origin" : str
        "destination" : str
        "date " : str (DD-MM-YY)
        "hour" : str (HH:MM)
        "seat_number" : str
        "boarding_gate" : str
        "qr_value" : str    
        }
    }
    """
    data = request.json
    print(data)
    #print(data["ticket"])
    add_to_gw_url = g_wallet.create_object(data.get("issuer_id"), data.get("class_suffix"), data.get("object_suffix"), data.get("ticket"))

    if "https://pay.google.com/gp/v/save/" not in add_to_gw_url:
        return jsonify({"error": "Something went wrong"}), 500
    
    return add_to_gw_url


@gw.route('/send-message', methods = ['POST'])
def send_message():
    data = request.json
    issuer_id = data["issuer_id"]
    object_suffix = data["object_suffix"]
    header = data["header"]
    body = data["body"]
    

    response = g_wallet.add_object_message(issuer_id, object_suffix, header, body)

    return jsonify({"status" : "message sended!"})