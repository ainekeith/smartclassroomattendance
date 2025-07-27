import firebase_admin
from firebase_admin import credentials, db
from pathlib import Path


class FirebaseService:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cred_path = Path(__file__).parent.parent / "serviceAccountKey.json"
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
        return cls._instance
    
    def push_attendance(self, data):
        ref = db.reference('attendance')
        ref.push(data)
        
    def update_device_status(self, device, status):
        ref = db.reference(f'devices/{device}')
        ref.set({
            'status': status,
            'last_updated': firebase_admin.db.SERVER_TIMESTAMP
        })