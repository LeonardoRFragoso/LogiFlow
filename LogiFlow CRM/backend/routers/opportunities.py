"""
LogiFlow CRM - Router Oportunidades (Opportunities)
Pipeline de vendas - Gestão de oportunidades de negócio
Integrado com SuiteCRM
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date
from loguru import logger

router = APIRouter(prefix="/opportunities", tags=["Oportunidades CRM"])


# ========== Schemas ==========

class OpportunityBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    account_id: Optional[str] = Field(None, description="ID do cliente")
    amount: Optional[float] = Field(None, ge=0, description="Valor estimado")
    sales_stage: str = Field(..., description="Estágio do pipeline")
    probability: Optional[int] = Field(None, ge=0, le=100, description="Probabilidade de fechamento")
    date_closed: Optional[date] = Field(None, description="Data prevista de fechamento")
    next_step: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    lead_source: Optional[str] = None
    opportunity_type: Optional[str] = None


class OpportunityCreate(OpportunityBase):
    pass


class OpportunityUpdate(BaseModel):
    name: Optional[str] = None
    account_id: Optional[str] = None
    amount: Optional[float] = None
    sales_stage: Optional[str] = None
    probability: Optional[int] = None
    date_closed: Optional[date] = None
    next_step: Optional[str] = None
    description: Optional[str] = None
    lead_source: Optional[str] = None
    opportunity_type: Optional[str] = None


class OpportunityResponse(OpportunityBase):
    id: str
    account_name: Optional[str] = None
    assigned_user_name: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


# ========== Endpoints ==========

@router.get("/", response_model=List[OpportunityResponse])
async def list_opportunities(
    sales_stage: Optional[str] = Query(None, description="Filtrar por estágio"),
    account_id: Optional[str] = Query(None, description="Filtrar por cliente"),
    min_amount: Optional[float] = Query(None, description="Valor mínimo"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100)
):
    """Lista oportunidades com filtros"""
    try:
        from services.suitecrm_service import suitecrm_service
        
        filters = {}
        if sales_stage:
            filters["sales_stage"] = sales_stage
        if account_id:
            filters["account_id"] = account_id
        
        result = await suitecrm_service.get_module_records(
            module="Opportunities",
            page_number=page,
            page_size=page_size,
            filters=filters if filters else None,
            fields=["name", "account_id", "account_name", "amount", "sales_stage", 
                   "probability", "date_closed", "next_step", "description",
                   "lead_source", "opportunity_type", "assigned_user_name"]
        )
        
        opportunities = []
        for item in result.get("data", []):
            attrs = item.get("attributes", {})
            opp = {
                "id": item.get("id"),
                "name": attrs.get("name", ""),
                "account_id": attrs.get("account_id"),
                "account_name": attrs.get("account_name"),
                "amount": float(attrs.get("amount", 0)) if attrs.get("amount") else None,
                "sales_stage": attrs.get("sales_stage", ""),
                "probability": int(attrs.get("probability", 0)) if attrs.get("probability") else None,
                "date_closed": attrs.get("date_closed"),
                "next_step": attrs.get("next_step"),
                "description": attrs.get("description"),
                "lead_source": attrs.get("lead_source"),
                "opportunity_type": attrs.get("opportunity_type"),
                "assigned_user_name": attrs.get("assigned_user_name"),
                "created_at": attrs.get("date_entered"),
                "updated_at": attrs.get("date_modified")
            }
            
            # Filtrar por valor mínimo
            if min_amount and opp["amount"] and opp["amount"] < min_amount:
                continue
            
            opportunities.append(opp)
        
        return opportunities
        
    except Exception as e:
        logger.error(f"Erro ao listar oportunidades: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{opportunity_id}", response_model=OpportunityResponse)
async def get_opportunity(opportunity_id: str):
    """Obtém detalhes de uma oportunidade"""
    try:
        from services.suitecrm_service import suitecrm_service
        
        result = await suitecrm_service.get_record("Opportunities", opportunity_id)
        
        attrs = result.get("data", {}).get("attributes", {})
        
        return {
            "id": opportunity_id,
            "name": attrs.get("name", ""),
            "account_id": attrs.get("account_id"),
            "account_name": attrs.get("account_name"),
            "amount": float(attrs.get("amount", 0)) if attrs.get("amount") else None,
            "sales_stage": attrs.get("sales_stage", ""),
            "probability": int(attrs.get("probability", 0)) if attrs.get("probability") else None,
            "date_closed": attrs.get("date_closed"),
            "next_step": attrs.get("next_step"),
            "description": attrs.get("description"),
            "lead_source": attrs.get("lead_source"),
            "opportunity_type": attrs.get("opportunity_type"),
            "assigned_user_name": attrs.get("assigned_user_name"),
            "created_at": attrs.get("date_entered"),
            "updated_at": attrs.get("date_modified")
        }
        
    except Exception as e:
        logger.error(f"Erro ao obter oportunidade {opportunity_id}: {e}")
        raise HTTPException(status_code=404, detail="Oportunidade não encontrada")


@router.post("/", response_model=OpportunityResponse, status_code=201)
async def create_opportunity(opportunity: OpportunityCreate):
    """Cria uma nova oportunidade"""
    try:
        from services.suitecrm_service import suitecrm_service
        
        attributes = {
            "name": opportunity.name,
            "sales_stage": opportunity.sales_stage,
            "amount": str(opportunity.amount) if opportunity.amount else None,
            "probability": str(opportunity.probability) if opportunity.probability else None,
            "date_closed": opportunity.date_closed.isoformat() if opportunity.date_closed else None,
            "next_step": opportunity.next_step,
            "description": opportunity.description,
            "lead_source": opportunity.lead_source,
            "opportunity_type": opportunity.opportunity_type
        }
        
        if opportunity.account_id:
            attributes["account_id"] = opportunity.account_id
        
        # Remover campos None
        attributes = {k: v for k, v in attributes.items() if v is not None}
        
        result = await suitecrm_service.create_record("Opportunities", attributes)
        
        opportunity_id = result.get("data", {}).get("id")
        
        logger.info(f"✅ Oportunidade criada: {opportunity.name} ({opportunity_id})")
        
        return await get_opportunity(opportunity_id)
        
    except Exception as e:
        logger.error(f"Erro ao criar oportunidade: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{opportunity_id}", response_model=OpportunityResponse)
async def update_opportunity(opportunity_id: str, opportunity: OpportunityUpdate):
    """Atualiza uma oportunidade"""
    try:
        from services.suitecrm_service import suitecrm_service
        
        attributes = {}
        
        if opportunity.name is not None:
            attributes["name"] = opportunity.name
        if opportunity.account_id is not None:
            attributes["account_id"] = opportunity.account_id
        if opportunity.amount is not None:
            attributes["amount"] = str(opportunity.amount)
        if opportunity.sales_stage is not None:
            attributes["sales_stage"] = opportunity.sales_stage
        if opportunity.probability is not None:
            attributes["probability"] = str(opportunity.probability)
        if opportunity.date_closed is not None:
            attributes["date_closed"] = opportunity.date_closed.isoformat()
        if opportunity.next_step is not None:
            attributes["next_step"] = opportunity.next_step
        if opportunity.description is not None:
            attributes["description"] = opportunity.description
        if opportunity.lead_source is not None:
            attributes["lead_source"] = opportunity.lead_source
        if opportunity.opportunity_type is not None:
            attributes["opportunity_type"] = opportunity.opportunity_type
        
        if not attributes:
            raise HTTPException(status_code=400, detail="Nenhum campo para atualizar")
        
        await suitecrm_service.update_record("Opportunities", opportunity_id, attributes)
        
        logger.info(f"✅ Oportunidade atualizada: {opportunity_id}")
        
        return await get_opportunity(opportunity_id)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao atualizar oportunidade {opportunity_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{opportunity_id}", status_code=204)
async def delete_opportunity(opportunity_id: str):
    """Deleta uma oportunidade"""
    try:
        from services.suitecrm_service import suitecrm_service
        
        await suitecrm_service.delete_record("Opportunities", opportunity_id)
        
        logger.info(f"✅ Oportunidade deletada: {opportunity_id}")
        
        return None
        
    except Exception as e:
        logger.error(f"Erro ao deletar oportunidade {opportunity_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats/pipeline")
async def get_pipeline_stats():
    """Estatísticas do pipeline de vendas"""
    try:
        from services.suitecrm_service import suitecrm_service
        
        result = await suitecrm_service.get_module_records(
            module="Opportunities",
            page_size=1000
        )
        
        opportunities = result.get("data", [])
        
        # Agrupar por estágio
        by_stage = {}
        total_value = 0
        weighted_value = 0
        
        for opp in opportunities:
            attrs = opp.get("attributes", {})
            stage = attrs.get("sales_stage", "Unknown")
            amount = float(attrs.get("amount", 0)) if attrs.get("amount") else 0
            probability = int(attrs.get("probability", 0)) if attrs.get("probability") else 0
            
            if stage not in by_stage:
                by_stage[stage] = {
                    "count": 0,
                    "total_value": 0,
                    "avg_probability": []
                }
            
            by_stage[stage]["count"] += 1
            by_stage[stage]["total_value"] += amount
            by_stage[stage]["avg_probability"].append(probability)
            
            total_value += amount
            weighted_value += (amount * probability / 100)
        
        # Calcular médias
        for stage in by_stage:
            probs = by_stage[stage]["avg_probability"]
            by_stage[stage]["avg_probability"] = sum(probs) / len(probs) if probs else 0
        
        return {
            "total_opportunities": len(opportunities),
            "total_pipeline_value": total_value,
            "weighted_pipeline_value": weighted_value,
            "by_stage": by_stage
        }
        
    except Exception as e:
        logger.error(f"Erro ao obter estatísticas do pipeline: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sales-stages/list")
async def list_sales_stages():
    """Lista os estágios de vendas disponíveis"""
    return {
        "stages": [
            {"value": "Prospecting", "label": "Prospecção", "order": 1},
            {"value": "Qualification", "label": "Qualificação", "order": 2},
            {"value": "Needs Analysis", "label": "Análise de Necessidades", "order": 3},
            {"value": "Value Proposition", "label": "Proposta de Valor", "order": 4},
            {"value": "Id. Decision Makers", "label": "Identificação de Decisores", "order": 5},
            {"value": "Perception Analysis", "label": "Análise de Percepção", "order": 6},
            {"value": "Proposal/Price Quote", "label": "Proposta/Cotação", "order": 7},
            {"value": "Negotiation/Review", "label": "Negociação/Revisão", "order": 8},
            {"value": "Closed Won", "label": "Ganho", "order": 9},
            {"value": "Closed Lost", "label": "Perdido", "order": 10}
        ]
    }
