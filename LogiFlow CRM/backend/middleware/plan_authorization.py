"""
LogiFlow CRM - Middleware de Autorização por Plano
Verifica se o tenant tem permissão para acessar funcionalidades baseado no plano
"""

from fastapi import HTTPException, Header, Depends
from typing import Optional
import logging

logger = logging.getLogger(__name__)


# ===========================================
# Definição de Funcionalidades por Plano
# ===========================================

PLAN_FEATURES = {
    "starter": {
        "name": "Starter",
        "price": 297,
        "features": [
            "cotacoes",
            "pedidos",
            "entregas",
            "motoristas",
            "veiculos",
            "clientes",
            "ocorrencias",
            "fiscal_cte",
            "fiscal_mdfe",
            "whatsapp",
            "dashboard",
            "relatorios_basicos"
        ],
        "limits": {
            "max_users": 3,
            "max_vehicles": 10,
            "max_orders_month": 100
        }
    },
    "pro": {
        "name": "Pro",
        "price": 597,
        "features": [
            # Tudo do Starter
            "cotacoes",
            "pedidos",
            "entregas",
            "motoristas",
            "veiculos",
            "clientes",
            "ocorrencias",
            "fiscal_cte",
            "fiscal_mdfe",
            "whatsapp",
            "dashboard",
            "relatorios_basicos",
            # Recursos Pro
            "cotacao_automatica",
            "integracao_frete",  # Melhor Envio, Frenet
            "integracao_erp",    # Omie, Bling, Tiny
            "nps_satisfacao",
            "health_score",
            "customer_success",
            "relatorios_avancados",
            "api_access"
        ],
        "limits": {
            "max_users": 10,
            "max_vehicles": 50,
            "max_orders_month": 500
        }
    },
    "enterprise": {
        "name": "Enterprise",
        "price": 997,
        "features": [
            # Tudo do Pro
            "cotacoes",
            "pedidos",
            "entregas",
            "motoristas",
            "veiculos",
            "clientes",
            "ocorrencias",
            "fiscal_cte",
            "fiscal_mdfe",
            "whatsapp",
            "dashboard",
            "relatorios_basicos",
            "cotacao_automatica",
            "integracao_frete",
            "integracao_erp",
            "nps_satisfacao",
            "health_score",
            "customer_success",
            "relatorios_avancados",
            "api_access",
            # Recursos Enterprise
            "rastreamento_gps",  # Sascar, Autotrac, Onixsat
            "bi_analytics",
            "white_label",
            "suporte_prioritario",
            "sla_garantido"
        ],
        "limits": {
            "max_users": -1,  # Ilimitado
            "max_vehicles": -1,  # Ilimitado
            "max_orders_month": -1  # Ilimitado
        }
    }
}


# Mapeamento de rotas para funcionalidades
ROUTE_FEATURE_MAP = {
    "/cotacao-automatica": "cotacao_automatica",
    "/melhor-envio": "integracao_frete",
    "/erp": "integracao_erp",
    "/nps": "nps_satisfacao",
    "/health-score": "health_score",
    "/customer-success": "customer_success",
    "/gps": "rastreamento_gps",
    "/tenant-credentials": "integracao_erp",  # Configuração de credenciais requer Pro+
}


# ===========================================
# Funções Helper
# ===========================================

def get_tenant_plan(tenant_id: str) -> str:
    """
    Obtém o plano do tenant
    
    TODO: Buscar do banco de dados
    Por enquanto, retorna 'pro' como padrão
    """
    # TODO: Implementar busca real do banco
    # tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    # return tenant.subscription_plan
    
    return "pro"  # Padrão para desenvolvimento


def check_feature_access(tenant_id: str, feature: str) -> bool:
    """
    Verifica se o tenant tem acesso à funcionalidade
    """
    plan = get_tenant_plan(tenant_id)
    
    if plan not in PLAN_FEATURES:
        logger.warning(f"Plano desconhecido: {plan}")
        return False
    
    return feature in PLAN_FEATURES[plan]["features"]


