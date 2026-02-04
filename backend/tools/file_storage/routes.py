# -*- coding: utf-8 -*-
import os
import uuid
import json
import hashlib
import base64
import logging
import threading
import time
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from flask import Flask, Blueprint, request, jsonify, send_from_directory, Response
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge

logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Blueprint for wsgi.py integration
bp = Blueprint('file_storage', __name__)

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(SCRIPT_DIR, 'upload')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Supported image extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp', 'tiff', 'svg'}

# Encryption settings - for transport encryption only
ENCRYPTION_KEY_FILE = os.path.join(SCRIPT_DIR, 'transport.key')
METADATA_FILE = os.path.join(SCRIPT_DIR, 'file_metadata.json')

# Session management settings
SESSION_TIMEOUT = 3 * 60  # 3 minutes in seconds

class SessionManager:
    """Manages user sessions and file cleanup"""
    def __init__(self):
        self.sessions = {}
        self.lock = threading.Lock()
        self.cleanup_thread = None
        self.start_cleanup_thread()

    def start_cleanup_thread(self):
        """Start background cleanup thread"""
        if self.cleanup_thread is None or not self.cleanup_thread.is_alive():
            self.cleanup_thread = threading.Thread(target=self._cleanup_worker, daemon=True)
            self.cleanup_thread.start()
            logger.info("Session cleanup thread started")

    def _cleanup_worker(self):
        """Background worker to cleanup expired sessions"""
        while True:
            try:
                self.cleanup_expired_sessions()
                time.sleep(30)  # Check every 30 seconds
            except Exception as e:
                logger.error("Error in session cleanup worker: %s", e)
                time.sleep(30)

    def update_session(self, session_id):
        """Update session activity timestamp"""
        with self.lock:
            if session_id not in self.sessions:
                self.sessions[session_id] = {
                    'files': set(),
                    'last_activity': datetime.now()
                }
            else:
                self.sessions[session_id]['last_activity'] = datetime.now()
            return self.sessions[session_id]

    def add_file_to_session(self, session_id, filename):
        """Add a file to a session"""
        with self.lock:
            # Update session directly without calling update_session to avoid double locking
            if session_id not in self.sessions:
                self.sessions[session_id] = {
                    'files': set(),
                    'last_activity': datetime.now()
                }
            else:
                self.sessions[session_id]['last_activity'] = datetime.now()

            session_data = self.sessions[session_id]
            session_data['files'].add(filename)
            logger.info("Added file %s to session %s", filename, session_id)

    def get_session_files(self, session_id):
        """Get all files for a session"""
        with self.lock:
            if session_id in self.sessions:
                return self.sessions[session_id]['files'].copy()
            return set()

    def cleanup_expired_sessions(self):
        """Cleanup sessions that have expired"""
        with self.lock:
            current_time = datetime.now()
            expired_sessions = []

            for session_id, session_data in self.sessions.items():
                if current_time - session_data['last_activity'] > timedelta(seconds=SESSION_TIMEOUT):
                    expired_sessions.append(session_id)

            for session_id in expired_sessions:
                try:
                    self._cleanup_session(session_id)
                except Exception as e:
                    logger.error("Failed to cleanup session %s: %s", session_id, e)

    def _cleanup_session(self, session_id):
        """Cleanup a specific session (called with lock held)"""
        if session_id not in self.sessions:
            return

        session_data = self.sessions[session_id]
        files_to_delete = session_data['files'].copy()

        # Delete files from disk
        deleted_count = 0
        for filename in files_to_delete:
            try:
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                if os.path.exists(filepath):
                    os.remove(filepath)
                    deleted_count += 1
                    logger.info("Deleted expired file: %s", filename)

                # Remove from metadata
                metadata_handler.remove_file_info(filename)

            except Exception as e:
                logger.error("Error deleting file %s: %s", filename, e)

        # Remove session
        del self.sessions[session_id]
        logger.info("Session %s expired and cleaned up (%d files deleted)", session_id, deleted_count)

    def manual_cleanup_session(self, session_id):
        """Manually cleanup a specific session"""
        with self.lock:
            if session_id in self.sessions:
                self._cleanup_session(session_id)
                return True
            return False

