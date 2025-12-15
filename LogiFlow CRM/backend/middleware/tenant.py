"""
Middleware de Multi-Tenancy para LogiFlow CRM

Resolve o tenant a partir de:
1. JWT claim (preferred)
2. Subdomínio
3. Header X-Tenant-ID (fallback)
"""
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import logging
from typing import Optional
import jwt
from config import settings

logger = logging.getLogger(__name__)


class TenantMiddleware(BaseHTTPMiddleware):
    """
    Middleware para resolver e validar o tenant em cada requisição
    """
    
    # Rotas que não requerem tenant
    EXEMPT_PATHS = [
        "/api/v1/auth/login",
        "/api/v1/auth/refresh",
        "/api/v1/auth/register",
        "/health",
        "/ready",
        "/docs",
        "/openapi.json",
        "/api/v1/tenants/",  # Criação de tenant
        "/api/v1/leads/",    # Captura de leads público
    ]
    
    async def dispatch(self, request: Request, call_next):
        """
        Processa cada requisição para resolver o tenant
        """
        path = request.url.path
        
        # Verificar se a rota está isenta
        if self._is_exempt_path(path):
            return await call_next(request)
        
        # Resolver tenant
        tenant_id = await self._resolve_tenant(request)
        
        if not tenant_id:
            return JSONResponse(
                status_code=400,
                content={
                    "error": "Tenant não identificado",
                    "message": "Forneça tenant via JWT, subdomínio ou header X-Tenant-ID"
                }
            )
        
        # Validar se tenant existe e está ativo
        tenant = await self._validate_tenant(tenant_id)
        
        if not tenant:
            return JSONResponse(
                status_code=403,
                content={
                    "error": "Tenant inválido ou inativo",
                    "message": f"Tenant {tenant_id} não encontrado ou desativado"
                }
            )
        
        # Adicionar tenant ao request state
        request.state.tenant_id = tenant_id
        request.state.tenant = tenant
        
        # Log da requisição com tenant
        logger.info(f"Request {request.method} {path} - Tenant: {tenant_id}")
        
        # Processar requisição
        response = await call_next(request)
        
        # Adicionar header de tenant na resposta
        response.headers["X-Tenant-ID"] = str(tenant_id)
        
        return response
    
    def _is_exempt_path(self, path: str) -> bool:
        """Verifica se a rota está isenta de validação de tenant"""
        for exempt_path in self.EXEMPT_PATHS:
            if path.startswith(exempt_path):
                return True
        return False
    
    async def _resolve_tenant(self, request: Request) -> Optional[int]:
        """
        Resolve o tenant na seguinte ordem:
        1. JWT claim 'tenant_id'
        2. Subdomínio (ex: acme.logiflow.com.br)
        3. Header X-Tenant-ID
        """
        # 1. Tentar JWT claim
        tenant_from_jwt = self._get_tenant_from_jwt(request)
        if tenant_from_jwt:
            return tenant_from_jwt
        
        # 2. Tentar subdomínio
        tenant_from_subdomain = self._get_tenant_from_subdomain(request)
        if tenant_from_subdomain:
            return tenant_from_subdomain
        
        # 3. Fallback para header
        tenant_from_header = request.headers.get("X-Tenant-ID")
        if tenant_from_header:
            try:
                return int(tenant_from_header)
            except ValueError:
                logger.warning(f"X-Tenant-ID inválido: {tenant_from_header}")
                return None
        
        return None
    
    def _get_tenant_from_jwt(self, request: Request) -> Optional[int]:
        """Extrai tenant_id do JWT token"""
        auth_header = request.headers.get("Authorization")
        
        if not auth_header or not auth_header.startswith("Bearer "):
            return None
        
        token = auth_header.replace("Bearer ", "")
        
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=["HS256"],
                options={"verify_exp": False}  # Validação de exp é feita em outro lugar
            )
            tenant_id = payload.get("tenant_id")
            if tenant_id:
                return int(tenant_id)
        except jwt.InvalidTokenError as e:
            logger.warning(f"Token JWT inválido: {e}")
        except (ValueError, TypeError) as e:
            logger.warning(f"tenant_id inválido no JWT: {e}")
        
        return None
    
    def _get_tenant_from_subdomain(self, request: Request) -> Optional[int]:
        """
        Extrai tenant_id do subdomínio
        Ex: acme.logiflow.com.br -> busca tenant com slug 'acme'
        """
        host = request.headers.get("Host", "")
        
        # Verificar se é subdomínio válido
        if not host or "localhost" in host or "127.0.0.1" in host:
            return None
        
        parts = host.split(".")
        
        # Ex: acme.logiflow.com.br -> parts = ['acme', 'logiflow', 'com', 'br']
        if len(parts) >= 3:
            subdomain = parts[0]
            
            # Buscar tenant pelo slug (implementar no futuro)
            # tenant = get_tenant_by_slug(subdomain)
            # return tenant.id if tenant else None
            
            logger.info(f"Subdomínio detectado: {subdomain} (lookup não implementado)")
        
        return None
    
    async def _validate_tenant(self, tenant_id: int) -> Optional[dict]:
        """
        Valida se o tenant existe e está ativo
        TODO: Implementar consulta real ao banco
        """
        # Mock - em produção, buscar do banco
        # from database import get_db
        # tenant = db.query(Tenant).filter(Tenant.id == tenant_id, Tenant.ativo == True).first()
        
        # Por enquanto, retornar mock
        return {
            "id": tenant_id,
            "nome": f"Tenant {tenant_id}",
            "ativo": True,
            "plano": "professional"
        }


def get_current_tenant_id(request: Request) -> int:
    """
    Helper para obter tenant_id do request
    Usar em rotas: tenant_id = get_current_tenant_id(request)
    """
    if not hasattr(request.state, "tenant_id"):
        raise HTTPException(
            status_code=400,
            detail="Tenant não identificado nesta requisição"
        )
    return request.state.tenant_id


def get_current_tenant(request: Request) -> dict:
    """
    Helper para obter dados completos do tenant
    Usar em rotas: tenant = get_current_tenant(request)
    """
    if not hasattr(request.state, "tenant"):
        raise HTTPException(
            status_code=400,
            detail="Tenant não identificado nesta requisição"
        )
    return request.state.tenant

