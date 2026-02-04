# -*- coding: utf-8 -*-
import os
import uuid
import logging
import base64
import threading
import time
from datetime import datetime, timedelta
from flask import Flask, Blueprint, request, jsonify, send_from_directory, Response
from flask_cors import CORS

logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB

# Setup Debug Logging
debug_log_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs', 'gemini_debug.log')
os.makedirs(os.path.dirname(debug_log_path), exist_ok=True)
file_handler = logging.FileHandler(debug_log_path)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)

bp = Blueprint('img_gen', __name__)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
GENERATED_FOLDER = os.path.join(SCRIPT_DIR, 'generated')
UPLOAD_FOLDER = os.path.join(os.path.dirname(SCRIPT_DIR), 'file_storage', 'upload')

os.makedirs(GENERATED_FOLDER, exist_ok=True)

SESSION_TIMEOUT = 3 * 60

class SessionManager:
    def __init__(self):
        self.sessions = {}
        self.lock = threading.Lock()
        self.cleanup_thread = None
        self.start_cleanup_thread()

    def start_cleanup_thread(self):
        if self.cleanup_thread is None or not self.cleanup_thread.is_alive():
            self.cleanup_thread = threading.Thread(target=self._cleanup_worker, daemon=True)
            self.cleanup_thread.start()

    def _cleanup_worker(self):
        while True:
            try:
                self.cleanup_expired_sessions()
                time.sleep(30)
            except Exception as e:
                logger.error("Cleanup worker error: %s", e)
                time.sleep(30)

    def update_session(self, session_id):
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
        with self.lock:
            if session_id not in self.sessions:
                self.sessions[session_id] = {
                    'files': set(),
                    'last_activity': datetime.now()
                }
            self.sessions[session_id]['files'].add(filename)

    def get_session_files(self, session_id):
        with self.lock:
            if session_id in self.sessions:
                return self.sessions[session_id]['files'].copy()
            return set()

    def cleanup_expired_sessions(self):
        with self.lock:
            current_time = datetime.now()
            expired = [sid for sid, data in self.sessions.items()
                      if current_time - data['last_activity'] > timedelta(seconds=SESSION_TIMEOUT)]
            for sid in expired:
                self._cleanup_session(sid)

    def _cleanup_session(self, session_id):
        if session_id not in self.sessions:
            return
        for filename in self.sessions[session_id]['files'].copy():
            try:
                filepath = os.path.join(GENERATED_FOLDER, filename)
                if os.path.exists(filepath):
                    os.remove(filepath)
                    logger.info("Deleted expired file: %s", filename)
            except Exception as e:
                logger.error("Error deleting %s: %s", filename, e)
        del self.sessions[session_id]

    def manual_cleanup(self, session_id):
        with self.lock:
            if session_id in self.sessions:
                self._cleanup_session(session_id)
                return True
            return False

session_manager = SessionManager()


def get_gemini_client():
    """Initialize Gemini client"""
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        raise ValueError("GEMINI_API_KEY not set")

    from google import genai
    client = genai.Client(api_key=api_key)
    return client


