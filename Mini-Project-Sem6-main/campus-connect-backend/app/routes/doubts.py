from flask import Blueprint, request, jsonify
from app.db import mongo
from datetime import datetime
from bson import ObjectId

doubts_bp = Blueprint('doubts', __name__)

@doubts_bp.route('/questions', methods=['POST'])
def post_question():
    data = request.get_json()
    required_fields = ['title', 'content', 'subject']
    
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    question = {
        "title": data['title'],
        "content": data['content'],
        "subject": data['subject'],
        "tags": data.get('tags', []),
        "created_at": datetime.utcnow(),
        "answers": [],
        "upvotes": 0,
        "downvotes": 0
    }
    
    result = mongo.db.questions.insert_one(question)
    return jsonify({'status': 'success', 'id': str(result.inserted_id)}), 201

@doubts_bp.route('/questions', methods=['GET'])
def list_questions():
    questions = mongo.db.questions.find()
    data = []
    for q in questions:
        data.append({
            "id": str(q['_id']),
            "title": q['title'],
            "subject": q['subject'],
            "created_at": q['created_at'].isoformat(),
            "upvotes": q['upvotes'],
            "downvotes": q['downvotes'],
            "answers_count": len(q.get('answers', []))
        })
    return jsonify({"status": "success", "data": data}), 200

@doubts_bp.route('/questions/<question_id>', methods=['GET'])
def get_question(question_id):
    question = mongo.db.questions.find_one({"_id": ObjectId(question_id)})
    
    if not question:
        return jsonify({'error': 'Question not found'}), 404
    
    return jsonify({
        "status": "success",
        "data": {
            "id": str(question['_id']),
            "title": question['title'],
            "content": question['content'],
            "subject": question['subject'],
            "tags": question['tags'],
            "created_at": question['created_at'].isoformat(),
            "answers": question['answers'],
            "upvotes": question['upvotes'],
            "downvotes": question['downvotes']
        }
    }), 200

@doubts_bp.route('/questions/<question_id>/answers', methods=['POST'])
def post_answer(question_id):
    question = mongo.db.questions.find_one({"_id": ObjectId(question_id)})
    
    if not question:
        return jsonify({'error': 'Question not found'}), 404
    
    data = request.get_json()
    required_fields = ['content']
    
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    answer = {
        "content": data['content'],
        "created_at": datetime.utcnow(),
        "upvotes": 0,
        "downvotes": 0
    }
    
    mongo.db.questions.update_one(
        {"_id": ObjectId(question_id)},
        {"$push": {"answers": answer}}
    )
    
    return jsonify({'status': 'success', 'message': 'Answer posted successfully'}), 201
