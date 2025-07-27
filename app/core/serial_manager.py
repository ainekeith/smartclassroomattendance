import serial
from services.firebase_service import FirebaseService
from core.camera_service import CameraService
from utils.emotion_detector import EmotionDetector
import time


class SerialManager:
    def __init__(self, port='/dev/ttyACM0', baudrate=9600):
        self.port = port
        self.baudrate = baudrate
        self.firebase = FirebaseService()
        self.camera = CameraService()
        self.detector = EmotionDetector()
        
    def monitor(self):
        try:
            arduino = serial.Serial(self.port, self.baudrate, timeout=1)
            arduino.reset_input_buffer()
            self.firebase.update_device_status('arduino', 'connected')
            
            while True:
                if arduino.in_waiting:
                    line = arduino.readline().decode().strip()
                    self.process_command(line)
                time.sleep(0.1)
                
        except Exception as e:
            self.firebase.update_device_status('arduino', 'disconnected')
            print(f"Serial error: {str(e)}")

    def process_command(self, command):
        if "ATTENDANCE" in command:
            student_id = command.split(':')[1] if ':' in command else 'unknown'
            img_path = self.camera.capture()
            
            if img_path:
                emotion = self.detector.analyze(img_path)
                data = {
                    'student_id': student_id,
                    'timestamp': time.time(),
                    'image_url': img_path,
                    'emotion': emotion
                }
                self.firebase.push_attendance(data)