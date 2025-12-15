"""
LogiFlow CRM - Router NPS e Satisfação
Endpoints para pesquisas NPS, CSAT e dashboard de satisfação (COM PERSISTÊNCIA)
"""

from fastapi import APIRouter, HTTPException, Query, Depends, Header
from typing import Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import logging

from services.nps_service import NPSService, CSATService, SatisfactionDashboard
from database import get_db

logger = logging.getLogger(__name__)

router = APIRouter()


# ===========================================
# NPS Endpoints
# ===========================================

@router.post("/nps/pesquisa/criar")
async def criar_pesquisa_nps(
    cliente_id: str,
    tipo: str = Query("30_dias", description="Tipo: 30_dias ou 90_dias"),
    x_tenant_id: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """
    Cria pesquisa NPS para um cliente (PERSISTENTE)
    
    Args:
        cliente_id: ID do cliente
        tipo: "30_dias" ou "90_dias"
        x_tenant_id: ID do tenant
        
    Returns:
        Pesquisa criada
    """
    try:
        if not x_tenant_id:
            raise HTTPException(status_code=400, detail="X-Tenant-ID obrigatório")
        
        nps_service = NPSService(db)
        pesquisa = nps_service.criar_pesquisa_nps(x_tenant_id, cliente_id, tipo)
        
        return {
            "success": True,
            "message": "Pesquisa NPS criada com sucesso",
            "data": pesquisa
        }
        
    except Exception as e:
        logger.error(f"Erro ao criar pesquisa NPS: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/nps/pesquisa/{pesquisa_id}/responder")
async def responder_pesquisa_nps(
    pesquisa_id: int,
    resposta: dict,
    db: Session = Depends(get_db)
):
    """
    Registra resposta de pesquisa NPS (PERSISTENTE)
    
    Args:
        pesquisa_id: ID da pesquisa
        resposta: {"score": 0-10, "feedback": "texto opcional"}
        
    Returns:
        Pesquisa atualizada
    """
    try:
        if "score" not in resposta:
            raise HTTPException(status_code=400, detail="Campo 'score' obrigatório")
        
        score = resposta["score"]
        feedback = resposta.get("feedback")
        ip = resposta.get("ip")
        
        nps_service = NPSService(db)
        pesquisa = nps_service.registrar_resposta_nps(pesquisa_id, score, feedback, ip)
        
        return {
            "success": True,
            "message": "Resposta registrada com sucesso",
            "data": pesquisa
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Erro ao registrar resposta NPS: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/nps/calcular")
async def calcular_nps(
    data_inicio: Optional[str] = Query(None, description="Data início (ISO)"),
    data_fim: Optional[str] = Query(None, description="Data fim (ISO)"),
    x_tenant_id: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """
    Calcula NPS de um período (REAL do banco)
    
    Args:
        data_inicio: Data inicial (opcional, padrão: 30 dias atrás)
        data_fim: Data final (opcional, padrão: hoje)
        x_tenant_id: ID do tenant
        
    Returns:
        NPS e estatísticas
    """
    try:
        if not x_tenant_id:
            raise HTTPException(status_code=400, detail="X-Tenant-ID obrigatório")
        
        # Parse datas
        if data_fim:
            dt_fim = datetime.fromisoformat(data_fim)
        else:
            dt_fim = datetime.utcnow()
        
        if data_inicio:
            dt_inicio = datetime.fromisoformat(data_inicio)
        else:
            dt_inicio = dt_fim - timedelta(days=30)
        
        nps_service = NPSService(db)
        resultado = nps_service.obter_nps_periodo(x_tenant_id, dt_inicio, dt_fim)
        
        return {
            "success": True,
            "data": resultado
        }
        
    except Exception as e:
        logger.error(f"Erro ao calcular NPS: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/nps/agendar-automaticas")
async def agendar_pesquisas_automaticas(
    x_tenant_id: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """
    Agenda pesquisas NPS automáticas para clientes elegíveis (PERSISTENTE)
    
    Args:
        x_tenant_id: ID do tenant
    
    Returns:
        Lista de pesquisas agendadas
    """
    try:
        if not x_tenant_id:
            raise HTTPException(status_code=400, detail="X-Tenant-ID obrigatório")
        
        nps_service = NPSService(db)
        pesquisas = nps_service.agendar_pesquisas_automaticas(x_tenant_id)
        
        return {
            "success": True,
            "message": f"{len(pesquisas)} pesquisas agendadas",
            "data": pesquisas
        }
        
    except Exception as e:
        logger.error(f"Erro ao agendar pesquisas: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ===========================================
# CSAT Endpoints
# ===========================================

@router.post("/csat/pesquisa/criar")
async def criar_pesquisa_csat(
    ticket_id: str,
    cliente_id: str,
    atendente: Optional[str] = None,
    x_tenant_id: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """
    Cria pesquisa CSAT após fechamento de ticket (PERSISTENTE)
    
    Args:
        ticket_id: ID do ticket de suporte
        cliente_id: ID do cliente
        atendente: Nome do atendente responsável
        x_tenant_id: ID do tenant
        
    Returns:
        Pesquisa criada
    """
    try:
        if not x_tenant_id:
            raise HTTPException(status_code=400, detail="X-Tenant-ID obrigatório")
        
        csat_service = CSATService(db)
        pesquisa = csat_service.criar_pesquisa_csat(x_tenant_id, ticket_id, cliente_id, atendente)
        
        return {
            "success": True,
            "message": "Pesquisa CSAT criada com sucesso",
            "data": pesquisa
        }
        
    except Exception as e:
        logger.error(f"Erro ao criar pesquisa CSAT: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/csat/pesquisa/{pesquisa_id}/responder")
async def responder_pesquisa_csat(
    pesquisa_id: int,
    resposta: dict,
    db: Session = Depends(get_db)
):
    """
    Registra resposta de pesquisa CSAT (PERSISTENTE)
    
    Args:
        pesquisa_id: ID da pesquisa
        resposta: {"score": 1-5, "comentario": "texto opcional"}
        
    Returns:
        Pesquisa atualizada
    """
    try:
        if "score" not in resposta:
            raise HTTPException(status_code=400, detail="Campo 'score' obrigatório")
        
        score = resposta["score"]
        comentario = resposta.get("comentario")
        ip = resposta.get("ip")
        
        csat_service = CSATService(db)
        pesquisa = csat_service.registrar_resposta_csat(pesquisa_id, score, comentario, ip)
        
        return {
            "success": True,
            "message": "Resposta registrada com sucesso",
            "data": pesquisa
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Erro ao registrar resposta CSAT: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/csat/calcular")
async def calcular_csat(
    data_inicio: Optional[str] = Query(None, description="Data início (ISO)"),
    data_fim: Optional[str] = Query(None, description="Data fim (ISO)"),
    x_tenant_id: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """
    Calcula CSAT médio de um período (REAL do banco)
    
    Args:
        data_inicio: Data inicial (opcional, padrão: 30 dias atrás)
        data_fim: Data final (opcional, padrão: hoje)
        x_tenant_id: ID do tenant
        
    Returns:
        CSAT e estatísticas
    """
    try:
        if not x_tenant_id:
            raise HTTPException(status_code=400, detail="X-Tenant-ID obrigatório")
        
        # Parse datas
        if data_fim:
            dt_fim = datetime.fromisoformat(data_fim)
        else:
            dt_fim = datetime.utcnow()
        
        if data_inicio:
            dt_inicio = datetime.fromisoformat(data_inicio)
        else:
            dt_inicio = dt_fim - timedelta(days=30)
        
        csat_service = CSATService(db)
        resultado = csat_service.calcular_csat_periodo(x_tenant_id, dt_inicio, dt_fim)
        
        return {
            "success": True,
            "data": resultado
        }
        
    except Exception as e:
        logger.error(f"Erro ao calcular CSAT: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ===========================================
# Dashboard de Satisfação
# ===========================================

@router.get("/satisfacao/dashboard")
async def obter_dashboard_satisfacao(
    periodo_dias: int = Query(30, description="Período em dias"),
    x_tenant_id: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """
    Obtém dashboard consolidado de NPS e CSAT (REAL)
    
    Args:
        periodo_dias: Período de análise em dias
        x_tenant_id: ID do tenant
        
    Returns:
        Dashboard com NPS, CSAT, tendências e alertas
    """
    try:
        if not x_tenant_id:
            raise HTTPException(status_code=400, detail="X-Tenant-ID obrigatório")
        
        dashboard = SatisfactionDashboard(db)
        resultado = dashboard.obter_dashboard(x_tenant_id, periodo_dias)
        
        return {
            "success": True,
            "data": resultado
        }
        
    except Exception as e:
        logger.error(f"Erro ao obter dashboard de satisfação: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/satisfacao/alertas")
async def obter_alertas_satisfacao(
    x_tenant_id: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """
    Obtém alertas ativos de satisfação (REAL - detratores e insatisfeitos)
    
    Args:
        x_tenant_id: ID do tenant
    
    Returns:
        Lista de alertas
    """
    try:
        if not x_tenant_id:
            raise HTTPException(status_code=400, detail="X-Tenant-ID obrigatório")
        
        dashboard = SatisfactionDashboard(db)
        alertas = dashboard._obter_alertas_ativos(x_tenant_id)
        
        return {
            "success": True,
            "total": len(alertas),
            "data": alertas
        }
        
    except Exception as e:
        logger.error(f"Erro ao obter alertas: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ===========================================
# Ações Automáticas
# ===========================================

@router.post("/satisfacao/acoes/executar")
async def executar_acoes_automaticas(
    x_tenant_id: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """
    Executa ações automáticas baseadas em scores de satisfação (REAL)
    
    - Detratores NPS: Criar alerta para CS
    - Promotores NPS: Solicitar depoimento
    - CSAT baixo: Criar ticket de follow-up
    
    Args:
        x_tenant_id: ID do tenant
    
    Returns:
        Resumo das ações executadas
    """
    try:
        if not x_tenant_id:
            raise HTTPException(status_code=400, detail="X-Tenant-ID obrigatório")
        
        from models import CustomerSuccessAction
        
        # Buscar ações pendentes
        acoes = db.query(CustomerSuccessAction).filter(
            CustomerSuccessAction.tenant_id == x_tenant_id,
            CustomerSuccessAction.status == "pendente"
        ).order_by(CustomerSuccessAction.prioridade.desc()).limit(20).all()
        
        acoes_executadas = [
            {
                "id": acao.id,
                "tipo": acao.origem_tipo,
                "cliente_id": acao.cliente_id,
                "titulo": acao.titulo,
                "descricao": acao.descricao,
                "prioridade": acao.prioridade,
                "responsavel": acao.responsavel,
                "prazo": acao.prazo.isoformat() if acao.prazo else None
            }
            for acao in acoes
        ]
        
        return {
            "success": True,
            "message": f"{len(acoes_executadas)} ações pendentes encontradas",
            "data": acoes_executadas
        }
        
    except Exception as e:
        logger.error(f"Erro ao executar ações automáticas: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ===========================================
# Relatórios
# ===========================================

@router.get("/satisfacao/relatorio/mensal")
async def relatorio_mensal_satisfacao(
    x_tenant_id: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """
    Gera relatório mensal de satisfação (REAL)
    
    Args:
        x_tenant_id: ID do tenant
    
    Returns:
        Relatório consolidado do mês
    """
    try:
        if not x_tenant_id:
            raise HTTPException(status_code=400, detail="X-Tenant-ID obrigatório")
        
        data_fim = datetime.utcnow()
        data_inicio = data_fim - timedelta(days=30)
        
        nps_service = NPSService(db)
        csat_service = CSATService(db)
        
        nps_data = nps_service.obter_nps_periodo(x_tenant_id, data_inicio, data_fim)
        csat_data = csat_service.calcular_csat_periodo(x_tenant_id, data_inicio, data_fim)
        
        # Contar ações criadas no período
        from models import CustomerSuccessAction
        from sqlalchemy import and_
        
        total_acoes = db.query(CustomerSuccessAction).filter(
            and_(
                CustomerSuccessAction.tenant_id == x_tenant_id,
                CustomerSuccessAction.data_criacao >= data_inicio,
                CustomerSuccessAction.data_criacao <= data_fim
            )
        ).count()
        
        acoes_por_tipo = db.query(
            CustomerSuccessAction.origem_tipo,
            func.count(CustomerSuccessAction.id)
        ).filter(
            and_(
                CustomerSuccessAction.tenant_id == x_tenant_id,
                CustomerSuccessAction.data_criacao >= data_inicio,
                CustomerSuccessAction.data_criacao <= data_fim
            )
        ).group_by(CustomerSuccessAction.origem_tipo).all()
        
        relatorio = {
            "periodo": {
                "inicio": data_inicio.isoformat(),
                "fim": data_fim.isoformat(),
                "dias": 30
            },
            "nps": nps_data,
            "csat": csat_data,
            "resumo": {
                "total_respostas_nps": nps_data["total_respostas"],
                "total_respostas_csat": csat_data["total_respostas"]
            },
            "acoes_tomadas": {
                "total": total_acoes,
                "por_tipo": {tipo: count for tipo, count in acoes_por_tipo}
            }
        }
        
        return {
            "success": True,
            "data": relatorio
        }
        
    except Exception as e:
        logger.error(f"Erro ao gerar relatório mensal: {e}")
        raise HTTPException(status_code=500, detail=str(e))
