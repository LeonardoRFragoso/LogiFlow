"""
LogiFlow CRM - Integrações Self-Service
Endpoints para clientes configurarem suas próprias integrações (Google Maps, ERPs, etc)
"""
from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel, Field
from typing import Optional, Dict, List
from sqlalchemy.orm import Session
import logging
import requests

from database import get_db
from models.tenant_credentials import TenantCredentials
from integrations.maps.distance_matrix import DistanceMatrixClient
from integrations.erp.omie import OmieClient
from integrations.erp.bling import BlingClient

logger = logging.getLogger(__name__)
router = APIRouter()


# ========================================
# Schemas
# ========================================

class TestIntegrationRequest(BaseModel):
    """Teste de integração genérica"""
    integration_type: str = Field(..., description="Tipo: maps, erp_omie, erp_bling")
    credentials: Dict = Field(..., description="Credenciais de acesso")


class ConfigureIntegrationRequest(BaseModel):
    """Configuração de integração"""
    integration_type: str = Field(..., description="Tipo da integração")
    provider: str = Field(..., description="Provider específico")
    credentials: Dict
    description: Optional[str] = None


# ========================================
# Google Maps
# ========================================

@router.post("/test/google-maps")
async def testar_google_maps(
    request: TestIntegrationRequest,
    x_tenant_id: Optional[str] = Header(None)
):
    """
    Testa credenciais do Google Maps ANTES de salvar
    
    O cliente precisa ter:
    - Google Cloud Project
    - Distance Matrix API habilitada
    - API Key com permissões
    """
    try:
        if not x_tenant_id:
            raise HTTPException(status_code=400, detail="X-Tenant-ID obrigatório")
        
        api_key = request.credentials.get("api_key")
        if not api_key:
            raise HTTPException(status_code=400, detail="api_key é obrigatório")
        
        logger.info(f"Testando Google Maps para tenant {x_tenant_id}")
        
        # Criar cliente e testar
        client = DistanceMatrixClient(api_key=api_key)
        
        # Teste: Calcular distância São Paulo → Rio de Janeiro
        resultado = client.calcular_distancia_por_cep(
            cep_origem="01310100",  # Av. Paulista, SP
            cep_destino="20040020"   # Centro, RJ
        )
        
        if not resultado.get("success"):
            return {
                "success": False,
                "error": "Falha ao calcular distância de teste",
                "details": resultado.get("error"),
                "recommendation": "Verifique se a API Key está correta e se a Distance Matrix API está habilitada"
            }
        
        distancia_km = resultado["distancia"]["km"]
        tempo_horas = resultado["duracao"]["horas"]
        
        return {
            "success": True,
            "message": "Google Maps configurado com sucesso!",
            "test_result": {
                "route": "São Paulo → Rio de Janeiro",
                "distance_km": distancia_km,
                "duration_hours": tempo_horas,
                "origin": resultado["origem"],
                "destination": resultado["destino"]
            },
            "quota_info": {
                "cost_per_request": "$0.005",
                "free_tier": "$200/mês (~40,000 requisições)",
                "recommendation": "Configure alertas de quota no Google Cloud Console"
            },
            "recommendation": "Tudo OK! Você pode salvar essas credenciais."
        }
    
    except Exception as e:
        logger.error(f"Erro ao testar Google Maps: {e}")
        return {
            "success": False,
            "error": str(e),
            "recommendation": "Verifique se a API Key está correta e se a API está habilitada no Google Cloud Console"
        }


# ========================================
# ERP Omie
# ========================================

