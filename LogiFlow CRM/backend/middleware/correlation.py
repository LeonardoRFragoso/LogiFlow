"""
Middleware de correlação para incluir X-Correlation-ID em cada requisição.
"""

import uuid
from fastapi import Request
from fastapi.responses import Response
from loguru import logger


async def correlation_middleware(request: Request, call_next):
    correlation_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
    request.state.correlation_id = correlation_id

    # Log de entrada
    logger.info(f"[{correlation_id}] -> {request.method} {request.url.path}")

    response: Response = await call_next(request)
    response.headers["X-Correlation-ID"] = correlation_id

    # Log de saída
    logger.info(f"[{correlation_id}] <- {response.status_code} {request.url.path}")

    return response

