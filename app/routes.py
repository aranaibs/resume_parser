from flask import Blueprint, render_template, jsonify, request, current_app
from werkzeug.utils import secure_filename
import os
from app.services.document_parser import DocumentParser
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

main_bp = Blueprint('main', __name__)
document_parser = DocumentParser(None)  # Initialize with None, we'll set it properly later

@main_bp.before_app_request  # Changed from before_app_first_request
def initialize_services():
    global document_parser
    if document_parser.upload_folder is None:  # Only initialize if not already set
        document_parser.upload_folder = current_app.config['UPLOAD_FOLDER']

@main_bp.route('/')
def index():
    """Render the upload page."""
    logger.info("Attempting to render upload.html")
    try:
        return render_template('upload.html')
    except Exception as e:
        logger.error(f"Error rendering template: {str(e)}")
        return str(e), 500

@main_bp.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and parsing."""
    try:
        if 'file' not in request.files:
            logger.error("No file in request")
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            logger.error("Empty filename")
            return jsonify({'error': 'No selected file'}), 400
        
        if not allowed_file(file.filename):
            logger.error(f"Invalid file type: {file.filename}")
            return jsonify({'error': 'Invalid file type'}), 400
        
        # Parse the document
        result = document_parser.save_and_parse(file)
        logger.info(f"Successfully processed file: {file.filename}")
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error processing upload: {str(e)}")
        return jsonify({'error': str(e)}), 500

def allowed_file(filename):
    """Check if the file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']