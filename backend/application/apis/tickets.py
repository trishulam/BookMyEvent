from application.models import *
from flask import jsonify, request
from application.database import db
from main import app
from flask_bcrypt import Bcrypt
from helpers import token_generate,token_required
from main import photos
import base64
import os

@app.route('/book', methods=['POST'])
def book():
    try:
        data = request.get_json()
        print(data)
        ticket=Tickets(event_id=data['event_id'], user_id=data['user_id'], quantity=data['tickets'])
        db.session.add(ticket)
        db.session.commit()
        return jsonify({'message': 'Event booked successfully'}), 200
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500
    
@app.route('/deleteticket/<int:id>', methods=['POST'])
def deleteticket(id):
    try:
        ticket = Tickets.query.filter_by(id=id).first()
        db.session.delete(ticket)
        db.session.commit()
        return jsonify({'message': 'Ticket deleted successfully'}), 200
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500

@app.route('/mytickets/<int:id>', methods=['GET'])
def mytickets(id):
    try:
        tickets = Tickets.query.filter_by(user_id=id).all()
        ticketlist = []
        for ticket in tickets:
            ticket_data = {}
            ticket_data['id'] = ticket.id
            ticket_data['event_id'] = ticket.event_id
            ticket_data['user_id'] = ticket.user_id
            ticket_data['quantity'] = ticket.quantity
            ticketlist.append(ticket_data)
        return jsonify({'tickets': ticketlist}), 200
    
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500

@app.route('/availabletickets/<int:id>', methods=['GET'])
def availabletickets(id):
    try:
        tickets = Tickets.query.filter_by(event_id=id).all()
        event=Events.query.filter_by(id=id).first()
        booked=0
        for ticket in tickets:
            booked+=ticket.quantity
        available=event.venue.capacity-booked
        return jsonify({'available': available}), 200
    
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500