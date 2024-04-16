from . import web_ticket
from flask import request, render_template, jsonify
import requests
import json

DATABASE_URL = "http://127.0.0.1:5001"

@web_ticket.route('/<int:ticket_id>', methods = ['POST', 'GET'])
def view_ticket(ticket_id):
    response = requests.get(f"{DATABASE_URL}/get/ticket/{ticket_id}")
    ticket = json.loads(response.text)

    #if ticket['status'] == 'error':
    #    return jsonify({"status": "error", "message": "ticket not found"}), 404

    if request.method == 'GET':
        url = f"{DATABASE_URL}/post/web-sub/{ticket["id"]}"
        return render_template("ticket.html", ticket = ticket, url = url)


@web_ticket.route('/service_worker.js', methods=['GET'])
def get_service_worker():
    return web_ticket.send_static_file('service_worker.js')