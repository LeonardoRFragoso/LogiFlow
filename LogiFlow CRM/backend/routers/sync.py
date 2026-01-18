"""
LogiFlow CRM - Router de Sincronização
======================================
Endpoints para sincronização manual entre banco local e SuiteCRM
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from loguru import logger

from services.sync_service import sync_service
from database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/sync", tags=["Sincronização"])


# ========== Schemas ==========

class SyncModuleRequest(BaseModel):
    modules: List[str]
    direction: str = "from_suitecrm"  # "from_suitecrm", "to_suitecrm", "bidirectional"


class SyncResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None
    timestamp: str


# ========== Endpoints ==========

@router.get("/status")
async def get_sync_status():
    """Retorna status atual da sincronização"""
    try:
        status = sync_service.get_sync_status()
        return {
            "success": True,
            "data": status,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Erro ao obter status de sincronização: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/from-suitecrm")
async def sync_from_suitecrm(
    modules: Optional[List[str]] = None,
    db: Session = Depends(get_db)
):
    """
    Sincroniza dados do SuiteCRM para o banco local
    
    Args:
        modules: Lista de módulos (None = todos)
    """
    try:
        if modules:
            # Sincronizar módulos específicos
            results = []
            for module in modules:
                result = await sync_service.sync_from_suitecrm(module, db)
                results.append(result)
            
            success_count = sum(1 for r in results if r.get("success"))
            
            return {
                "success": True,
                "message": f"Sincronização concluída: {success_count}/{len(modules)} módulos",
                "data": {
                    "results": results,
                    "modules_synced": success_count,
                    "total_modules": len(modules)
                },
                "timestamp": datetime.now().isoformat()
            }
        else:
            # Sincronizar todos os módulos
            result = await sync_service.sync_all_from_suitecrm(db)
            
            return {
                "success": True,
                "message": "Sincronização completa do SuiteCRM concluída",
                "data": result,
                "timestamp": datetime.now().isoformat()
            }
            
    except Exception as e:
        logger.error(f"Erro ao sincronizar do SuiteCRM: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/to-suitecrm")
async def sync_to_suitecrm(
    modules: Optional[List[str]] = None,
    db: Session = Depends(get_db)
):
    """
    Sincroniza dados do banco local para o SuiteCRM
    
    Args:
        modules: Lista de módulos (None = todos)
    """
    try:
        if modules:
            # Sincronizar módulos específicos
            results = []
            for module in modules:
                result = await sync_service.sync_module_to_suitecrm(module, db)
                results.append(result)
            
            success_count = sum(1 for r in results if r.get("success"))
            
            return {
                "success": True,
                "message": f"Sincronização concluída: {success_count}/{len(modules)} módulos",
                "data": {
                    "results": results,
                    "modules_synced": success_count,
                    "total_modules": len(modules)
                },
                "timestamp": datetime.now().isoformat()
            }
        else:
            # Sincronizar todos os módulos
            result = await sync_service.sync_all_to_suitecrm(db)
            
            return {
                "success": True,
                "message": "Sincronização completa para o SuiteCRM concluída",
                "data": result,
                "timestamp": datetime.now().isoformat()
            }
            
    except Exception as e:
        logger.error(f"Erro ao sincronizar para o SuiteCRM: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/bidirectional")
async def sync_bidirectional(
    modules: Optional[List[str]] = None,
    db: Session = Depends(get_db)
):
    """
    Sincronização bidirecional: SuiteCRM → Local → SuiteCRM
    
    1. Puxa dados atualizados do SuiteCRM
    2. Envia dados locais não sincronizados
    """
    try:
        # Primeiro: puxar do SuiteCRM
        if modules:
            from_crm_results = []
            for module in modules:
                result = await sync_service.sync_from_suitecrm(module, db)
                from_crm_results.append(result)
        else:
            from_crm_result = await sync_service.sync_all_from_suitecrm(db)
            from_crm_results = from_crm_result.get("results", [])
        
        # Segundo: enviar para SuiteCRM
        if modules:
            to_crm_results = []
            for module in modules:
                result = await sync_service.sync_module_to_suitecrm(module, db)
                to_crm_results.append(result)
        else:
            to_crm_result = await sync_service.sync_all_to_suitecrm(db)
            to_crm_results = to_crm_result.get("results", [])
        
        return {
            "success": True,
            "message": "Sincronização bidirecional concluída",
            "data": {
                "from_suitecrm": from_crm_results,
                "to_suitecrm": to_crm_results
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Erro na sincronização bidirecional: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/modules")
async def list_available_modules():
    """Lista módulos disponíveis para sincronização"""
    return {
        "success": True,
        "modules": list(sync_service.MODULE_MAPPING.keys()),
        "count": len(sync_service.MODULE_MAPPING),
        "timestamp": datetime.now().isoformat()
    }


@router.post("/module/{module_name}/from-suitecrm")
async def sync_single_module_from_suitecrm(
    module_name: str,
    db: Session = Depends(get_db)
):
    """Sincroniza um módulo específico do SuiteCRM"""
    try:
        if module_name not in sync_service.MODULE_MAPPING:
            raise HTTPException(
                status_code=404,
                detail=f"Módulo '{module_name}' não encontrado"
            )
        
        result = await sync_service.sync_from_suitecrm(module_name, db)
        
        return {
            "success": result.get("success", False),
            "message": f"Sincronização de {module_name} concluída",
            "data": result,
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao sincronizar {module_name}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/module/{module_name}/to-suitecrm")
async def sync_single_module_to_suitecrm(
    module_name: str,
    db: Session = Depends(get_db)
):
    """Sincroniza um módulo específico para o SuiteCRM"""
    try:
        if module_name not in sync_service.MODULE_MAPPING:
            raise HTTPException(
                status_code=404,
                detail=f"Módulo '{module_name}' não encontrado"
            )
        
        result = await sync_service.sync_module_to_suitecrm(module_name, db)
        
        return {
            "success": result.get("success", False),
            "message": f"Sincronização de {module_name} para SuiteCRM concluída",
            "data": result,
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao sincronizar {module_name} para SuiteCRM: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/force-full-sync")
async def force_full_sync(db: Session = Depends(get_db)):
    """
    Força sincronização completa (use com cuidado)
    
    1. Limpa histórico de sincronização
    2. Sincroniza tudo do SuiteCRM
    3. Envia tudo para o SuiteCRM
    """
    try:
        logger.warning("⚠️ Iniciando sincronização COMPLETA forçada")
        
        # Limpar histórico
        sync_service.last_sync.clear()
        
        # Sync bidirecional completo
        from_crm = await sync_service.sync_all_from_suitecrm(db)
        to_crm = await sync_service.sync_all_to_suitecrm(db)
        
        return {
            "success": True,
            "message": "Sincronização completa forçada concluída",
            "data": {
                "from_suitecrm": from_crm,
                "to_suitecrm": to_crm
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Erro na sincronização completa forçada: {e}")
        raise HTTPException(status_code=500, detail=str(e))
