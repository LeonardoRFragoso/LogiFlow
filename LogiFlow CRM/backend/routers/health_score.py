"""
LogiFlow CRM - Router Health Score e Customer Success
Endpoints para cálculo de Health Score e alertas de churn (COM PERSISTÊNCIA)
"""

from fastapi import APIRouter, HTTPException, Query, Depends, Header
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
import logging

from services.health_score import HealthScoreCalculator, ChurnAlertSystem
from database import get_db

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/health-score/{cliente_id}")
async def calcular_health_score(cliente_id: str):
    """
    Calcula Health Score de um cliente específico
    
    Args:
        cliente_id: ID do cliente
        
    Returns:
        Health Score completo com métricas e recomendações
    """
    try:
        calculator = HealthScoreCalculator(cliente_id)
        resultado = calculator.calcular_health_score()
        
        return {
            "success": True,
            "data": resultado
        }
        
    except Exception as e:
        logger.error(f"Erro ao calcular Health Score: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health-score/batch")
async def calcular_health_score_lote(
    cliente_ids: List[str] = Query(..., description="Lista de IDs de clientes")
):
    """
    Calcula Health Score de múltiplos clientes
    
    Args:
        cliente_ids: Lista de IDs de clientes
        
    Returns:
        Lista de Health Scores
    """
    try:
        resultados = []
        
        for cliente_id in cliente_ids:
            calculator = HealthScoreCalculator(cliente_id)
            resultado = calculator.calcular_health_score()
            resultados.append(resultado)
        
        return {
            "success": True,
            "total": len(resultados),
            "data": resultados
        }
        
    except Exception as e:
        logger.error(f"Erro ao calcular Health Score em lote: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health-score/{cliente_id}/metricas")
