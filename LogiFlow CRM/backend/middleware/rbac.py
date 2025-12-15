"""
Role-Based Access Control (RBAC) e Auditoria

Controla acesso baseado em papéis de usuário e registra ações sensíveis
"""
from fastapi import HTTPException, Depends, Request
from functools import wraps
from typing import List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


# Definição de Roles
class Role:
    ADMIN = "admin"
    MANAGER = "manager"
    USER = "user"
    MOTORISTA = "motorista"
    CLIENTE = "cliente"


# Permissões por role
ROLE_PERMISSIONS = {
    Role.ADMIN: [
        "tenant:manage",
        "user:manage",
        "credentials:read",
        "credentials:write",
        "credentials:delete",
        "credentials:decrypt",  # Permissão sensível
        "billing:manage",
        "settings:manage",
    ],
    Role.MANAGER: [
        "credentials:read",
        "credentials:write",
        "user:view",
        "reports:view",
    ],
    Role.USER: [
        "credentials:read",
        "deliveries:view",
        "deliveries:update",
    ],
    Role.MOTORISTA: [
        "deliveries:view",
        "deliveries:update",
        "location:update",
    ],
    Role.CLIENTE: [
        "tracking:view",
    ]
}


def get_user_role(request: Request) -> str:
    """
    Obtém o role do usuário do request
    TODO: Implementar lógica real baseada em JWT ou sessão
    """
    # Mock - em produção, buscar do JWT payload
    if hasattr(request.state, "user"):
        return request.state.user.get("role", Role.USER)
    return Role.USER


def has_permission(user_role: str, permission: str) -> bool:
    """
    Verifica se um role tem determinada permissão
    """
    permissions = ROLE_PERMISSIONS.get(user_role, [])
    return permission in permissions


def require_permission(permission: str):
    """
    Decorator para proteger endpoints com permissão específica
    
    Uso:
        @router.get("/credentials/{id}/decrypt")
        @require_permission("credentials:decrypt")
        async def decrypt_credential(id: int, request: Request):
            ...
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, request: Request = None, **kwargs):
            if not request:
                # Buscar request nos kwargs
                request = kwargs.get("request")
            
            if not request:
                raise HTTPException(
                    status_code=500,
                    detail="Request object não encontrado"
                )
            
            user_role = get_user_role(request)
            
            if not has_permission(user_role, permission):
                # Log de tentativa de acesso não autorizado
                audit_log(
                    request=request,
                    action=f"DENIED:{permission}",
                    details=f"Role {user_role} tentou acessar {permission}",
                    success=False
                )
                
                raise HTTPException(
                    status_code=403,
                    detail=f"Permissão negada: requer {permission}"
                )
            
            # Log de acesso autorizado
            audit_log(
                request=request,
                action=permission,
                details=f"Acesso autorizado para {user_role}",
                success=True
            )
            
            return await func(*args, request=request, **kwargs)
        
        return wrapper
    return decorator


def require_role(allowed_roles: List[str]):
    """
    Decorator para proteger endpoints com roles específicos
    
    Uso:
        @router.get("/admin/dashboard")
        @require_role([Role.ADMIN, Role.MANAGER])
        async def admin_dashboard(request: Request):
            ...
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, request: Request = None, **kwargs):
            if not request:
                request = kwargs.get("request")
            
            if not request:
                raise HTTPException(
                    status_code=500,
                    detail="Request object não encontrado"
                )
            
            user_role = get_user_role(request)
            
            if user_role not in allowed_roles:
                audit_log(
                    request=request,
                    action="ROLE_DENIED",
                    details=f"Role {user_role} tentou acessar endpoint que requer {allowed_roles}",
                    success=False
                )
                
                raise HTTPException(
                    status_code=403,
                    detail=f"Acesso negado: requer um dos roles: {', '.join(allowed_roles)}"
                )
            
            return await func(*args, request=request, **kwargs)
        
        return wrapper
    return decorator


# Sistema de Auditoria
class AuditLog:
    """
    Registro de auditoria para ações sensíveis
    """
    def __init__(self):
        self.logs = []  # Em produção, salvar no banco de dados
    
    def log(
        self,
        tenant_id: int,
        user_id: Optional[int],
        action: str,
        resource_type: str,
        resource_id: Optional[int],
        details: Optional[dict],
        ip_address: str,
        user_agent: str,
        success: bool
    ):
        """
        Registra uma ação de auditoria
        """
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "tenant_id": tenant_id,
            "user_id": user_id,
            "action": action,
            "resource_type": resource_type,
            "resource_id": resource_id,
            "details": details,
            "ip_address": ip_address,
            "user_agent": user_agent,
            "success": success
        }
        
        # Log no logger
        logger.info(f"[AUDIT] {action} - Tenant:{tenant_id} User:{user_id} Success:{success}")
        
        # Salvar no banco (TODO: implementar)
        self.logs.append(log_entry)
        
        return log_entry


audit_logger = AuditLog()


def audit_log(
    request: Request,
    action: str,
    details: Optional[str] = None,
    resource_type: Optional[str] = None,
    resource_id: Optional[int] = None,
    success: bool = True
):
    """
    Helper para registrar log de auditoria
    """
    tenant_id = getattr(request.state, "tenant_id", None)
    user_id = getattr(request.state, "user", {}).get("id")
    ip_address = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("User-Agent", "unknown")
    
    return audit_logger.log(
        tenant_id=tenant_id,
        user_id=user_id,
        action=action,
        resource_type=resource_type or "unknown",
        resource_id=resource_id,
        details={"message": details} if details else None,
        ip_address=ip_address,
        user_agent=user_agent,
        success=success
    )


def get_audit_logs(tenant_id: int, limit: int = 100) -> List[dict]:
    """
    Obtém logs de auditoria de um tenant
    """
    # TODO: Buscar do banco de dados
    return [log for log in audit_logger.logs if log["tenant_id"] == tenant_id][:limit]

