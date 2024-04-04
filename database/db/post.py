from flask import Blueprint, request, jsonify
from .models import Ticket, Trip, WebSubscription
from . import db

# Blueprint used to handle POST requests
# It's used to add registers to the database, using the information received from the request
# Return JSON that represents the result of the request

post = Blueprint('post', __name__)

@post.route('/ticket', methods = ['POST'])
def add_ticket_to_db():
    # Retrieve information from the request
    return jsonify({'status': 'sucess', 'message': 'request detected'})

@post.route('/trip/', methods = ['POST'])
def add_trip_to_db():
    return jsonify({'status': 'sucess', 'message': 'request detected'})

@post.route('/web-suscription', methods = ['POST'])
def add_web_sus_to_db():
    return jsonify({'status': 'sucess', 'message': 'request detected'})