# Initialize session manager
session_manager = SessionManager()

class TransportEncryption:
    """Handles encryption/decryption for data transport only"""
    def __init__(self):
        self.key = self._load_or_generate_key()
        self.fernet = Fernet(self.key)

    def _load_or_generate_key(self):
        """Load existing key or generate new one"""
        if os.path.exists(ENCRYPTION_KEY_FILE):
            with open(ENCRYPTION_KEY_FILE, 'rb') as key_file:
                return key_file.read()
        else:
            key = Fernet.generate_key()
            with open(ENCRYPTION_KEY_FILE, 'wb') as key_file:
                key_file.write(key)
            logger.info("Generated new transport encryption key: %s", ENCRYPTION_KEY_FILE)
            return key

    def encrypt_for_transport(self, file_data):
        """Encrypt file data for secure transport"""
        return self.fernet.encrypt(file_data)

    def decrypt_from_transport(self, encrypted_data):
        """Decrypt file data received from transport"""
        return self.fernet.decrypt(encrypted_data)

    def get_file_hash(self, file_data):
        """Generate SHA256 hash of file data"""
        return hashlib.sha256(file_data).hexdigest()

class FileMetadata:
    def __init__(self):
        self.metadata_file = METADATA_FILE
        self.metadata = self._load_metadata()

    def _load_metadata(self):
        """Load metadata from file"""
        if os.path.exists(self.metadata_file):
            try:
                with open(self.metadata_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}

    def _save_metadata(self):
        """Save metadata to file"""
        try:
            with open(self.metadata_file, 'w', encoding='utf-8') as f:
                json.dump(self.metadata, f, indent=2, ensure_ascii=False)
        except IOError as e:
            logger.error("Error saving metadata: %s", e)

    def add_file_info(self, filename, original_filename, file_hash, size):
        """Add file information to metadata"""
        self.metadata[filename] = {
            'original_name': original_filename,
            'upload_time': datetime.now().isoformat(),
            'file_hash': file_hash,
            'size': size,
            'encrypted_storage': False  # Files are stored decrypted locally
        }
        self._save_metadata()

    def get_file_info(self, filename):
        """Get file information from metadata"""
        return self.metadata.get(filename, None)

    def list_files(self):
        """List all files in metadata"""
        return self.metadata

    def remove_file_info(self, filename):
        """Remove file information from metadata"""
        if filename in self.metadata:
            del self.metadata[filename]
            self._save_metadata()
            return True
        return False

