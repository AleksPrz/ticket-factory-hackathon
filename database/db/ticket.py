from flask import Blueprint, request

ticket = Blueprint('ticket', __name__)

@ticket.route("/get/<int:id>")
def get_ticket(id):
    
    pass