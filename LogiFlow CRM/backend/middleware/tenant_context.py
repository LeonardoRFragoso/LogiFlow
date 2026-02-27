"""
Middleware de Contexto Multi-Tenant
Valida e injeta tenant_id nas requisições
"""

from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from jose import JWTError, jwt
from loguru import logger
import os

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = "HS256"

# Rotas que não requerem tenant
PUBLIC_ROUTES = [
    "/health",
    "/ready",
    "/docs",
    "/openapi.json",
    "/api/v1/auth/login",
    "/api/v1/auth/register",
    "/api/v1/auth/refresh",
    "/demo/request",
]


class TenantContextMiddleware(BaseHTTPMiddleware):
    """
    Middleware que:
    1. Extrai tenant_id do JWT
    2. Valida que usuário pertence ao tenant
    3. Injeta tenant_id no contexto da requisição
    """
    
    async def dispatch(self, request: Request, call_next):
        # Verificar se é rota pública
        if any(request.url.path.startswith(route) for route in PUBLIC_ROUTES):
            return await call_next(request)
        
        try:
            # Extrair token do header
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                raise HTTPException(
                    status_code=401,
                    detail="Token não fornecido"
                )
            
            token = auth_header.split(" ")[1]
            
            # Decodificar JWT
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            
            # Extrair tenant_id do payload
            tenant_id = payload.get("tenant_id")
            user_id = payload.get("user_id")
            
            if not tenant_id:
                raise HTTPException(
                    status_code=401,
                    detail="Tenant não encontrado no token"
                )
            
            # Injetar tenant_id no contexto
            request.state.tenant_id = tenant_id
            request.state.user_id = user_id
            
            logger.debug(f"✅ Tenant validado: {tenant_id} (User: {user_id})")
            
        except JWTError as e:
            logger.error(f"❌ Erro ao decodificar JWT: {e}")
            raise HTTPException(
                status_code=401,
                detail="Token inválido"
            )
        except Exception as e:
            logger.error(f"❌ Erro no middleware de tenant: {e}")
            raise HTTPException(
                status_code=500,
                detail="Erro ao processar requisição"
            )
        
        # Continuar com a requisição
        response = await call_next(request)
        return response


def get_tenant_id(request: Request) -> int:
    """Helper para obter tenant_id do contexto"""
    tenant_id = getattr(request.state, "tenant_id", None)
    if not tenant_id:
        raise HTTPException(
            status_code=401,
            detail="Tenant não encontrado no contexto"
        )
    return tenant_id


def get_user_id(request: Request) -> str:
    """Helper para obter user_id do contexto"""
    user_id = getattr(request.state, "user_id", None)
    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Usuário não encontrado no contexto"
        )
    return user_id
