from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)

    #Handle requests from external soruces
    CORS(app, origins = "*")

    #Register all Blueprints
    return app