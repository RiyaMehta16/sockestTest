from flask import Flask, render_template
from flask_socketio import SocketIO
import time

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('index.html')

def send_data():
    while True:
        data = {
            "message": "Real-time update",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        print("Sending data:", data)
        socketio.emit('update_data', data)  # Send data to frontend
        time.sleep(5)  # Send data every 5 seconds

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    socketio.start_background_task(send_data)

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, debug=True)
