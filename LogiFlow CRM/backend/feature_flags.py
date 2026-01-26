"""
LogiFlow CRM - Feature Flags para BETA
=======================================
Sistema simples de controle de funcionalidades para lançamento BETA.
NÃO ADICIONAR NOVO ESCOPO - apenas controlar o que já existe.
"""

from typing import Dict, Any
from enum import Enum


class FeatureStatus(str, Enum):
    """Status das features"""
    ENABLED = "enabled"
    DISABLED = "disabled"
    BETA = "beta"
    SIMULATION = "simulation"


class BetaFeatureFlags:
    """
    Feature Flags para controle do ambiente BETA.
    
    REGRAS:
    - ENABLED: Funcionalidade ativa e testada
    - BETA: Funcionalidade em teste no BETA
    - SIMULATION: Funcionalidade em modo simulação (sem integrações reais)
    - DISABLED: Funcionalidade desativada (escondida do usuário)
    """
    
    # ========== FUNCIONALIDADES CORE (ENABLED) ==========
    AUTH = FeatureStatus.ENABLED
    DASHBOARD = FeatureStatus.ENABLED
    COTACOES = FeatureStatus.ENABLED
    PEDIDOS_FRETE = FeatureStatus.ENABLED
    CLIENTES = FeatureStatus.ENABLED
    
    # ========== FROTA (BETA) ==========
    MOTORISTAS = FeatureStatus.BETA
    VEICULOS = FeatureStatus.BETA
    ENTREGAS = FeatureStatus.BETA
    OCORRENCIAS = FeatureStatus.BETA
    
    # ========== GPS (SIMULATION) ==========
    GPS_TRACKING = FeatureStatus.SIMULATION
    GPS_SASCAR = FeatureStatus.SIMULATION
    GPS_AUTOTRAC = FeatureStatus.SIMULATION
    GPS_ONIXSAT = FeatureStatus.SIMULATION
    
    # ========== INTEGRAÇÕES FISCAIS (SIMULATION) ==========
    FISCAL_CTE = FeatureStatus.SIMULATION
    FISCAL_MDFE = FeatureStatus.SIMULATION
    FOCUS_NFE = FeatureStatus.SIMULATION
    
    # ========== INTEGRAÇÕES FRETE (BETA) ==========
    MELHOR_ENVIO = FeatureStatus.BETA
    FRENET = FeatureStatus.BETA
    COTACAO_AUTOMATICA = FeatureStatus.BETA
    
    # ========== INTEGRAÇÕES ERP (DISABLED BETA) ==========
    ERP_OMIE = FeatureStatus.DISABLED
    ERP_BLING = FeatureStatus.DISABLED
    ERP_TINY = FeatureStatus.DISABLED
    ERP_SYNC_AUTO = FeatureStatus.DISABLED
    
    # ========== CUSTOMER SUCCESS (BETA) ==========
    NPS = FeatureStatus.BETA
    CSAT = FeatureStatus.BETA
    HEALTH_SCORE = FeatureStatus.BETA
    
    # ========== COMUNICAÇÃO (SIMULATION) ==========
    WHATSAPP = FeatureStatus.SIMULATION
    EMAIL_SMTP = FeatureStatus.SIMULATION
    
    # ========== BILLING (BETA) ==========
    MERCADO_PAGO = FeatureStatus.BETA
    ASSINATURAS = FeatureStatus.BETA
    
    @classmethod
    def is_enabled(cls, feature: str) -> bool:
        """Verifica se feature está habilitada (ENABLED ou BETA)"""
        status = getattr(cls, feature.upper(), None)
        return status in [FeatureStatus.ENABLED, FeatureStatus.BETA]
    
    @classmethod
    def is_simulation(cls, feature: str) -> bool:
        """Verifica se feature está em modo simulação"""
        status = getattr(cls, feature.upper(), None)
        return status == FeatureStatus.SIMULATION
    
    @classmethod
    def is_disabled(cls, feature: str) -> bool:
        """Verifica se feature está desabilitada"""
        status = getattr(cls, feature.upper(), None)
        return status == FeatureStatus.DISABLED
    
    @classmethod
    def get_status(cls, feature: str) -> str:
        """Retorna status da feature"""
        return getattr(cls, feature.upper(), FeatureStatus.DISABLED).value
    
    @classmethod
    def get_all_features(cls) -> Dict[str, str]:
        """Retorna mapeamento de todas as features e seus status"""
        return {
            attr: getattr(cls, attr).value
            for attr in dir(cls)
            if not attr.startswith('_') and attr.isupper()
        }
    
    @classmethod
    def get_enabled_features(cls) -> list:
        """Retorna lista de features habilitadas"""
        return [
            attr for attr in dir(cls)
            if not attr.startswith('_') and attr.isupper()
            and getattr(cls, attr) in [FeatureStatus.ENABLED, FeatureStatus.BETA]
        ]
    
    @classmethod
    def get_beta_warning(cls, feature: str) -> str:
        """Retorna mensagem de aviso para features em BETA"""
        status = getattr(cls, feature.upper(), None)
        
        if status == FeatureStatus.BETA:
            return "⚠️ Funcionalidade em BETA - pode conter instabilidades"
        elif status == FeatureStatus.SIMULATION:
            return "🧪 Modo Simulação - dados de exemplo (sem integrações reais)"
        elif status == FeatureStatus.DISABLED:
            return "🚧 Funcionalidade desabilitada - disponível em breve"
        
        return ""


# Atalhos para validação rápida
def require_feature(feature: str):
    """
    Decorator para endpoints que requerem feature habilitada.
    
    Uso:
    @require_feature("GPS_TRACKING")
    async def gps_endpoint():
        ...
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not BetaFeatureFlags.is_enabled(feature):
                from fastapi import HTTPException
                raise HTTPException(
                    status_code=403,
                    detail=f"Feature '{feature}' não disponível no BETA"
                )
            return func(*args, **kwargs)
        return wrapper
    return decorator


def get_feature_status_response() -> Dict[str, Any]:
    """
    Retorna JSON com status de todas as features para frontend.
    
    Uso no endpoint:
    @router.get("/features")
    async def get_features():
        return get_feature_status_response()
    """
    return {
        "features": BetaFeatureFlags.get_all_features(),
        "enabled": BetaFeatureFlags.get_enabled_features(),
        "environment": "BETA",
        "version": "1.0.0-beta"
    }
