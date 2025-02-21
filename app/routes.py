from flask import Blueprint, render_template, jsonify, request
from werkzeug.utils import secure_filename
import os

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Render the upload page."""
    return render_template('upload.html')

@main_bp.route('/health')
def health_check():
    """Basic health check endpoint."""
    return jsonify({'status': 'healthy'})

@main_bp.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        return jsonify({'message': 'File uploaded successfully'})
    
    return jsonify({'error': 'Invalid file type'}), 400

def allowed_file(filename):
    """Check if the file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'pdf', 'doc', 'docx'}