"""
LogiFlow CRM - Router de Monitoramento de Quotas (Admin Only)
Endpoints para visualizar uso de APIs externas
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, List
import logging

from utils.quota_monitor import quota_monitor
from middleware.rbac import require_permission

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/quotas")
@require_permission("admin:view_quotas")
async def listar_quotas() -> Dict:
    """
    Lista uso de quotas de todas as APIs monitoradas
    
    Requer permissão: admin:view_quotas
    """
    apis = [
        "google_maps_distance_matrix",
        # Adicionar outras APIs aqui conforme necessário
    ]
    
    quotas = {}
    
    for api_name in apis:
        try:
            stats = quota_monitor.get_usage_stats(api_name)
            if "error" not in stats:
                quotas[api_name] = stats
        except Exception as e:
            logger.error(f"Erro ao obter stats de {api_name}: {e}")
            quotas[api_name] = {"error": str(e)}
    
    return {
        "success": True,
        "quotas": quotas
    }


@router.get("/quotas/{api_name}")
@require_permission("admin:view_quotas")
async def obter_quota_especifica(api_name: str) -> Dict:
    """
    Obtém detalhes de quota de uma API específica
    
    Args:
        api_name: Nome da API (ex: google_maps_distance_matrix)
    
    Requer permissão: admin:view_quotas
    """
    try:
        stats = quota_monitor.get_usage_stats(api_name)
        
        if "error" in stats:
            raise HTTPException(status_code=404, detail=f"API '{api_name}' não está sendo monitorada")
        
        return {
            "success": True,
            **stats
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao obter quota: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/quotas/{api_name}/reset")
@require_permission("admin:manage_quotas")
async def resetar_quota(api_name: str) -> Dict:
    """
    Reseta contadores de quota (emergência apenas!)
    
    Args:
        api_name: Nome da API
    
    Requer permissão: admin:manage_quotas
    """
    # Esta função é perigosa e deve ser auditada
    logger.warning(
        f"Quota reset requested for {api_name}",
        extra={"api_name": api_name, "action": "quota_reset"}
    )
    
    # Implementar reset se necessário
    # Para produção, considerar não permitir reset manual
    
    return {
        "success": True,
        "message": "Quota reset não implementado por segurança. Os contadores resetam automaticamente no período configurado."
    }

