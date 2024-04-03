from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask()
    #TO HANDLE REQUESTS FROM EXTERNAL SOURCES
    CORS(app, origins= "*") #origins = "*" IS NOT SECURE CAUSE WE ARE ALLOWING REQUESTS FROM EVERYWHERE
    
    return app

