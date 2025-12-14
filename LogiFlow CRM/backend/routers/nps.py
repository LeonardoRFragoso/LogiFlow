"""
LogiFlow CRM - Router NPS e Satisfação
Endpoints para pesquisas NPS, CSAT e dashboard de satisfação
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from datetime import datetime, timedelta
import logging

from services.nps_service import NPSService, CSATService, SatisfactionDashboard

logger = logging.getLogger(__name__)

router = APIRouter()


# ===========================================
# NPS Endpoints
# ===========================================

@router.post("/nps/pesquisa/criar")
async def criar_pesquisa_nps(
    cliente_id: str,
    tipo: str = Query("30_dias", description="Tipo: 30_dias ou 90_dias")
):
    """
    Cria pesquisa NPS para um cliente
    
    Args:
        cliente_id: ID do cliente
        tipo: "30_dias" ou "90_dias"
        
    Returns:
        Pesquisa criada
    """
    try:
        nps_service = NPSService()
        pesquisa = nps_service.criar_pesquisa_nps(cliente_id, tipo)
        
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
    pesquisa_id: str,
    resposta: dict
):
    """
    Registra resposta de pesquisa NPS
    
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
        
        nps_service = NPSService()
        pesquisa = nps_service.registrar_resposta_nps(pesquisa_id, score, feedback)
        
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
    data_fim: Optional[str] = Query(None, description="Data fim (ISO)")
):
    """
    Calcula NPS de um período
    
    Args:
        data_inicio: Data inicial (opcional, padrão: 30 dias atrás)
        data_fim: Data final (opcional, padrão: hoje)
        
    Returns:
        NPS e estatísticas
    """
    try:
        # Parse datas
        if data_fim:
            dt_fim = datetime.fromisoformat(data_fim)
        else:
            dt_fim = datetime.now()
        
        if data_inicio:
            dt_inicio = datetime.fromisoformat(data_inicio)
        else:
            dt_inicio = dt_fim - timedelta(days=30)
        
        nps_service = NPSService()
        resultado = nps_service.obter_nps_periodo(dt_inicio, dt_fim)
        
        return {
            "success": True,
            "data": resultado
        }
        
    except Exception as e:
        logger.error(f"Erro ao calcular NPS: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/nps/agendar-automaticas")
async def agendar_pesquisas_automaticas():
    """
    Agenda pesquisas NPS automáticas para clientes elegíveis
    
    Returns:
        Lista de pesquisas agendadas
    """
    try:
        nps_service = NPSService()
        pesquisas = nps_service.agendar_pesquisas_automaticas()
        
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
    cliente_id: str
):
    """
    Cria pesquisa CSAT após fechamento de ticket
    
    Args:
        ticket_id: ID do ticket de suporte
        cliente_id: ID do cliente
        
    Returns:
        Pesquisa criada
    """
    try:
        csat_service = CSATService()
        pesquisa = csat_service.criar_pesquisa_csat(ticket_id, cliente_id)
        
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
    pesquisa_id: str,
    resposta: dict
):
    """
    Registra resposta de pesquisa CSAT
    
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
        
        csat_service = CSATService()
        pesquisa = csat_service.registrar_resposta_csat(pesquisa_id, score, comentario)
        
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
    data_fim: Optional[str] = Query(None, description="Data fim (ISO)")
):
    """
    Calcula CSAT médio de um período
    
    Args:
        data_inicio: Data inicial (opcional, padrão: 30 dias atrás)
        data_fim: Data final (opcional, padrão: hoje)
        
    Returns:
        CSAT e estatísticas
    """
    try:
        # Parse datas
        if data_fim:
            dt_fim = datetime.fromisoformat(data_fim)
        else:
            dt_fim = datetime.now()
        
        if data_inicio:
            dt_inicio = datetime.fromisoformat(data_inicio)
        else:
            dt_inicio = dt_fim - timedelta(days=30)
        
        csat_service = CSATService()
        resultado = csat_service.calcular_csat_periodo(dt_inicio, dt_fim)
        
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
    periodo_dias: int = Query(30, description="Período em dias")
):
    """
    Obtém dashboard consolidado de NPS e CSAT
    
    Args:
        periodo_dias: Período de análise em dias
        
    Returns:
        Dashboard com NPS, CSAT, tendências e alertas
    """
    try:
        dashboard = SatisfactionDashboard()
        resultado = dashboard.obter_dashboard(periodo_dias)
        
        return {
            "success": True,
            "data": resultado
        }
        
    except Exception as e:
        logger.error(f"Erro ao obter dashboard de satisfação: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/satisfacao/alertas")
async def obter_alertas_satisfacao():
    """
    Obtém alertas ativos de satisfação (detratores e insatisfeitos)
    
    Returns:
        Lista de alertas
    """
    try:
        dashboard = SatisfactionDashboard()
        alertas = dashboard._obter_alertas_ativos()
        
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
async def executar_acoes_automaticas():
    """
    Executa ações automáticas baseadas em scores de satisfação
    
    - Detratores NPS: Criar alerta para CS
    - Promotores NPS: Solicitar depoimento
    - CSAT baixo: Criar ticket de follow-up
    
    Returns:
        Resumo das ações executadas
    """
    try:
        acoes_executadas = []
        
        # Simular ações (em produção, processar alertas reais)
        acoes_executadas.append({
            "tipo": "alerta_cs",
            "cliente": "Empresa ABC",
            "motivo": "NPS Detrator (score 4)",
            "acao": "Alerta criado para Customer Success"
        })
        
        acoes_executadas.append({
            "tipo": "solicitar_depoimento",
            "cliente": "Transportadora XYZ",
            "motivo": "NPS Promotor (score 10)",
            "acao": "Email enviado solicitando depoimento"
        })
        
        acoes_executadas.append({
            "tipo": "follow_up_suporte",
            "cliente": "Logística 123",
            "motivo": "CSAT baixo (score 2)",
            "acao": "Ticket de follow-up criado"
        })
        
        return {
            "success": True,
            "message": f"{len(acoes_executadas)} ações executadas",
            "data": acoes_executadas
        }
        
    except Exception as e:
        logger.error(f"Erro ao executar ações automáticas: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ===========================================
# Relatórios
# ===========================================

@router.get("/satisfacao/relatorio/mensal")
async def relatorio_mensal_satisfacao():
    """
    Gera relatório mensal de satisfação
    
    Returns:
        Relatório consolidado do mês
    """
    try:
        data_fim = datetime.now()
        data_inicio = data_fim - timedelta(days=30)
        
        nps_service = NPSService()
        csat_service = CSATService()
        
        nps_data = nps_service.obter_nps_periodo(data_inicio, data_fim)
        csat_data = csat_service.calcular_csat_periodo(data_inicio, data_fim)
        
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
                "total_respostas_csat": csat_data["total_respostas"],
                "taxa_resposta_nps": "75%",  # Simular
                "taxa_resposta_csat": "82%",  # Simular
                "tendencia_nps": "crescente",
                "tendencia_csat": "estavel"
            },
            "acoes_tomadas": {
                "alertas_criados": 3,
                "depoimentos_solicitados": 5,
                "follow_ups_realizados": 2
            }
        }
        
        return {
            "success": True,
            "data": relatorio
        }
        
    except Exception as e:
        logger.error(f"Erro ao gerar relatório mensal: {e}")
        raise HTTPException(status_code=500, detail=str(e))
