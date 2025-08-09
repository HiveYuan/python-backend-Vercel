from flask import Flask, jsonify
from flask_cors import CORS
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask application
app = Flask(__name__)
CORS(app)  # Enable CORS support

# Application configuration
app.config['JSON_AS_ASCII'] = False  # Support Chinese JSON return
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'success',
        'message': 'API service is running normally',
        'version': '1.0.0'
    })

# Root path endpoint
@app.route('/', methods=['GET'])
def root():
    """Root path endpoint that returns basic API information"""
    return jsonify({
        'name': 'Python Backend API Service',
        'description': 'Universal Python backend API service',
        'version': '1.0.0',
        'endpoints': {
            'health': '/api/health'
        }
    })

# Error handling
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'status': 'error',
        'message': 'Requested endpoint does not exist',
        'code': 404
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'status': 'error',
        'message': 'Internal server error',
        'code': 500
    }), 500

# For Vercel deployment - expose the app object
application = app

if __name__ == '__main__':
    # Run in development environment
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting Flask application, port: {port}, debug mode: {debug}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)