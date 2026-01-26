"""
LogiFlow CRM - Integrations Router
Gerenciamento de configurações de integrações por tenant
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Optional, Dict, List
from datetime import datetime
import json

from database import get_db
from models import TenantIntegration, User
from services.encryption_service import encrypt_api_key, decrypt_api_key
from auth import get_current_user
from loguru import logger

router = APIRouter(prefix="/api/integrations", tags=["integrations"])


# ========================================
# Schemas
# ========================================

class IntegrationConfigBase(BaseModel):
    integration_type: str = Field(..., description="Tipo: focusnfe, melhor_envio, frenet, evolution_api, etc")
    environment: str = Field(default="production", description="production ou sandbox")
    is_active: bool = Field(default=True)


class FocusNFeConfig(IntegrationConfigBase):
    integration_type: str = "focusnfe"
    api_token: str = Field(..., description="Token Focus NFe")
    environment: str = Field(default="homologacao", description="homologacao ou producao")


class MelhorEnvioConfig(IntegrationConfigBase):
    integration_type: str = "melhor_envio"
    api_token: str = Field(..., description="Token Melhor Envio")
    environment: str = Field(default="production", description="sandbox ou production")


class FrenetConfig(IntegrationConfigBase):
    integration_type: str = "frenet"
    api_token: str = Field(..., description="Token Frenet")


class EvolutionAPIConfig(IntegrationConfigBase):
    integration_type: str = "evolution_api"
    api_url: str = Field(..., description="URL da Evolution API")
    api_key: str = Field(..., description="API Key Evolution")
    instance_name: str = Field(..., description="Nome da instância")


class IntegrationResponse(BaseModel):
    id: int
    integration_type: str
    environment: str
    is_active: bool
    is_valid: bool
    last_validation: Optional[datetime]
    validation_error: Optional[str]
    request_count: int
    last_request: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ========================================
# Endpoints - CRUD
# ========================================

@router.post("/", response_model=IntegrationResponse)
async def create_integration(
    config: Dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Criar nova integração
    
    Body deve conter:
    - integration_type: focusnfe, melhor_envio, frenet, evolution_api
    - Demais campos específicos de cada integração
    """
    try:
        integration_type = config.get("integration_type")
        
        if not integration_type:
            raise HTTPException(400, "integration_type é obrigatório")
        
        # Verificar se já existe
        existing = db.query(TenantIntegration).filter(
            TenantIntegration.tenant_id == current_user.tenant_id,
            TenantIntegration.integration_type == integration_type
        ).first()
        
        if existing:
            raise HTTPException(400, f"Integração {integration_type} já existe. Use PUT para atualizar.")
        
        # Extrair e criptografar credenciais
        api_key = None
        api_secret = None
        access_token = None
        config_json = {}
        
        if integration_type == "focusnfe":
            api_key = encrypt_api_key(config.get("api_token", ""))
            config_json["environment"] = config.get("environment", "homologacao")
            
        elif integration_type == "melhor_envio":
            access_token = encrypt_api_key(config.get("api_token", ""))
            config_json["environment"] = config.get("environment", "production")
            
        elif integration_type == "frenet":
            api_key = encrypt_api_key(config.get("api_token", ""))
            
        elif integration_type == "evolution_api":
            api_key = encrypt_api_key(config.get("api_key", ""))
            config_json["api_url"] = config.get("api_url", "")
            config_json["instance_name"] = config.get("instance_name", "")
        
        # Criar registro
        integration = TenantIntegration(
            tenant_id=current_user.tenant_id,
            integration_type=integration_type,
            api_key=api_key,
            api_secret=api_secret,
            access_token=access_token,
            config=json.dumps(config_json) if config_json else None,
            environment=config.get("environment", "production"),
            is_active=config.get("is_active", True),
            created_by=current_user.id
        )
        
        db.add(integration)
        db.commit()
        db.refresh(integration)
        
        logger.success(f"✅ Integração {integration_type} criada para tenant {current_user.tenant_id}")
        
        return integration
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao criar integração: {e}")
        db.rollback()
        raise HTTPException(500, f"Erro ao criar integração: {str(e)}")


@router.get("/", response_model=List[IntegrationResponse])
async def list_integrations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Listar todas as integrações do tenant"""
    integrations = db.query(TenantIntegration).filter(
        TenantIntegration.tenant_id == current_user.tenant_id
    ).all()
    
    return integrations


@router.get("/{integration_type}", response_model=IntegrationResponse)
async def get_integration(
    integration_type: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obter configuração de uma integração específica"""
    integration = db.query(TenantIntegration).filter(
        TenantIntegration.tenant_id == current_user.tenant_id,
        TenantIntegration.integration_type == integration_type
    ).first()
    
    if not integration:
        raise HTTPException(404, f"Integração {integration_type} não encontrada")
    
    return integration


