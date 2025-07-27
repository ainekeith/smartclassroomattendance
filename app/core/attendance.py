import cv2
import serial
from flask import Flask, render_template, g
import threading
import sqlite3
from datetime import datetime
import os
import atexit
from utils.firebase_handler import FirebaseHandler
from utils.emotion_detector import EmotionDetector

app = Flask(__name__, template_folder='templates')

# Initialize Firebase
firebase = FirebaseHandler()

# Initialize Emotion Detector
emotion_detector = EmotionDetector('models/emotion_model.h5', 
                                 'models/haarcascade_frontalface_default.xml')

# Database setup


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('attendance.db')
        g.db.row_factory = sqlite3.Row
    return g.db

def init_db():
    with app.app_context():
        db = get_db()
        db.execute('''CREATE TABLE IF NOT EXISTS attendance
                     (id INTEGER PRIMARY KEY,
                      timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                      photo_path TEXT,
                      emotion TEXT,
                      student_id TEXT)''')
        db.commit()

init_db()

@app.teardown_appcontext
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def capture_and_analyze():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        firebase.update_status('camera', 'error')
        return False, None
        
    ret, frame = cap.read()
    cap.release()
    
    if ret:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"static/captures/capture_{timestamp}.jpg"
        
        # Ensure directories exist
        os.makedirs('static/captures', exist_ok=True)
        
        # Save image
        cv2.imwrite(filename, frame)
        
        # Detect emotion
        emotion = emotion_detector.detect_emotion(frame)
        
        return filename, emotion
    
    firebase.update_status('camera', 'error')
    return False, None

def handle_serial():
    try:
        arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        arduino.reset_input_buffer()
        firebase.update_status('arduino', 'active')
        
        while True:
            if arduino.in_waiting:
                line = arduino.readline().decode().strip()
                if "ATTENDANCE" in line:
                    # Expected format: "ATTENDANCE:STUDENT_ID"
                    student_id = line.split(':')[1] if ':' in line else 'unknown'
                    
                    photo_path, emotion = capture_and_analyze()
                    if photo_path:
                        with app.app_context():
                            db = get_db()
                            db.execute(
                                "INSERT INTO attendance (photo_path, emotion, student_id) VALUES (?, ?, ?)",
                                (photo_path, emotion, student_id)
                            )
                            db.commit()
                            
                            # Update Firebase
                            firebase.log_attendance({
                                'timestamp': datetime.now().isoformat(),
                                'photo_url': photo_path,
                                'emotion': emotion,
                                'student_id': student_id,
                                'device': 'raspberry_pi'
                            })
                            
                            print(f"Logged attendance for {student_id} with emotion {emotion}")
    except Exception as e:
        print(f"Serial error: {str(e)}")
        firebase.update_status('arduino', 'error')

@app.route('/')
def dashboard():
    try:
        db = get_db()
        count = db.execute("SELECT COUNT(*) FROM attendance").fetchone()[0]
        
        latest_entry = db.execute(
            "SELECT photo_path, emotion, student_id FROM attendance ORDER BY timestamp DESC LIMIT 1"
        ).fetchone()
        
        return render_template('dashboard.html', 
                            attendance=count,
                            latest_entry=latest_entry)
    except Exception as e:
        print(f"Error in dashboard: {str(e)}")
        return render_template('error.html', error=str(e))

@app.route('/firebase')
def firebase_dashboard():
    return render_template('firebase-dashboard.html')

def cleanup():
    print("Cleaning up resources...")
    firebase.update_status('system', 'offline')

atexit.register(cleanup)

if __name__ == '__main__':
    # Initialize status
    firebase.update_status('system', 'starting')
    firebase.update_status('camera', 'initializing')
    firebase.update_status('arduino', 'initializing')
    
    # Start serial handler thread
    serial_thread = threading.Thread(target=handle_serial, daemon=True)
    serial_thread.start()
    
    # Mark system as online
    firebase.update_status('system', 'online')
    
    # Run Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)