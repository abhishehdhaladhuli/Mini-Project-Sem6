from flask import Blueprint, request, jsonify
from app.db import mongo

marketplace_bp = Blueprint('marketplace', __name__)

@marketplace_bp.route('/items', methods=['GET'])
def list_items():
    items = mongo.db.items.find()
    data = []
    for item in items:
        data.append({
            "id": str(item.get('_id')),
            "name": item.get('name'),
            "price": item.get('price'),
            "description": item.get('description')
        })
    return jsonify({"status": "success", "data": data}), 200

@marketplace_bp.route('/add', methods=['POST'])
def add_item():
    data = request.get_json()
    required_fields = ['name', 'price', 'description']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    result = mongo.db.items.insert_one(data)
    return jsonify({'status': 'success', 'id': str(result.inserted_id)}), 201