@router.put("/{integration_type}", response_model=IntegrationResponse)
async def update_integration(
    integration_type: str,
    config: Dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Atualizar integração existente"""
    integration = db.query(TenantIntegration).filter(
        TenantIntegration.tenant_id == current_user.tenant_id,
        TenantIntegration.integration_type == integration_type
    ).first()
    
    if not integration:
        raise HTTPException(404, f"Integração {integration_type} não encontrada")
    
    try:
        # Atualizar credenciais se fornecidas
        if "api_token" in config:
            if integration_type == "melhor_envio":
                integration.access_token = encrypt_api_key(config["api_token"])
            else:
                integration.api_key = encrypt_api_key(config["api_token"])
        
        if "api_key" in config and integration_type == "evolution_api":
            integration.api_key = encrypt_api_key(config["api_key"])
        
        # Atualizar configurações
        if "environment" in config:
            integration.environment = config["environment"]
        
        if "is_active" in config:
            integration.is_active = config["is_active"]
        
        # Atualizar config JSON
        current_config = json.loads(integration.config) if integration.config else {}
        
        if integration_type == "evolution_api":
            if "api_url" in config:
                current_config["api_url"] = config["api_url"]
            if "instance_name" in config:
                current_config["instance_name"] = config["instance_name"]
        
        integration.config = json.dumps(current_config)
        integration.updated_at = datetime.utcnow()
        
        # Reset validação
        integration.is_valid = False
        integration.last_validation = None
        integration.validation_error = None
        
        db.commit()
        db.refresh(integration)
        
        logger.success(f"✅ Integração {integration_type} atualizada")
        
        return integration
        
    except Exception as e:
        logger.error(f"❌ Erro ao atualizar integração: {e}")
        db.rollback()
        raise HTTPException(500, f"Erro ao atualizar integração: {str(e)}")


@router.delete("/{integration_type}")
async def delete_integration(
    integration_type: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Deletar integração"""
    integration = db.query(TenantIntegration).filter(
        TenantIntegration.tenant_id == current_user.tenant_id,
        TenantIntegration.integration_type == integration_type
    ).first()
    
    if not integration:
        raise HTTPException(404, f"Integração {integration_type} não encontrada")
    
    db.delete(integration)
    db.commit()
    
    logger.info(f"🗑️ Integração {integration_type} deletada")
    
    return {"success": True, "message": f"Integração {integration_type} deletada"}


# ========================================
# Validação de Integrações
# ========================================

@router.post("/{integration_type}/validate")
async def validate_integration(
    integration_type: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Validar credenciais de uma integração"""
    integration = db.query(TenantIntegration).filter(
        TenantIntegration.tenant_id == current_user.tenant_id,
        TenantIntegration.integration_type == integration_type
    ).first()
    
    if not integration:
        raise HTTPException(404, f"Integração {integration_type} não encontrada")
    
    try:
        is_valid = False
        error_message = None
        
        if integration_type == "focusnfe":
            from integrations.fiscal.focusnfe import FocusNFeClient
            
            token = decrypt_api_key(integration.api_key)
            config = json.loads(integration.config) if integration.config else {}
            environment = config.get("environment", "homologacao")
            
            client = FocusNFeClient(token=token, ambiente=environment)
            
            import requests
            response = requests.get(
                f"{client.base_url}/v2/nfes",
                headers=client.headers,
                timeout=10
            )
            
            is_valid = response.status_code in [200, 404]
            if not is_valid:
                error_message = f"HTTP {response.status_code}: {response.text[:200]}"
        
        elif integration_type == "melhor_envio":
            from integrations.frete.melhor_envio import MelhorEnvioClient
            
            token = decrypt_api_key(integration.access_token)
            config = json.loads(integration.config) if integration.config else {}
            sandbox = config.get("environment") == "sandbox"
            
            client = MelhorEnvioClient(token=token, sandbox=sandbox)
            
            import requests
            response = requests.get(
                f"{client.base_url}/api/v2/me",
                headers=client.headers,
                timeout=10
            )
            
            is_valid = response.status_code == 200
            if not is_valid:
                error_message = f"HTTP {response.status_code}: {response.text[:200]}"
        
        elif integration_type == "frenet":
            from integrations.frete.frenet import FrenetClient
            
            token = decrypt_api_key(integration.api_key)
            client = FrenetClient(token=token)
            
            import requests
            response = requests.post(
                f"{client.base_url}/shipping/quote",
                headers=client.headers,
                json={"CEPOrigem": "01310100", "CEPDestino": "20040020"},
                timeout=10
            )
            
            is_valid = response.status_code in [200, 400]
            if not is_valid:
                error_message = f"HTTP {response.status_code}"
        
        elif integration_type == "evolution_api":
            config = json.loads(integration.config) if integration.config else {}
            api_url = config.get("api_url", "")
            api_key = decrypt_api_key(integration.api_key)
            instance_name = config.get("instance_name", "")
            
            import requests
            response = requests.get(
                f"{api_url}/instance/connectionState/{instance_name}",
                headers={"apikey": api_key},
                timeout=10
            )
            
            is_valid = response.status_code == 200
            if not is_valid:
                error_message = f"HTTP {response.status_code}"
        
        # Atualizar status
        integration.is_valid = is_valid
        integration.last_validation = datetime.utcnow()
        integration.validation_error = error_message
        
        db.commit()
        
        if is_valid:
            logger.success(f"✅ Integração {integration_type} validada com sucesso")
            return {"success": True, "message": "Integração validada com sucesso"}
        else:
            logger.warning(f"⚠️ Integração {integration_type} inválida: {error_message}")
            return {"success": False, "error": error_message}
    
    except Exception as e:
        logger.error(f"❌ Erro ao validar integração {integration_type}: {e}")
        
        integration.is_valid = False
        integration.last_validation = datetime.utcnow()
        integration.validation_error = str(e)
        db.commit()
        
        raise HTTPException(400, f"Erro ao validar: {str(e)}")


# ========================================
# Helper - Obter configuração
# ========================================

def get_tenant_integration(
    tenant_id: int,
    integration_type: str,
    db: Session
) -> Optional[TenantIntegration]:
    """Helper para obter integração de um tenant"""
    return db.query(TenantIntegration).filter(
        TenantIntegration.tenant_id == tenant_id,
        TenantIntegration.integration_type == integration_type,
        TenantIntegration.is_active == True
    ).first()
