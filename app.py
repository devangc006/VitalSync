"""
Personal Health & Environmental Wellness Recommendation System
Main Application Entry Point

Connects all route blueprints, initializes database, and configures sessions.
"""

import os
from flask import Flask, render_template, redirect, url_for
from config import config_by_name
from database.db_connection import init_db

# Import route blueprints
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.profile import profile_bp
from routes.weather import weather_bp
from routes.recommendation import recommendation_bp
from routes.history import history_bp
from routes.settings import settings_bp


def create_app(config_name='development'):
    """Application factory pattern."""
    app = Flask(__name__)
    app.config.from_object(config_by_name.get(config_name, config_by_name['development']))
    
    # Initialize database tables on first run
    with app.app_context():
        init_db()
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(weather_bp)
    app.register_blueprint(recommendation_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(settings_bp)
    
    # Landing page route
    @app.route('/')
    def landing():
        return render_template('index.html')
    
    # Custom error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('base.html', error_code=404, error_message='Page Not Found'), 404
    
    @app.errorhandler(500)
    def internal_error(e):
        return render_template('base.html', error_code=500, error_message='Internal Server Error'), 500
    
    return app


# Run the application
if __name__ == '__main__':
    env = os.environ.get('FLASK_ENV', 'development')
    app = create_app(env)
    app.run(host='0.0.0.0', port=5000, debug=True)