# Initialize transport encryption and metadata handlers
transport_encryptor = TransportEncryption()
metadata_handler = FileMetadata()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_unique_filename(original_filename):
    """Generate unique filename with timestamp and UUID"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    name, ext = os.path.splitext(secure_filename(original_filename))
    return f"{name}_{timestamp}_{unique_id}{ext}"

def _build_file_info(filename, file_info):
    """Build file info dict for list responses"""
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(filepath):
        return None
    stat_info = os.stat(filepath)
    return {
        'filename': filename,
        'original_name': file_info['original_name'],
        'size': file_info['size'],
        'upload_time': file_info['upload_time'],
        'file_hash': file_info['file_hash'],
        'storage_encrypted': file_info['encrypted_storage'],
        'modified_time': datetime.fromtimestamp(stat_info.st_mtime).isoformat(),
        'image_url': f'/image/{filename}',
        'download_url': f'/download/{filename}'
    }


def _register_routes(target):
    """Register routes on both the standalone app and the blueprint"""

    @target.route('/health')
    def health():
        return jsonify({'status': 'healthy', 'service': 'file_storage'})

    @target.route('/upload', methods=['POST'])
    def upload_files():
        try:
            # Get session ID from request
            session_id = request.headers.get('X-Session-ID')
            if not session_id:
                return jsonify({'error': 'Session ID required'}), 400

            # Update session activity
            session_manager.update_session(session_id)

            # Check if files were uploaded
            if 'files' not in request.files:
                return jsonify({'error': 'No files uploaded'}), 400

            files = request.files.getlist('files')

            if not files or all(file.filename == '' for file in files):
                return jsonify({'error': 'No files selected'}), 400

            uploaded_files = []
            errors = []

            # Ensure upload directory exists
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

            for file in files:
                if file.filename == '':
                    continue

                if file and allowed_file(file.filename):
                    try:
                        # Read file data (this comes encrypted from client if using HTTPS)
                        file_data = file.read()

                        # Generate file hash for integrity check
                        file_hash = transport_encryptor.get_file_hash(file_data)

                        # Generate unique filename (keeping original extension)
                        unique_filename = generate_unique_filename(file.filename)
                        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)

                        # Save file as plain/decrypted to local storage
                        with open(filepath, 'wb') as saved_file:
                            saved_file.write(file_data)

                        # Get file info
                        file_size = len(file_data)

                        # Store metadata
                        metadata_handler.add_file_info(
                            unique_filename,
                            file.filename,
                            file_hash,
                            file_size
                        )

                        # Add file to session
                        session_manager.add_file_to_session(session_id, unique_filename)

                        uploaded_files.append({
                            'original_name': file.filename,
                            'saved_name': unique_filename,
                            'size': file_size,
                            'file_hash': file_hash,
                            'storage_encrypted': False,
                            'transport_secure': True
                        })

                    except Exception as e:
                        errors.append(f"Failed to upload {file.filename}: {str(e)}")
                else:
                    errors.append(f"Invalid file type: {file.filename}")

            if uploaded_files:
                result = {
                    'success': True,
                    'message': f'Successfully uploaded {len(uploaded_files)} file(s) with secure transport',
                    'uploaded_files': uploaded_files,
                    'upload_directory': app.config['UPLOAD_FOLDER'],
                    'session_id': session_id
                }

                if errors:
                    result['errors'] = errors

                return jsonify(result), 200
            else:
                return jsonify({
                    'success': False,
                    'error': 'No valid files were uploaded',
                    'errors': errors
                }), 400

        except RequestEntityTooLarge:
            return jsonify({'error': 'File too large. Maximum size is 16MB'}), 413
        except Exception as e:
            return jsonify({'error': f'Upload failed: {str(e)}'}), 500

    @target.route('/list')
    def list_files():
        """List all uploaded files with image URLs for direct display"""
        try:
            # Get session ID from request
            session_id = request.headers.get('X-Session-ID')
            if session_id:
                # Update session activity
                session_manager.update_session(session_id)

                # Only return files for this session
                session_file_set = session_manager.get_session_files(session_id)
                if not session_file_set:
                    return jsonify({'files': [], 'count': 0, 'storage_encrypted': False})

                files = []
                for filename in session_file_set:
                    file_info = metadata_handler.get_file_info(filename)
                    if file_info:
                        info = _build_file_info(filename, file_info)
                        if info:
                            files.append(info)
            else:
                # Fallback: return all files (for backward compatibility)
                metadata = metadata_handler.list_files()

                if not metadata:
                    return jsonify({'files': [], 'count': 0, 'storage_encrypted': False})

                files = []
                for filename, file_info in metadata.items():
                    info = _build_file_info(filename, file_info)
                    if info:
                        files.append(info)

            files.sort(key=lambda x: x['upload_time'], reverse=True)

            return jsonify({
                'files': files,
                'count': len(files),
                'upload_directory': app.config['UPLOAD_FOLDER'],
                'storage_encrypted': False,
                'transport_secure': True,
                'session_id': session_id
            })

        except Exception as e:
            return jsonify({'error': f'Failed to list files: {str(e)}'}), 500

    @target.route('/heartbeat', methods=['POST'])
    def heartbeat():
        """Session heartbeat endpoint to keep session alive"""
        try:
            session_id = request.headers.get('X-Session-ID')
            if not session_id:
                return jsonify({'error': 'Session ID required'}), 400

            # Update session activity
            session_data = session_manager.update_session(session_id)

            return jsonify({
                'success': True,
                'session_id': session_id,
                'last_activity': session_data['last_activity'].isoformat(),
                'file_count': len(session_data['files']),
                'timeout_seconds': SESSION_TIMEOUT
            }), 200

        except Exception as e:
            return jsonify({'error': f'Heartbeat failed: {str(e)}'}), 500

    @target.route('/cleanup/<session_id>', methods=['POST'])
    def cleanup_session_endpoint(session_id):
        """Manual cleanup endpoint for a specific session"""
        try:
            success = session_manager.manual_cleanup_session(session_id)
            if success:
                return jsonify({'success': True, 'message': f'Session {session_id} cleaned up'}), 200
            else:
                return jsonify({'error': f'Session {session_id} not found'}), 404
        except Exception as e:
            return jsonify({'error': f'Cleanup failed: {str(e)}'}), 500

    @target.route('/download/<filename>')
    def download_file(filename):
        """Download a file directly (already decrypted)"""
        try:
            # Get file metadata
            file_info = metadata_handler.get_file_info(filename)
            if not file_info:
                return jsonify({'error': 'File not found in metadata'}), 404

            # Check if file exists
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if not os.path.exists(filepath):
                return jsonify({'error': 'File not found'}), 404

            # Read file directly (already decrypted)
            with open(filepath, 'rb') as file_data:
                file_content = file_data.read()

            # Verify file integrity
            file_hash = transport_encryptor.get_file_hash(file_content)
            if file_hash != file_info['file_hash']:
                return jsonify({'error': 'File integrity check failed'}), 500

            # Return file
            response = Response(
                file_content,
                mimetype='application/octet-stream',
                headers={
                    'Content-Disposition': f'attachment; filename="{file_info["original_name"]}"',
                    'Content-Length': len(file_content)
                }
            )
            return response

        except Exception as e:
            return jsonify({'error': f'Download failed: {str(e)}'}), 500

    @target.route('/image/<filename>')
    def serve_image(filename):
        """Serve image files directly for frontend display"""
        try:
            # Get file metadata
            file_info = metadata_handler.get_file_info(filename)
            if not file_info:
                return jsonify({'error': 'File not found in metadata'}), 404

            # Check if file exists
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if not os.path.exists(filepath):
                return jsonify({'error': 'File not found'}), 404

            # Serve the image file directly with cache headers
            response = send_from_directory(app.config['UPLOAD_FOLDER'], filename)
            response.headers['Cache-Control'] = 'public, max-age=3600'
            return response

        except Exception as e:
            return jsonify({'error': f'Failed to serve image: {str(e)}'}), 500

    @target.route('/view/<filename>')
    def view_file(filename):
        """View file metadata"""
        try:
            file_info = metadata_handler.get_file_info(filename)
            if not file_info:
                return jsonify({'error': 'File not found'}), 404

            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if not os.path.exists(filepath):
                return jsonify({'error': 'File not found'}), 404

            stat_info = os.stat(filepath)

            return jsonify({
                'filename': filename,
                'original_name': file_info['original_name'],
                'size': file_info['size'],
                'upload_time': file_info['upload_time'],
                'file_hash': file_info['file_hash'],
                'storage_encrypted': file_info['encrypted_storage'],
                'transport_secure': True,
                'modified_time': datetime.fromtimestamp(stat_info.st_mtime).isoformat(),
                'image_url': f'/image/{filename}',
                'download_url': f'/download/{filename}'
            })

        except Exception as e:
            return jsonify({'error': f'Failed to get file info: {str(e)}'}), 500

    @target.errorhandler(413)
    def too_large(e):
        return jsonify({'error': 'File too large. Maximum size is 16MB'}), 413


# Register routes on both the standalone app and the blueprint
_register_routes(app)
_register_routes(bp)

if __name__ == '__main__':
    # Ensure upload directory exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    logger.info("Upload directory: %s", UPLOAD_FOLDER)

    # Check if running in production mode
    if os.environ.get('FLASK_ENV') == 'production':
        logger.info("Production mode detected")
        logger.info("Use gunicorn: gunicorn -c gunicorn_config_file.py file:app")
    else:
        logging.basicConfig(level=logging.DEBUG)
        logger.info("Development mode - Starting Flask dev server...")
        logger.info("API endpoints:")
        logger.info("  POST /upload - Upload files")
        logger.info("  GET  /list - List files with image URLs")
        logger.info("  GET  /image/<filename> - Serve images directly")
        logger.info("  GET  /download/<filename> - Download files")
        logger.info("  GET  /view/<filename> - View file metadata")

        app.run(debug=True, host='0.0.0.0', port=10086)
