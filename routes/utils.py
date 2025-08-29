import re
import cv2
import json
import numpy as np
import base64

def image_sanity_check(image_b64):
    # Strip header if exists (e.g., "data:image/jpeg;base64,...")
    if "," in image_b64:
        image_b64 = image_b64.split(",", 1)[1]

    # Base64 decode
    image_bytes = base64.b64decode(image_b64)

    # Convert to numpy + decode with OpenCV
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Invalid base64 image string.")
    
    return img

def clean_json_str(output: str) -> str:
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", output.strip(), flags=re.MULTILINE)
    return cleaned.strip()


def validate_output(json_str: str):
    try:
        json_str = clean_json_str(json_str)
        data = json.loads(json_str)
    except json.JSONDecodeError:
        return {
            "ingredients": [],
            "total_calories": None,
            "confidence": 0.0,
            "recommendation": "Cannot estimate food. Please retry."
        }

    # Ensure keys exist
    for key in ["ingredients", "total_calories", "confidence", "recommendation"]:
        if key not in data:
            return {
                "ingredients": [],
                "total_calories": None,
                "confidence": 0.0,
                "recommendation": "Output missing required fields. Please retry."
            }

    # Successful parse with ingredients
    if isinstance(data["ingredients"], list) and len(data["ingredients"]) > 0:
        # Normalize ingredient objects
        normalized_ingredients = []
        for ing in data["ingredients"]:
            normalized_ingredients.append({
                "name": str(ing.get("name", "")),
                "quantity": str(ing.get("quantity", "")),
                "unit": str(ing.get("unit", "")),
                "calories_per_unit": str(ing.get("calories_per_unit", "")),
                "calories": str(ing.get("calories", "")),
            })
        return {
            "ingredients": normalized_ingredients,
            "total_calories": data.get("total_calories"),
            "confidence": float(data.get("confidence", 0.0)),
            "recommendation": None
        }

    # Failure case
    return {
        "ingredients": [],
        "total_calories": None,
        "confidence": 0.0,
        "recommendation": str(data.get("recommendation", "Unknown error."))
    }
