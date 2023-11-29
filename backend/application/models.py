from .database import db
from datetime import datetime

class Ratings(db.Model):
    __tablename__="Ratings"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('Events.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

class Tickets(db.Model):
    __tablename__="Tickets"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_id = db.Column(db.Integer, db.ForeignKey('Events.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)

class Users(db.Model):
    __tablename__="Users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, unique=True, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    admin = db.Column(db.Boolean, default=False)
    tickets=db.relationship('Tickets', backref='user', lazy=True,cascade="all, delete")
    ratings=db.relationship('Ratings', backref='user', lazy=True,cascade="all, delete")

class Venues(db.Model):
    __tablename__="Venues"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True, nullable=False)
    address = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    state = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String, nullable=False, default="None")
    events=db.relationship('Events', backref='venue', lazy=True,cascade="all, delete")

class Events(db.Model):
    __tablename__="Events"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False)
    time = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String, nullable=False, default="None")
    tags = db.Column(db.String, nullable=True)
    tickets=db.relationship('Tickets', backref='event', lazy=True,cascade="all, delete")
    ratings=db.relationship('Ratings', backref='event', lazy=True,cascade="all, delete")
    venue_id = db.Column(db.Integer, db.ForeignKey('Venues.id'), nullable=False)

