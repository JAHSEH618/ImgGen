from flask import Flask, jsonify
from flask_cors import CORS
import os
import sys

# Add backend directory to path so we can import tools
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tools.img_gen.routes import bp as img_gen_bp
from tools.file_storage.routes import bp as file_storage_bp

app = Flask(__name__)
CORS(app)  # Enable CORS globally

# Register Blueprints
app.register_blueprint(img_gen_bp, url_prefix='/api/tools/img-gen')
app.register_blueprint(file_storage_bp, url_prefix='/api/tools/file-storage')

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'version': '1.0.0'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug)
