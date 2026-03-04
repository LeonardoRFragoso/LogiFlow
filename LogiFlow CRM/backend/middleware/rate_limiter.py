"""
Rate Limiting Middleware
========================
Proteção contra DDoS e abuso de API usando slowapi
"""
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request, status
from fastapi.responses import JSONResponse
from loguru import logger

# Inicializar limiter
limiter = Limiter(key_func=get_remote_address)


async def rate_limit_error_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    """
    Handler customizado para erros de rate limit
    Retorna JSON em vez de HTML
    """
    logger.warning(f"Rate limit exceeded for {get_remote_address(request)}")
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={
            "detail": "Rate limit exceeded. Try again later.",
            "retry_after": exc.detail
        }
    )


def setup_rate_limiter(app):
    """
    Setup do rate limiter na aplicação
    
    Uso:
    @limiter.limit("5/minute")
    async def my_endpoint(request: Request):
        pass
    """
    # Limites globais
    # 100 requests per minute por IP
    
    # Error handler
    app.add_exception_handler(RateLimitExceeded, rate_limit_error_handler)
    
    logger.info("Rate limiter configured")
    
    return limiter


# Presets de limites recomendados
RATE_LIMITS = {
    "auth_login": "5/minute",           # Login: 5x por minuto
    "auth_register": "3/minute",        # Registro: 3x por minuto
    "default": "100/minute",            # Default: 100x por minuto
    "heavy": "10/minute",               # Heavy operations: 10x
    "webhook": "1000/hour",             # Webhooks: 1000x por hora
}
