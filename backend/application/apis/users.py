from application.models import *
from flask import jsonify, request
from application.database import db
from main import app
from flask_bcrypt import Bcrypt
from helpers import token_generate, token_required

@app.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        user = Users.query.filter_by(email=data['email']).first()
        if user:
            return jsonify({'message': 'User already exists'}), 409
        else:
            b=Bcrypt()
            hashed_password = b.generate_password_hash(data['password'])
            new_user = Users(email=data['email'], username=data['username'] ,password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return jsonify({"token": token_generate(new_user.username)}), 201
            
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        user = Users.query.filter_by(email=data['email']).first()
        if user:
            b=Bcrypt()
            if b.check_password_hash(user.password, data['password']):
                #check if admin and pass admin to frontend
                if user.admin:
                    return jsonify({"token": token_generate(user.username), "admin": True}), 200
                else:
                    return jsonify({"token": token_generate(user.username), "admin": False, "user_id":user.id}), 200
            else:
                return jsonify({'message': 'Invalid password'}), 401
        else:
            return jsonify({'message': 'User does not exist'}), 404
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500
    
@app.route('/users', methods=['GET'])
@token_required
def get_users():
    try:
        users = Users.query.all()
        return jsonify([user.serialize() for user in users]), 200
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500

@app.route('/users/<int:id>', methods=['GET'])
@token_required
def get_user(curret_user,id):
    try:
        user = Users.query.get(id)
        if user:
            user_data = {}
            user_data['id'] = user.id
            user_data['email'] = user.email
            user_data['username'] = user.username
            user_data['admin'] = user.admin
            return jsonify({ 'user' : user_data }), 200
        else:
            return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500