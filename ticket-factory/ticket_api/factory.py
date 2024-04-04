from flask import Blueprint, request
from .emailing import send_email
import requests
from . import ISSUER_ID, CLASS_SUFFIX

factory = Blueprint('factory', __name__)

DATABASE_URL = "http://127.0.0.1:5003/post"
WALLET_API_URL = "http://127.0.0.1:5004"

@factory.route('/create-ticket', methods = ['POST'])
def create_ticket():
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
	"service_number" : service_number (int)
	} 	
	"""
	ticket_data = request.json

	wallet_data = {
		"issuer_id" : ISSUER_ID,
		"class_suffix": CLASS_SUFFIX,
		"object_suffix" : ticket_data["object_suffix"],
		"ticket" : {
			"category" : ticket_data["category"],
			"passenger_name" : ticket_data["passenger_name"],
			"origin" : ticket_data["origin"],
			"destination" : ticket_data["destination"],
			"date " : ticket_data["date"],
			"hour" : ticket_data["hour"],
			"seat_number" : ticket_data["seat_number"],
			"boarding_gate" : ticket_data["boarding_gate"],
			"qr_value" : f"{ticket_data["passenger_name"]}"    
        }
	}
	
	wallet_response = requests.post(url= f"{WALLET_API_URL}/create-pass" , json = wallet_data)
	wallet_url = wallet_response.text
	
	ticket_data['wallet_url'] = wallet_url

	response_url = requests.post(url = f"{DATABASE_URL}/ticket", data = ticket_data)
	ticket_url = response_url.text

	# Send the email to the user, containing the URL to view the ticket
	email = ticket_data.get('email')
	wallet_url = ticket_data.get('wallet_url')
	passenger_name = ticket_data.get('passenger_name')

	send_email(email, ticket_url, passenger_name)

	return response_url.text