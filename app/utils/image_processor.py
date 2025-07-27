import cv2
from pathlib import Path
import os


def save_image(image, filename):
    save_dir = Path(__file__).parent.parent / "static/captures"
    os.makedirs(save_dir, exist_ok=True)
    
    img_path = save_dir / f"{filename}.jpg"
    cv2.imwrite(str(img_path), image)
    
    return f"static/captures/{filename}.jpg"