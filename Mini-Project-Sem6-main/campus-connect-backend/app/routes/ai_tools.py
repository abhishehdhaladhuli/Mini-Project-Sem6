from flask import Blueprint, request, jsonify

ai_tools_bp = Blueprint('ai_tools', __name__)

@ai_tools_bp.route('/recommendations', methods=['POST'])
def get_recommendations():
    data = request.get_json()
    user_input = data.get('user_input', '').strip()
    
    if not user_input:
        return jsonify({'error': 'Missing user_input in request body'}), 400
    
    # Example: Generate personalized recommendations based on user input
    recommendations = [
        {"id": 101, "title": "Custom Study Group", "description": f"Based on your interest in '{user_input}', join this study group."},
        {"id": 102, "title": "Personalized Resources", "description": f"Resources tailored for your focus area: {user_input}."}
    ]
    
    return jsonify({"status": "success", "data": recommendations}), 200
