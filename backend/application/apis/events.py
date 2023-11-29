from application.models import *
from flask import jsonify, request
from application.database import db
from main import app
from flask_bcrypt import Bcrypt
from helpers import token_generate,token_required
from main import photos
import base64
import os


#create all event relate routes

@app.route('/addevent', methods=['POST'])
def addevent():
    try:
        name = request.form['name']
        date = request.form['date']
        time = request.form['time']
        description = request.form['description']
        price = request.form['price']
        venue_id = request.form['venue_id']
        image = photos.save(request.files['file'])
        if request.form['tags']:
            tags = request.form['tags']
        else:
            tags = None
        new_event = Events(name=name, date=date, time=time, description=description, price=price, venue_id=venue_id, image=image, tags=tags)
        db.session.add(new_event)
        db.session.commit()
        return jsonify({"message": "Event added successfully"}), 201
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500

@app.route('/deleteevent', methods=['POST'])
def deleteevent():
    try:
        data = request.get_json()
        event = Events.query.filter_by(id=data['id']).first()
        db.session.delete(event)
        db.session.commit()
        return jsonify({'message': 'Event deleted successfully'}), 200
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500

@app.route('/updateevent', methods=['POST'])
def updateevent():
    try:
        data = request.get_json()
        event = Events.query.filter_by(id=data['id']).first()
        event.name=data['name']
        event.date=data['date']
        event.time=data['time']
        event.description=data['description']
        if data['tags']:
            event.tags=(',').join(data['tags'])
        else:
            event.tags=None
        event.venue_id=data['venue_id']
        db.session.commit()
        return jsonify({'message': 'Event updated successfully'}), 200
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500    

@app.route('/venueevents/<int:id>', methods=['GET'])
def venueevents(id):
    try:
        events = Events.query.filter_by(venue_id=id).all()
        event_data = []
        for event in events:
            event_format = {}
            event_format['id'] = event.id
            event_format['name'] = event.name
            event_format['date'] = event.date
            event_format['time'] = event.time
            event_format['description'] = event.description
            event_format['price'] = event.price
            event_format['venue_id'] = event.venue_id
            eimage_path = os.path.join('static', 'images', event.image)
            with open(eimage_path, 'rb') as f:
                image_data = f.read()
                base64_encoded_data = base64.b64encode(image_data).decode('utf-8')
            event_format['image'] = base64_encoded_data
            sum=0
            for rating in event.ratings:
                sum+=rating.rating
            if len(event.ratings)==0:
                event_format['rating']=2.5
            else:
                event_format['rating']=sum/len(event.ratings)
            if event.tags:
                event_format['tags'] = event.tags.split(',')
            else:
                event_format['tags'] = None
            event_data.append(event_format)
        return jsonify({'events': event_data})
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500

@app.route('/events/<int:id>', methods=['GET'])

def getevent(id):
    try:
        event = Events.query.filter_by(id=id).first()
        event_data = {}
        event_data['id'] = event.id
        event_data['name'] = event.name
        event_data['date'] = event.date
        event_data['time'] = event.time
        event_data['description'] = event.description
        event_data['price'] = event.price
        event_data['venue_id'] = event.venue_id
        eimage_path = os.path.join('static', 'images', event.image)
        with open(eimage_path, 'rb') as f:
            image_data = f.read()
            base64_encoded_data = base64.b64encode(image_data).decode('utf-8')
        event_data['image']=base64_encoded_data
        return jsonify({'event': event_data})
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500

@app.route('/tags', methods=['GET'])
def gettagscount():
    try:
        tags = Events.query.with_entities(Events.tags).all()
        tags_list = []
        for tag in tags:
            if tag.tags:
                tags_list.extend(tag.tags.split(','))
        tags_list = list(set(tags_list))
        tags_count = []
        for tag in tags_list:
            tag_data={}
            tag_data['name']=tag
            tag_data['count']=0
            for event in Events.query.all():
                if event.tags:
                    if tag in event.tags.split(','):
                        tag_data['count']+=1
            tags_count.append(tag_data)
        return jsonify({'tags': tags_count})
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500