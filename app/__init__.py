from flask import Flask
from config import Config  # Changed from relative to absolute import
import os

def create_app(config_class=Config):
    """Create and configure the Flask application."""
    # Initialize Flask app
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config_class)
    
    # Ensure required directories exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Register blueprints
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    return app