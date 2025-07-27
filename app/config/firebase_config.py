from utils.config_loader import Config


class FirebaseConfig:
    DATABASE_URL = Config.FIREBASE_DB_URL
    CREDENTIALS_PATH = "serviceAccountKey.json"