from flask import Blueprint
from .calendar import calendar_bp
from .doubts import doubts_bp
from .feedback import feedback_bp
from .notes import notes_bp
from .users import users_bp
from .ai_tools import ai_tools_bp
from .marketplace import marketplace_bp
from .internships import internships_bp
from .study_groups import study_groups_bp

def register_routes(app):
    """Register all routes with the Flask app"""
    app.register_blueprint(calendar_bp, url_prefix='/calendar')
    app.register_blueprint(doubts_bp, url_prefix='/doubts')
    app.register_blueprint(feedback_bp, url_prefix='/feedback')
    app.register_blueprint(notes_bp, url_prefix='/notes')
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(ai_tools_bp, url_prefix='/ai_tools')
    app.register_blueprint(marketplace_bp, url_prefix='/marketplace')
    app.register_blueprint(internships_bp, url_prefix='/internships')
    app.register_blueprint(study_groups_bp, url_prefix='/study_groups')
