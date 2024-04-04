from flask import Flask
from flask_cors import CORS

ISSUER_ID = "3388000000022334672"
CLASS_SUFFIX = "hackathonclase"

def create_factory_api():
    api = Flask(__name__)

    # Handle requests from external sources
    CORS(api, origins= "*")

    from .factory import factory

    api.register_blueprint(factory, url_prefix = '/factory')

    return api