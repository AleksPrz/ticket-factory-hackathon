from flask import Flask
from .endpoints import gw

def create_api():
    api = Flask(__name__)
    
    api.register_blueprint(gw, url_prefix = '/')
    return api