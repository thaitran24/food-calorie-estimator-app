import base64
import uuid
from loguru import logger
from locust import HttpUser, between, task


def image_to_base64(image_path):
    with open(image_path, "rb") as f:
        image_bytes = f.read()
    return base64.b64encode(image_bytes).decode("utf-8")


class ModelUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        self.image_b64 = image_to_base64("examples/image.jpeg")

    @task
    def predict(self):
        logger.info("Sending POST request")
        request_id = str(uuid.uuid4())
        payload = {
            "request_id": request_id,
            "image": self.image_b64
        }
        with self.client.post("/predict", json=payload, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Failed with status {response.status_code}: {response.text}")
