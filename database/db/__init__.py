from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import path

db = SQLAlchemy()

def create_database():
    app = Flask(__name__)

    # Configure the database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    app.app_context().push()

    from .models import Ticket, Trip, WebSubscription
    create_db_file(app)

    # Handle requests from external sources
    CORS(app, origins= "*")

    from .get import get
    from .post import post

    # Blueprints
    app.register_blueprint(get, url_prefix = '/get')
    app.register_blueprint(post, url_prefix = '/post')
    
    return app

def create_db_file(app):
    if not path.exists('instance/db.sqlite3'):
        with app.app_context():
            db.create_all()
            print("Created database")