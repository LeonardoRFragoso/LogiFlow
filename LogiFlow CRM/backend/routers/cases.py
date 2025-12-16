"""
LogiFlow CRM - Router Cases (Suporte/Tickets)
Gestão de casos de suporte e atendimento ao cliente
Integrado com SuiteCRM
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from loguru import logger

router = APIRouter(prefix="/cases", tags=["Suporte/Cases"])


# ========== Schemas ==========

class CaseBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Assunto do caso")
    account_id: Optional[str] = Field(None, description="ID do cliente")
    status: str = Field(default="New", description="Status do caso")
    priority: str = Field(default="Medium", description="Prioridade")
    type: Optional[str] = Field(None, description="Tipo de caso")
    description: Optional[str] = Field(None, description="Descrição detalhada")
    resolution: Optional[str] = Field(None, description="Resolução do caso")


class CaseCreate(CaseBase):
    pass


class CaseUpdate(BaseModel):
    name: Optional[str] = None
    account_id: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    type: Optional[str] = None
    description: Optional[str] = None
    resolution: Optional[str] = None


class CaseResponse(CaseBase):
    id: str
    case_number: Optional[str] = None
    account_name: Optional[str] = None
    assigned_user_name: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


# ========== Endpoints ==========

@router.get("/", response_model=List[CaseResponse])
async def list_cases(
    status: Optional[str] = Query(None, description="Filtrar por status"),
    priority: Optional[str] = Query(None, description="Filtrar por prioridade"),
    account_id: Optional[str] = Query(None, description="Filtrar por cliente"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100)
):
    """Lista casos de suporte com filtros"""
    try:
        from services.suitecrm_service import suitecrm_service
        
        filters = {}
        if status:
            filters["status"] = status
        if priority:
            filters["priority"] = priority
        if account_id:
            filters["account_id"] = account_id
        
        result = await suitecrm_service.get_module_records(
            module="Cases",
            page_number=page,
            page_size=page_size,
            filters=filters if filters else None,
            fields=["case_number", "name", "account_id", "account_name", "status", 
                   "priority", "type", "description", "resolution", "assigned_user_name"]
        )
        
        cases = []
        for item in result.get("data", []):
            attrs = item.get("attributes", {})
            cases.append({
                "id": item.get("id"),
                "case_number": attrs.get("case_number"),
                "name": attrs.get("name", ""),
                "account_id": attrs.get("account_id"),
                "account_name": attrs.get("account_name"),
                "status": attrs.get("status", "New"),
                "priority": attrs.get("priority", "Medium"),
                "type": attrs.get("type"),
                "description": attrs.get("description"),
                "resolution": attrs.get("resolution"),
                "assigned_user_name": attrs.get("assigned_user_name"),
                "created_at": attrs.get("date_entered"),
                "updated_at": attrs.get("date_modified")
            })
        
        return cases
        
    except Exception as e:
        logger.error(f"Erro ao listar casos: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{case_id}", response_model=CaseResponse)
async def get_case(case_id: str):
    """Obtém detalhes de um caso"""
    try:
        from services.suitecrm_service import suitecrm_service
        
        result = await suitecrm_service.get_record("Cases", case_id)
        
        attrs = result.get("data", {}).get("attributes", {})
        
        return {
            "id": case_id,
            "case_number": attrs.get("case_number"),
            "name": attrs.get("name", ""),
            "account_id": attrs.get("account_id"),
            "account_name": attrs.get("account_name"),
            "status": attrs.get("status", "New"),
            "priority": attrs.get("priority", "Medium"),
            "type": attrs.get("type"),
            "description": attrs.get("description"),
            "resolution": attrs.get("resolution"),
            "assigned_user_name": attrs.get("assigned_user_name"),
            "created_at": attrs.get("date_entered"),
            "updated_at": attrs.get("date_modified")
        }
        
    except Exception as e:
        logger.error(f"Erro ao obter caso {case_id}: {e}")
        raise HTTPException(status_code=404, detail="Caso não encontrado")


@router.post("/", response_model=CaseResponse, status_code=201)
async def create_case(case: CaseCreate):
    """Cria um novo caso de suporte"""
    try:
        from services.suitecrm_service import suitecrm_service
        
        attributes = {
            "name": case.name,
            "status": case.status,
            "priority": case.priority,
            "type": case.type,
            "description": case.description,
            "resolution": case.resolution
        }
        
        if case.account_id:
            attributes["account_id"] = case.account_id
        
        # Remover campos None
        attributes = {k: v for k, v in attributes.items() if v is not None}
        
        result = await suitecrm_service.create_record("Cases", attributes)
        
        case_id = result.get("data", {}).get("id")
        
        logger.info(f"✅ Caso criado: {case.name} ({case_id})")
        
        return await get_case(case_id)
        
    except Exception as e:
        logger.error(f"Erro ao criar caso: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{case_id}", response_model=CaseResponse)
async def update_case(case_id: str, case: CaseUpdate):
    """Atualiza um caso existente"""
    try:
        from services.suitecrm_service import suitecrm_service
        
        attributes = {}
        
        if case.name is not None:
            attributes["name"] = case.name
        if case.account_id is not None:
            attributes["account_id"] = case.account_id
        if case.status is not None:
            attributes["status"] = case.status
        if case.priority is not None:
            attributes["priority"] = case.priority
        if case.type is not None:
            attributes["type"] = case.type
        if case.description is not None:
            attributes["description"] = case.description
        if case.resolution is not None:
            attributes["resolution"] = case.resolution
        
        if not attributes:
            raise HTTPException(status_code=400, detail="Nenhum campo para atualizar")
        
        await suitecrm_service.update_record("Cases", case_id, attributes)
        
        logger.info(f"✅ Caso atualizado: {case_id}")
        
        return await get_case(case_id)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao atualizar caso {case_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{case_id}", status_code=204)
async def delete_case(case_id: str):
    """Deleta um caso"""
    try:
        from services.suitecrm_service import suitecrm_service
        
        await suitecrm_service.delete_record("Cases", case_id)
        
        logger.info(f"✅ Caso deletado: {case_id}")
        
        return None
        
    except Exception as e:
        logger.error(f"Erro ao deletar caso {case_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats/summary")
async def get_cases_stats():
    """Estatísticas de casos de suporte"""
    try:
        from services.suitecrm_service import suitecrm_service
        
        result = await suitecrm_service.get_module_records(
            module="Cases",
            page_size=1000
        )
        
        cases = result.get("data", [])
        
        # Agrupar por status
        by_status = {}
        by_priority = {}
        
        for case in cases:
            attrs = case.get("attributes", {})
            status = attrs.get("status", "Unknown")
            priority = attrs.get("priority", "Medium")
            
            by_status[status] = by_status.get(status, 0) + 1
            by_priority[priority] = by_priority.get(priority, 0) + 1
        
        return {
            "total_cases": len(cases),
            "by_status": by_status,
            "by_priority": by_priority,
            "open_cases": sum(by_status.get(s, 0) for s in ["New", "Assigned", "Pending Input"]),
            "closed_cases": by_status.get("Closed", 0)
        }
        
    except Exception as e:
        logger.error(f"Erro ao obter estatísticas de casos: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/options/status")
async def list_case_statuses():
    """Lista opções de status disponíveis"""
    return {
        "statuses": [
            {"value": "New", "label": "Novo"},
            {"value": "Assigned", "label": "Atribuído"},
            {"value": "Closed", "label": "Fechado"},
            {"value": "Pending Input", "label": "Aguardando Resposta"},
            {"value": "Rejected", "label": "Rejeitado"},
            {"value": "Duplicate", "label": "Duplicado"}
        ]
    }


@router.get("/options/priority")
async def list_case_priorities():
    """Lista opções de prioridade disponíveis"""
    return {
        "priorities": [
            {"value": "P1", "label": "P1 - Urgente"},
            {"value": "P2", "label": "P2 - Alta"},
            {"value": "P3", "label": "P3 - Média"},
            {"value": "Low", "label": "Baixa"}
        ]
    }
