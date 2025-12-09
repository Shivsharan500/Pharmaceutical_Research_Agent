"""
Flask API Server for Pharmaceutical Research System
Run with: python server.py
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import os
import threading
import uuid
import time

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# Store research job status
jobs = {}

def run_research(job_id, molecule_name):
    """Run the main.py research script in a background thread"""
    try:
        jobs[job_id]['status'] = 'running'
        
        # Get the directory where this server.py is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        main_script = os.path.join(script_dir, 'main.py')
        output_file = os.path.join(script_dir, 'output.txt')
        
        # Modify main.py execution to save output to output.txt
        # We'll run a modified version that saves to output.txt
        env = os.environ.copy()
        env['MOLECULE_NAME'] = molecule_name
        
        # Run the research script
        result = subprocess.run(
            ['python', main_script, molecule_name],
            capture_output=True,
            text=True,
            cwd=script_dir,
            env=env,
            timeout=1800  # 30 minute timeout
        )
        
        # Read output file
        if os.path.exists(output_file):
            with open(output_file, 'r', encoding='utf-8') as f:
                output_content = f.read()
            jobs[job_id]['status'] = 'complete'
            jobs[job_id]['result'] = output_content
        else:
            # If no output.txt, use stdout
            jobs[job_id]['status'] = 'complete'
            jobs[job_id]['result'] = result.stdout or "Research completed but no output file found."
            
    except subprocess.TimeoutExpired:
        jobs[job_id]['status'] = 'error'
        jobs[job_id]['error'] = 'Research timed out after 30 minutes'
    except Exception as e:
        jobs[job_id]['status'] = 'error'
        jobs[job_id]['error'] = str(e)


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'message': 'Server is running'})


@app.route('/api/research/start', methods=['POST'])
def start_research():
    """Start a new research job for a molecule"""
    data = request.get_json()
    molecule_name = data.get('molecule_name')
    
    if not molecule_name:
        return jsonify({'error': 'molecule_name is required'}), 400
    
    # Create a new job
    job_id = str(uuid.uuid4())
    jobs[job_id] = {
        'id': job_id,
        'molecule_name': molecule_name,
        'status': 'pending',
        'result': None,
        'error': None,
        'started_at': time.time()
    }
    
    # Start research in background thread
    thread = threading.Thread(target=run_research, args=(job_id, molecule_name))
    thread.daemon = True
    thread.start()
    
    return jsonify({
        'job_id': job_id,
        'message': f'Research started for {molecule_name}'
    })


@app.route('/api/research/status/<job_id>', methods=['GET'])
def get_research_status(job_id):
    """Get the status of a research job"""
    if job_id not in jobs:
        return jsonify({'error': 'Job not found'}), 404
    
    job = jobs[job_id]
    response = {
        'job_id': job_id,
        'molecule_name': job['molecule_name'],
        'status': job['status'],
        'elapsed_seconds': int(time.time() - job['started_at'])
    }
    
    if job['status'] == 'complete':
        response['result'] = job['result']
    elif job['status'] == 'error':
        response['error'] = job['error']
    
    return jsonify(response)


@app.route('/api/research/result/<job_id>', methods=['GET'])
def get_research_result(job_id):
    """Get the final result of a completed research job"""
    if job_id not in jobs:
        return jsonify({'error': 'Job not found'}), 404
    
    job = jobs[job_id]
    
    if job['status'] != 'complete':
        return jsonify({
            'error': 'Research not complete yet',
            'status': job['status']
        }), 400
    
    return jsonify({
        'job_id': job_id,
        'molecule_name': job['molecule_name'],
        'result': job['result']
    })


if __name__ == '__main__':
    print("=" * 60)
    print("Pharmaceutical Research API Server")
    print("=" * 60)
    print("\nEndpoints:")
    print("  POST /api/research/start   - Start new research")
    print("  GET  /api/research/status/<job_id> - Check status")
    print("  GET  /api/research/result/<job_id> - Get results")
    print("  GET  /api/health           - Health check")
    print("\nStarting server on http://localhost:5000")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5000, debug=True)
