from flask import Blueprint, request, jsonify
from .models import Ticket, Trip, WebSubscription
from . import db

# Blueprint used to handle POST requests
# It's used to add registers to the database, using the information received from the request
# The endpoints return JSON that represents the result of the request

post = Blueprint('post', __name__)

@post.route('/ticket', methods = ['POST'])
def add_ticket_to_db():
	# Retrieve information from the request and create the ticket
	data = request.form
	# trip = get_trip(data)

	new_ticket = Ticket(
		passenger_name = data.get("passenger_name"),
		email = data.get("email"),
		seat_number = data.get("seat_number"),
		category = data.get("category"),
		status = "VIGENTE",     #A new ticket is ACTIVE BY DEFAULT
		service_number = data.get("service_number"),
		operation_number = data.get("operation_number"),
		payment_method = data.get("payment_method"),
		total_payment = data.get("total_payment"),
		billing_token = data.get("billing_token"),
		#wallet_url = "www.com",
		trip = trip
	)

	# Add it to the database
	return jsonify({'status': 'sucess', 'message': 'request detected'})

@post.route('/trip/', methods = ['POST'])
def add_trip_to_db():
	return jsonify({'status': 'sucess', 'message': 'request detected'})

@post.route('/web-suscription', methods = ['POST'])
def add_web_sus_to_db():
	return jsonify({'status': 'sucess', 'message': 'request detected'})