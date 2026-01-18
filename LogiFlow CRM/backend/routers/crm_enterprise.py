"""
LogiFlow CRM - Router Enterprise Principal
===========================================
Endpoints completos para CRM nível Enterprise
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload, selectinload
from typing import List, Optional
from datetime import datetime, date
from pydantic import BaseModel, Field
from loguru import logger

from database import get_db
from models import (
    Opportunity, CustomerInteraction, Cliente, Lead,
    OpportunityStageHistory, SalesStage, InteractionType, StatusLead, User
)
from models_crm_enterprise import (
    OpportunityNote, OpportunityProduct, SalesActivity,
    ClienteFieldHistory, LeadStatusHistory
)
from services.crm_metrics_service import CRMMetricsService
from services.crm_alerts_service import CRMAlertsService
from services.health_score_service import HealthScoreService
from services.sales_forecast_service import SalesForecastService
from services.opportunity_sla_service import OpportunitySLAService


router = APIRouter(prefix="/crm", tags=["CRM Enterprise"])


# ========================================
# Schemas
# ========================================

class OpportunityCreate(BaseModel):
    cliente_id: str
    nome: str
    descricao: Optional[str] = None
    valor_estimado: float = 0
    probabilidade: int = 0
    sales_stage: str = SalesStage.LEAD.value
    data_prevista_fechamento: Optional[datetime] = None
    responsavel_id: Optional[str] = None
    origem: Optional[str] = None
    proximo_passo: Optional[str] = None


class OpportunityUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    valor_estimado: Optional[float] = None
    probabilidade: Optional[int] = None
    sales_stage: Optional[str] = None
    data_prevista_fechamento: Optional[datetime] = None
    responsavel_id: Optional[str] = None
    proximo_passo: Optional[str] = None
    motivo_perda: Optional[str] = None
    concorrente: Optional[str] = None


class OpportunityResponse(BaseModel):
    id: str
    cliente_id: str
    cliente_nome: Optional[str]
    nome: str
    descricao: Optional[str]
    valor_estimado: float
    probabilidade: int
    sales_stage: str
    data_prevista_fechamento: Optional[datetime]
    data_fechamento: Optional[datetime]
    responsavel_id: Optional[str]
    responsavel_nome: Optional[str]
    origem: Optional[str]
    proximo_passo: Optional[str]
    criado_em: datetime
    atualizado_em: datetime

    class Config:
        from_attributes = True


class InteractionCreate(BaseModel):
    cliente_id: str
    oportunidade_id: Optional[str] = None
    tipo: str
    assunto: str
    descricao: Optional[str] = None
    responsavel_id: str
    data_interacao: datetime
    duracao_minutos: Optional[int] = None
    resultado: Optional[str] = None
    proxima_acao: Optional[str] = None
    data_proxima_acao: Optional[datetime] = None


class InteractionUpdate(BaseModel):
    assunto: Optional[str] = None
    descricao: Optional[str] = None
    duracao_minutos: Optional[int] = None
    resultado: Optional[str] = None
    proxima_acao: Optional[str] = None
    data_proxima_acao: Optional[datetime] = None


class InteractionResponse(BaseModel):
    id: int
    cliente_id: str
    cliente_nome: Optional[str]
    oportunidade_id: Optional[str]
    oportunidade_nome: Optional[str]
    tipo: str
    assunto: str
    descricao: Optional[str]
    responsavel_id: str
    responsavel_nome: Optional[str]
    data_interacao: datetime
    duracao_minutos: Optional[int]
    resultado: Optional[str]
    proxima_acao: Optional[str]
    data_proxima_acao: Optional[datetime]
    criado_em: datetime

    class Config:
        from_attributes = True


class LeadUpdateEnterprise(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    cargo: Optional[str] = None
    status: Optional[str] = None
    lead_score: Optional[int] = None
    estagio_maturidade: Optional[str] = None
    assigned_to: Optional[str] = None
    necessidade_descrita: Optional[str] = None
    proximo_followup_em: Optional[datetime] = None


# ========================================
# Oportunidades Endpoints
# ========================================

@router.post("/opportunities", response_model=OpportunityResponse, status_code=201)
async def criar_oportunidade(
    opp: OpportunityCreate,
    db: Session = Depends(get_db)
):
    """Cria nova oportunidade"""
    cliente = db.query(Cliente).filter(Cliente.id == opp.cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    nova_opp = Opportunity(
        cliente_id=opp.cliente_id,
        nome=opp.nome,
        descricao=opp.descricao,
        valor_estimado=opp.valor_estimado,
        probabilidade=opp.probabilidade,
        sales_stage=opp.sales_stage,
        data_prevista_fechamento=opp.data_prevista_fechamento,
        responsavel_id=opp.responsavel_id,
        origem=opp.origem,
        proximo_passo=opp.proximo_passo
    )
    
    db.add(nova_opp)
    db.flush()
    
    historico = OpportunityStageHistory(
        oportunidade_id=nova_opp.id,
        estagio_anterior=None,
        estagio_novo=opp.sales_stage,
        usuario_id=opp.responsavel_id
    )
    db.add(historico)
    
    db.commit()
    db.refresh(nova_opp)
    
    logger.info(f"Oportunidade criada: {nova_opp.nome} ({nova_opp.id})")
    
    return OpportunityResponse(
        id=nova_opp.id,
        cliente_id=nova_opp.cliente_id,
        cliente_nome=cliente.razao_social,
        nome=nova_opp.nome,
        descricao=nova_opp.descricao,
        valor_estimado=nova_opp.valor_estimado,
        probabilidade=nova_opp.probabilidade,
        sales_stage=nova_opp.sales_stage,
        data_prevista_fechamento=nova_opp.data_prevista_fechamento,
        data_fechamento=nova_opp.data_fechamento,
        responsavel_id=nova_opp.responsavel_id,
        responsavel_nome=nova_opp.responsavel.nome if nova_opp.responsavel else None,
        origem=nova_opp.origem,
        proximo_passo=nova_opp.proximo_passo,
        criado_em=nova_opp.criado_em,
        atualizado_em=nova_opp.atualizado_em
    )


@router.get("/opportunities", response_model=List[OpportunityResponse])
async def listar_oportunidades(
    sales_stage: Optional[str] = None,
    cliente_id: Optional[str] = None,
    responsavel_id: Optional[str] = None,
    limit: int = Query(50, le=200),
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """Lista oportunidades com filtros"""
    # Eager loading para evitar N+1 queries
    query = db.query(Opportunity)\
        .options(joinedload(Opportunity.cliente))\
        .options(joinedload(Opportunity.responsavel))
    
    if sales_stage:
        query = query.filter(Opportunity.sales_stage == sales_stage)
    if cliente_id:
        query = query.filter(Opportunity.cliente_id == cliente_id)
    if responsavel_id:
        query = query.filter(Opportunity.responsavel_id == responsavel_id)
    
    query = query.order_by(Opportunity.criado_em.desc())
    opps = query.offset(offset).limit(limit).all()
    
    resultado = []
    for opp in opps:
        resultado.append(OpportunityResponse(
            id=opp.id,
            cliente_id=opp.cliente_id,
            cliente_nome=opp.cliente.razao_social if opp.cliente else None,
            nome=opp.nome,
            descricao=opp.descricao,
            valor_estimado=opp.valor_estimado,
            probabilidade=opp.probabilidade,
            sales_stage=opp.sales_stage,
            data_prevista_fechamento=opp.data_prevista_fechamento,
            data_fechamento=opp.data_fechamento,
            responsavel_id=opp.responsavel_id,
            responsavel_nome=opp.responsavel.nome if opp.responsavel else None,
            origem=opp.origem,
            proximo_passo=opp.proximo_passo,
            criado_em=opp.criado_em,
            atualizado_em=opp.atualizado_em
        ))
    
    return resultado


@router.get("/opportunities/{opportunity_id}", response_model=OpportunityResponse)
async def obter_oportunidade(
    opportunity_id: str,
    db: Session = Depends(get_db)
):
    """Obtém detalhes de uma oportunidade"""
    opp = db.query(Opportunity)\
        .options(joinedload(Opportunity.cliente))\
        .options(joinedload(Opportunity.responsavel))\
        .filter(Opportunity.id == opportunity_id)\
        .first()
    if not opp:
        raise HTTPException(status_code=404, detail="Oportunidade não encontrada")
    
    return OpportunityResponse(
        id=opp.id,
        cliente_id=opp.cliente_id,
        cliente_nome=opp.cliente.razao_social if opp.cliente else None,
        nome=opp.nome,
        descricao=opp.descricao,
        valor_estimado=opp.valor_estimado,
        probabilidade=opp.probabilidade,
        sales_stage=opp.sales_stage,
        data_prevista_fechamento=opp.data_prevista_fechamento,
        data_fechamento=opp.data_fechamento,
        responsavel_id=opp.responsavel_id,
        responsavel_nome=opp.responsavel.nome if opp.responsavel else None,
        origem=opp.origem,
        proximo_passo=opp.proximo_passo,
        criado_em=opp.criado_em,
        atualizado_em=opp.atualizado_em
    )


@router.put("/opportunities/{opportunity_id}", response_model=OpportunityResponse)
async def atualizar_oportunidade(
    opportunity_id: str,
    opp_update: OpportunityUpdate,
    usuario_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Atualiza oportunidade"""
    opp = db.query(Opportunity)\
        .options(joinedload(Opportunity.cliente))\
        .options(joinedload(Opportunity.responsavel))\
        .filter(Opportunity.id == opportunity_id)\
        .first()
    if not opp:
        raise HTTPException(status_code=404, detail="Oportunidade não encontrada")
    
    estagio_anterior = opp.sales_stage
    
    if opp_update.nome is not None:
        opp.nome = opp_update.nome
    if opp_update.descricao is not None:
        opp.descricao = opp_update.descricao
    if opp_update.valor_estimado is not None:
        opp.valor_estimado = opp_update.valor_estimado
    if opp_update.probabilidade is not None:
        opp.probabilidade = opp_update.probabilidade
    if opp_update.sales_stage is not None and opp_update.sales_stage != estagio_anterior:
        opp.sales_stage = opp_update.sales_stage
        
        historico = OpportunityStageHistory(
            oportunidade_id=opp.id,
            estagio_anterior=estagio_anterior,
            estagio_novo=opp_update.sales_stage,
            usuario_id=usuario_id
        )
        db.add(historico)
        
        if opp_update.sales_stage == SalesStage.GANHO.value:
            opp.data_fechamento = datetime.utcnow()
        elif opp_update.sales_stage == SalesStage.PERDIDO.value:
            opp.data_fechamento = datetime.utcnow()
    
    if opp_update.data_prevista_fechamento is not None:
        opp.data_prevista_fechamento = opp_update.data_prevista_fechamento
    if opp_update.responsavel_id is not None:
        opp.responsavel_id = opp_update.responsavel_id
    if opp_update.proximo_passo is not None:
        opp.proximo_passo = opp_update.proximo_passo
    if opp_update.motivo_perda is not None:
        opp.motivo_perda = opp_update.motivo_perda
    if opp_update.concorrente is not None:
        opp.concorrente = opp_update.concorrente
    
    opp.atualizado_em = datetime.utcnow()
    
    db.commit()
    db.refresh(opp)
    
    logger.info(f"Oportunidade atualizada: {opp.id}")
    
    return OpportunityResponse(
        id=opp.id,
        cliente_id=opp.cliente_id,
        cliente_nome=opp.cliente.razao_social if opp.cliente else None,
        nome=opp.nome,
        descricao=opp.descricao,
        valor_estimado=opp.valor_estimado,
        probabilidade=opp.probabilidade,
        sales_stage=opp.sales_stage,
        data_prevista_fechamento=opp.data_prevista_fechamento,
        data_fechamento=opp.data_fechamento,
        responsavel_id=opp.responsavel_id,
        responsavel_nome=opp.responsavel.nome if opp.responsavel else None,
        origem=opp.origem,
        proximo_passo=opp.proximo_passo,
        criado_em=opp.criado_em,
        atualizado_em=opp.atualizado_em
    )


