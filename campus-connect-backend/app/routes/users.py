# app/routes/users.py

from flask import Blueprint, request, jsonify
from app.db import get_db
from datetime import datetime
from bson import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

users_bp = Blueprint('users', __name__)

@users_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    required_fields = ['username', 'email', 'password', 'name', 'year', 'department']
    
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    db = get_db()
    existing_user = db.users.find_one({"email": data['email']})
    
    if existing_user:
        return jsonify({'error': 'Email already registered'}), 400
    
    user = {
        "username": data['username'],
        "email": data['email'],
        "password_hash": generate_password_hash(data['password']),
        "name": data['name'],
        "year": data['year'],
        "department": data['department'],
        "created_at": datetime.utcnow(),
        "last_active": datetime.utcnow(),
        "role": "student",  # Default role
        "profile_picture": None,
        "bio": None,
        "social_links": {},
        "notifications": [],
        "preferences": {
            "email_notifications": True,
            "push_notifications": True
        }
    }
    
    result = db.users.insert_one(user)
    return jsonify({'status': 'success', 'id': str(result.inserted_id)}), 201

@users_bp.route('/profile/<user_id>', methods=['GET'])
def get_profile(user_id):
    db = get_db()
    user = db.users.find_one({"_id": ObjectId(user_id)})
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        "status": "success",
        "data": {
            "id": str(user['_id']),
            "username": user['username'],
            "email": user['email'],
            "name": user['name'],
            "year": user['year'],
            "department": user['department'],
            "created_at": user['created_at'].isoformat(),
            "last_active": user['last_active'].isoformat(),
            "role": user['role'],
            "profile_picture": user['profile_picture'],
            "bio": user['bio'],
            "social_links": user['social_links'],
            "preferences": user['preferences']
        }
    }), 200

@users_bp.route('/profile/<user_id>', methods=['PUT'])
def update_profile(user_id):
    data = request.get_json()
    db = get_db()
    
    update_fields = {
        "name": data.get('name'),
        "bio": data.get('bio'),
        "social_links": data.get('social_links'),
        "profile_picture": data.get('profile_picture'),
        "preferences": data.get('preferences')
    }
    
    # Remove None values
    update_fields = {k: v for k, v in update_fields.items() if v is not None}
    
    if update_fields:
        update_fields["last_active"] = datetime.utcnow()
        
        result = db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_fields}
        )
        
        if result.modified_count == 0:
            return jsonify({'error': 'Failed to update profile'}), 400
            
    return jsonify({'status': 'success', 'message': 'Profile updated successfully'}), 200

@users_bp.route('/change_password/<user_id>', methods=['POST'])
def change_password(user_id):
    data = request.get_json()
    required_fields = ['current_password', 'new_password']
    
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    db = get_db()
    user = db.users.find_one({"_id": ObjectId(user_id)})
    
    if not check_password_hash(user['password_hash'], data['current_password']):
        return jsonify({'error': 'Invalid current password'}), 400
    
    new_hash = generate_password_hash(data['new_password'])
    db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"password_hash": new_hash}}
    )
    
    return jsonify({'status': 'success', 'message': 'Password changed successfully'}), 200