"""
Integration Manager - Gerencia acesso a integrações configuradas por tenant
Busca credenciais do banco e instancia clientes das integrações
"""

from sqlalchemy.orm import Session
from typing import Optional
from loguru import logger

from models import TenantIntegration
from services.encryption_service import decrypt_api_key
import json


def get_focusnfe_client(tenant_id: int, db: Session):
    """
    Obtém cliente Focus NFe configurado para o tenant
    
    Returns:
        FocusNFeClient ou None se não configurado
    """
    integration = db.query(TenantIntegration).filter(
        TenantIntegration.tenant_id == tenant_id,
        TenantIntegration.integration_type == "focusnfe",
        TenantIntegration.is_active == True
    ).first()
    
    if not integration:
        logger.warning(f"Focus NFe não configurado para tenant {tenant_id}")
        return None
    
    try:
        from integrations.fiscal.focusnfe import FocusNFeClient
        
        token = decrypt_api_key(integration.api_key)
        config = json.loads(integration.config) if integration.config else {}
        environment = config.get("environment", "homologacao")
        
        client = FocusNFeClient(token=token, ambiente=environment)
        
        # Atualizar last_request
        from datetime import datetime
        integration.last_request = datetime.utcnow()
        integration.request_count += 1
        db.commit()
        
        return client
        
    except Exception as e:
        logger.error(f"Erro ao criar cliente Focus NFe: {e}")
        return None


def get_melhor_envio_client(tenant_id: int, db: Session):
    """
    Obtém cliente Melhor Envio configurado para o tenant
    
    Returns:
        MelhorEnvioClient ou None se não configurado
    """
    integration = db.query(TenantIntegration).filter(
        TenantIntegration.tenant_id == tenant_id,
        TenantIntegration.integration_type == "melhor_envio",
        TenantIntegration.is_active == True
    ).first()
    
    if not integration:
        logger.warning(f"Melhor Envio não configurado para tenant {tenant_id}")
        return None
    
    try:
        from integrations.frete.melhor_envio import MelhorEnvioClient
        
        token = decrypt_api_key(integration.access_token)
        config = json.loads(integration.config) if integration.config else {}
        sandbox = config.get("environment") == "sandbox"
        
        client = MelhorEnvioClient(token=token, sandbox=sandbox)
        
        # Atualizar last_request
        from datetime import datetime
        integration.last_request = datetime.utcnow()
        integration.request_count += 1
        db.commit()
        
        return client
        
    except Exception as e:
        logger.error(f"Erro ao criar cliente Melhor Envio: {e}")
        return None


def get_frenet_client(tenant_id: int, db: Session):
    """
    Obtém cliente Frenet configurado para o tenant
    
    Returns:
        FrenetClient ou None se não configurado
    """
    integration = db.query(TenantIntegration).filter(
        TenantIntegration.tenant_id == tenant_id,
        TenantIntegration.integration_type == "frenet",
        TenantIntegration.is_active == True
    ).first()
    
    if not integration:
        logger.warning(f"Frenet não configurado para tenant {tenant_id}")
        return None
    
    try:
        from integrations.frete.frenet import FrenetClient
        
        token = decrypt_api_key(integration.api_key)
        client = FrenetClient(token=token)
        
        # Atualizar last_request
        from datetime import datetime
        integration.last_request = datetime.utcnow()
        integration.request_count += 1
        db.commit()
        
        return client
        
    except Exception as e:
        logger.error(f"Erro ao criar cliente Frenet: {e}")
        return None


def get_evolution_api_client(tenant_id: int, db: Session):
    """
    Obtém cliente Evolution API configurado para o tenant
    
    Returns:
        Dict com configuração ou None se não configurado
    """
    integration = db.query(TenantIntegration).filter(
        TenantIntegration.tenant_id == tenant_id,
        TenantIntegration.integration_type == "evolution_api",
        TenantIntegration.is_active == True
    ).first()
    
    if not integration:
        logger.warning(f"Evolution API não configurado para tenant {tenant_id}")
        return None
    
    try:
        config = json.loads(integration.config) if integration.config else {}
        api_key = decrypt_api_key(integration.api_key)
        
        # Atualizar last_request
        from datetime import datetime
        integration.last_request = datetime.utcnow()
        integration.request_count += 1
        db.commit()
        
        return {
            "api_url": config.get("api_url", ""),
            "api_key": api_key,
            "instance_name": config.get("instance_name", "")
        }
        
    except Exception as e:
        logger.error(f"Erro ao obter config Evolution API: {e}")
        return None


def check_integration_configured(tenant_id: int, integration_type: str, db: Session) -> bool:
    """
    Verifica se uma integração está configurada e ativa para o tenant
    
    Args:
        tenant_id: ID do tenant
        integration_type: Tipo da integração (focusnfe, melhor_envio, etc)
        db: Sessão do banco
        
    Returns:
        True se configurado e ativo, False caso contrário
    """
    integration = db.query(TenantIntegration).filter(
        TenantIntegration.tenant_id == tenant_id,
        TenantIntegration.integration_type == integration_type,
        TenantIntegration.is_active == True
    ).first()
    
    return integration is not None


def get_integration_status(tenant_id: int, integration_type: str, db: Session) -> dict:
    """
    Obtém status detalhado de uma integração
    
    Returns:
        Dict com informações da integração
    """
    integration = db.query(TenantIntegration).filter(
        TenantIntegration.tenant_id == tenant_id,
        TenantIntegration.integration_type == integration_type
    ).first()
    
    if not integration:
        return {
            "configured": False,
            "active": False
        }
    
    return {
        "configured": True,
        "active": integration.is_active,
        "valid": integration.is_valid,
        "last_validation": integration.last_validation,
        "validation_error": integration.validation_error,
        "request_count": integration.request_count,
        "last_request": integration.last_request,
        "environment": integration.environment
    }