@router.get("/opportunities/{opportunity_id}/history")
async def obter_historico_oportunidade(
    opportunity_id: str,
    db: Session = Depends(get_db)
):
    """Obtém histórico de mudanças de estágio"""
    opp = db.query(Opportunity).filter(Opportunity.id == opportunity_id).first()
    if not opp:
        raise HTTPException(status_code=404, detail="Oportunidade não encontrada")
    
    historico = db.query(OpportunityStageHistory).filter(
        OpportunityStageHistory.oportunidade_id == opportunity_id
    ).order_by(OpportunityStageHistory.data_mudanca.desc()).all()
    
    return {
        'oportunidade_id': opportunity_id,
        'oportunidade_nome': opp.nome,
        'historico': [
            {
                'id': h.id,
                'estagio_anterior': h.estagio_anterior,
                'estagio_novo': h.estagio_novo,
                'usuario_nome': h.usuario.nome if h.usuario else 'Sistema',
                'data_mudanca': h.data_mudanca.isoformat(),
                'motivo': h.motivo
            }
            for h in historico
        ]
    }


# ========================================
# Interações Endpoints
# ========================================

@router.post("/interactions", response_model=InteractionResponse, status_code=201)
async def criar_interacao(
    interaction: InteractionCreate,
    db: Session = Depends(get_db)
):
    """Registra nova interação"""
    cliente = db.query(Cliente).filter(Cliente.id == interaction.cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    nova_interacao = CustomerInteraction(
        cliente_id=interaction.cliente_id,
        oportunidade_id=interaction.oportunidade_id,
        tipo=interaction.tipo,
        assunto=interaction.assunto,
        descricao=interaction.descricao,
        responsavel_id=interaction.responsavel_id,
        data_interacao=interaction.data_interacao,
        duracao_minutos=interaction.duracao_minutos,
        resultado=interaction.resultado,
        proxima_acao=interaction.proxima_acao,
        data_proxima_acao=interaction.data_proxima_acao
    )
    
    db.add(nova_interacao)
    
    cliente.data_ultimo_contato = interaction.data_interacao
    
    db.commit()
    db.refresh(nova_interacao)
    
    logger.info(f"Interação registrada: {nova_interacao.tipo} com {cliente.razao_social}")
    
    return InteractionResponse(
        id=nova_interacao.id,
        cliente_id=nova_interacao.cliente_id,
        cliente_nome=cliente.razao_social,
        oportunidade_id=nova_interacao.oportunidade_id,
        oportunidade_nome=nova_interacao.oportunidade.nome if nova_interacao.oportunidade else None,
        tipo=nova_interacao.tipo,
        assunto=nova_interacao.assunto,
        descricao=nova_interacao.descricao,
        responsavel_id=nova_interacao.responsavel_id,
        responsavel_nome=nova_interacao.responsavel.nome if nova_interacao.responsavel else None,
        data_interacao=nova_interacao.data_interacao,
        duracao_minutos=nova_interacao.duracao_minutos,
        resultado=nova_interacao.resultado,
        proxima_acao=nova_interacao.proxima_acao,
        data_proxima_acao=nova_interacao.data_proxima_acao,
        criado_em=nova_interacao.criado_em
    )


@router.get("/interactions", response_model=List[InteractionResponse])
async def listar_interacoes(
    cliente_id: Optional[str] = None,
    oportunidade_id: Optional[str] = None,
    tipo: Optional[str] = None,
    responsavel_id: Optional[str] = None,
    limit: int = Query(50, le=200),
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """Lista interações com filtros"""
    # Eager loading para evitar N+1 queries
    query = db.query(CustomerInteraction)\
        .options(joinedload(CustomerInteraction.cliente))\
        .options(joinedload(CustomerInteraction.responsavel))\
        .options(joinedload(CustomerInteraction.oportunidade))
    
    if cliente_id:
        query = query.filter(CustomerInteraction.cliente_id == cliente_id)
    if oportunidade_id:
        query = query.filter(CustomerInteraction.oportunidade_id == oportunidade_id)
    if tipo:
        query = query.filter(CustomerInteraction.tipo == tipo)
    if responsavel_id:
        query = query.filter(CustomerInteraction.responsavel_id == responsavel_id)
    
    query = query.order_by(CustomerInteraction.data_interacao.desc())
    interacoes = query.offset(offset).limit(limit).all()
    
    resultado = []
    for inter in interacoes:
        resultado.append(InteractionResponse(
            id=inter.id,
            cliente_id=inter.cliente_id,
            cliente_nome=inter.cliente.razao_social if inter.cliente else None,
            oportunidade_id=inter.oportunidade_id,
            oportunidade_nome=inter.oportunidade.nome if inter.oportunidade else None,
            tipo=inter.tipo,
            assunto=inter.assunto,
            descricao=inter.descricao,
            responsavel_id=inter.responsavel_id,
            responsavel_nome=inter.responsavel.nome if inter.responsavel else None,
            data_interacao=inter.data_interacao,
            duracao_minutos=inter.duracao_minutos,
            resultado=inter.resultado,
            proxima_acao=inter.proxima_acao,
            data_proxima_acao=inter.data_proxima_acao,
            criado_em=inter.criado_em
        ))
    
    return resultado


# ========================================
# Métricas e Analytics Endpoints
# ========================================

@router.get("/metrics/conversion-rates")
async def obter_taxas_conversao(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """Obtém taxas de conversão do funil"""
    service = CRMMetricsService(db)
    return service.get_funnel_conversion_rates(start_date, end_date)


@router.get("/metrics/pipeline-value")
async def obter_valor_pipeline(db: Session = Depends(get_db)):
    """Obtém valor do pipeline"""
    service = CRMMetricsService(db)
    return service.get_pipeline_value()


@router.get("/metrics/customer-activity")
async def obter_atividade_clientes(db: Session = Depends(get_db)):
    """Analisa atividade de clientes"""
    service = CRMMetricsService(db)
    return service.get_customer_activity_status()


@router.get("/metrics/dashboard")
async def obter_dashboard_completo(db: Session = Depends(get_db)):
    """Retorna dashboard completo de métricas"""
    service = CRMMetricsService(db)
    return service.get_complete_dashboard()


# ========================================
# Alertas Endpoints
# ========================================

@router.get("/alerts/all")
async def obter_todos_alertas(db: Session = Depends(get_db)):
    """Retorna todos os alertas comerciais"""
    service = CRMAlertsService(db)
    return service.get_all_alerts()


@router.get("/alerts/inactive-customers")
async def obter_clientes_inativos(
    days: int = Query(30, ge=1, le=180),
    minimum_revenue: float = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """Lista clientes sem contato há X dias"""
    service = CRMAlertsService(db)
    return service.get_inactive_customers(days, minimum_revenue)


@router.get("/alerts/stalled-opportunities")
async def obter_oportunidades_paradas(
    days: int = Query(15, ge=1, le=90),
    db: Session = Depends(get_db)
):
    """Lista oportunidades paradas no funil"""
    service = CRMAlertsService(db)
    return service.get_stalled_opportunities(days)


# ========================================
# Health Score Endpoints
# ========================================

@router.get("/health-score/{cliente_id}")
async def calcular_health_score_cliente(
    cliente_id: str,
    salvar: bool = True,
    db: Session = Depends(get_db)
):
    """Calcula health score de um cliente"""
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    service = HealthScoreService(db)
    return service.calcular_health_score(cliente, salvar)


@router.post("/health-score/recalcular-todos")
async def recalcular_todos_health_scores(db: Session = Depends(get_db)):
    """Recalcula health score de todos os clientes"""
    service = HealthScoreService(db)
    return service.recalcular_todos_clientes()


@router.get("/health-score/clientes-em-risco")
async def obter_clientes_em_risco(
    threshold: float = Query(40.0, ge=0, le=100),
    db: Session = Depends(get_db)
):
    """Lista clientes com health score abaixo do threshold"""
    service = HealthScoreService(db)
    return service.identificar_clientes_em_risco(threshold)


# ========================================
# Forecast Endpoints
# ========================================

@router.get("/forecast/mensal")
async def obter_forecast_mensal(
    ano: int,
    mes: int = Query(..., ge=1, le=12),
    responsavel_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Obtém forecast de vendas mensal"""
    service = SalesForecastService(db)
    return service.calcular_forecast_mensal(ano, mes, responsavel_id)


@router.get("/forecast/trimestral")
async def obter_forecast_trimestral(
    ano: int,
    trimestre: int = Query(..., ge=1, le=4),
    responsavel_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Obtém forecast de vendas trimestral"""
    service = SalesForecastService(db)
    return service.calcular_forecast_trimestral(ano, trimestre, responsavel_id)


# ========================================
# SLA Endpoints
# ========================================

@router.get("/sla/opportunity/{opportunity_id}")
async def verificar_sla_oportunidade(
    opportunity_id: str,
    db: Session = Depends(get_db)
):
    """Verifica SLA de uma oportunidade"""
    opp = db.query(Opportunity).filter(Opportunity.id == opportunity_id).first()
    if not opp:
        raise HTTPException(status_code=404, detail="Oportunidade não encontrada")
    
    service = OpportunitySLAService(db)
    return service.verificar_sla_oportunidade(opp)


@router.get("/sla/aging")
async def obter_aging_pipeline(db: Session = Depends(get_db)):
    """Obtém aging do pipeline completo"""
    service = OpportunitySLAService(db)
    return service.calcular_aging_pipeline()


@router.get("/sla/vencidas")
async def listar_oportunidades_vencidas(db: Session = Depends(get_db)):
    """Lista oportunidades com SLA vencido"""
    service = OpportunitySLAService(db)
    return service.listar_oportunidades_vencidas()


# ========================================
# Cliente 360 Endpoint
# ========================================

@router.get("/cliente-360/{cliente_id}")
async def obter_visao_360_cliente(
    cliente_id: str,
    db: Session = Depends(get_db)
):
    """Retorna visão 360º completa do cliente"""
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    oportunidades = db.query(Opportunity).filter(
        Opportunity.cliente_id == cliente_id
    ).order_by(Opportunity.criado_em.desc()).limit(10).all()
    
    interacoes = db.query(CustomerInteraction).filter(
        CustomerInteraction.cliente_id == cliente_id
    ).order_by(CustomerInteraction.data_interacao.desc()).limit(20).all()
    
    from models import Pedido
    pedidos = db.query(Pedido).filter(
        Pedido.cliente_id == cliente_id
    ).order_by(Pedido.criado_em.desc()).limit(10).all()
    
    health_service = HealthScoreService(db)
    health_score_info = health_service.calcular_health_score(cliente, salvar=False)
    
    return {
        'cliente': {
            'id': cliente.id,
            'razao_social': cliente.razao_social,
            'nome_fantasia': cliente.nome_fantasia,
            'cnpj': cliente.cnpj,
            'email': cliente.email,
            'telefone': cliente.telefone,
            'cidade': cliente.cidade,
            'uf': cliente.uf,
            'segmento': cliente.segmento,
            'porte': cliente.porte,
            'status_comercial': cliente.status_comercial,
            'classificacao': cliente.classificacao,
            'responsavel_comercial': cliente.responsavel_comercial.nome if cliente.responsavel_comercial else None,
            'criado_em': cliente.criado_em.isoformat()
        },
        'health_score': health_score_info,
        'metricas': {
            'valor_total_gasto': cliente.valor_total_gasto or 0,
            'ticket_medio': cliente.ticket_medio or 0,
            'total_pedidos': len(cliente.pedidos) if cliente.pedidos else 0,
            'total_oportunidades': len(oportunidades),
            'total_interacoes': len(interacoes),
            'data_primeira_compra': cliente.data_primeira_compra.isoformat() if cliente.data_primeira_compra else None,
            'data_ultima_compra': cliente.data_ultima_compra.isoformat() if cliente.data_ultima_compra else None,
            'data_ultimo_contato': cliente.data_ultimo_contato.isoformat() if cliente.data_ultimo_contato else None
        },
        'oportunidades_recentes': [
            {
                'id': opp.id,
                'nome': opp.nome,
                'valor_estimado': opp.valor_estimado,
                'sales_stage': opp.sales_stage,
                'probabilidade': opp.probabilidade,
                'criado_em': opp.criado_em.isoformat()
            }
            for opp in oportunidades
        ],
        'interacoes_recentes': [
            {
                'id': inter.id,
                'tipo': inter.tipo,
                'assunto': inter.assunto,
                'data_interacao': inter.data_interacao.isoformat(),
                'responsavel': inter.responsavel.nome if inter.responsavel else None
            }
            for inter in interacoes
        ],
        'timeline': self._construir_timeline(cliente, oportunidades, interacoes, pedidos)
    }


def _construir_timeline(cliente, oportunidades, interacoes, pedidos):
    """Constrói timeline consolidada de eventos do cliente"""
    eventos = []
    
    for opp in oportunidades:
        eventos.append({
            'tipo': 'oportunidade_criada',
            'data': opp.criado_em,
            'titulo': f'Oportunidade: {opp.nome}',
            'descricao': f'Valor estimado: R$ {opp.valor_estimado:,.2f}',
            'metadata': {'oportunidade_id': opp.id}
        })
    
    for inter in interacoes:
        eventos.append({
            'tipo': 'interacao',
            'data': inter.data_interacao,
            'titulo': f'{inter.tipo.upper()}: {inter.assunto}',
            'descricao': inter.descricao,
            'metadata': {'interacao_id': inter.id}
        })
    
    for pedido in pedidos:
        eventos.append({
            'tipo': 'pedido',
            'data': pedido.criado_em,
            'titulo': f'Pedido #{pedido.numero}',
            'descricao': f'Valor: R$ {pedido.valor_frete:,.2f} - Status: {pedido.status}',
            'metadata': {'pedido_id': pedido.id}
        })
    
    eventos.sort(key=lambda x: x['data'], reverse=True)
    
    return [
        {
            **evento,
            'data': evento['data'].isoformat()
        }
        for evento in eventos[:50]
    ]
