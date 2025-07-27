from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    # Firebase
    FIREBASE_DB_URL = os.getenv('FIREBASE_DB_URL')
    
    # Hardware
    CAMERA_INDEX = int(os.getenv('CAMERA_INDEX', 0))
    ARDUINO_PORT = os.getenv('ARDUINO_PORT', '/dev/ttyACM0')
    
    # Application
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'