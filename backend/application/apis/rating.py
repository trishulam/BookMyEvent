from application.models import *
from flask import jsonify, request
from application.database import db
from main import app
from flask_bcrypt import Bcrypt
from helpers import token_generate,token_required
from main import photos
import base64
import os

@app.route('/addrating', methods=['POST'])
def addrating():
    try:
        data = request.get_json()
        print(data)
        rating=Ratings(event_id=data['event_id'], user_id=data['user_id'], rating=data['rating'])
        db.session.add(rating)
        db.session.commit()
        return jsonify({'message': 'Rating added successfully'}), 200
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500