def check_limit(tenant_id: str, limit_type: str, current_value: int) -> bool:
    """
    Verifica se o tenant está dentro dos limites do plano
    """
    plan = get_tenant_plan(tenant_id)
    
    if plan not in PLAN_FEATURES:
        return False
    
    limit = PLAN_FEATURES[plan]["limits"].get(limit_type, 0)
    
    # -1 significa ilimitado
    if limit == -1:
        return True
    
    return current_value < limit


# ===========================================
# Middleware / Dependency
# ===========================================

def require_feature(feature: str):
    """
    Dependency que verifica se o tenant tem acesso à funcionalidade
    
    Uso:
    @router.get("/endpoint", dependencies=[Depends(require_feature("cotacao_automatica"))])
    """
    def check_access(x_tenant_id: str = Header(None)):
        if not x_tenant_id:
            raise HTTPException(
                status_code=400,
                detail="X-Tenant-ID header obrigatório"
            )
        
        if not check_feature_access(x_tenant_id, feature):
            plan = get_tenant_plan(x_tenant_id)
            plan_name = PLAN_FEATURES.get(plan, {}).get("name", plan)
            
            # Descobrir qual plano tem essa feature
            required_plan = None
            for plan_id, plan_data in PLAN_FEATURES.items():
                if feature in plan_data["features"]:
                    required_plan = plan_data["name"]
                    break
            
            raise HTTPException(
                status_code=403,
                detail={
                    "error": "Funcionalidade não disponível no seu plano",
                    "feature": feature,
                    "current_plan": plan_name,
                    "required_plan": required_plan,
                    "upgrade_url": "/checkout"
                }
            )
        
        return x_tenant_id
    
    return check_access


def require_plan(min_plan: str):
    """
    Dependency que verifica se o tenant tem plano mínimo
    
    Uso:
    @router.get("/endpoint", dependencies=[Depends(require_plan("pro"))])
    """
    plan_hierarchy = ["starter", "pro", "enterprise"]
    
    def check_plan(x_tenant_id: str = Header(None)):
        if not x_tenant_id:
            raise HTTPException(
                status_code=400,
                detail="X-Tenant-ID header obrigatório"
            )
        
        current_plan = get_tenant_plan(x_tenant_id)
        
        if current_plan not in plan_hierarchy:
            raise HTTPException(status_code=403, detail="Plano inválido")
        
        if plan_hierarchy.index(current_plan) < plan_hierarchy.index(min_plan):
            raise HTTPException(
                status_code=403,
                detail={
                    "error": "Plano insuficiente",
                    "current_plan": PLAN_FEATURES[current_plan]["name"],
                    "required_plan": PLAN_FEATURES[min_plan]["name"],
                    "upgrade_url": "/checkout"
                }
            )
        
        return x_tenant_id
    
    return check_plan


def check_usage_limit(limit_type: str, current_value: int):
    """
    Dependency que verifica limites de uso
    
    Uso:
    @router.post("/veiculos", dependencies=[Depends(check_usage_limit("max_vehicles", current_count))])
    """
    def check_limit_dep(x_tenant_id: str = Header(None)):
        if not x_tenant_id:
            raise HTTPException(
                status_code=400,
                detail="X-Tenant-ID header obrigatório"
            )
        
        if not check_limit(x_tenant_id, limit_type, current_value):
            plan = get_tenant_plan(x_tenant_id)
            limit = PLAN_FEATURES[plan]["limits"].get(limit_type, 0)
            
            raise HTTPException(
                status_code=403,
                detail={
                    "error": "Limite do plano atingido",
                    "limit_type": limit_type,
                    "current_value": current_value,
                    "max_allowed": limit,
                    "upgrade_url": "/checkout"
                }
            )
        
        return x_tenant_id
    
    return check_limit_dep


# ===========================================
# Funções de Informação
# ===========================================

def get_plan_info(plan: str) -> dict:
    """Retorna informações sobre um plano"""
    return PLAN_FEATURES.get(plan, {})


def get_tenant_features(tenant_id: str) -> list:
    """Retorna lista de features disponíveis para o tenant"""
    plan = get_tenant_plan(tenant_id)
    return PLAN_FEATURES.get(plan, {}).get("features", [])


def get_tenant_limits(tenant_id: str) -> dict:
    """Retorna limites do plano do tenant"""
    plan = get_tenant_plan(tenant_id)
    return PLAN_FEATURES.get(plan, {}).get("limits", {})
