"""
LogiFlow CRM - Router de Informações de Planos
Fornece informações sobre planos e funcionalidades disponíveis
"""

from fastapi import APIRouter, Header, HTTPException
from typing import Dict, List
from middleware.plan_authorization import (
    PLAN_FEATURES,
    get_tenant_plan,
    get_tenant_features,
    get_tenant_limits,
    get_plan_info
)

router = APIRouter()


@router.get("/plans")
async def listar_planos():
    """
    Lista todos os planos disponíveis e suas funcionalidades
    
    Endpoint público para página de pricing
    """
    return {
        "success": True,
        "plans": {
            plan_id: {
                "id": plan_id,
                "name": plan_data["name"],
                "price": plan_data["price"],
                "features": plan_data["features"],
                "limits": plan_data["limits"]
            }
            for plan_id, plan_data in PLAN_FEATURES.items()
        }
    }


@router.get("/plans/{plan_id}")
async def obter_plano(plan_id: str):
    """
    Obtém detalhes de um plano específico
    """
    plan_data = get_plan_info(plan_id)
    
    if not plan_data:
        raise HTTPException(status_code=404, detail="Plano não encontrado")
    
    return {
        "success": True,
        "plan": {
            "id": plan_id,
            "name": plan_data["name"],
            "price": plan_data["price"],
            "features": plan_data["features"],
            "limits": plan_data["limits"]
        }
    }


@router.get("/my-plan")
async def meu_plano(x_tenant_id: str = Header(None)):
    """
    Retorna informações do plano atual do tenant
    """
    if not x_tenant_id:
        raise HTTPException(status_code=400, detail="X-Tenant-ID header obrigatório")
    
    plan_id = get_tenant_plan(x_tenant_id)
    plan_data = get_plan_info(plan_id)
    features = get_tenant_features(x_tenant_id)
    limits = get_tenant_limits(x_tenant_id)
    
    return {
        "success": True,
        "tenant_id": x_tenant_id,
        "plan": {
            "id": plan_id,
            "name": plan_data.get("name", plan_id),
            "price": plan_data.get("price", 0),
            "features": features,
            "limits": limits
        }
    }


@router.get("/my-features")
async def minhas_funcionalidades(x_tenant_id: str = Header(None)):
    """
    Retorna lista de funcionalidades disponíveis para o tenant
    
    Usado pelo frontend para mostrar/ocultar features
    """
    if not x_tenant_id:
        raise HTTPException(status_code=400, detail="X-Tenant-ID header obrigatório")
    
    features = get_tenant_features(x_tenant_id)
    
    return {
        "success": True,
        "tenant_id": x_tenant_id,
        "features": features,
        "feature_map": {
            "cotacao_automatica": "Cotação Automática",
            "integracao_frete": "Integração de Frete (Melhor Envio, Frenet)",
            "integracao_erp": "Integração ERP (Omie, Bling, Tiny)",
            "nps_satisfacao": "NPS e Satisfação",
            "health_score": "Health Score",
            "customer_success": "Customer Success",
            "rastreamento_gps": "Rastreamento GPS",
            "relatorios_avancados": "Relatórios Avançados",
            "api_access": "Acesso à API",
            "bi_analytics": "BI e Analytics",
            "white_label": "White Label",
            "suporte_prioritario": "Suporte Prioritário"
        }
    }


@router.get("/check-feature/{feature}")
async def verificar_funcionalidade(feature: str, x_tenant_id: str = Header(None)):
    """
    Verifica se o tenant tem acesso a uma funcionalidade específica
    """
    if not x_tenant_id:
        raise HTTPException(status_code=400, detail="X-Tenant-ID header obrigatório")
    
    features = get_tenant_features(x_tenant_id)
    has_access = feature in features
    
    if not has_access:
        # Descobrir qual plano tem essa feature
        required_plan = None
        for plan_id, plan_data in PLAN_FEATURES.items():
            if feature in plan_data["features"]:
                required_plan = {
                    "id": plan_id,
                    "name": plan_data["name"],
                    "price": plan_data["price"]
                }
                break
    else:
        required_plan = None
    
    return {
        "success": True,
        "feature": feature,
        "has_access": has_access,
        "current_plan": get_tenant_plan(x_tenant_id),
        "required_plan": required_plan
    }


@router.get("/compare")
async def comparar_planos():
    """
    Retorna comparação entre planos
    
    Usado na página de pricing
    """
    comparison = []
    
    for plan_id in ["starter", "pro", "enterprise"]:
        plan_data = PLAN_FEATURES[plan_id]
        comparison.append({
            "id": plan_id,
            "name": plan_data["name"],
            "price": plan_data["price"],
            "features_count": len(plan_data["features"]),
            "limits": plan_data["limits"],
            "highlights": {
                "starter": [
                    "Gestão completa de fretes",
                    "Emissão CT-e/MDF-e",
                    "WhatsApp integrado",
                    "Até 10 veículos"
                ],
                "pro": [
                    "Tudo do Starter +",
                    "Cotação automática",
                    "Integração ERP",
                    "NPS e Satisfação",
                    "Até 50 veículos"
                ],
                "enterprise": [
                    "Tudo do Pro +",
                    "Rastreamento GPS",
                    "BI e Analytics",
                    "Veículos ilimitados",
                    "Suporte prioritário"
                ]
            }[plan_id]
        })
    
    return {
        "success": True,
        "plans": comparison
    }