def _register_routes(target):

    @target.route('/health')
    def health():
        return jsonify({'status': 'healthy', 'service': 'img_gen'})

    @target.route('/generate', methods=['POST'])
    def generate():
        try:
            session_id = request.headers.get('X-Session-ID')
            if not session_id:
                return jsonify({'error': 'Session ID required'}), 400

            session_manager.update_session(session_id)

            data = request.get_json()
            if not data:
                return jsonify({'error': 'No data provided'}), 400

            prompt = data.get('prompt', '').strip()
            if not prompt:
                return jsonify({'error': 'Prompt is required'}), 400

            input_images = data.get('images')
            if input_images is None:
                input_images = []
            
            logger.info(f"Processing generation request. Prompt: {prompt[:50]}..., Images: {len(input_images)}")

            client = get_gemini_client()
            from google.genai import types

            # Prepare contents for Gemini
            contents = [prompt]

            # Add input images if provided
            for img_filename in input_images:
                img_path = os.path.join(UPLOAD_FOLDER, img_filename)
                if os.path.exists(img_path):
                    with open(img_path, 'rb') as f:
                        img_data = f.read()
                    # Detect mime type
                    ext = os.path.splitext(img_filename)[1].lower()
                    mime_map = {'.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
                               '.gif': 'image/gif', '.webp': 'image/webp'}
                    mime_type = mime_map.get(ext, 'image/png')
                    contents.append(types.Part.from_bytes(data=img_data, mime_type=mime_type))

            # Call Gemini API for image generation (using latest model)
            try:
                response = client.models.generate_content(
                    model='gemini-3-pro-image-preview',
                    contents=contents,
                    config=types.GenerateContentConfig(
                        response_modalities=['IMAGE']
                    )
                )
                logger.info(f"Gemini Response Candidates: {response.candidates}")
                if response.candidates:
                     logger.info(f"First Candidate Content: {response.candidates[0].content}")
            except Exception as api_error:
                logger.error(f"Gemini API Error: {api_error}")
                raise api_error

            generated_images = []

            # Process response
            if response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
                for part in response.candidates[0].content.parts:
                    if part.inline_data is not None:
                        # Save generated image
                        img_data = part.inline_data.data
                        mime_type = part.inline_data.mime_type or 'image/png'

                        ext = '.png'
                        if 'jpeg' in mime_type:
                            ext = '.jpg'
                        elif 'webp' in mime_type:
                            ext = '.webp'

                        filename = f"gen_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}{ext}"
                        filepath = os.path.join(GENERATED_FOLDER, filename)

                        with open(filepath, 'wb') as f:
                            f.write(img_data)

                        session_manager.add_file_to_session(session_id, filename)
                        generated_images.append({'filename': filename})
                        logger.info("Generated image: %s", filename)

            if generated_images:
                return jsonify({
                    'success': True,
                    'generated_images': generated_images,
                    'message': f'Generated {len(generated_images)} image(s)'
                })
            else:
                # No images generated, return detailed info
                candidate = response.candidates[0] if response.candidates else None
                finish_reason = candidate.finish_reason.name if candidate and candidate.finish_reason else "UNKNOWN"
                
                text_response = ""
                if candidate and candidate.content and candidate.content.parts:
                    for part in candidate.content.parts:
                        if part.text:
                            text_response += part.text

                logger.warning(f"No images generated. Finish reason: {finish_reason}")
                
                return jsonify({
                    'success': False,  # Mark as false if no images
                    'generated_images': [],
                    'text_response': text_response,
                    'finish_reason': finish_reason,
                    'message': f'No images generated. Reason: {finish_reason}. {text_response[:100]}'
                })

        except Exception as e:
            logger.error("Generation failed: %s", e)
            return jsonify({'error': str(e)}), 500

    @target.route('/image/<filename>')
    def serve_image(filename):
        try:
            # Get session ID from query param or header
            session_id = request.args.get('session_id') or request.headers.get('X-Session-ID')
            if not session_id:
                return jsonify({'error': 'Unauthorized: Session ID required for access'}), 403

            # Check if file belongs to session
            allowed_files = session_manager.get_session_files(session_id)
            if filename not in allowed_files:
                return jsonify({'error': 'Forbidden: Access denied to this file'}), 403

            filepath = os.path.join(GENERATED_FOLDER, filename)
            if not os.path.exists(filepath):
                return jsonify({'error': 'File not found'}), 404

            response = send_from_directory(GENERATED_FOLDER, filename)
            response.headers['Cache-Control'] = 'private, max-age=3600'
            return response
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @target.route('/download/<filename>')
    def download(filename):
        try:
            # Get session ID from query param or header
            session_id = request.args.get('session_id') or request.headers.get('X-Session-ID')
            if not session_id:
                return jsonify({'error': 'Unauthorized: Session ID required for access'}), 403

            # Check if file belongs to session
            allowed_files = session_manager.get_session_files(session_id)
            if filename not in allowed_files:
                return jsonify({'error': 'Forbidden: Access denied to this file'}), 403

            filepath = os.path.join(GENERATED_FOLDER, filename)
            if not os.path.exists(filepath):
                return jsonify({'error': 'File not found'}), 404

            with open(filepath, 'rb') as f:
                content = f.read()

            return Response(
                content,
                mimetype='application/octet-stream',
                headers={'Content-Disposition': f'attachment; filename="{filename}"'}
            )
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @target.route('/list_generated')
    def list_generated():
        try:
            session_id = request.headers.get('X-Session-ID')
            if session_id:
                session_manager.update_session(session_id)
                files = session_manager.get_session_files(session_id)
            else:
                files = set(os.listdir(GENERATED_FOLDER)) if os.path.exists(GENERATED_FOLDER) else set()

            result = []
            for filename in files:
                filepath = os.path.join(GENERATED_FOLDER, filename)
                if os.path.exists(filepath):
                    stat = os.stat(filepath)
                    result.append({
                        'filename': filename,
                        'size': stat.st_size,
                        'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                        'url': f'/image/{filename}'
                    })

            result.sort(key=lambda x: x['created'], reverse=True)
            return jsonify({'files': result, 'count': len(result)})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @target.route('/heartbeat', methods=['POST'])
    def heartbeat():
        try:
            session_id = request.headers.get('X-Session-ID')
            if not session_id:
                return jsonify({'error': 'Session ID required'}), 400

            session_data = session_manager.update_session(session_id)
            return jsonify({
                'success': True,
                'session_id': session_id,
                'file_count': len(session_data['files'])
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @target.route('/cleanup/<session_id>', methods=['POST'])
    def cleanup(session_id):
        try:
            if session_manager.manual_cleanup(session_id):
                return jsonify({'success': True})
            return jsonify({'error': 'Session not found'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500


_register_routes(app)
_register_routes(bp)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logger.info("Starting AI Image Generation Service on port 8088")
    app.run(debug=True, host='0.0.0.0', port=8088)
