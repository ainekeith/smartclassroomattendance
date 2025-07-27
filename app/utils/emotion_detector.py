import cv2
import numpy as np
from keras.models import load_model
from pathlib import Path


class EmotionDetector:
    def __init__(self):
        model_path = Path(__file__).parent.parent / "models/facial_expression/model.h5"
        cascade_path = Path(__file__).parent.parent / "models/haarcascade_frontalface_default.xml"
        self.model = load_model(str(model_path))
        self.face_cascade = cv2.CascadeClassifier(str(cascade_path))
        self.emotions = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
        
    def analyze(self, image_path):
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        
        if len(faces) == 0:
            return 'no_face'
            
        (x,y,w,h) = faces[0]
        face = gray[y:y+h, x:x+w]
        face = cv2.resize(face, (48,48))
        face = face.astype('float32') / 255
        face = np.expand_dims(face, 0)
        face = np.expand_dims(face, -1)
        
        preds = self.model.predict(face)[0]
        return self.emotions[np.argmax(preds)]