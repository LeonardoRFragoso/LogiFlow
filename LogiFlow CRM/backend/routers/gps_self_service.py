"""
LogiFlow CRM - GPS Self-Service
Endpoints para clientes configurarem e testarem suas próprias integrações GPS
"""
from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel, Field
from typing import Optional, Dict, List
from sqlalchemy.orm import Session
import logging

from database import get_db
from models.tenant_credentials import TenantCredentials
from integrations.gps.generic_client import GenericGPSClient

logger = logging.getLogger(__name__)
router = APIRouter()


# ========================================
# Schemas
# ========================================

class TestConnectionRequest(BaseModel):
    """Teste de conexão com provider GPS"""
    provider: str = Field(..., description="Nome do provider: sascar, autotrac, onixsat")
    credentials: Dict = Field(..., description="Credenciais de acesso")
    custom_config: Optional[Dict] = Field(None, description="Configuração customizada (opcional)")


class ConfigureGPSRequest(BaseModel):
    """Configuração de GPS do cliente"""
    provider: str
    credentials: Dict
    base_url: Optional[str] = None
    custom_config: Optional[Dict] = None
    description: Optional[str] = None


class CustomEndpointsRequest(BaseModel):
    """Personalização de endpoints"""
    provider: str
    endpoints: Dict = Field(..., description="Mapa de endpoints personalizados")
    response_mapping: Optional[Dict] = Field(None, description="Mapeamento de campos")


# ========================================
# Endpoints
# ========================================

@router.post("/test-connection")
async def testar_conexao_gps(
    request: TestConnectionRequest,
    x_tenant_id: Optional[str] = Header(None)
):
    """
    Testa conexão com provider GPS ANTES de salvar
    
    Permite ao cliente testar suas credenciais sem persistir no banco.
    Útil para validar antes de salvar.
    """
    try:
        if not x_tenant_id:
            raise HTTPException(status_code=400, detail="X-Tenant-ID obrigatório")
        
        logger.info(f"Testando conexão GPS: {request.provider} para tenant {x_tenant_id}")
        
        # Criar cliente GPS com credenciais fornecidas
        client = GenericGPSClient(
            provider=request.provider,
            credentials=request.credentials,
            simulation_mode=False  # Forçar chamada real
        )
        
        # Aplicar configuração customizada se fornecida
        if request.custom_config:
            client.config.update(request.custom_config)
        
        # Teste 1: Listar veículos
        resultado_veiculos = client.listar_veiculos()
        
        if not resultado_veiculos.get("success"):
            return {
                "success": False,
                "error": "Falha ao listar veículos",
                "details": resultado_veiculos.get("error"),
                "hint": resultado_veiculos.get("hint"),
                "recommendation": "Verifique se as credenciais e Base URL estão corretas"
            }
        
        # Teste 2: Se houver veículos, testar posição do primeiro
        veiculos = resultado_veiculos.get("veiculos", [])
        teste_posicao = None
        
        if veiculos and len(veiculos) > 0:
            primeiro_veiculo = veiculos[0]
            placa = primeiro_veiculo.get("placa") or primeiro_veiculo.get("id")
            
            if placa:
                resultado_posicao = client.obter_posicao_veiculo(placa)
                teste_posicao = {
                    "success": resultado_posicao.get("success"),
                    "placa": placa,
                    "posicao": resultado_posicao.get("posicao") if resultado_posicao.get("success") else None,
                    "error": resultado_posicao.get("error") if not resultado_posicao.get("success") else None
                }
        
        return {
            "success": True,
            "message": "Conexão testada com sucesso!",
            "provider": request.provider,
            "testes": {
                "listar_veiculos": {
                    "success": True,
                    "total_veiculos": len(veiculos),
                    "veiculos_sample": veiculos[:3] if len(veiculos) > 0 else []
                },
                "obter_posicao": teste_posicao
            },
            "recommendation": "Tudo OK! Você pode salvar essas credenciais."
        }
    
    except Exception as e:
        logger.error(f"Erro ao testar conexão GPS: {e}")
        return {
            "success": False,
            "error": str(e),
            "recommendation": "Verifique os logs e a documentação da API do provider"
        }


