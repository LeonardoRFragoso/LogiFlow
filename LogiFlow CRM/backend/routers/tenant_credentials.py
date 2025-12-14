"""
LogiFlow CRM - Router de Credenciais por Tenant
Permite que clientes configurem suas próprias credenciais de integrações
"""

from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel
from typing import Optional, Dict, List
from datetime import datetime
import logging

from models.tenant_credentials import (
    TenantCredentials,
    ALL_CREDENTIALS_SCHEMAS,
    ERP_CREDENTIALS_SCHEMAS,
    GPS_CREDENTIALS_SCHEMAS,
    FREIGHT_CREDENTIALS_SCHEMAS
)

logger = logging.getLogger(__name__)
router = APIRouter()


# ===========================================
# Schemas Pydantic
# ===========================================

class CredentialCreate(BaseModel):
    integration_type: str  # 'erp', 'gps', 'freight'
    provider: str  # 'omie', 'bling', 'sascar', etc
    credentials: Dict[str, str]


class CredentialUpdate(BaseModel):
    credentials: Dict[str, str]
    is_active: Optional[bool] = None


class CredentialResponse(BaseModel):
    id: int
    integration_type: str
    provider: str
    is_active: bool
    is_validated: bool
    last_validation: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    # Não retorna credenciais por segurança


class CredentialValidationResponse(BaseModel):
    is_valid: bool
    message: str
    details: Optional[Dict] = None


# ===========================================
# Helpers
# ===========================================

def get_tenant_id(x_tenant_id: str = Header(None)) -> str:
    """Obtém tenant_id do header"""
    if not x_tenant_id:
        raise HTTPException(status_code=400, detail="X-Tenant-ID header obrigatório")
    return x_tenant_id


def validate_credential_schema(integration_type: str, provider: str, credentials: Dict) -> bool:
    """Valida se as credenciais têm os campos necessários"""
    if integration_type not in ALL_CREDENTIALS_SCHEMAS:
        raise HTTPException(status_code=400, detail=f"Tipo de integração inválido: {integration_type}")
    
    if provider not in ALL_CREDENTIALS_SCHEMAS[integration_type]:
        raise HTTPException(status_code=400, detail=f"Provider inválido: {provider}")
    
    schema = ALL_CREDENTIALS_SCHEMAS[integration_type][provider]
    required_fields = schema["required"]
    
    for field in required_fields:
        if field not in credentials or not credentials[field]:
            raise HTTPException(
                status_code=400,
                detail=f"Campo obrigatório ausente: {field}"
            )
    
    return True


# ===========================================
# Endpoints - Listar Schemas Disponíveis
# ===========================================

@router.get("/schemas")
async def listar_schemas_disponiveis():
    """
    Lista todos os schemas de credenciais disponíveis
    
    Retorna informações sobre quais integrações estão disponíveis
    e quais campos são necessários para cada uma
    """
    return {
        "success": True,
        "schemas": {
            "erp": {
                provider: {
                    "display_name": schema["display_name"],
                    "fields": schema["fields"],
                    "required": schema["required"]
                }
                for provider, schema in ERP_CREDENTIALS_SCHEMAS.items()
            },
            "gps": {
                provider: {
                    "display_name": schema["display_name"],
                    "fields": schema["fields"],
                    "required": schema["required"]
                }
                for provider, schema in GPS_CREDENTIALS_SCHEMAS.items()
            },
            "freight": {
                provider: {
                    "display_name": schema["display_name"],
                    "fields": schema["fields"],
                    "required": schema["required"]
                }
                for provider, schema in FREIGHT_CREDENTIALS_SCHEMAS.items()
            }
        }
    }


# ===========================================
# Endpoints - CRUD de Credenciais
# ===========================================

