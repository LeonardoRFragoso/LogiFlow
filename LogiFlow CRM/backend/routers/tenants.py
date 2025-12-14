"""
LogiFlow CRM - Router Tenants
Endpoints para gestão de tenants e estatísticas de uso
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Dict
from database import get_db
from models import Tenant
from middleware.plan_limits import get_usage_stats

router = APIRouter()


@router.get("/{tenant_id}/usage")
def get_tenant_usage(
    tenant_id: int,
    db: Session = Depends(get_db)
) -> Dict:
    """
    Retorna estatísticas de uso do tenant
    
    Mostra:
    - Plano atual
    - Limites de usuários, veículos e pedidos
    - Uso atual vs disponível
    - Status do trial
    """
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant não encontrado")
    
    return get_usage_stats(tenant, db)


@router.get("/{tenant_id}/info")
def get_tenant_info(
    tenant_id: int,
    db: Session = Depends(get_db)
) -> Dict:
    """
    Retorna informações básicas do tenant
    """
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant não encontrado")
    
    return {
        "id": tenant.id,
        "company_name": tenant.company_name,
        "subdomain": tenant.subdomain,
        "plan": tenant.plan,
        "status": tenant.status,
        "created_at": tenant.created_at.isoformat(),
        "trial_ends_at": tenant.trial_ends_at.isoformat() if tenant.trial_ends_at else None,
        "limits": {
            "max_users": tenant.max_users if tenant.max_users != -1 else "ilimitado",
            "max_vehicles": tenant.max_vehicles if tenant.max_vehicles != -1 else "ilimitado",
            "max_orders_per_month": tenant.max_orders_per_month if tenant.max_orders_per_month != -1 else "ilimitado"
        }
    }
