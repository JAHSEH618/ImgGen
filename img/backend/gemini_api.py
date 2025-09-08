# -*- coding: utf-8 -*-
import datetime
import mimetypes
import os
import glob
import shutil
import base64
import atexit
import uuid
import threading
import time
import signal
from datetime import timedelta
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from google import genai
from google.genai import types
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max total

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(SCRIPT_DIR, 'upload')
GENERATED_FOLDER = os.path.join(SCRIPT_DIR, 'generated')

# Create folders if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(GENERATED_FOLDER, exist_ok=True)

# Gemini API configuration - Client will automatically get API key from GEMINI_API_KEY environment variable
MODEL_NAME = "gemini-2.5-flash-image-preview"

SUPPORTED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'webp'}

# Session management settings
SESSION_TIMEOUT = 3 * 60  # 3 minutes in seconds
session_files = {}  # session_id -> {'files': set(), 'last_activity': datetime}
session_lock = threading.Lock()

class SessionManager:
    """Manages user sessions and generated file cleanup"""
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
            print("AI Session cleanup thread started")
    
    def _cleanup_worker(self):
        """Background worker to cleanup expired sessions"""
        while True:
            try:
                self.cleanup_expired_sessions()
                time.sleep(30)  # Check every 30 seconds
            except Exception as e:
                print(f"Error in AI session cleanup worker: {e}")
                time.sleep(30)
    
    def update_session(self, session_id):
        """Update session activity timestamp"""
        with self.lock:
            if session_id not in self.sessions:
                self.sessions[session_id] = {
                    'files': set(),
                    'last_activity': datetime.datetime.now()
                }
            else:
                self.sessions[session_id]['last_activity'] = datetime.datetime.now()
            return self.sessions[session_id]
    
    def add_file_to_session(self, session_id, filename):
        """Add a generated file to a session"""
        with self.lock:
            # Update session directly without calling update_session to avoid double locking
            if session_id not in self.sessions:
                self.sessions[session_id] = {
                    'files': set(),
                    'last_activity': datetime.datetime.now()
                }
            else:
                self.sessions[session_id]['last_activity'] = datetime.datetime.now()
            
            session_data = self.sessions[session_id]
            session_data['files'].add(filename)
            print(f"Added generated file {filename} to session {session_id}")
    
    def get_session_files(self, session_id):
        """Get all generated files for a session"""
        with self.lock:
            if session_id in self.sessions:
                return self.sessions[session_id]['files'].copy()
            return set()
    
    def cleanup_expired_sessions(self):
        """Cleanup sessions that have expired"""
        with self.lock:
            current_time = datetime.datetime.now()
            expired_sessions = []
            
            for session_id, session_data in self.sessions.items():
                if current_time - session_data['last_activity'] > timedelta(seconds=SESSION_TIMEOUT):
                    expired_sessions.append(session_id)
            
            for session_id in expired_sessions:
                self._cleanup_session(session_id)
    
    def _cleanup_session(self, session_id):
        """Cleanup a specific session (called with lock held)"""
        if session_id not in self.sessions:
            return
        
        session_data = self.sessions[session_id]
        files_to_delete = session_data['files'].copy()
        
        # Delete generated files from disk
        deleted_count = 0
        for filename in files_to_delete:
            try:
                filepath = os.path.join(GENERATED_FOLDER, filename)
                if os.path.exists(filepath):
                    os.remove(filepath)
                    deleted_count += 1
                    print(f"Deleted expired generated file: {filename}")
                
            except Exception as e:
                print(f"Error deleting generated file {filename}: {e}")
        
        # Remove session
        del self.sessions[session_id]
        print(f"AI Session {session_id} expired and cleaned up ({deleted_count} generated files deleted)")
    
    def manual_cleanup_session(self, session_id):
        """Manually cleanup a specific session"""
        with self.lock:
            if session_id in self.sessions:
                self._cleanup_session(session_id)
                return True
            return False

# Initialize session manager
ai_session_manager = SessionManager()

# Legacy session management for backward compatibility
session_files = {}
session_lock = threading.Lock()

def cleanup_session_files(session_id):
    """Clean up files for a specific session"""
    with session_lock:
        if session_id in session_files:
            files_to_clean = session_files[session_id]
            for file_path in files_to_clean:
                try:
                    if os.path.exists(file_path):
                        os.remove(file_path)
                        print(f"Cleaned up: {file_path}")
                except Exception as e:
                    print(f"Error cleaning up {file_path}: {e}")
            del session_files[session_id]
            print(f"Session {session_id} cleaned up")

