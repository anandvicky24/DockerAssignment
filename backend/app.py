from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Enable CORS
CORS(app)

# Path to data file
DATA_FILE = 'data.json'

def load_data_from_file():
    """Load data from JSON file"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []

def save_data_to_file(data):
    """Save data to JSON file"""
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except IOError as e:
        print(f"Error saving to file: {e}")
        return False

@app.route('/api', methods=['GET'])
def get_data():
    """
    GET /api - Returns JSON list of all submitted data
    Reads from data.json file
    """
    try:
        submissions = load_data_from_file()
        return jsonify(submissions), 200
    except Exception as e:
        print(f"Error fetching data: {e}")
        return jsonify([]), 200

@app.route('/api/submit', methods=['POST'])
def submit_data():
    """
    POST /api/submit - Handle form submission
    Inserts data into data.json file
    """
    try:
        # Validate request data
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate required fields
        required_fields = ['name', 'email', 'message']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Validate email format
        if '@' not in data.get('email', ''):
            return jsonify({'error': 'Invalid email format'}), 400
        
        # Prepare submission data
        submission = {
            'name': data['name'].strip(),
            'email': data['email'].strip(),
            'message': data['message'].strip(),
            'createdAt': datetime.utcnow().isoformat()
        }
        
        # Load existing data, add new submission, and save
        submissions = load_data_from_file()
        submissions.append(submission)
        
        if save_data_to_file(submissions):
            return jsonify({
                'success': True,
                'message': 'Data submitted successfully',
                'data': submission
            }), 201
        else:
            return jsonify({'error': 'Failed to save data'}), 500
    
    except Exception as e:
        print(f"Error submitting data: {e}")
        return jsonify({'error': 'Failed to process submission'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'}), 200

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Route not found'}), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=os.getenv('FLASK_ENV') == 'development')