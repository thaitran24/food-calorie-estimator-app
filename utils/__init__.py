from loguru import logger as LOGGER
from config import APP_CONFIG
from .database import MongoDBLogger

DB_LOGGER = MongoDBLogger(APP_CONFIG["DATABASE"])