def cleanup_all_sessions():
    """Clean up all sessions on app exit"""
    with session_lock:
        for session_id in list(session_files.keys()):
            cleanup_session_files(session_id)
    
    # Also clean up folders
    try:
        if os.path.exists(UPLOAD_FOLDER):
            shutil.rmtree(UPLOAD_FOLDER)
        if os.path.exists(GENERATED_FOLDER):
            shutil.rmtree(GENERATED_FOLDER)
        print("Cleaned up all folders on exit")
    except Exception as e:
        print(f"Error cleaning up folders on exit: {e}")

# Register cleanup function to run on app exit
atexit.register(cleanup_all_sessions)


def get_mime_type(file_path):
    """Get the correct MIME type for an image file"""
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type and mime_type.startswith('image/'):
        return mime_type
    
    # Fallback based on file extension
    ext = os.path.splitext(file_path)[1].lower()
    mime_map = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg', 
        '.png': 'image/png',
        '.gif': 'image/gif',
        '.webp': 'image/webp'
    }
    return mime_map.get(ext, 'image/jpeg')

def validate_image(file_path):
    """Validate image file size and format"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Image file not found: {file_path}")
    
    # Check file size (limit to 20MB per image)
    file_size = os.path.getsize(file_path)
    if file_size > 20 * 1024 * 1024:
        raise ValueError(f"Image file too large: {file_size} bytes. Maximum is 20MB")
    
    # Check if it's a supported image format
    ext = os.path.splitext(file_path)[1].lower()
    if ext.lstrip('.') not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported image format: {ext}. Supported: {SUPPORTED_EXTENSIONS}")

def get_image_files(directory_path):
    """Get all supported image files from a directory"""
    if not os.path.exists(directory_path):
        return []
    
    supported_extensions = ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.webp', 
                           '*.JPG', '*.JPEG', '*.PNG', '*.GIF', '*.WEBP']
    image_files = []
    
    for ext in supported_extensions:
        pattern = os.path.join(directory_path, ext)
        image_files.extend(glob.glob(pattern))
    
    return sorted(image_files)

def save_binary_file(file_name, data, output_dir, session_id):
    """Save binary data to file and track for session cleanup"""
    try:
        file_path = os.path.join(output_dir, file_name)
        with open(file_path, "wb") as f:
            f.write(data)
        print(f"Generated file saved to: {file_path}")
        
        # Track file for new session manager
        ai_session_manager.add_file_to_session(session_id, file_name)
        
        # Legacy session tracking for backward compatibility
        with session_lock:
            if session_id not in session_files:
                session_files[session_id] = []
            session_files[session_id].append(file_path)
        
        return file_path
    except Exception as e:
        print(f"Error saving generated file {file_name}: {e}")
        return None

def get_api_key():
    """获取Gemini API密钥"""
    # 首先尝试环境变量
    api_key = os.getenv('GEMINI_API_KEY')
    if api_key:
        return api_key
    
    # 尝试从.env文件读取
    env_files = [
        os.path.join(SCRIPT_DIR, '.env'),
        os.path.join(SCRIPT_DIR, '..', '..', '.env'),
        '.env'
    ]
    
    for env_file in env_files:
        if os.path.exists(env_file):
            try:
                with open(env_file, 'r') as f:
                    for line in f:
                        if line.startswith('GEMINI_API_KEY='):
                            api_key = line.split('=', 1)[1].strip().strip('"\'')
                            if api_key:
                                print(f"Loaded GEMINI_API_KEY from {env_file}")
                                return api_key
            except Exception as e:
                print(f"Error reading {env_file}: {e}")
    
    print("ERROR: GEMINI_API_KEY not found in environment variables or .env files")
    return None

def create_optimized_gemini_client():
    """Create Gemini client optimized for container environments with timeout handling"""
    try:
        # 获取API密钥
        api_key = get_api_key()
        if not api_key:
            raise ValueError("GEMINI_API_KEY is required")
        
        # Set timeout environment variables for HTTP requests
        import os
        os.environ['HTTPX_TIMEOUT'] = '120'
        os.environ['REQUESTS_TIMEOUT'] = '120'
        
        # Clear proxy environment variables to avoid network issues
        for proxy_var in ['http_proxy', 'https_proxy', 'HTTP_PROXY', 'HTTPS_PROXY']:
            if proxy_var in os.environ:
                print(f"Clearing proxy variable: {proxy_var}")
                del os.environ[proxy_var]
        
        # 创建客户端
        client = genai.Client(api_key=api_key)
        print("Created Gemini client successfully")
        
        return client
    except Exception as e:
        print(f"Error creating Gemini client: {e}")
        raise

class TimeoutError(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutError("API call timed out")

def call_with_timeout(func, timeout_seconds, *args, **kwargs):
    """Execute function with timeout using threading"""
    result = [None]
    exception = [None]
    
    def target():
        try:
            result[0] = func(*args, **kwargs)
        except Exception as e:
            exception[0] = e
    
    thread = threading.Thread(target=target)
    thread.daemon = True
    thread.start()
    thread.join(timeout_seconds)
    
    if thread.is_alive():
        # Force cleanup - thread can't be killed but we can return with timeout
        raise TimeoutError(f"Function call timed out after {timeout_seconds} seconds")
    
    if exception[0]:
        raise exception[0]
    
    return result[0]

def make_api_request_with_retry(client, model, contents, max_retries=3):
    """Make API request with retry mechanism for container environments"""
    for attempt in range(max_retries):
        try:
            print(f"API call attempt {attempt + 1}/{max_retries}...")
            
            # Make API call (timeout configuration not supported in request_options)
            response = client.models.generate_content(
                model=model,
                contents=contents
            )
            
            print(f"API call successful on attempt {attempt + 1}")
            return response
            
        except Exception as e:
            print(f"API call attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                # Exponential backoff
                wait_time = (2 ** attempt) * 5  # 5, 10, 20 seconds
                print(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print("All API call attempts failed")
                raise e

def generate_text_to_image(prompt, session_id):
    """Generate images from text prompt using Gemini API with streaming and timeout handling"""
    # Create client with timeout configuration for container environment
    client = create_optimized_gemini_client()
    
    try:
        print(f"Making text-to-image API call with prompt: {prompt[:100]}...")
        
        # Prepare content for streaming
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=prompt),
                ],
            ),
        ]
        
        generate_content_config = types.GenerateContentConfig(
            response_modalities=[
                "IMAGE",
                "TEXT",
            ],
        )
        
        generated_files = []
        text_response = ""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        file_index = 0
        
        print("Starting streaming API call...")
        start_time = time.time()
        chunk_count = 0
        
        # Use streaming approach with timeout handling
        def streaming_call():
            chunks_received = 0
            for chunk in client.models.generate_content_stream(
                model=MODEL_NAME,
                contents=contents,
                config=generate_content_config,
            ):
                chunks_received += 1
                elapsed_time = time.time() - start_time
                print(f"Received chunk {chunks_received} after {elapsed_time:.1f}s")
                
                # Check for timeout (5 minutes max)
                if elapsed_time > 300:
                    raise TimeoutError("Streaming timeout exceeded 5 minutes")
                
                if (
                    chunk.candidates is None
                    or chunk.candidates[0].content is None
                    or chunk.candidates[0].content.parts is None
                ):
                    continue
                    
                for part in chunk.candidates[0].content.parts:
                    if part.inline_data and part.inline_data.data:
                        # Save generated image
                        file_extension = mimetypes.guess_extension(part.inline_data.mime_type) or ".jpg"
                        output_filename = f"text_generated_{timestamp}_{file_index}{file_extension}"
                        
                        saved_path = save_binary_file(output_filename, part.inline_data.data, GENERATED_FOLDER, session_id)
                        if saved_path:
                            generated_files.append(saved_path)
                            print(f"Saved text-to-image: {saved_path}")
                        file_index += 1
                    elif part.text:
                        text_response += part.text
                        print(f"Text response: {part.text}")
                        
            return chunks_received
        
        try:
            # Execute streaming with 5-minute timeout
            chunk_count = call_with_timeout(streaming_call, 300)
        except Exception as stream_error:
            elapsed_time = time.time() - start_time
            print(f"Streaming error after {elapsed_time:.1f}s: {stream_error}")
            raise
        
        total_time = time.time() - start_time
        print(f"Streaming completed in {total_time:.1f}s with {chunk_count} chunks")
        print(f"Generated {len(generated_files)} images from text prompt")
        
        return {
            'success': True,
            'text_response': text_response,
            'generated_files': generated_files,
            'generated_count': len(generated_files),
            'processing_time': total_time,
            'chunks_received': chunk_count
        }
        
    except Exception as e:
        print(f"Error during text-to-image generation: {e}")
        print(f"Exception type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return {
            'success': False,
            'error': str(e),
            'generated_count': 0
        }

def generate_images_batch(image_paths, prompt, session_id):
    """Generate images for multiple input images using Gemini API with streaming"""
    # Create client with timeout configuration for container environment
    client = create_optimized_gemini_client()
    
    # Validate all images first
    for image_path in image_paths:
        validate_image(image_path)
    
    # Prepare content parts - text prompt + multiple images
    content_parts = []
    
    # Add text prompt first
    content_parts.append(types.Part.from_text(text=prompt))
    
    # Add all images to the same request
    for image_path in image_paths:
        mime_type = get_mime_type(image_path)
        print(f"Adding image: {os.path.basename(image_path)} (MIME: {mime_type})")
        
        with open(image_path, 'rb') as f:
            image_bytes = f.read()
        
        # Use types.Part.from_bytes for image data
        content_parts.append(
            types.Part.from_bytes(
                data=image_bytes, 
                mime_type=mime_type
            )
        )
    
    try:
        print(f"Making API call to {MODEL_NAME} with {len(image_paths)} images...")
        
        # Prepare content for streaming
        contents = [
            types.Content(
                role="user",
                parts=content_parts,
            ),
        ]
        
        generate_content_config = types.GenerateContentConfig(
            response_modalities=[
                "IMAGE",
                "TEXT",
            ],
        )
        
        generated_files = []
        text_response = ""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        file_index = 0
        
        print("Starting streaming API call...")
        start_time = time.time()
        chunk_count = 0
        
        # Use streaming approach with timeout handling
        try:
            for chunk in client.models.generate_content_stream(
                model=MODEL_NAME,
                contents=contents,
                config=generate_content_config,
            ):
                chunk_count += 1
                elapsed_time = time.time() - start_time
                print(f"Received chunk {chunk_count} after {elapsed_time:.1f}s")
                
                # Check for timeout (5 minutes max)
                if elapsed_time > 300:
                    raise TimeoutError("Streaming timeout exceeded 5 minutes")
                
                if (
                    chunk.candidates is None
                    or chunk.candidates[0].content is None
                    or chunk.candidates[0].content.parts is None
                ):
                    continue
                    
                for part in chunk.candidates[0].content.parts:
                    if part.inline_data and part.inline_data.data:
                        # Save generated image
                        file_extension = mimetypes.guess_extension(part.inline_data.mime_type) or ".jpg"
                        output_filename = f"generated_{timestamp}_{file_index}{file_extension}"
                        
                        saved_path = save_binary_file(output_filename, part.inline_data.data, GENERATED_FOLDER, session_id)
                        if saved_path:
                            generated_files.append(saved_path)
                            print(f"Saved generated image: {saved_path}")
                        file_index += 1
                    elif part.text:
                        text_response += part.text
                        print(f"Text response: {part.text}")
        
        except Exception as stream_error:
            elapsed_time = time.time() - start_time
            print(f"Streaming error after {elapsed_time:.1f}s, {chunk_count} chunks: {stream_error}")
            raise
        
        total_time = time.time() - start_time
        print(f"Streaming completed in {total_time:.1f}s with {chunk_count} chunks")
        print(f"Generated {len(generated_files)} images")
        print(f"Text response: {text_response}")
        
        return {
            'success': True,
            'text_response': text_response,
            'generated_files': generated_files,
            'processed_images': len(image_paths),
            'processing_time': total_time,
            'chunks_received': chunk_count
        }
        
    except Exception as e:
        print(f"Error during content generation: {e}")
        print(f"Exception type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return {
            'success': False,
            'error': str(e),
            'processed_images': 0
        }



@app.route('/generate', methods=['POST'])
def generate_images():
    try:
        # Get session ID from request header
        session_id = request.headers.get('X-Session-ID')
        if not session_id:
            return jsonify({'error': 'Session ID required'}), 400
        
        # Update session activity
        ai_session_manager.update_session(session_id)
        
        prompt = request.form.get('prompt', '').strip()
        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400
        
        # Check if files were uploaded (optional for text-to-image)
        files = []
        if 'images' in request.files:
            files = request.files.getlist('images')
            files = [f for f in files if f.filename != '']
        
        # Save uploaded files with session tracking (if any)
        saved_files = []
        if files:
            for file in files:
                if file.filename == '':
                    continue
                    
                # Check file extension
                ext = os.path.splitext(file.filename)[1].lower().lstrip('.')
                if ext not in SUPPORTED_EXTENSIONS:
                    return jsonify({'error': f'Unsupported file type: {file.filename}'}), 400
                
                # Save file
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"upload_{session_id}_{timestamp}_{len(saved_files)}_{file.filename}"
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(filepath)
                saved_files.append(filepath)
                
                # Track file for session cleanup
                with session_lock:
                    if session_id not in session_files:
                        session_files[session_id] = []
                    session_files[session_id].append(filepath)
        
        print(f"Processing prompt: {prompt[:100]}... with {len(saved_files)} images")
        
        # Generate images using Gemini API (supports both text-to-image and image editing)
        if saved_files:
            # Image editing with uploaded images
            result = generate_images_batch(saved_files, prompt, session_id)
        else:
            # Pure text-to-image generation
            result = generate_text_to_image(prompt, session_id)
        
        if result['success']:
            if saved_files:
                # Image editing response
                return jsonify({
                    'success': True,
                    'message': f'Successfully processed {result["processed_images"]} images',
                    'text_response': result['text_response'],
                    'generated_files': [os.path.basename(f) for f in result['generated_files']],
                    'processed_count': result['processed_images'],
                    'generation_type': 'image-editing',
                    'session_id': session_id
                }), 200
            else:
                # Text-to-image response
                return jsonify({
                    'success': True,
                    'message': f'Successfully generated {result["generated_count"]} images from text',
                    'text_response': result['text_response'],
                    'generated_files': [os.path.basename(f) for f in result['generated_files']],
                    'generated_count': result['generated_count'],
                    'generation_type': 'text-to-image',
                    'session_id': session_id
                }), 200
        else:
            generation_type = 'image-editing' if saved_files else 'text-to-image'
            processed_count = result.get('processed_images', 0) if saved_files else result.get('generated_count', 0)
            
            return jsonify({
                'success': False,
                'error': result['error'],
                'processed_count': processed_count,
                'generation_type': generation_type
            }), 500
            
    except Exception as e:
        return jsonify({'error': f'Processing failed: {str(e)}'}), 500

@app.route('/cleanup/<session_id>', methods=['POST'])
def cleanup_session(session_id):
    """Manual cleanup endpoint for a specific session"""
    try:
        # Cleanup with new session manager
        success = ai_session_manager.manual_cleanup_session(session_id)
        
        # Legacy cleanup
        cleanup_session_files(session_id)
        
        message = f'Session {session_id} cleaned up'
        if success:
            return jsonify({'success': True, 'message': message}), 200
        else:
            return jsonify({'success': True, 'message': f'Session {session_id} not found or already cleaned'}), 200
    except Exception as e:
        return jsonify({'error': f'Cleanup failed: {str(e)}'}), 500

@app.route('/heartbeat', methods=['POST'])
def ai_heartbeat():
    """AI Session heartbeat endpoint to keep session alive"""
    try:
        session_id = request.headers.get('X-Session-ID')
        if not session_id:
            return jsonify({'error': 'Session ID required'}), 400
        
        # Update session activity
        session_data = ai_session_manager.update_session(session_id)
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'last_activity': session_data['last_activity'].isoformat(),
            'generated_file_count': len(session_data['files']),
            'timeout_seconds': SESSION_TIMEOUT
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'AI Heartbeat failed: {str(e)}'}), 500

@app.route('/image/<filename>')
def serve_generated_image(filename):
    """Serve generated images directly for frontend display"""
    try:
        # Check if file exists in generated folder
        filepath = os.path.join(GENERATED_FOLDER, filename)
        if not os.path.exists(filepath):
            return jsonify({'error': 'Generated image not found'}), 404
        
        return send_from_directory(GENERATED_FOLDER, filename)
        
    except Exception as e:
        return jsonify({'error': f'Failed to serve image: {str(e)}'}), 500

@app.route('/download/<filename>')
def download_generated_image(filename):
    """Download generated images with proper headers"""
    try:
        # Check if file exists in generated folder
        filepath = os.path.join(GENERATED_FOLDER, filename)
        if not os.path.exists(filepath):
            return jsonify({'error': 'Generated image not found'}), 404
        
        return send_from_directory(
            GENERATED_FOLDER, 
            filename, 
            as_attachment=True,
            download_name=f"ai_generated_{filename}"
        )
        
    except Exception as e:
        return jsonify({'error': f'Failed to download image: {str(e)}'}), 500

@app.route('/list_generated')
def list_generated_images():
    """List all available generated images"""
    try:
        if not os.path.exists(GENERATED_FOLDER):
            return jsonify({'images': [], 'count': 0})
        
        images = []
        for filename in os.listdir(GENERATED_FOLDER):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                filepath = os.path.join(GENERATED_FOLDER, filename)
                stat_info = os.stat(filepath)
                images.append({
                    'filename': filename,
                    'size': stat_info.st_size,
                    'created_time': datetime.datetime.fromtimestamp(stat_info.st_ctime).isoformat(),
                    'image_url': f'/image/{filename}',
                    'download_url': f'/download/{filename}'
                })
        
        # Sort by creation time (newest first)
        images.sort(key=lambda x: x['created_time'], reverse=True)
        
        return jsonify({
            'images': images,
            'count': len(images)
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to list images: {str(e)}'}), 500

@app.route('/test_api', methods=['GET'])
def test_gemini_api():
    """Test endpoint to verify Gemini API connectivity"""
    try:
        print("Testing Gemini API connection...")
        
        # Create client with timeout configuration for container environment
        client = create_optimized_gemini_client()
        
        # Test API call with retry mechanism
        response = make_api_request_with_retry(
            client=client,
            model=MODEL_NAME,
            contents=["Explain how AI works in a few words"],
            max_retries=2  # Fewer retries for test endpoint
        )
        
        return jsonify({
            'success': True,
            'message': 'Gemini API connection successful',
            'response': response.text,
            'model': MODEL_NAME
        }), 200
        
    except Exception as e:
        print(f"Gemini API test failed: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Gemini API test failed: {str(e)}',
            'model': MODEL_NAME
        }), 500

@app.errorhandler(413)
def too_large(e):
    return jsonify({'error': 'Files too large. Maximum total size is 50MB'}), 413

if __name__ == '__main__':
    # Ensure directories exist
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(GENERATED_FOLDER, exist_ok=True)
    
    print(f"Upload directory: {UPLOAD_FOLDER}")
    print(f"Generated directory: {GENERATED_FOLDER}")
    
    # Test Gemini API connection at startup
    print("\n🔍 Testing Gemini API connection...")
    try:
        # Create client with timeout configuration for container environment
        test_client = create_optimized_gemini_client()
        
        # Test API call with retry mechanism for startup
        test_response = make_api_request_with_retry(
            client=test_client,
            model=MODEL_NAME,
            contents=["Hello"],
            max_retries=2
        )
        print("✅ Gemini API connection successful!")
        print(f"✅ Model: {MODEL_NAME}")
        print(f"✅ Test response: {test_response.text}")
    except Exception as e:
        print(f"❌ Gemini API connection failed: {e}")
        print("⚠️  AI generation will not work until API connection is fixed")
    
    # Check if running in production mode
    if os.environ.get('FLASK_ENV') == 'production':
        print("🚀 Production mode detected")
        print("Use gunicorn: gunicorn -c gunicorn_config.py gemini_api:app")
    else:
        print("⚠️  Development mode - Starting Flask dev server...")
        print("⚠️  WARNING: This is a development server. Do not use it in a production deployment.")
        print("⚠️  Use a production WSGI server instead.")
        print("")
        print("📡 For production deployment:")
        print("   pip install gunicorn")
        print("   gunicorn -c gunicorn_config.py gemini_api:app")
        print("")
        print("🔧 Development server starting...")
        print("API endpoint: http://localhost:8088/generate")
        print("Image serving: http://localhost:8088/image/<filename>")
        print("Download: http://localhost:8088/download/<filename>")
        
        app.run(debug=True, host='0.0.0.0', port=8088)