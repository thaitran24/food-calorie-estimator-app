from utils import LOGGER
from config import APP_CONFIG
from .openai_estimator import OpenAICalorieEstimator
from .gemini_estimator import GeminiCalorieEstimator

model_dict = {
    "gemini": GeminiCalorieEstimator,
    "openai": OpenAICalorieEstimator
}
model_name = APP_CONFIG["MODEL"]["MODEL_NAME"]
model_version = APP_CONFIG["MODEL"]["MODEL_ID"]
ESTIMATOR = model_dict[model_name](APP_CONFIG["MODEL"])
LOGGER.info(f"Model loaded successfull. Using {model_name}: {model_version}")