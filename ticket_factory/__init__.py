from flask import Flask, send_from_directory
from flask_cors import CORS
from . import wallet, web_ticket, factory

#Blueprints
api = wallet.api
web = web_ticket.web_ticket
ticket_factory = factory.factory

def create_app():
    app = Flask(__name__)

    #Handle requests from external soruces
    CORS(app, origins = "*")

    #Register all Blueprints

    app.register_blueprint(ticket_factory, url_prefix = "/", static_folder = "static/factory")
    app.register_blueprint(web, url_prefix = "/view", static_folder = "static/web_ticket")
    app.register_blueprint(api, url_prefix = "/api")

    #Allows to send static files such as images and javascript files in a secure way
    @app.route('/static/<path:path>')
    def send_static(path):
        return send_from_directory('static', path) 

    return app