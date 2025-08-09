from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import logging
from typing import Dict, Any

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask application
app = Flask(__name__)
CORS(app)  # Enable CORS support

# Application configuration
app.config['JSON_AS_ASCII'] = False  # Support Chinese JSON return
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# Import managers and routes
from managers.tool_manager import ToolManager
from routes.tools import tools_bp

# Register blueprints
app.register_blueprint(tools_bp, url_prefix='/api')

# Initialize tool manager
tool_manager = ToolManager()

# Make tool manager globally available
app.tool_manager = tool_manager

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'success',
        'message': 'API service is running normally',
        'version': '1.0.0',
        'available_tools': len(tool_manager.get_all_tools())
    })

# Root path endpoint
@app.route('/', methods=['GET'])
def root():
    """Root path endpoint that returns basic API information"""
    return jsonify({
        'name': 'Python Backend API Service',
        'description': 'Universal Python backend API service supporting multiple tool calls',
        'version': '1.0.0',
        'endpoints': {
            'health': '/api/health',
            'tools_list': '/api/tools',
            'tool_info': '/api/tools/{tool_name}',
            'web_crawler': '/api/crawler?url={url}',
            'generic_execute': '/api/execute?tool={tool_name}&{parameters}'
        },
        'available_tools': tool_manager.get_all_tools()
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

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'status': 'error',
        'message': 'Request parameter error',
        'code': 400
    }), 400

# Handler required for Vercel deployment
def handler(request):
    """Vercel serverless function handler"""
    return app(request.environ, request.start_response)

if __name__ == '__main__':
    # Run in development environment
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting Flask application, port: {port}, debug mode: {debug}")
    logger.info(f"Available tools count: {len(tool_manager.get_all_tools())}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)