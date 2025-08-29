import numpy as np
from datetime import datetime
from pymongo import MongoClient, errors

from .utils import now
from . import LOGGER

def sanitize_for_mongo(obj):
    if isinstance(obj, np.generic):
        return obj.item()
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {k: sanitize_for_mongo(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [sanitize_for_mongo(v) for v in obj]
    return obj

class MongoDBLogger:
    def __init__(self, config):
        self.config = config
        self.use_db = bool(self.config.get("HOST"))
        self.db_connected = False
        
        if not self.use_db:
            LOGGER.warning("MongoDB logging disabled (HOST not set).")
            return
        
        try:
            self.client = MongoClient(
                host=self.config["HOST"],
                port=self.config["PORT"],
                username=self.config["USERNAME"],
                password=self.config["PASSWORD"],
                authSource=self.config["AUTH"]
            )
            self.client.admin.command("ping")
            self.db_name = self.config["DB_NAME"]
            self.db = self.client[self.db_name]
            # TODO: Ping to check whether connected or not
            self.db_connected = True
            LOGGER.info("Connected to MongoDB successfully.")

        except errors.ServerSelectionTimeoutError:
            LOGGER.error("Could not connect to MongoDB (ping timeout).")

        except Exception as e:
            LOGGER.error(f"Error connecting to MongoDB: {e}.")
            
    def insert_log(self, data):
        # TODO: For this demo, database not needed. Currently ignore it. 
        if not self.use_db:
            return
        
        date_str = now().strftime("%y%m%d")
        data["log_time"] = now()
        try:
            self.db[date_str].insert_one(sanitize_for_mongo(data))
            LOGGER.info(f"Insert log to local database successfully.")
        except Exception as e:
            LOGGER.error(f"Error logging to local database: {e}")
        
    def update_log(self, date, requestId, response):
        # TODO: For this demo, database not needed. Currently ignore it. 
        if not self.use_db:
            return
        
        date_str = date.strftime("%y%m%d") if isinstance(date, datetime) else str(date)
        response_res = {
            "response": response,
            "log_time": now()
        }
        try:
            result = self.db[date_str].update_one(
                {"requestId": requestId},
                {"$set": sanitize_for_mongo(response_res)}
            )
            if result.matched_count:
                LOGGER.info(f"Updated log with requestId={requestId} in collection '{date_str}' successfully.")
            else:
                LOGGER.warning(f"No log found with requestId={requestId} in collection '{date_str}'.")
        except Exception as e:
            LOGGER.error(f"Error updating log with requestId={requestId} in collection '{date_str}': {e}")