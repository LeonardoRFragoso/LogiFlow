"""
LogiFlow CRM - SuiteCRM Router
Endpoints para integração com SuiteCRM
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from loguru import logger

router = APIRouter(prefix="/suitecrm", tags=["SuiteCRM"])


# ========== Schemas ==========

class SuiteCRMRecord(BaseModel):
    module: str
    attributes: Dict[str, Any]

class SuiteCRMUpdate(BaseModel):
    attributes: Dict[str, Any]

class SyncRequest(BaseModel):
    modules: List[str]

class StatusUpdate(BaseModel):
    novo_status: str
    observacao: Optional[str] = None


# ========== Endpoints ==========

@router.get("/status")
async def get_connection_status():
    """Testa conexão com SuiteCRM"""
    try:
        from services.suitecrm_service import suitecrm_service
        result = await suitecrm_service.test_connection()
        return {
            "success": result.get("success", False),
            "data": result,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Erro ao testar conexão SuiteCRM: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": "SuiteCRM não configurado ou indisponível"
        }


@router.get("/modules/{module}")
async def list_module_records(
    module: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: Optional[str] = None
):
    """Lista registros de um módulo do SuiteCRM"""
    try:
        from services.suitecrm_service import suitecrm_service
        
        filters = {}
        if status:
            filters["status"] = status
        
        result = await suitecrm_service.get_module_records(
            module=module,
            page_number=page,
            page_size=page_size,
            filters=filters if filters else None
        )
        
        return {
            "success": True,
            "module": module,
            "data": result.get("data", []),
            "meta": result.get("meta", {}),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Erro ao listar {module}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/modules/{module}/{record_id}")
async def get_module_record(module: str, record_id: str):
    """Obtém um registro específico do SuiteCRM"""
    try:
        from services.suitecrm_service import suitecrm_service
        result = await suitecrm_service.get_record(module, record_id)
        
        return {
            "success": True,
            "data": result.get("data"),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Erro ao obter {module}/{record_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/modules/{module}")
async def create_module_record(module: str, record: SuiteCRMRecord):
    """Cria um novo registro no SuiteCRM"""
    try:
        from services.suitecrm_service import suitecrm_service
        result = await suitecrm_service.create_record(module, record.attributes)
        
        return {
            "success": True,
            "data": result.get("data"),
            "message": f"Registro criado em {module}",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Erro ao criar em {module}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/modules/{module}/{record_id}")
async def update_module_record(module: str, record_id: str, update: SuiteCRMUpdate):
    """Atualiza um registro no SuiteCRM"""
    try:
        from services.suitecrm_service import suitecrm_service
        result = await suitecrm_service.update_record(module, record_id, update.attributes)
        
        return {
            "success": True,
            "data": result.get("data"),
            "message": f"Registro {record_id} atualizado",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Erro ao atualizar {module}/{record_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/modules/{module}/{record_id}")
async def delete_module_record(module: str, record_id: str):
    """Deleta um registro no SuiteCRM"""
    try:
        from services.suitecrm_service import suitecrm_service
        await suitecrm_service.delete_record(module, record_id)
        
        return {
            "success": True,
            "message": f"Registro {record_id} deletado de {module}",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Erro ao deletar {module}/{record_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ========== Endpoints Específicos LogiFlow ==========

@router.get("/cotacoes")
async def list_cotacoes(status: Optional[str] = None):
    """Lista cotações do SuiteCRM"""
    try:
        from services.suitecrm_service import suitecrm_service
        cotacoes = await suitecrm_service.get_cotacoes(status)
        
        return {
            "success": True,
            "data": cotacoes,
            "count": len(cotacoes),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Erro ao listar cotações: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/pedidos")
async def list_pedidos(status: Optional[str] = None):
    """Lista pedidos de frete do SuiteCRM"""
    try:
        from services.suitecrm_service import suitecrm_service
        pedidos = await suitecrm_service.get_pedidos(status)
        
        return {
            "success": True,
            "data": pedidos,
            "count": len(pedidos),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Erro ao listar pedidos: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/entregas")
async def list_entregas(motorista_id: Optional[str] = None):
    """Lista entregas do SuiteCRM"""
    try:
        from services.suitecrm_service import suitecrm_service
        entregas = await suitecrm_service.get_entregas(motorista_id)
        
        return {
            "success": True,
            "data": entregas,
            "count": len(entregas),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Erro ao listar entregas: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/entregas/{entrega_id}/status")
async def update_entrega_status(entrega_id: str, status_update: StatusUpdate):
    """Atualiza status de uma entrega"""
    try:
        from services.suitecrm_service import suitecrm_service
        result = await suitecrm_service.atualizar_status_entrega(
            entrega_id,
            status_update.novo_status,
            status_update.observacao
        )
        
        return {
            "success": True,
            "data": result,
            "message": f"Status atualizado para {status_update.novo_status}",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Erro ao atualizar status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/motoristas")
async def list_motoristas(ativo: bool = True):
    """Lista motoristas do SuiteCRM"""
    try:
        from services.suitecrm_service import suitecrm_service
        motoristas = await suitecrm_service.get_motoristas(ativo)
        
        return {
            "success": True,
            "data": motoristas,
            "count": len(motoristas),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Erro ao listar motoristas: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/veiculos")
async def list_veiculos(disponivel: bool = True):
    """Lista veículos do SuiteCRM"""
    try:
        from services.suitecrm_service import suitecrm_service
        veiculos = await suitecrm_service.get_veiculos(disponivel)
        
        return {
            "success": True,
            "data": veiculos,
            "count": len(veiculos),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Erro ao listar veículos: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ========== Sincronização ==========

@router.post("/sync")
async def sync_modules(request: SyncRequest):
    """Sincroniza módulos do SuiteCRM"""
    try:
        from services.suitecrm_service import suitecrm_service
        
        results = []
        for module in request.modules:
            result = await suitecrm_service.sync_from_suitecrm(module)
            results.append(result)
        
        return {
            "success": True,
            "results": results,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Erro ao sincronizar: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/sync/all")
async def sync_all_modules():
    """Sincroniza todos os módulos LogiFlow do SuiteCRM"""
    modules = [
        "LF_Cotacoes",
        "LF_PedidosFrete",
        "LF_Entregas",
        "LF_Motoristas",
        "LF_Veiculos",
        "LF_Ocorrencias"
    ]
    
    try:
        from services.suitecrm_service import suitecrm_service
        
        results = []
        for module in modules:
            result = await suitecrm_service.sync_from_suitecrm(module)
            results.append(result)
        
        success_count = sum(1 for r in results if r.get("success"))
        
        return {
            "success": True,
            "message": f"Sincronização concluída: {success_count}/{len(modules)} módulos",
            "results": results,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Erro ao sincronizar todos: {e}")
        raise HTTPException(status_code=500, detail=str(e))
