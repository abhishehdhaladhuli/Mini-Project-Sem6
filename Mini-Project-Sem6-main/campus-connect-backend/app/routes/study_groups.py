from flask import Blueprint, request, jsonify
from app.db import mongo

study_groups_bp = Blueprint('study_groups', __name__)

@study_groups_bp.route('/list', methods=['GET'])
def list_study_groups():
    study_groups = mongo.db.study_groups.find()
    data = []
    for group in study_groups:
        data.append({
            "id": str(group.get('_id')),
            "name": group.get('name'),
            "subject": group.get('subject'),
            "members": group.get('members'),
            "description": group.get('description')
        })
    return jsonify({"status": "success", "data": data}), 200

@study_groups_bp.route('/add', methods=['POST'])
def add_study_group():
    data = request.get_json()
    required_fields = ['name', 'subject', 'members', 'description']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    result = mongo.db.study_groups.insert_one(data)
    return jsonify({'status': 'success', 'id': str(result.inserted_id)}), 201
