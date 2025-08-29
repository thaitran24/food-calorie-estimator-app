
import json
import inspect
import functools
from fastapi import Request, Response

from utils import DB_LOGGER, LOGGER

import asyncio

def safe_log_insert(data):
    try:
        DB_LOGGER.insert_log(data)
    except Exception as e:
        LOGGER.error(f"Async log insert failed: {e}")

def request_wrapper(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        request: Request = kwargs.get("request")
        request_id = None

        if request:
            body = await request.body()
            LOGGER.info(f"Incoming request: {request.method} {request.url}")
            LOGGER.info(f"Headers: {dict(request.headers)}")

            body_str = body.decode(errors="ignore")
            try:
                body_log = json.loads(body_str)
                request_id = body_log.get("request_id") if isinstance(body_log, dict) else None
            except Exception:
                body_log = {"raw": body_str}

            # schedule log insert asynchronously
            asyncio.create_task(
                asyncio.to_thread(safe_log_insert, {
                    "type": "request",
                    "method": request.method,
                    "url": str(request.url),
                    "headers": dict(request.headers),
                    "body": body_log,
                    "request_id": request_id,
                })
            )

        # execute wrapped function
        response: Response = await func(*args, **kwargs) if inspect.iscoroutinefunction(func) else func(*args, **kwargs)

        if isinstance(response, Response):
            LOGGER.info(f"Response status: {response.status_code}")
            try:
                body_str = response.body.decode()
                try:
                    body_log = json.loads(body_str)
                    if isinstance(body_log, dict) and "request_id" in body_log:
                        request_id = body_log["request_id"]
                except Exception:
                    body_log = {"raw": body_str}

                # schedule log insert asynchronously
                asyncio.create_task(
                    asyncio.to_thread(safe_log_insert, {
                        "type": "response",
                        "status_code": response.status_code,
                        "body": body_log,
                        "request_id": request_id,
                    })
                )
            except Exception as e:
                LOGGER.warning(f"Response body not loggable: {e}")

        return response

    return wrapper