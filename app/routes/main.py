# This module defines the routes for the application
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User, Account
from app import db
import uuid

main = Blueprint('main', __name__)

@main.route('/api/signup', methods=['POST'])
def signup():
    """This function creates a new user account and associated account."""
    try:
        data = request.get_json()
        if 'username' not in data or 'email' not in data or 'password' not in data:
            return jsonify({'error': 'Invalid data'}), 400
        
        username = data['username']
        email = data['email']
        password = data['password']
        
        password_hash = generate_password_hash(password)
        
        new_user = User(
            uuid=uuid.uuid4(),
            username=username,
            email=email,
            password_hash=password_hash
        )
        
        db.session.add(new_user)
        
        # Commit the user creation first to get the user ID
        db.session.commit()
        
        # Now create the associated account
        new_account = Account(
            uuid=uuid.uuid4(),
            email=email,
            user_id=new_user.id,  # Use the newly created user's ID
            created_at=new_user.created_at,  # Use the user's created_at timestamp
            updated_at=new_user.updated_at  # Use the user's updated_at timestamp
        )
        
        db.session.add(new_account)
        db.session.commit()
        
        return jsonify(new_account), 201
    
    except Exception as e:
        db.session.rollback()
        error_msg = str(e)
        if 'unique_email_accounts' in error_msg:
            return jsonify({'error': 'Email address already exists.'}), 400
        else:
            return jsonify({'error': 'Database error occurred.'}), 500

@main.route('/api/login', methods=['POST'])
def login():
    """Authenticating a user login"""
    data = request.get_json()
    if 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Invalid data'}), 400
    
    email = data['email']
    password = data['password']
    
    user = User.query.filter_by(email=email).first()
    
    if user and check_password_hash(user.password_hash, password):
        return jsonify({'id': user.id, 'username': user.username, 'email': user.email}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401
