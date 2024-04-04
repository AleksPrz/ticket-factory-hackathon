from flask import Blueprint, request, jsonify
from .bus_pass import Pass

gw = Blueprint(__name__)
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

    data = request.form
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
    "object_suffix" : str
    "ticket" : {
        "category" : str
        "passenger_name" : str
        "origin" : str
        "destination" : str
        "date " : str (DD-MM-YY)
        "hour" : str (HH:MM)
        "seat_number" : str
        "status" : str
        "boarding_gate" : str
        "qr_value" : str    
        }
    }
    """
    data = request.form
    pass

