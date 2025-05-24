# app/routes/study_groups.py

from flask import Blueprint, request, jsonify

study_groups_bp = Blueprint('study_groups', __name__)

@study_groups_bp.route('/list', methods=['GET'])
def list_study_groups():
    # Placeholder for study group listings
    study_groups = [
        {"id": 1, "name": "Math Study Group", "subject": "Mathematics", "members": 5, "description": "Join us to solve math problems together."},
        {"id": 2, "name": "Programming Club", "subject": "Computer Science", "members": 8, "description": "Learn programming languages and algorithms."}
    ]
    return jsonify({"status": "success", "data": study_groups}), 200
