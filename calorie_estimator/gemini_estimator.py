import numpy as np
from google import genai
from google.genai.types import Part
from .utils import read_template, image_to_bytes

class GeminiCalorieEstimator:
    def __init__(self, config):
        self.config = config
        self.model_id = self.config["MODEL_ID"]
        self.client = genai.Client(api_key=self.config["MODEL_KEY"])
        self.template_prompt = read_template(self.config["TEMPLATE_PROMPT"])
        self.image_size = self.config["IMAGE_SIZE"]

    async def predict(self, image: np.ndarray):
        image_bytes = image_to_bytes(image, self.image_size)
        response = self.client.models.generate_content(
            model=self.config["MODEL_ID"],
            contents=[
                self.template_prompt,
                Part.from_bytes(
                    data=image_bytes,
                    mime_type='image/jpeg',
                ),
            ]
        )
        return response.text

    def predict_sync(self, image: np.ndarray):
        image_bytes = image_to_bytes(image, self.image_size)
        response = self.client.models.generate_content(
            model=self.config["MODEL_ID"],
            contents=[
                self.template_prompt,
                Part.from_bytes(
                    data=image_bytes,
                    mime_type='image/jpeg',
                ),
            ]
        )
        return response.text