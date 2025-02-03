from flask import Flask, render_template, request, jsonify
import subprocess
import os
import signal

app = Flask(__name__)

# Global variable to store the detection process
detection_process = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_detection', methods=['POST'])
def start_detection():
    global detection_process

    mode = request.json.get('mode')

    if mode == 'single':
        script_path = 'single_detection.py'
    elif mode == 'multi':
        script_path = 'multi_detection.py'
    elif mode == 'alert':
        script_path = 'alert.py'
    else:
        return jsonify({'error': 'Invalid mode'}), 400

    # Start the detection script as a subprocess
    detection_process = subprocess.Popen(['python', script_path])
    return jsonify({'message': f'{mode.capitalize()} detection started'})

@app.route('/stop_detection', methods=['POST'])
def stop_detection():
    global detection_process

    if detection_process:
        # Terminate the detection process
        detection_process.terminate()
        detection_process = None
        return jsonify({'message': 'Detection stopped'})
    else:
        return jsonify({'error': 'No detection process running'}), 400

if __name__ == '__main__':
    app.run(debug=True)