from application.models import *
from flask import jsonify, request
from application.database import db
from main import app
from flask_bcrypt import Bcrypt
from helpers import token_generate,token_required
from main import photos
import base64
import os
from main import redis_cli
import json


@app.route('/addvenue', methods=['POST'])
def addvenue():
    try:
        name = request.form['name']
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        description = request.form['description']
        capacity = request.form['capacity']
        image=photos.save(request.files['file'])
        new_venue = Venues(name=name, address=address, city=city, state=state, description=description, capacity=capacity, image=image)
        db.session.add(new_venue)
        db.session.commit()
        venue_data={
            'id': new_venue.id,
            'name': new_venue.name,
            'address': new_venue.address,
            'city': new_venue.city,
            'state': new_venue.state,
            'description': new_venue.description,
            'capacity': new_venue.capacity,
            'image': new_venue.image,
            'events': ''
        }
        redis_cli.set(f'venue:{new_venue.id}', json.dumps(venue_data))
        return jsonify({"message": "Venue added successfully"}), 201
    
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500

@app.route('/deletevenue', methods=['POST'])
def deletevenue():
    data = request.get_json()
    venue_id = data['id']
    venue_key = f'venue:{venue_id}'
    if redis_cli.exists(venue_key):
        redis_cli.delete(venue_key)
    venue = Venues.query.filter_by(id=data['id']).first()
    if not venue:
        return jsonify({'message': 'No venue found!'})
    db.session.delete(venue)
    db.session.commit()
    return jsonify({'message': 'Venue deleted successfully'}), 200

@app.route('/updatevenue', methods=['POST'])
def updatevenue():
    try:
        data = request.get_json()
        venue_id = data['id']
        venue_key = f'venue:{venue_id}'

        # Fetch the existing venue data from Redis
        venue_data = json.loads(redis_cli.get(venue_key))

        if venue_data:
            # Update the venue data from the request
            venue_data['name'] = data['name']
            venue_data['address'] = data['address']
            venue_data['city'] = data['city']
            venue_data['state'] = data['state']
            venue_data['description'] = data['description']
            venue_data['capacity'] = data['capacity']

            # Store the updated venue data back in Redis
            redis_cli.set(venue_key, json.dumps(venue_data))

        # Continue with your existing code to update the venue in the database
        venue = Venues.query.filter_by(id=venue_id).first()
        if not venue:
            return jsonify({'message': 'No venue found!'})

        venue.name = data['name']
        venue.address = data['address']
        venue.city = data['city']
        venue.state = data['state']
        venue.description = data['description']
        venue.capacity = data['capacity']

        db.session.commit()

        return jsonify({'message': 'Venue updated successfully'}), 200

    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500



@app.route('/venues', methods=['GET'])
@token_required
def get_venues(current_user):
    venue_ids = redis_cli.keys('venue:*')
    venuelist=[]
    cache_output = []
    db_output = []
    if venue_ids:
        for venue_id in venue_ids:
            venue = json.loads(redis_cli.get(venue_id))
            venue_data={}
            venue_data['id']=venue['id']  
            venue_data['name']=venue['name']
            venue_data['address']=venue['address']
            venue_data['city']=venue['city']
            venue_data['state']=venue['state']
            venue_data['description']=venue['description']
            venue_data['capacity']=venue['capacity']
            image_path = os.path.join('static', 'images', venue['image'])
            with open(image_path, 'rb') as f:
                image_data = f.read()
                base64_encoded_data = base64.b64encode(image_data).decode('utf-8')
            venue_data['image']=base64_encoded_data
            venuelist.append(venue_data)
    cache_output=venuelist
    if not len(cache_output):
        print('cache miss')
        venues = Venues.query.all()
        for venue in venues:
            venue_data={}
            venue_data['id']=venue.id   
            venue_data['name']=venue.name
            venue_data['address']=venue.address
            venue_data['city']=venue.city
            venue_data['state']=venue.state
            venue_data['description']=venue.description
            venue_data['capacity']=venue.capacity
            image_path = os.path.join('static', 'images', venue.image)
            with open(image_path, 'rb') as f:
                image_data = f.read()
                base64_encoded_data = base64.b64encode(image_data).decode('utf-8')
            venue_data['image']=base64_encoded_data

            venuelist.append(venue_data)  
        db_output=venuelist


    if not len(cache_output) and not len(db_output):
        return jsonify({'message': 'No venues found!'})
    if cache_output:
        print('cache hit')
    return jsonify({'venues': cache_output if len(cache_output) else db_output})

@app.route('/venue/<id>', methods=['GET'])
def get_venue(id):
    try:
        venue = Venues.query.filter_by(id=id).first()
        venue_data={}
        venue_data['id']=venue.id   
        venue_data['name']=venue.name
        venue_data['address']=venue.address
        venue_data['city']=venue.city
        venue_data['state']=venue.state
        venue_data['description']=venue.description
        venue_data['capacity']=venue.capacity
        image_path = os.path.join('static', 'images', venue.image)
        with open(image_path, 'rb') as f:
            image_data = f.read()
            base64_encoded_data = base64.b64encode(image_data).decode('utf-8')
        venue_data['image']=base64_encoded_data
        return jsonify({'venue': venue_data}), 200
    
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500