async def obter_metricas_detalhadas(cliente_id: str):
    """
    Obtém métricas detalhadas de um cliente
    
    Args:
        cliente_id: ID do cliente
        
    Returns:
        Métricas individuais detalhadas
    """
    try:
        calculator = HealthScoreCalculator(cliente_id)
        
        # Calcular cada métrica individualmente
        metricas = {
            'uso': calculator.calcular_metrica_uso(),
            'adocao': calculator.calcular_metrica_adocao(),
            'engajamento': calculator.calcular_metrica_engajamento(),
            'suporte': calculator.calcular_metrica_suporte(),
            'financeiro': calculator.calcular_metrica_financeiro()
        }
        
        return {
            "success": True,
            "cliente_id": cliente_id,
            "metricas": metricas,
            "data_calculo": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Erro ao obter métricas: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/alertas")
async def obter_alertas_churn(
    urgencia: Optional[str] = Query(None, description="Filtrar por urgência: alta, media, critico"),
    limite: int = Query(50, description="Número máximo de alertas"),
    x_tenant_id: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """
    Obtém alertas de risco de churn (REAL do banco)
    
    Args:
        urgencia: Filtrar por urgência (baixo, medio, alto, critico)
        limite: Número máximo de alertas
        x_tenant_id: ID do tenant
        
    Returns:
        Lista de clientes em risco de churn
    """
    try:
        if not x_tenant_id:
            raise HTTPException(status_code=400, detail="X-Tenant-ID obrigatório")
        
        alert_system = ChurnAlertSystem(db)
        alertas = alert_system.obter_alertas_ativos(x_tenant_id)
        
        # Filtrar por nível de risco se especificado
        if urgencia:
            alertas = [a for a in alertas if a['nivel_risco'] == urgencia]
        
        # Limitar resultados
        alertas = alertas[:limite]
        
        return {
            "success": True,
            "total_alertas": len(alertas),
            "alertas": alertas,
            "data_verificacao": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Erro ao obter alertas de churn: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dashboard")
async def obter_dashboard_cs(
    x_tenant_id: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """
    Obtém dados consolidados para Dashboard de Customer Success (REAL)
    
    Args:
        x_tenant_id: ID do tenant
    
    Returns:
        Estatísticas gerais e clientes em risco
    """
    try:
        if not x_tenant_id:
            raise HTTPException(status_code=400, detail="X-Tenant-ID obrigatório")
        
        from models import Cliente, ChurnAlert
        from sqlalchemy import and_, func
        
        # Buscar alertas ativos
        alert_system = ChurnAlertSystem(db)
        alertas = alert_system.obter_alertas_ativos(x_tenant_id)
        
        # Total de clientes ativos
        total_clientes = db.query(Cliente).filter(
            and_(
                Cliente.tenant_id == x_tenant_id,
                Cliente.ativo == True
            )
        ).count()
        
        # Distribuição por nível de risco
        clientes_baixo = len([a for a in alertas if a['nivel_risco'] == 'baixo'])
        clientes_medio = len([a for a in alertas if a['nivel_risco'] == 'medio'])
        clientes_alto = len([a for a in alertas if a['nivel_risco'] == 'alto'])
        clientes_critico = len([a for a in alertas if a['nivel_risco'] == 'critico'])
        
        # Health Score médio
        if alertas:
            health_score_medio = sum(a['health_score'] for a in alertas) / len(alertas)
        else:
            health_score_medio = 0
        
        # Top 5 clientes em risco
        top_risco = sorted(alertas, key=lambda x: x['health_score'])[:5]
        
        # Top 5 clientes saudáveis (buscar do banco)
        clientes_saudaveis = db.query(Cliente).filter(
            and_(
                Cliente.tenant_id == x_tenant_id,
                Cliente.ativo == True
            )
        ).limit(5).all()
        
        top_saudaveis = [
            {
                "cliente_id": str(c.id),
                "cliente_nome": c.razao_social or c.nome_fantasia,
                "health_score": 85  # Simular por enquanto
            }
            for c in clientes_saudaveis
        ]
        
        # Taxa de risco de churn
        clientes_em_risco = clientes_alto + clientes_critico
        taxa_risco = (clientes_em_risco / total_clientes * 100) if total_clientes > 0 else 0
        
        return {
            "success": True,
            "estatisticas": {
                "total_clientes": total_clientes,
                "health_score_medio": round(health_score_medio, 2),
                "distribuicao": {
                    "baixo": clientes_baixo,
                    "medio": clientes_medio,
                    "alto": clientes_alto,
                    "critico": clientes_critico
                },
                "taxa_risco_churn": round(taxa_risco, 2)
            },
            "top_risco": top_risco,
            "top_saudaveis": top_saudaveis,
            "total_alertas_ativos": len([a for a in alertas if a['acao_requerida']]),
            "data_atualizacao": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Erro ao obter dashboard CS: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/customer-success/tendencias")
async def obter_tendencias(
    periodo_dias: int = Query(30, description="Período em dias para análise")
):
    """
    Obtém tendências de Health Score ao longo do tempo
    
    Args:
        periodo_dias: Período de análise em dias
        
    Returns:
        Dados de tendência e evolução
    """
    try:
        # Simular dados históricos (em produção, buscar do DB)
        tendencias = {
            "periodo_dias": periodo_dias,
            "evolucao_health_score": [
                {"data": "2024-11-14", "score_medio": 72.5},
                {"data": "2024-11-21", "score_medio": 74.2},
                {"data": "2024-11-28", "score_medio": 75.8},
                {"data": "2024-12-05", "score_medio": 76.1},
                {"data": "2024-12-12", "score_medio": 77.3}
            ],
            "evolucao_churn": [
                {"data": "2024-11-14", "taxa_risco": 15.2},
                {"data": "2024-11-21", "taxa_risco": 14.8},
                {"data": "2024-11-28", "taxa_risco": 13.5},
                {"data": "2024-12-05", "taxa_risco": 12.9},
                {"data": "2024-12-12", "taxa_risco": 11.7}
            ],
            "metricas_criticas": {
                "uso_sistema": {"atual": 78, "anterior": 75, "variacao": 3},
                "adocao_features": {"atual": 65, "anterior": 62, "variacao": 3},
                "engajamento": {"atual": 72, "anterior": 70, "variacao": 2},
                "suporte": {"atual": 85, "anterior": 83, "variacao": 2},
                "financeiro": {"atual": 92, "anterior": 90, "variacao": 2}
            }
        }
        
        return {
            "success": True,
            "data": tendencias
        }
        
    except Exception as e:
        logger.error(f"Erro ao obter tendências: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/customer-success/acao/{cliente_id}")
async def registrar_acao_cs(
    cliente_id: str,
    acao: dict
):
    """
    Registra ação de Customer Success para um cliente
    
    Args:
        cliente_id: ID do cliente
        acao: Dados da ação (tipo, descrição, responsável, etc)
        
    Returns:
        Confirmação de registro
    """
    try:
        # Validar ação
        if 'tipo' not in acao or 'descricao' not in acao:
            raise HTTPException(status_code=400, detail="Campos obrigatórios: tipo, descricao")
        
        # Registrar ação (em produção, salvar no DB)
        acao_registrada = {
            "id": f"acao_{datetime.now().timestamp()}",
            "cliente_id": cliente_id,
            "tipo": acao['tipo'],
            "descricao": acao['descricao'],
            "responsavel": acao.get('responsavel', 'Sistema'),
            "status": "pendente",
            "data_criacao": datetime.now().isoformat(),
            "prazo": acao.get('prazo')
        }
        
        logger.info(f"Ação CS registrada para cliente {cliente_id}: {acao['tipo']}")
        
        return {
            "success": True,
            "message": "Ação registrada com sucesso",
            "data": acao_registrada
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao registrar ação CS: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/customer-success/acoes/{cliente_id}")
async def listar_acoes_cs(
    cliente_id: str,
    status: Optional[str] = Query(None, description="Filtrar por status")
):
    """
    Lista ações de Customer Success de um cliente
    
    Args:
        cliente_id: ID do cliente
        status: Filtrar por status (pendente, em_andamento, concluida)
        
    Returns:
        Lista de ações
    """
    try:
        # Simular ações (em produção, buscar do DB)
        acoes = [
            {
                "id": "acao_001",
                "cliente_id": cliente_id,
                "tipo": "treinamento",
                "descricao": "Agendar treinamento de reciclagem",
                "responsavel": "João Silva",
                "status": "pendente",
                "data_criacao": "2024-12-10T10:00:00",
                "prazo": "2024-12-20T18:00:00"
            },
            {
                "id": "acao_002",
                "cliente_id": cliente_id,
                "tipo": "reuniao",
                "descricao": "Reunião de alinhamento trimestral",
                "responsavel": "Maria Santos",
                "status": "em_andamento",
                "data_criacao": "2024-12-05T14:00:00",
                "prazo": "2024-12-15T16:00:00"
            }
        ]
        
        # Filtrar por status se especificado
        if status:
            acoes = [a for a in acoes if a['status'] == status]
        
        return {
            "success": True,
            "total": len(acoes),
            "data": acoes
        }
        
    except Exception as e:
        logger.error(f"Erro ao listar ações CS: {e}")
        raise HTTPException(status_code=500, detail=str(e))
