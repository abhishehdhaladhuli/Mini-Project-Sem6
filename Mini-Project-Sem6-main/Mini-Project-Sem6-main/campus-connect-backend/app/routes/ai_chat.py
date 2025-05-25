from flask import Blueprint, request, jsonify
from app.db import mongo
from datetime import datetime
from bson import ObjectId
import os
import requests

chat_bp = Blueprint('chat', __name__)
print("ai_chat.py loaded")

# Load Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
print("Gemini API Key Loaded:", GEMINI_API_KEY)

# Create a new chat room
@chat_bp.route('/chat_rooms', methods=['POST'])
def create_chat_room():
    data = request.get_json() or {}
    room_name = data.get('name', 'Default Chat Room')
    room = {
        "name": room_name,
        "messages": [],
        "created_at": datetime.utcnow()
    }
    result = mongo.db.chat_rooms.insert_one(room)
    return jsonify({"status": "success", "chat_room_id": str(result.inserted_id)}), 201

# List all chat rooms
@chat_bp.route('/chat_rooms', methods=['GET'])
def list_chat_rooms():
    rooms = mongo.db.chat_rooms.find()
    data = [{
        "id": str(room['_id']),
        "name": room['name'],
        "created_at": room['created_at'].isoformat()
    } for room in rooms]
    return jsonify({"status": "success", "data": data}), 200

# Post a message to a chat room and get a response from Gemini
@chat_bp.route('/chat_rooms/<room_id>/messages', methods=['POST'])
def post_message(room_id):
    data = request.get_json() or {}
    user_text = data.get("text", "").strip()

    if not user_text:
        return jsonify({"error": "Message text is required"}), 400

    # Find chat room
    try:
        room = mongo.db.chat_rooms.find_one({"_id": ObjectId(room_id)})
    except Exception:
        return jsonify({"error": "Invalid chat room ID format"}), 400

    if not room:
        return jsonify({"error": "Chat room not found"}), 404

    # Add user message
    user_message = {
        "sender": "user",
        "text": user_text,
        "timestamp": datetime.utcnow()
    }
    mongo.db.chat_rooms.update_one(
        {"_id": ObjectId(room_id)},
        {"$push": {"messages": user_message}}
    )

    # Call Gemini API
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": user_text}
                ]
            }
        ]
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(GEMINI_API_URL, json=payload, headers=headers)

    if response.status_code != 200:
        return jsonify({"error": "Failed to get response from Gemini API", "details": response.text}), response.status_code

    res_json = response.json()
    try:
        generated_text = res_json["candidates"][0]["content"]
    except (KeyError, IndexError):
        generated_text = "No response generated."

    # Add AI response
    ai_message = {
        "sender": "ai",
        "text": generated_text,
        "timestamp": datetime.utcnow()
    }
    mongo.db.chat_rooms.update_one(
        {"_id": ObjectId(room_id)},
        {"$push": {"messages": ai_message}}
    )

    return jsonify({"status": "success", "response": generated_text}), 200
