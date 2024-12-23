from flask import Flask, request, jsonify, render_template
import json

app = Flask(__name__)

# Path to the JSON file where student progress will be saved
progress_file = 'MonitorStudents.json'

# Load current progress data from JSON file
def load_progress():
    try:
        with open(progress_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Save student progress data to JSON file
def save_progress(progress_data):
    with open(progress_file, 'w') as f:
        json.dump(progress_data, f, indent=4)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/save-progress', methods=['POST'])
def save_progress_data():
    data = request.json
    student_name = data.get('name')
    video_title = data.get('videoTitle')
    watched = data.get('watched')

    progress_data = load_progress()

    if student_name not in progress_data:
        progress_data[student_name] = {}

    progress_data[student_name][video_title] = watched

    save_progress(progress_data)

    return jsonify({"message": "Progress saved successfully!", "name": student_name, "watched": watched}), 200

@app.route('/get-progress', methods=['GET'])
def get_progress():
    progress_data = load_progress()
    return jsonify(progress_data)

if __name__ == '__main__':
    app.run(debug=True)