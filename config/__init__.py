import os
import yaml

with open(f"config/config.yaml", "r") as f:
    APP_CONFIG = yaml.safe_load(f)

APP_CONFIG["MODEL"]["MODEL_NAME"] = os.environ["MODEL_NAME"]
APP_CONFIG["MODEL"]["MODEL_ID"] = os.environ["MODEL_ID"]
APP_CONFIG["MODEL"]["MODEL_KEY"] = os.environ["MODEL_KEY"]

APP_CONFIG["DATABASE"]["HOST"] = os.environ["DB_HOST"]
APP_CONFIG["DATABASE"]["PORT"] = int(os.environ["DB_PORT"])
APP_CONFIG["DATABASE"]["USERNAME"] = os.environ["DB_USERNAME"]
APP_CONFIG["DATABASE"]["PASSWORD"] = os.environ["DB_PASSWORD"]
APP_CONFIG["DATABASE"]["AUTH"] = os.environ["DB_AUTH"]