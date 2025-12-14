"""
LogiFlow CRM - Router Integrações ERP
Endpoints para sincronização com Omie e Bling
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime
import logging

from integrations.erp.omie import OmieClient
from integrations.erp.bling import BlingClient
from integrations.erp.tiny import TinyClient
from services.erp_sync import ERPSyncService
from config import settings

logger = logging.getLogger(__name__)
router = APIRouter()


# ========================================
# Schemas
# ========================================

class ClienteSyncRequest(BaseModel):
    cliente_id: str = Field(..., description="ID do cliente no LogiFlow")
    nome: str
    cnpj: Optional[str] = None
    cpf: Optional[str] = None
    ie: Optional[str] = None
    telefone: Optional[str] = None
    celular: Optional[str] = None
    email: Optional[str] = None
    endereco: Optional[str] = None
    numero: Optional[str] = None
    complemento: Optional[str] = None
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    uf: Optional[str] = None
    cep: Optional[str] = None
    nome_fantasia: Optional[str] = None


class PedidoSyncRequest(BaseModel):
    pedido_id: str = Field(..., description="ID do pedido no LogiFlow")
    numero: str
    cliente_id: str
    data_entrega_prevista: Optional[str] = None
    observacoes: Optional[str] = None
    tipo_frete: Optional[str] = "CIF"
    itens: List[Dict]


class SyncStatusResponse(BaseModel):
    success: bool
    erp: str
    tipo: str
    id_logiflow: str
    id_erp: Optional[str] = None
    message: str
    detalhes: Optional[Dict] = None


# ========================================
# Dependencies
# ========================================

def get_omie_client() -> OmieClient:
    """Retorna cliente Omie configurado"""
    app_key = settings.OMIE_APP_KEY if hasattr(settings, 'OMIE_APP_KEY') else None
    app_secret = settings.OMIE_APP_SECRET if hasattr(settings, 'OMIE_APP_SECRET') else None
    
    if not app_key or not app_secret:
        raise HTTPException(
            status_code=500,
            detail="Credenciais Omie não configuradas. Configure OMIE_APP_KEY e OMIE_APP_SECRET no .env"
        )
    
    return OmieClient(app_key=app_key, app_secret=app_secret)


def get_bling_client() -> BlingClient:
    """Retorna cliente Bling configurado"""
    access_token = settings.BLING_ACCESS_TOKEN if hasattr(settings, 'BLING_ACCESS_TOKEN') else None
    
    if not access_token:
        raise HTTPException(
            status_code=500,
            detail="Token Bling não configurado. Configure BLING_ACCESS_TOKEN no .env"
        )
    
    return BlingClient(access_token=access_token)


# ========================================
# Endpoints Omie
# ========================================

@router.get("/omie/clientes")
async def listar_clientes_omie(
    pagina: int = Query(1, ge=1),
    registros_por_pagina: int = Query(50, ge=1, le=100),
    client: OmieClient = Depends(get_omie_client)
):
    """Lista clientes do Omie"""
    try:
        result = client.listar_clientes(pagina, registros_por_pagina)
        
        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("message"))
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao listar clientes Omie: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/omie/clientes/sincronizar")
async def sincronizar_cliente_omie(
    request: ClienteSyncRequest,
    client: OmieClient = Depends(get_omie_client)
):
    """Sincroniza cliente do LogiFlow com Omie"""
    try:
        cliente_data = request.dict()
        result = client.sincronizar_cliente(cliente_data)
        
        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("message"))
        
        return {
            "success": True,
            "message": "Cliente sincronizado com Omie",
            "data": result.get("data")
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao sincronizar cliente com Omie: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/omie/pedidos")
async def listar_pedidos_omie(
    pagina: int = Query(1, ge=1),
    registros_por_pagina: int = Query(50, ge=1, le=100),
    client: OmieClient = Depends(get_omie_client)
):
    """Lista pedidos do Omie"""
    try:
        result = client.listar_pedidos(pagina, registros_por_pagina)
        
        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("message"))
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao listar pedidos Omie: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/omie/pedidos/sincronizar")
async def sincronizar_pedido_omie(
    request: PedidoSyncRequest,
    client: OmieClient = Depends(get_omie_client)
):
    """Sincroniza pedido do LogiFlow com Omie"""
    try:
        pedido_data = request.dict()
        result = client.sincronizar_pedido(pedido_data)
        
        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("message"))
        
        return {
            "success": True,
            "message": "Pedido sincronizado com Omie",
            "data": result.get("data")
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao sincronizar pedido com Omie: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ========================================
# Endpoints Bling
# ========================================

@router.get("/bling/contatos")
async def listar_contatos_bling(
    pagina: int = Query(1, ge=1),
    limite: int = Query(100, ge=1, le=100),
    tipo: Optional[str] = Query(None, description="Cliente, Fornecedor, Transportador"),
    client: BlingClient = Depends(get_bling_client)
):
    """Lista contatos do Bling"""
    try:
        result = client.listar_contatos(pagina, limite, tipo)
        
        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("message"))
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao listar contatos Bling: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/bling/contatos/sincronizar")
async def sincronizar_cliente_bling(
    request: ClienteSyncRequest,
    client: BlingClient = Depends(get_bling_client)
):
    """Sincroniza cliente do LogiFlow com Bling"""
    try:
        cliente_data = request.dict()
        result = client.sincronizar_cliente(cliente_data)
        
        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("message"))
        
        return {
            "success": True,
            "message": "Cliente sincronizado com Bling",
            "data": result.get("data")
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao sincronizar cliente com Bling: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/bling/pedidos")
async def listar_pedidos_bling(
    pagina: int = Query(1, ge=1),
    limite: int = Query(100, ge=1, le=100),
    data_inicial: Optional[str] = Query(None, description="YYYY-MM-DD"),
    data_final: Optional[str] = Query(None, description="YYYY-MM-DD"),
    client: BlingClient = Depends(get_bling_client)
):
    """Lista pedidos do Bling"""
    try:
        result = client.listar_pedidos(pagina, limite, data_inicial, data_final)
        
        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("message"))
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao listar pedidos Bling: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/bling/pedidos/sincronizar")
async def sincronizar_pedido_bling(
    request: PedidoSyncRequest,
    client: BlingClient = Depends(get_bling_client)
):
    """Sincroniza pedido do LogiFlow com Bling"""
    try:
        pedido_data = request.dict()
        result = client.sincronizar_pedido(pedido_data)
        
        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("message"))
        
        return {
            "success": True,
            "message": "Pedido sincronizado com Bling",
            "data": result.get("data")
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao sincronizar pedido com Bling: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ========================================
# Endpoints de Status
# ========================================

@router.get("/status")
async def verificar_status_integracoes():
    """Verifica status das integrações ERP"""
    status = {
        "omie": {
            "configurado": hasattr(settings, 'OMIE_APP_KEY') and settings.OMIE_APP_KEY is not None,
            "ativo": False
        },
        "bling": {
            "configurado": hasattr(settings, 'BLING_ACCESS_TOKEN') and settings.BLING_ACCESS_TOKEN is not None,
            "ativo": False
        }
    }
    
    # Testar conexão Omie
    if status["omie"]["configurado"]:
        try:
            client = get_omie_client()
            result = client.listar_clientes(pagina=1, registros_por_pagina=1)
            status["omie"]["ativo"] = result.get("success", False)
        except:
            pass
    
    # Testar conexão Bling
    if status["bling"]["configurado"]:
        try:
            client = get_bling_client()
            result = client.listar_contatos(pagina=1, limite=1)
            status["bling"]["ativo"] = result.get("success", False)
        except:
            pass
    
    return {
        "success": True,
        "data": status
    }
