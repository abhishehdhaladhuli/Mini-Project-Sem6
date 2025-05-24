from flask import Blueprint, request, jsonify
from app.db import mongo

internships_bp = Blueprint('internships', __name__)

@internships_bp.route('/list', methods=['GET'])
def list_internships():
    internships = mongo.db.internships.find()
    data = []
    for internship in internships:
        data.append({
            "id": str(internship.get('_id')),
            "title": internship.get('title'),
            "company": internship.get('company'),
            "location": internship.get('location'),
            "description": internship.get('description')
        })
    return jsonify({"status": "success", "data": data}), 200

@internships_bp.route('/add', methods=['POST'])
def add_internship():
    data = request.get_json()
    required_fields = ['title', 'company', 'location', 'description']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    result = mongo.db.internships.insert_one(data)
    return jsonify({'status': 'success', 'id': str(result.inserted_id)}), 201
