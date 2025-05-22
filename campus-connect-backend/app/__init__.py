# app/__init__.py

from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Configure MongoDB connection
    app.config["MONGO_URI"] = os.getenv('MONGO_URI')
    
    # Initialize MongoDB
    from .db import mongo
    mongo.init_app(app)
    
    # Enable CORS for all routes
    CORS(app)
    
    # Register blueprints
    from .routes.users import users_bp
    from .routes.doubts import doubts_bp
    from .routes.notes import notes_bp
    from .routes.calendar import calendar_bp
    from .routes.feedback import feedback_bp
    from .routes.ai_tools import ai_tools_bp
    from .routes.marketplace import marketplace_bp
    from .routes.internships import internships_bp
    from .routes.study_groups import study_groups_bp
    
    app.register_blueprint(users_bp)
    app.register_blueprint(doubts_bp)
    app.register_blueprint(notes_bp)
    app.register_blueprint(calendar_bp)
    app.register_blueprint(feedback_bp)
    app.register_blueprint(ai_tools_bp)
    app.register_blueprint(marketplace_bp)
    app.register_blueprint(internships_bp)
    app.register_blueprint(study_groups_bp)
    
    # Root endpoint
    @app.route('/')
    def index():
        return jsonify({
            'message': 'Welcome to CampusConnect API',
            'version': '1.0.0',
            'endpoints': {
                'users': '/users/register',
                'doubts': '/doubts/questions',
                'notes': '/notes',
                'calendar': '/calendar',
                'feedback': '/feedback',
                'ai_tools': '/ai_tools/recommendations',
                'marketplace': '/marketplace/items',
                'internships': '/internships/list',
                'study_groups': '/study_groups/list'
            }
        })
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': 'Not Found',
            'message': 'The requested URL was not found on the server.'
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An internal server error occurred.'
        }), 500
    
    return app