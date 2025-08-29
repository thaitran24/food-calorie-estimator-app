import cv2
import json
import numpy as np
import base64

def image_to_base64(img, size=448):
    h, w = img.shape[:2]
    if h > w:
        new_h = size
        new_w = int(w * (size / h))
    else:
        new_w = size
        new_h = int(h * (size / w))
    resized = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)

    # Encode back to base64
    success, buffer = cv2.imencode(".jpg", resized)
    if not success:
        raise ValueError("Failed to encode resized image.")
    
    b64_resized = base64.b64encode(buffer).decode("utf-8")
    return b64_resized

def image_to_bytes(img, size=448):
    h, w = img.shape[:2]
    if h > w:
        new_h = size
        new_w = int(w * (size / h))
    else:
        new_w = size
        new_h = int(h * (size / w))
    resized = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
    # cv2.imwrite("debug/debug.jpg", resized)

    # Encode back to JPEG bytes
    success, buffer = cv2.imencode(".jpg", resized)
    if not success:
        raise ValueError("Failed to encode image.")
    
    return buffer.tobytes()


def read_template(template_path):
    with open(template_path, "r") as f:
        return f.read()


def parse_output(text):
    data = json.loads(text)
    return data