import cv2
from datetime import datetime
from utils.image_processor import save_image
from services.firebase_service import FirebaseService


class CameraService:
    def __init__(self, camera_index=0):
        self.camera_index = camera_index
        self.firebase = FirebaseService()
        
    def capture(self):
        cap = cv2.VideoCapture(self.camera_index)
        if not cap.isOpened():
            self.firebase.update_device_status('camera', 'error')
            return None
            
        ret, frame = cap.read()
        cap.release()
        
        if ret:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            img_path = save_image(frame, f"capture_{timestamp}")
            self.firebase.update_device_status('camera', 'active')
            return img_path
            
        self.firebase.update_device_status('camera', 'inactive')
        return None