from flask import Blueprint, request, jsonify
from .models import Ticket, Trip, WebSubscription
from . import db

# Blueprint used to handle GET requests
# Return JSON that represents the asked object, like tickets, trips and websuscriptions

get = Blueprint('get', __name__)

@get.route('/ticket/<int:ticket_id>', methods = ['GET'])
def get_ticket_by_id(ticket_id):
    print(ticket_id)
    return jsonify({'status': 'sucess', 'message': 'request detected'})

@get.route('/trip/<int:trip_id>', methods = ['GET'])
def get_trip_by_id(trip_id):
    print(trip_id)
    return jsonify({'status': 'sucess', 'message': 'request detected'})

@get.route('/web-suscription/<int:web_sus_id>', methods = ['GET'])
def get_web_sus_by_id(web_sus_id):
    print(web_sus_id)
    return jsonify({'status': 'sucess', 'message': 'request detected'})