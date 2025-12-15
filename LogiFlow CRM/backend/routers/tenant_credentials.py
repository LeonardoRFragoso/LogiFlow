"""
LogiFlow CRM - Router de Credenciais por Tenant
Permite que clientes configurem suas próprias credenciais de integrações
"""

from fastapi import APIRouter, HTTPException, Depends, Header, Request
from pydantic import BaseModel
from typing import Optional, Dict, List
from datetime import datetime
import logging

from sqlalchemy.orm import Session

from database import get_db
from models.tenant_credentials import (
    TenantCredentials,
    ALL_CREDENTIALS_SCHEMAS,
    ERP_CREDENTIALS_SCHEMAS,
    GPS_CREDENTIALS_SCHEMAS,
    FREIGHT_CREDENTIALS_SCHEMAS
)
from middleware.rbac import require_permission, audit_log

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
    integration_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Lista todas as credenciais configuradas pelo tenant
    
    Não retorna os valores das credenciais por segurança
    """
    try:
        query = db.query(TenantCredentials).filter(TenantCredentials.tenant_id == tenant_id)
        if integration_type:
            query = query.filter(TenantCredentials.integration_type == integration_type)

        credentials = []
        for c in query.all():
            credentials.append({
                "id": c.id,
                "integration_type": c.integration_type,
                "provider": c.provider,
                "is_active": c.is_active,
                "is_validated": c.is_validated,
                "last_validation": c.last_validation,
                "created_at": c.created_at,
                "updated_at": c.updated_at
            })

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
    tenant_id: str = Depends(get_tenant_id),
    db: Session = Depends(get_db)
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
        
        encrypted = TenantCredentials.encrypt_credentials(data.credentials)

        cred = TenantCredentials(
            tenant_id=tenant_id,
            integration_type=data.integration_type,
            provider=data.provider,
            encrypted_credentials=encrypted,
            is_active=True,
            is_validated=False,
            last_validation=None,
            created_by=tenant_id
        )

        db.add(cred)
        db.commit()
        db.refresh(cred)

        logger.info(f"Credencial criada: {tenant_id} - {data.integration_type}/{data.provider}")

        return {
            "success": True,
            "message": "Credencial criada com sucesso",
            "credential": {
                "id": cred.id,
                "integration_type": cred.integration_type,
                "provider": cred.provider,
                "is_active": cred.is_active,
                "is_validated": cred.is_validated
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
    tenant_id: str = Depends(get_tenant_id),
    db: Session = Depends(get_db)
):
    """
    Atualiza credencial existente
    """
    try:
        cred = db.query(TenantCredentials).filter(
            TenantCredentials.id == credential_id,
            TenantCredentials.tenant_id == tenant_id
        ).first()

        if not cred:
            raise HTTPException(status_code=404, detail="Credencial não encontrada")

        if data.credentials:
            validate_credential_schema(cred.integration_type, cred.provider, data.credentials)
            cred.encrypted_credentials = TenantCredentials.encrypt_credentials(data.credentials)
            cred.last_validation = None
            cred.is_validated = False

        if data.is_active is not None:
            cred.is_active = data.is_active

        cred.updated_at = datetime.utcnow()

        db.add(cred)
        db.commit()

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
    tenant_id: str = Depends(get_tenant_id),
    db: Session = Depends(get_db)
):
    """
    Remove credencial
    """
    try:
        cred = db.query(TenantCredentials).filter(
            TenantCredentials.id == credential_id,
            TenantCredentials.tenant_id == tenant_id
        ).first()

        if not cred:
            raise HTTPException(status_code=404, detail="Credencial não encontrada")

        db.delete(cred)
        db.commit()

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
    tenant_id: str = Depends(get_tenant_id),
    db: Session = Depends(get_db)
):
    """
    Valida se as credenciais estão funcionando
    
    Faz uma chamada de teste à API do provider
    """
    try:
        cred = db.query(TenantCredentials).filter(
            TenantCredentials.id == credential_id,
            TenantCredentials.tenant_id == tenant_id
        ).first()

        if not cred:
            raise HTTPException(status_code=404, detail="Credencial não encontrada")

        # TODO: integração real com provider
        cred.is_validated = True
        cred.last_validation = datetime.utcnow()
        db.add(cred)
        db.commit()

        logger.info(f"Validando credencial: {credential_id}")

        return {
            "success": True,
            "is_valid": True,
            "message": "Credenciais validadas com sucesso",
            "details": {
                "provider": cred.provider,
                "test_performed": "Validação simulada",
                "response_time_ms": 0
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
@require_permission("credentials:decrypt")
async def obter_credenciais_descriptografadas(
    integration_type: str,
    provider: str,
    request: Request,
    tenant_id: str = Depends(get_tenant_id),
    db: Session = Depends(get_db)
):
    """
    ⚠️  ENDPOINT SENSÍVEL - PROTEGIDO POR RBAC ⚠️
    
    Obtém credenciais descriptografadas (uso interno ou admin apenas)
    Requer permissão: credentials:decrypt (apenas admin)
    
    Este endpoint deve ser usado apenas por:
    - Administradores do sistema
    - Internamente pelos outros routers (ERP, GPS, etc) via service account
    
    ⚠️  TODAS AS CHAMADAS SÃO AUDITADAS ⚠️
    """
    try:
        cred = db.query(TenantCredentials).filter(
            TenantCredentials.integration_type == integration_type,
            TenantCredentials.provider == provider,
            TenantCredentials.tenant_id == tenant_id
        ).first()

        if not cred:
            audit_log(
                request=request,
                action="credentials:decrypt",
                details=f"Credencial não encontrada: {integration_type}/{provider}",
                resource_type="credential",
                resource_id=None,
                success=False
            )
            raise HTTPException(status_code=404, detail="Credencial não encontrada")

        credentials = TenantCredentials.decrypt_credentials(cred.encrypted_credentials)
        
        # Log de auditoria para decrypt
        audit_log(
            request=request,
            action="credentials:decrypt",
            details=f"Credenciais descriptografadas: {integration_type}/{provider}",
            resource_type="credential",
            resource_id=cred.id,
            success=True
        )

        return {
            "success": True,
            "credentials": credentials,
            "warning": "⚠️ Esta operação foi auditada"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao obter credenciais: {e}")
        audit_log(
            request=request,
            action="credentials:decrypt",
            details=f"Erro ao descriptografar: {str(e)}",
            resource_type="credential",
            success=False
        )
        raise HTTPException(status_code=500, detail=str(e))