@router.post("/test/erp-omie")
async def testar_omie(
    request: TestIntegrationRequest,
    x_tenant_id: Optional[str] = Header(None)
):
    """
    Testa credenciais do Omie ANTES de salvar
    
    O cliente precisa ter:
    - Conta Omie
    - App Key e App Secret
    """
    try:
        if not x_tenant_id:
            raise HTTPException(status_code=400, detail="X-Tenant-ID obrigatório")
        
        app_key = request.credentials.get("app_key")
        app_secret = request.credentials.get("app_secret")
        
        if not app_key or not app_secret:
            raise HTTPException(
                status_code=400,
                detail="app_key e app_secret são obrigatórios"
            )
        
        logger.info(f"Testando Omie para tenant {x_tenant_id}")
        
        # Criar cliente
        client = OmieClient(app_key=app_key, app_secret=app_secret)
        
        # Teste 1: Listar categorias (endpoint simples para validar credenciais)
        resultado = client.listar_categorias()
        
        if not resultado.get("success"):
            return {
                "success": False,
                "error": "Falha ao conectar com Omie",
                "details": resultado.get("error"),
                "recommendation": "Verifique se App Key e App Secret estão corretos no painel Omie"
            }
        
        # Teste 2: Listar clientes (para validar permissões)
        clientes = client.listar_clientes(pagina=1, registros_por_pagina=1)
        
        return {
            "success": True,
            "message": "Omie configurado com sucesso!",
            "test_result": {
                "connection": "✓ Conectado",
                "permissions": "✓ Permissões OK",
                "total_customers": clientes.get("total_de_registros", 0) if clientes.get("success") else "N/A"
            },
            "available_features": [
                "Sincronizar clientes",
                "Criar pedidos",
                "Consultar produtos",
                "Gerar faturas"
            ],
            "recommendation": "Tudo OK! Você pode salvar essas credenciais."
        }
    
    except Exception as e:
        logger.error(f"Erro ao testar Omie: {e}")
        return {
            "success": False,
            "error": str(e),
            "recommendation": "Verifique suas credenciais no painel Omie"
        }


# ========================================
# ERP Bling
# ========================================

@router.post("/test/erp-bling")
async def testar_bling(
    request: TestIntegrationRequest,
    x_tenant_id: Optional[str] = Header(None)
):
    """
    Testa credenciais do Bling ANTES de salvar
    
    O cliente precisa ter:
    - Conta Bling
    - API Key
    """
    try:
        if not x_tenant_id:
            raise HTTPException(status_code=400, detail="X-Tenant-ID obrigatório")
        
        api_key = request.credentials.get("api_key")
        
        if not api_key:
            raise HTTPException(status_code=400, detail="api_key é obrigatório")
        
        logger.info(f"Testando Bling para tenant {x_tenant_id}")
        
        # Criar cliente
        client = BlingClient(api_key=api_key)
        
        # Teste: Listar situações (endpoint simples)
        resultado = client.listar_situacoes()
        
        if not resultado.get("success"):
            return {
                "success": False,
                "error": "Falha ao conectar com Bling",
                "details": resultado.get("error"),
                "recommendation": "Verifique se a API Key está correta no painel Bling"
            }
        
        # Teste 2: Listar contatos (validar permissões)
        contatos = client.listar_contatos(pagina=1)
        
        return {
            "success": True,
            "message": "Bling configurado com sucesso!",
            "test_result": {
                "connection": "✓ Conectado",
                "permissions": "✓ Permissões OK",
                "total_contacts": len(contatos.get("data", [])) if contatos.get("success") else "N/A"
            },
            "available_features": [
                "Sincronizar clientes",
                "Criar pedidos",
                "Consultar produtos",
                "Gerenciar estoque"
            ],
            "recommendation": "Tudo OK! Você pode salvar essas credenciais."
        }
    
    except Exception as e:
        logger.error(f"Erro ao testar Bling: {e}")
        return {
            "success": False,
            "error": str(e),
            "recommendation": "Verifique sua API Key no painel Bling"
        }


# ========================================
# Configuração Unificada
# ========================================

