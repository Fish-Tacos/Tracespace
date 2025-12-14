"""
Trace Space Web Server
Flask server that serves visualization and provides API endpoints
"""

from flask import Flask, send_from_directory, jsonify
from pathlib import Path
import config

app = Flask(__name__, static_folder='visualization')

# Serve index.html at root
@app.route('/')
def index():
    """Serve main visualization page"""
    return send_from_directory('visualization', 'index.html')

# Serve JavaScript
@app.route('/tracespace.js')
def tracespace_js():
    """Serve visualization JavaScript"""
    return send_from_directory('visualization', 'tracespace.js')

# Serve data files
@app.route('/data/<path:filename>')
def serve_data(filename):
    """Serve data files from visualization/data directory"""
    return send_from_directory('visualization/data', filename)

# API endpoint - get latest data
@app.route('/api/latest')
def api_latest():
    """
    API endpoint to get latest organism data
    Returns JSON with current state
    """
    data_file = Path('visualization/data/latest.json')
    
    if not data_file.exists():
        return jsonify({
            'error': 'No data available',
            'message': 'Run the pipeline first: python run.py'
        }), 404
    
    with open(data_file, 'r') as f:
        import json
        data = json.load(f)
    
    return jsonify(data)

# API endpoint - health check
@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'service': 'Trace Space',
        'version': '1.0.0'
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Not found',
        'message': str(error)
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'error': 'Internal server error',
        'message': str(error)
    }), 500

def main():
    """Run the Flask development server"""
    print("\n" + "="*60)
    print("TRACE SPACE - WEB SERVER")
    print("="*60)
    print(f"Starting server on http://localhost:{config.VISUALIZATION_PORT}")
    print("\nEndpoints:")
    print(f"  Main:   http://localhost:{config.VISUALIZATION_PORT}/")
    print(f"  API:    http://localhost:{config.VISUALIZATION_PORT}/api/latest")
    print(f"  Health: http://localhost:{config.VISUALIZATION_PORT}/api/health")
    print("\nPress Ctrl+C to stop")
    print("="*60 + "\n")
    
    app.run(
        host='0.0.0.0',
        port=config.VISUALIZATION_PORT,
        debug=True,
        use_reloader=False  # Avoid double initialization
    )

if __name__ == '__main__':
    main()
