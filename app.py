import logging
from fastapi import FastAPI
from routes import CALORIE_EST_ROUTER
from utils import LOGGER
LOGGER.info("=================== START APP =====================")

app = FastAPI(
    title="Calorie Estimator",
    description="""Calorie Estimator API""",
    version="0.0.1",
    docs_url="/docs"
)

app.include_router(CALORIE_EST_ROUTER, prefix="/api", tags=["API"])
logging.info("Application load successfully. Start serving ... ")