@router.post("/configure")
async def configurar_gps(
    request: ConfigureGPSRequest,
    x_tenant_id: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """
    Configura integração GPS do cliente
    
    Salva as credenciais criptografadas no banco.
    """
    try:
        if not x_tenant_id:
            raise HTTPException(status_code=400, detail="X-Tenant-ID obrigatório")
        
        logger.info(f"Configurando GPS: {request.provider} para tenant {x_tenant_id}")
        
        # Preparar credenciais completas
        full_credentials = request.credentials.copy()
        
        if request.base_url:
            full_credentials["base_url"] = request.base_url
        
        if request.custom_config:
            full_credentials["custom_config"] = request.custom_config
        
        # Criar ou atualizar credencial
        existing = db.query(TenantCredentials).filter(
            TenantCredentials.tenant_id == x_tenant_id,
            TenantCredentials.integration_type == "gps",
            TenantCredentials.provider == request.provider
        ).first()
        
        if existing:
            # Atualizar
            existing.encrypted_credentials = TenantCredentials.encrypt_credentials(full_credentials)
            existing.is_active = True
            existing.is_validated = False  # Resetar validação
            logger.info(f"Credencial GPS atualizada: {request.provider}")
        else:
            # Criar nova
            new_cred = TenantCredentials(
                tenant_id=x_tenant_id,
                integration_type="gps",
                provider=request.provider,
                encrypted_credentials=TenantCredentials.encrypt_credentials(full_credentials),
                is_active=True,
                is_validated=False
            )
            db.add(new_cred)
            logger.info(f"Nova credencial GPS criada: {request.provider}")
        
        db.commit()
        
        return {
            "success": True,
            "message": f"Provider GPS {request.provider} configurado com sucesso!",
            "provider": request.provider,
            "next_steps": [
                "Teste a integração em: GPS → Rastreamento",
                "Configure alertas e notificações",
                "Integre com rotas de entrega"
            ]
        }
    
    except Exception as e:
        db.rollback()
        logger.error(f"Erro ao configurar GPS: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/customize-endpoints")
async def personalizar_endpoints(
    request: CustomEndpointsRequest,
    x_tenant_id: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """
    Personaliza endpoints e mapeamento de campos
    
    Para clientes cujo provider tem API com estrutura diferente do padrão.
    """
    try:
        if not x_tenant_id:
            raise HTTPException(status_code=400, detail="X-Tenant-ID obrigatório")
        
        # Buscar credencial existente
        cred = db.query(TenantCredentials).filter(
            TenantCredentials.tenant_id == x_tenant_id,
            TenantCredentials.integration_type == "gps",
            TenantCredentials.provider == request.provider
        ).first()
        
        if not cred:
            raise HTTPException(
                status_code=404,
                detail=f"Provider {request.provider} não configurado. Configure primeiro em /configure"
            )
        
        # Descriptografar credenciais atuais
        current_creds = TenantCredentials.decrypt_credentials(cred.encrypted_credentials)
        
        # Adicionar/atualizar custom_config
        custom_config = current_creds.get("custom_config", {})
        custom_config["endpoints"] = request.endpoints
        
        if request.response_mapping:
            custom_config["response_mapping"] = request.response_mapping
        
        current_creds["custom_config"] = custom_config
        
        # Criptografar e salvar
        cred.encrypted_credentials = TenantCredentials.encrypt_credentials(current_creds)
        cred.is_validated = False  # Resetar validação
        
        db.commit()
        
        return {
            "success": True,
            "message": "Endpoints personalizados salvos!",
            "provider": request.provider,
            "custom_config": custom_config
        }
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Erro ao personalizar endpoints: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/providers-supported")
async def listar_providers_suportados():
    """
    Lista todos os providers GPS suportados
    
    Retorna informações sobre quais providers o cliente pode configurar.
    """
    return {
        "success": True,
        "providers": [
            {
                "id": "sascar",
                "name": "Sascar",
                "description": "Rastreamento via Sascar",
                "auth_type": "bearer",
                "required_fields": ["api_key"],
                "optional_fields": ["api_secret", "base_url"],
                "documentation_url": "https://www.sascar.com.br"
            },
            {
                "id": "autotrac",
                "name": "Autotrac",
                "description": "Rastreamento via Autotrac",
                "auth_type": "basic",
                "required_fields": ["username", "password"],
                "optional_fields": ["base_url"],
                "documentation_url": "https://www.autotrac.com.br"
            },
            {
                "id": "onixsat",
                "name": "Onixsat",
                "description": "Rastreamento via Onixsat",
                "auth_type": "bearer",
                "required_fields": ["api_token"],
                "optional_fields": ["base_url"],
                "documentation_url": "https://www.onixsat.com.br"
            },
            {
                "id": "custom",
                "name": "Provider Customizado",
                "description": "Configure qualquer provider GPS com API REST",
                "auth_type": "custom",
                "required_fields": ["base_url", "credentials"],
                "optional_fields": ["custom_config"],
                "documentation_url": None
            }
        ]
    }


@router.get("/my-configuration")
async def obter_minha_configuracao(
    x_tenant_id: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """
    Retorna a configuração GPS atual do cliente (sem credenciais sensíveis)
    """
    try:
        if not x_tenant_id:
            raise HTTPException(status_code=400, detail="X-Tenant-ID obrigatório")
        
        creds = db.query(TenantCredentials).filter(
            TenantCredentials.tenant_id == x_tenant_id,
            TenantCredentials.integration_type == "gps",
            TenantCredentials.is_active == True
        ).all()
        
        providers_configurados = []
        
        for cred in creds:
            # Não retornar credenciais sensíveis
            providers_configurados.append({
                "provider": cred.provider,
                "is_active": cred.is_active,
                "is_validated": cred.is_validated,
                "last_validation": cred.last_validation.isoformat() if cred.last_validation else None,
                "created_at": cred.created_at.isoformat() if cred.created_at else None,
                "has_custom_config": "custom_config" in TenantCredentials.decrypt_credentials(cred.encrypted_credentials)
            })
        
        return {
            "success": True,
            "tenant_id": x_tenant_id,
            "providers_configurados": providers_configurados,
            "total": len(providers_configurados)
        }
    
    except Exception as e:
        logger.error(f"Erro ao obter configuração: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/remove/{provider}")
async def remover_configuracao(
    provider: str,
    x_tenant_id: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """
    Remove configuração de um provider GPS
    """
    try:
        if not x_tenant_id:
            raise HTTPException(status_code=400, detail="X-Tenant-ID obrigatório")
        
        cred = db.query(TenantCredentials).filter(
            TenantCredentials.tenant_id == x_tenant_id,
            TenantCredentials.integration_type == "gps",
            TenantCredentials.provider == provider
        ).first()
        
        if not cred:
            raise HTTPException(status_code=404, detail=f"Provider {provider} não encontrado")
        
        db.delete(cred)
        db.commit()
        
        logger.info(f"Credencial GPS removida: {provider} do tenant {x_tenant_id}")
        
        return {
            "success": True,
            "message": f"Provider {provider} removido com sucesso"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Erro ao remover configuração: {e}")
        raise HTTPException(status_code=500, detail=str(e))

