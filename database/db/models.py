from . import db

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    passenger_name = db.Column(db.String(50))
    email = db.Column(db.String(70))
    seat_number = db.Column(db.String(10))
    category = db.Column(db.String(30))
    status = db.Column(db.String(30))
    billing_token = db.Column(db.String(30))
    total_payment = db.Column(db.Float)
    payment_method = db.Column(db.String(30))
    operation_number = db.Column(db.Integer)
    service_number = db.Column(db.Integer)

    wallet_url = db.Column(db.String(30))
    qr_url = db.Column(db.String(30))

    trip_id = db.Column(db.Integer, db.ForeignKey('trip.id'))
    trip = db.relationship('Trip', back_populates = "tickets")

    web_subscription = db.relationship("WebSubscription", back_populates = "ticket", uselist = False, cascade = "all, delete-orphan", single_parent = True) 
    
    
class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    origin = db.Column(db.String(30))
    destination = db.Column(db.String(30))
    date = db.Column(db.Date)
    day = db.Column(db.String(10))
    hour = db.Column(db.Time)
    time = db.Column(db.String(10))
    boarding_gate = db.Column(db.String(10))
    tickets = db.relationship('Ticket', back_populates = "trip", cascade = "all, delete-orphan")

class WebSubscription(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('ticket.id'), primary_key=True)
    data = db.Column(db.String(1000))
    ticket = db.relationship('Ticket', back_populates = "web_subscription", uselist = False)


"""
uselist=False    Relación de una sola instancia
cascade="all, delete-orphan" si eliminas una instancia padre, tambien se eliminan sus hijos asociados
single_parent=True garantiza que solo una instancia de WebSubscription este relacionada con un solo Ticket.
"""