from abc import ABC, abstractmethod
import fitz  # PyMuPDF
from docx import Document
import textract
import os
from werkzeug.utils import secure_filename
from typing import Dict, Optional
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseDocumentParser(ABC):
    """Abstract base class for document parsers."""
    
    @abstractmethod
    def parse(self, file_path: str) -> str:
        """Parse document and return text content."""
        pass

class PDFParser(BaseDocumentParser):
    """Parser for PDF documents."""
    
    def parse(self, file_path: str) -> str:
        try:
            doc = fitz.open(file_path)
            text = []
            for page in doc:
                text.append(page.get_text())
            return '\n'.join(text)
        except Exception as e:
            logger.error(f"Error parsing PDF {file_path}: {str(e)}")
            raise
        finally:
            if 'doc' in locals():
                doc.close()

class DOCXParser(BaseDocumentParser):
    """Parser for DOCX documents."""
    
    def parse(self, file_path: str) -> str:
        try:
            doc = Document(file_path)
            return '\n'.join([paragraph.text for paragraph in doc.paragraphs])
        except Exception as e:
            logger.error(f"Error parsing DOCX {file_path}: {str(e)}")
            raise

class DOCParser(BaseDocumentParser):
    """Parser for legacy DOC documents."""
    
    def parse(self, file_path: str) -> str:
        try:
            return textract.process(file_path).decode('utf-8')
        except Exception as e:
            logger.error(f"Error parsing DOC {file_path}: {str(e)}")
            raise

class DocumentParser:
    """Main document parser class that handles different document types."""
    
    def __init__(self, upload_folder: str):
        self.upload_folder = upload_folder
        self._parsers = {
            'pdf': PDFParser(),
            'docx': DOCXParser(),
            'doc': DOCParser()
        }

    def save_and_parse(self, file) -> Dict[str, str]:
        """Save uploaded file and parse its content."""
        try:
            # Secure the filename and save the file
            filename = secure_filename(file.filename)
            filepath = os.path.join(self.upload_folder, filename)
            file.save(filepath)
            
            # Parse the document
            parsed_text = self.parse_document(filepath)
            
            # Basic text cleaning
            cleaned_text = self._clean_text(parsed_text)
            
            return {
                'status': 'success',
                'text': cleaned_text,
                'filename': filename
            }
            
        except Exception as e:
            logger.error(f"Error processing file {file.filename}: {str(e)}")
            return {
                'status': 'error',
                'message': str(e),
                'filename': file.filename if file else None
            }
            
        finally:
            # Cleanup temporary file
            if 'filepath' in locals() and os.path.exists(filepath):
                os.remove(filepath)

    def parse_document(self, filepath: str) -> str:
        """Parse document based on file extension."""
        ext = filepath.split('.')[-1].lower()
        
        if ext not in self._parsers:
            raise ValueError(f"Unsupported file format: {ext}")
            
        return self._parsers[ext].parse(filepath)

    def _clean_text(self, text: str) -> str:
        """Clean extracted text."""
        if not text:
            return ""
            
        # Basic cleaning operations
        cleaned = text.replace('\r', '\n')  # Normalize line endings
        cleaned = '\n'.join(line.strip() for line in cleaned.split('\n'))  # Remove extra whitespace
        cleaned = '\n'.join(filter(None, cleaned.split('\n')))  # Remove empty lines
        
        return cleaned

    def cleanup_file(self, filename: str) -> None:
        """Remove processed file."""
        filepath = os.path.join(self.upload_folder, filename)
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
            except Exception as e:
                logger.error(f"Error cleaning up file {filepath}: {str(e)}")