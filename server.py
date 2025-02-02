from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from main import TrafficAnalyzer, determine_traffic_signals
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure upload folder
UPLOAD_FOLDER = 'Videos'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.split('.')[-1].lower() in ALLOWED_EXTENSIONS

@app.route('/analyze', methods=['POST'])
def analyze_videos():
    try:
        if 'junction1' not in request.files or 'junction2' not in request.files:
            return jsonify({'error': 'Both video files are required'}), 400

        video1 = request.files['junction1']
        video2 = request.files['junction2']

        # Check if files are valid
        if not (video1 and video2 and 
                allowed_file(video1.filename) and 
                allowed_file(video2.filename)):
            return jsonify({'error': 'Invalid file format'}), 400

        # Save videos with secure filenames
        video1_path = os.path.join(app.config['UPLOAD_FOLDER'], 'junction1.mp4')
        video2_path = os.path.join(app.config['UPLOAD_FOLDER'], 'junction2.mp4')

        video1.save(video1_path)
        video2.save(video2_path)

        # Analyze videos using existing logic from main.py
        analyzer = TrafficAnalyzer()
        density1 = analyzer.analyze_video(video1_path)
        density2 = analyzer.analyze_video(video2_path)

        if density1 is None or density2 is None:
            return jsonify({'error': 'Failed to analyze videos'}), 500

        # Get signal timings
        signal_timings = determine_traffic_signals(density1, density2)

        # Return analysis results
        return jsonify({
            'junction1': {
                'density': round(density1, 2),
                'timings': signal_timings['junction1']
            },
            'junction2': {
                'density': round(density2, 2),
                'timings': signal_timings['junction2']
            },
            'total_cycle_time': signal_timings['cycle_time']
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000) 