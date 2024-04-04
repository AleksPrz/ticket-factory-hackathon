from flask import Blueprint, request, jsonify, send_from_directory
from .models import Ticket, Trip, WebSubscription
from . import db

# Blueprint used to handle GET requests
# All the endpoints return JSON that represents the asked object, like tickets, trips and websuscriptions

get = Blueprint('get', __name__)

#@get.route("/<str:image>.png")
#def get_image(image):
#    return get.send_static_file(f"{image}.png")

@get.route('/ticket/<int:ticket_id>', methods = ['GET'])
def get_ticket_by_id(ticket_id):
    # Look for the ticket in the database
    ticket = Ticket.query.filter_by(id = ticket_id).first() 
    
    if not ticket:
        return jsonify({"status": "error", "message": "ticket not found"}), 404

    # If the ticket with such id was found, convert it to a dictionary and return it as JSON
    trip = ticket.trip
    ticket_data = ticket.__dict__
    trip_data = trip.__dict__

    # Parse correctly the date and hour
    trip_data["date"] = trip.date.strftime("%d-%m-%Y")  
    trip_data["hour"] = trip.hour.strftime("%H:%M") 

    #Delete the sqlalchemy values we don't need
    del ticket_data['_sa_instance_state']   
    del trip_data['_sa_instance_state']

    ticket_data["trip"] = trip_data
    return jsonify(ticket_data), 200


@get.route('/trip/<int:trip_id>', methods = ['GET'])
def get_trip_by_id(trip_id): 
    # Look for the trip in the database
    trip = Trip.query.filter_by(id = trip_id).first()

    if not trip:
        return jsonify({"status": "error", "message": "trip not found"}), 404

    # If the trip with such id was found, convert it to a dictionary and return it as JSON
    trip_data = trip.__dict__

    # Parse correctly the date and hour
    trip_data["date"] = trip.date.strftime("%d-%m-%Y")  
    trip_data["hour"] = trip.hour.strftime("%H:%M") 

    #Delete the sqlalchemy value we don't need
    del trip_data['_sa_instance_state']
    
    return jsonify(trip_data), 200 


@get.route('/web-subscription/<int:web_subs_id>', methods = ['GET'])
def get_web_subscription_by_id(web_subs_id):
    # Look for the suscription in the database
    web_subscription = WebSubscription.query.filter_by(id = web_subs_id).first()

    if not web_subscription:
        return jsonify({"status": "error", "message": "suscription not found"}), 404

    web_subs_data = web_subscription.__dict__
    del web_subs_data['_sa_instance_state']

    return jsonify(web_subs_data), 200


@get.route('/qr/<int:qr_id>', methods = ['GET'])
def get_qr_img(qr_id):
    # Look for the ticked with that id in the database
    ticket = Ticket.query.filter_by(id = qr_id).first() 
    
    if not ticket:
        return jsonify({"status": "error", "message": "image not found"}), 404

    # Serve the static content
    return send_from_directory('static', f'{qr_id}.png')