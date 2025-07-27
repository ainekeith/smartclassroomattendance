from utils.config_loader import Config


class DeviceConfig:
    CAMERA = {
        'index': Config.CAMERA_INDEX,
        'resolution': (640, 480)
    }
    ARDUINO = {
        'port': Config.ARDUINO_PORT,
        'baudrate': 9600
    }