from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

from .db import mongo
from .routes import register_routes

def create_app():
    app = Flask(__name__)
    
    # Load MongoDB URI from .env
    app.config["MONGO_URI"] = os.getenv('MONGO_URI')
    print("MONGO_URI loaded:", app.config["MONGO_URI"])  # Debug
    
    # Initialize MongoDB
    mongo.init_app(app)
    
    with app.app_context():
        print("Mongo DB collections:", mongo.db.list_collection_names())
    
    # Enable CORS
    CORS(app)
    
    # Register all routes centrally
    register_routes(app)
    
    # Root API endpoint
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
        return jsonify({'error': 'Not Found', 'message': 'The requested URL was not found.'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal Server Error', 'message': 'An internal error occurred.'}), 500
    
    return app
