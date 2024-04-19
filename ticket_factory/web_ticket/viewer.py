from flask import request, render_template, jsonify, Blueprint, send_from_directory
import requests
import json

web_ticket = Blueprint('web_ticket',__name__)

@web_ticket.route('/<int:ticket_id>', methods = ['POST', 'GET'])
def view_ticket(ticket_id):
    """Displays the ticket to te user with all its data"""

    base_url = request.host_url[:-6] #"http:localhost:" if opened from this device | "http:public_ip:" if opened from an external device

    response = requests.get(f"{base_url}:5001/get/ticket/{ticket_id}") #Consults the ticket data in the database
    
    if response.status_code != 200:
        return jsonify({'error': 'Not found'}), 404
    
    ticket : dict = json.loads(response.text)

    if request.method == 'GET':

        post_url = f"{base_url}:5001/post/web-sub/{ticket_id}" #This url is which manages the notification subscription storage

        #url = f"{DATABASE_URL}/post/web-sub/{ticket["id"]}"
        return render_template("ticket.html", ticket = ticket, url = post_url)


#@web_ticket.route('/service_worker.js', methods=['GET'])
#def get_service_worker():
#    """Allows to send the service worker to the client browser"""
#
#    return web_ticket.send_static_file('service_worker.js')

#TEST ENDPOINT
@web_ticket.route('/1', methods = ['GET'])
def hello():
    """Displays the ticket to te user with all its data"""

    base_url = request.host_url[:-6] #"http:localhost:" if opened from this device | "http:public_ip:" if opened from an external device
    
    
    ticket = {
    "trip" : {
        "origin" : "Campeche",
        "destination" : "Guadalajara",
        "date" : "03-04-2024",
        "day" : "MIERCOLES",
        "hour" : "4:40",
        "time" : "TARDE",
        "boarding_gate" : "59"
    },
    "object_suffix" : "hackatonprueba461",
    "email": "alexis4g2@gmail.com",
    "passenger_name" : "Valeria Lee Almeyda",
    "seat_number" : "13",
    "category" : "ADULTO",
    "billing_token" : "123456789",
    "total_payment" : 100.00,
    "payment_method" : "Tarjeta de debito",
    "operation_number" : 58,
    "service_number" : 77,
    "wallet_url" : "hola",
    "qr_url" : "urp"
}

    if request.method == 'GET':

        post_url = f"{base_url}:5001/post/web-sub/prueba" #This url is which manages the notification subscription storage
        print(post_url)

        return render_template("ticket.html", ticket = ticket, url = post_url)