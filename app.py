
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
import time

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_endpoint():
    data = request.get_json()
    endpoint = data.get('endpoint')

    if not endpoint:
        return jsonify({"error": "No endpoint provided"}), 400

    print(f"Received endpoint request: {endpoint}")

    # Acknowledge the request first
    socketio.emit('status', {"message": "Server received the request for " + endpoint})

    # Simulating a processing delay with a background task
    socketio.start_background_task(target=simulate_backend_task, endpoint=endpoint)

    return jsonify({"message": "Request received, processing started!"})

def simulate_backend_task(endpoint):
    """Simulated long-running task that emits data when done."""
    time.sleep(5)  # Simulate processing delay
    
    # Simulated result
    result = f"Processed data from {endpoint}"
    
    print("Sending result:", result)
    socketio.emit('update_result', {"message": result})

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, debug=True)
