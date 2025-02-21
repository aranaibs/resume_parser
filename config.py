import os
import torch

class Config:
    # Basic Flask Config
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-change-in-production'
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cache')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}
    
    # Model Configuration
    MODEL_PATH = os.environ.get('MODEL_PATH') or "google/flan-t5-small"  # Example model
    BATCH_SIZE = 4
    MAX_LENGTH = 512
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    
    # Processing Configuration
    CACHE_TIMEOUT = 3600  # 1 hour
    ENABLE_ASYNC_PROCESSING = True