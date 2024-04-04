from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)

    # Handle requests from external sources
    CORS(app, origins= "*")

    from .viewer import viewer
    app.register_blueprint(viewer)
    
    return app