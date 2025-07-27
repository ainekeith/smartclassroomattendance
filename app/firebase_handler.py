import firebase_admin
from firebase_admin import credentials, db


def init_firebase():
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://smartclassroom-attendance-default-rtdb.firebaseio.com/'
    })
    return db.reference('/')
