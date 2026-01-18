"""
LogiFlow CRM - Feature Flags API
=================================
Endpoint para frontend consultar features habilitadas no BETA.
"""

from fastapi import APIRouter
from typing import Dict, Any
from feature_flags import BetaFeatureFlags, get_feature_status_response

router = APIRouter(prefix="/features", tags=["Features"])


@router.get("", response_model=Dict[str, Any])
async def get_features():
    """
    Retorna status de todas as features do sistema.
    
    Usado pelo frontend para:
    - Habilitar/desabilitar funcionalidades
    - Mostrar badges (BETA, Simulação)
    - Exibir mensagens de aviso
    """
    return get_feature_status_response()


@router.get("/{feature_name}", response_model=Dict[str, Any])
async def get_feature_status(feature_name: str):
    """
    Retorna status de uma feature específica.
    
    Returns:
    - status: enabled, beta, simulation, disabled
    - warning: mensagem de aviso (se aplicável)
    - available: se está disponível para uso
    """
    status = BetaFeatureFlags.get_status(feature_name)
    warning = BetaFeatureFlags.get_beta_warning(feature_name)
    
    return {
        "feature": feature_name,
        "status": status,
        "available": BetaFeatureFlags.is_enabled(feature_name),
        "simulation": BetaFeatureFlags.is_simulation(feature_name),
        "warning": warning
    }
