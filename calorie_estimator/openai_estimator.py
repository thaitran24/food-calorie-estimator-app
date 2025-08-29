import numpy as np
from openai import OpenAI
from .utils import read_template, image_to_base64

class OpenAICalorieEstimator:
    def __init__(self, config):
        self.config = config
        self.model_id = self.config["MODEL_ID"]
        self.client = OpenAI(api_key=self.config["MODEL_KEY"])
        self.system_prompt = read_template(self.config["SYSTEM_PROMPT"])
        self.template_prompt = read_template(self.config["TEMPLATE_PROMPT"])
        self.image_size = self.config["IMAGE_SIZE"]

    async def predict(self, image: np.ndarray):
        image_b64 = image_to_base64(image, self.image_size)
        response = self.client.chat.completions.create(
            model=self.model_id,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": self.template_prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}
                        },
                    ],
                },
            ],
        )
        return response.choices[0].message.content