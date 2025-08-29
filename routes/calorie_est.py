import base64
from fastapi import APIRouter, Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse

from .wrapper import request_wrapper
from utils import LOGGER
from .utils import image_sanity_check, validate_output
from calorie_estimator import ESTIMATOR


CALORIE_EST_ROUTER = APIRouter()


class RequestInputs(BaseModel):
    request_id: str
    image: str  # base64 image

@CALORIE_EST_ROUTER.post(
    "/predict",
    tags=["API"],
    summary="Estimate Calories by Image",
    responses={
        200: {"content": {"application/json": {}}, "description": "Estimated calories"}
    }
)
@request_wrapper
async def predict_calorie(request: Request, parsed_input: RequestInputs):
    request_id = parsed_input.request_id
    image_b64 = parsed_input.image

    try:
        image = image_sanity_check(image_b64)
    except Exception as e:
        LOGGER.error(f"Prediction failed: {e}")
        return JSONResponse(
            content={"error": str(e)},
            status_code=400
        )

    try:
        LOGGER.info(f"Request [{request_id}] received, start processing.")

        est_result = await ESTIMATOR.predict(image)
        response = validate_output(est_result)

        return JSONResponse(
            content=response
        )
    except Exception as e:
        LOGGER.error(f"Prediction failed: {e}")
        return JSONResponse(
            content={"error": str(e)},
            status_code=400
        )