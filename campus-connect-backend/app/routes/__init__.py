# app/routes/__init__.py

from flask import Blueprint
from .calendar import calendar_bp
from .doubts import doubts_bp
from .feedback import feedback_bp
from .notes import notes_bp
from .users import users_bp

def register_routes(app):
    """Register all routes with the Flask app"""
    app.register_blueprint(calendar_bp, url_prefix='/calendar')
    app.register_blueprint(doubts_bp, url_prefix='/doubts')
    app.register_blueprint(feedback_bp, url_prefix='/feedback')
    app.register_blueprint(notes_bp, url_prefix='/notes')
    app.register_blueprint(users_bp, url_prefix='/users')

    # Enable CORS for all routes
    from flask_cors import CORS
    CORS(app, resources={r"/*": {"origins": "*"}})