@router.get("/credentials")
async def listar_credenciais(
    tenant_id: str = Depends(get_tenant_id),
    integration_type: Optional[str] = None
):
    """
    Lista todas as credenciais configuradas pelo tenant
    
    Não retorna os valores das credenciais por segurança
    """
    try:
        # TODO: Buscar do banco de dados
        # Por enquanto, retorna exemplo
        
        credentials = [
            {
                "id": 1,
                "integration_type": "erp",
                "provider": "omie",
                "is_active": True,
                "is_validated": True,
                "last_validation": datetime.now().isoformat(),
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
        ]
        
        if integration_type:
            credentials = [c for c in credentials if c["integration_type"] == integration_type]
        
        return {
            "success": True,
            "tenant_id": tenant_id,
            "credentials": credentials
        }
        
    except Exception as e:
        logger.error(f"Erro ao listar credenciais: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/credentials")
async def criar_credencial(
    data: CredentialCreate,
    tenant_id: str = Depends(get_tenant_id)
):
    """
    Cria nova credencial de integração para o tenant
    
    As credenciais são criptografadas antes de serem salvas
    """
    try:
        # Validar schema
        validate_credential_schema(
            data.integration_type,
            data.provider,
            data.credentials
        )
        
        # Criptografar credenciais
        encrypted = TenantCredentials.encrypt_credentials(data.credentials)
        
        # TODO: Salvar no banco de dados
        # Por enquanto, apenas simula
        
        logger.info(f"Credencial criada: {tenant_id} - {data.integration_type}/{data.provider}")
        
        return {
            "success": True,
            "message": "Credencial criada com sucesso",
            "credential": {
                "id": 1,
                "integration_type": data.integration_type,
                "provider": data.provider,
                "is_active": True,
                "is_validated": False
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao criar credencial: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/credentials/{credential_id}")
async def atualizar_credencial(
    credential_id: int,
    data: CredentialUpdate,
    tenant_id: str = Depends(get_tenant_id)
):
    """
    Atualiza credencial existente
    """
    try:
        # TODO: Buscar credencial do banco
        # TODO: Verificar se pertence ao tenant
        # TODO: Atualizar credenciais criptografadas
        
        logger.info(f"Credencial atualizada: {credential_id}")
        
        return {
            "success": True,
            "message": "Credencial atualizada com sucesso"
        }
        
    except Exception as e:
        logger.error(f"Erro ao atualizar credencial: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/credentials/{credential_id}")
async def deletar_credencial(
    credential_id: int,
    tenant_id: str = Depends(get_tenant_id)
):
    """
    Remove credencial
    """
    try:
        # TODO: Buscar credencial do banco
        # TODO: Verificar se pertence ao tenant
        # TODO: Deletar
        
        logger.info(f"Credencial deletada: {credential_id}")
        
        return {
            "success": True,
            "message": "Credencial removida com sucesso"
        }
        
    except Exception as e:
        logger.error(f"Erro ao deletar credencial: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ===========================================
# Endpoints - Validação de Credenciais
# ===========================================

@router.post("/credentials/{credential_id}/validate")
async def validar_credencial(
    credential_id: int,
    tenant_id: str = Depends(get_tenant_id)
):
    """
    Valida se as credenciais estão funcionando
    
    Faz uma chamada de teste à API do provider
    """
    try:
        # TODO: Buscar credencial do banco
        # TODO: Descriptografar
        # TODO: Fazer chamada de teste à API
        # TODO: Atualizar is_validated e last_validation
        
        logger.info(f"Validando credencial: {credential_id}")
        
        return {
            "success": True,
            "is_valid": True,
            "message": "Credenciais validadas com sucesso",
            "details": {
                "provider": "omie",
                "test_performed": "Listagem de clientes",
                "response_time_ms": 245
            }
        }
        
    except Exception as e:
        logger.error(f"Erro ao validar credencial: {e}")
        return {
            "success": False,
            "is_valid": False,
            "message": f"Erro na validação: {str(e)}"
        }


# ===========================================
# Endpoints - Obter Credenciais (Interno)
# ===========================================

@router.get("/credentials/{integration_type}/{provider}/decrypt")
async def obter_credenciais_descriptografadas(
    integration_type: str,
    provider: str,
    tenant_id: str = Depends(get_tenant_id)
):
    """
    Obtém credenciais descriptografadas (uso interno apenas)
    
    Este endpoint deve ser protegido e usado apenas internamente
    pelos outros routers (ERP, GPS, etc)
    """
    try:
        # TODO: Buscar credencial do banco
        # TODO: Verificar se pertence ao tenant
        # TODO: Descriptografar
        
        # Exemplo:
        credentials = {
            "app_key": "123456",
            "app_secret": "secret123"
        }
        
        return {
            "success": True,
            "credentials": credentials
        }
        
    except Exception as e:
        logger.error(f"Erro ao obter credenciais: {e}")
        raise HTTPException(status_code=500, detail=str(e))
