"""
LogiFlow CRM - Health Check Router
"""

from fastapi import APIRouter, Request
from datetime import datetime

router = APIRouter()


@router.get("/health")
async def health_check(request: Request):
    """Verifica saúde da aplicação"""
    checks = {
        "api": "ok",
        "redis": "unknown",
        "timestamp": datetime.now().isoformat()
    }
    
    # Verificar Redis
    try:
        if hasattr(request.app.state, 'redis'):
            request.app.state.redis.ping()
            checks["redis"] = "ok"
    except Exception:
        checks["redis"] = "error"
    
    # Status geral
    all_ok = all(v == "ok" for k, v in checks.items() if k != "timestamp")
    
    return {
        "status": "healthy" if all_ok else "degraded",
        "checks": checks
    }


@router.get("/ready")
async def readiness_check():
    """Verifica se aplicação está pronta para receber tráfego"""
    return {"ready": True}


@router.get("/live")
async def liveness_check():
    """Verifica se aplicação está viva"""
    return {"alive": True}
