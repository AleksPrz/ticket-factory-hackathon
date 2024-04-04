from flask import Blueprint, request, jsonify
from .models import Ticket
# from datetime import datetime
from . import db
from .auxiliar_funcs import get_trip, create_qr

# Blueprint used to handle POST requests
# It's used to add registers to the database, using the information received from the request
# The endpoints return JSON that represents the result of the request

post = Blueprint('post', __name__)


@post.route('/ticket', methods = ['POST'])
def add_ticket_to_db():
	""" 
	This endpoint expects this information:
	{
	"email": passenger_email (str),
	"passenger_name" : passenger_name (str),
	"seat_number" : seat_number (int),
	"origin" : "origin (str),
	"destination" : destination (str),
	"date" : date (str),
	"day" : day (str),
	"hour" : hour (str),
	"time" : time_of_the_day (str),
	"boarding_gate" : boarding_gate (int),
	"category" : category (str),
	"billing_token" : billing_token (str),
	"total_payment" : total_payment (int),
	"payment_method" : payment_method (str),
	"operation_number" : operation_number (int),
	"service_number" : service_number (int),
	"wallet_url": wallet_url (str),
	"qr_url": qr_url (str)
	} 	
	"""
	
	# Retrieve information from the request
	data = request.form
	trip = get_trip(data)

	# Create the ticket
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
		wallet_url = data.get("wallet_url"),
		trip = trip
	)

	# Add it to the database
	db.session.add(new_ticket) 
	db.session.commit()

	# Add the QR URL atribute, which is the URL to view the image hosted in the server
	new_ticket.qr_url = create_qr(new_ticket)
	db.session.commit()

	return jsonify({'status': 'sucess', 'message': 'ticket created'})