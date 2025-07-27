# Initialize core package
from .attendance_manager import AttendanceManager
from .camera_service import CameraService
from .serial_manager import SerialManager

__all__ = ['AttendanceManager', 'CameraService', 'SerialManager']