@router.post("/configure")
async def configurar_integracao(
    request: ConfigureIntegrationRequest,
    x_tenant_id: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """
    Configura qualquer integração (Maps, ERPs, etc)
    
    Salva as credenciais criptografadas no banco.
    """
    try:
        if not x_tenant_id:
            raise HTTPException(status_code=400, detail="X-Tenant-ID obrigatório")
        
        logger.info(f"Configurando {request.integration_type}/{request.provider} para tenant {x_tenant_id}")
        
        # Criar ou atualizar credencial
        existing = db.query(TenantCredentials).filter(
            TenantCredentials.tenant_id == x_tenant_id,
            TenantCredentials.integration_type == request.integration_type,
            TenantCredentials.provider == request.provider
        ).first()
        
        if existing:
            # Atualizar
            existing.encrypted_credentials = TenantCredentials.encrypt_credentials(request.credentials)
            existing.is_active = True
            existing.is_validated = False
            logger.info(f"Credencial atualizada: {request.integration_type}/{request.provider}")
        else:
            # Criar nova
            new_cred = TenantCredentials(
                tenant_id=x_tenant_id,
                integration_type=request.integration_type,
                provider=request.provider,
                encrypted_credentials=TenantCredentials.encrypt_credentials(request.credentials),
                is_active=True,
                is_validated=False
            )
            db.add(new_cred)
            logger.info(f"Nova credencial criada: {request.integration_type}/{request.provider}")
        
        db.commit()
        
        return {
            "success": True,
            "message": f"Integração {request.provider} configurada com sucesso!",
            "integration_type": request.integration_type,
            "provider": request.provider
        }
    
    except Exception as e:
        db.rollback()
        logger.error(f"Erro ao configurar integração: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/supported")
async def listar_integracoes_suportadas():
    """
    Lista todas as integrações que podem ser configuradas
    """
    return {
        "success": True,
        "integrations": {
            "maps": {
                "providers": [
                    {
                        "id": "google_maps",
                        "name": "Google Maps Distance Matrix",
                        "description": "Cálculo de distâncias e rotas",
                        "required_fields": ["api_key"],
                        "setup_url": "https://console.cloud.google.com",
                        "cost": "$0.005 por requisição",
                        "free_tier": "$200/mês",
                        "documentation": "https://developers.google.com/maps/documentation/distance-matrix"
                    }
                ]
            },
            "erp": {
                "providers": [
                    {
                        "id": "omie",
                        "name": "Omie ERP",
                        "description": "Sincronização de clientes, produtos e pedidos",
                        "required_fields": ["app_key", "app_secret"],
                        "setup_url": "https://app.omie.com.br",
                        "documentation": "https://developer.omie.com.br"
                    },
                    {
                        "id": "bling",
                        "name": "Bling ERP",
                        "description": "Gestão de vendas e estoque",
                        "required_fields": ["api_key"],
                        "setup_url": "https://www.bling.com.br",
                        "documentation": "https://ajuda.bling.com.br/hc/pt-br/categories/360002186394-API-para-Desenvolvedores"
                    }
                ]
            },
            "gps": {
                "providers": [
                    {
                        "id": "sascar",
                        "name": "Sascar",
                        "description": "Rastreamento GPS",
                        "required_fields": ["api_key"],
                        "note": "Configure em /gps-config"
                    },
                    {
                        "id": "autotrac",
                        "name": "Autotrac",
                        "description": "Rastreamento GPS",
                        "required_fields": ["username", "password"],
                        "note": "Configure em /gps-config"
                    },
                    {
                        "id": "onixsat",
                        "name": "Onixsat",
                        "description": "Rastreamento GPS",
                        "required_fields": ["api_token"],
                        "note": "Configure em /gps-config"
                    }
                ]
            }
        }
    }


@router.get("/my-integrations")
async def listar_minhas_integracoes(
    x_tenant_id: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """
    Lista todas as integrações configuradas pelo cliente
    """
    try:
        if not x_tenant_id:
            raise HTTPException(status_code=400, detail="X-Tenant-ID obrigatório")
        
        creds = db.query(TenantCredentials).filter(
            TenantCredentials.tenant_id == x_tenant_id,
            TenantCredentials.is_active == True
        ).all()
        
        integracoes = {}
        
        for cred in creds:
            tipo = cred.integration_type
            if tipo not in integracoes:
                integracoes[tipo] = []
            
            integracoes[tipo].append({
                "provider": cred.provider,
                "is_active": cred.is_active,
                "is_validated": cred.is_validated,
                "last_validation": cred.last_validation.isoformat() if cred.last_validation else None,
                "created_at": cred.created_at.isoformat() if cred.created_at else None
            })
        
        return {
            "success": True,
            "tenant_id": x_tenant_id,
            "integrations": integracoes,
            "total": len(creds)
        }
    
    except Exception as e:
        logger.error(f"Erro ao listar integrações: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/remove/{integration_type}/{provider}")
async def remover_integracao(
    integration_type: str,
    provider: str,
    x_tenant_id: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """
    Remove uma integração configurada
    """
    try:
        if not x_tenant_id:
            raise HTTPException(status_code=400, detail="X-Tenant-ID obrigatório")
        
        cred = db.query(TenantCredentials).filter(
            TenantCredentials.tenant_id == x_tenant_id,
            TenantCredentials.integration_type == integration_type,
            TenantCredentials.provider == provider
        ).first()
        
        if not cred:
            raise HTTPException(
                status_code=404,
                detail=f"Integração {integration_type}/{provider} não encontrada"
            )
        
        db.delete(cred)
        db.commit()
        
        logger.info(f"Integração removida: {integration_type}/{provider} do tenant {x_tenant_id}")
        
        return {
            "success": True,
            "message": f"Integração {provider} removida com sucesso"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Erro ao remover integração: {e}")
        raise HTTPException(status_code=500, detail=str(e))

