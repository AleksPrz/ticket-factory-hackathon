from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()

def create_database():
    app = Flask(__name__)

    #DATABASE
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    app.app_context().push()
    
    from .models import Ticket, Trip, WebSubscription
    create_db_file(app)

    #BLUEPRINTS
    from .ticket import ticket
    from .trip import trip
    from .web import web

    app.register_blueprint(ticket, url_prefix = '/ticket')
    app.register_blueprint(trip, url_prefix = '/trip')
    app.register_blueprint(web, url_prefix = '/web')

    
    return app

def create_db_file(app):
    if not path.exists('instance/db.sqlite3'):
        with app.app_context():
            db.create_all()
            print("Created database")