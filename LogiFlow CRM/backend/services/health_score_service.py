"""
LogiFlow CRM - Serviço de Health Score Enterprise
==================================================
Cálculo automático e inteligente de saúde do cliente
"""

from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime, timedelta
from typing import Dict, Any, List
from loguru import logger

from models import Cliente, Pedido, CustomerInteraction, Opportunity, SalesStage
from models_crm_enterprise import CustomerHealthScoreLog, ClienteSegmentacao


class HealthScoreService:
    """
    Serviço de cálculo de Health Score do cliente
    
    Fatores considerados:
    - Recência de compras e interações (peso: 30%)
    - Frequência de pedidos (peso: 25%)
    - Valor monetário (peso: 25%)
    - Engajamento (interações) (peso: 15%)
    - Relacionamento (tempo como cliente) (peso: 5%)
    """
    
    PESO_RECENCIA = 0.30
    PESO_FREQUENCIA = 0.25
    PESO_MONETARIO = 0.25
    PESO_ENGAJAMENTO = 0.15
    PESO_RELACIONAMENTO = 0.05
    
    def __init__(self, db: Session):
        self.db = db
    
    def calcular_score_recencia(self, cliente: Cliente) -> float:
        """
        Calcula score baseado em recência (últimas atividades)
        
        Escala:
        - Atividade < 7 dias: 100
        - Atividade < 15 dias: 85
        - Atividade < 30 dias: 70
        - Atividade < 60 dias: 50
        - Atividade < 90 dias: 30
        - Atividade > 90 dias: 10
        """
        now = datetime.utcnow()
        
        # Buscar última atividade do cliente (pedido ou interação)
        last_order = self.db.query(func.max(Pedido.criado_em)).filter(
            Pedido.cliente_id == cliente.id
        ).scalar()
        
        last_interaction = self.db.query(func.max(CustomerInteraction.data_interacao)).filter(
            CustomerInteraction.cliente_id == cliente.id
        ).scalar()
        
        # Considera a atividade mais recente (pedido ou interação)
        last_activity = max([d for d in [last_order, last_interaction] if d], default=None)
        
        # Se nunca houve atividade, score crítico
        if not last_activity:
            return 10.0
        
        # Calcular dias desde a última atividade
        days_since = (now - last_activity).days
        
        if days_since <= 7:
            return 100.0
        elif days_since <= 15:
            return 85.0
        elif days_since <= 30:
            return 70.0
        elif days_since <= 60:
            return 50.0
        elif days_since <= 90:
            return 30.0
        else:
            return 10.0
    
    def calcular_score_frequencia(self, cliente: Cliente) -> float:
        """
        Calcula score baseado em frequência de pedidos
        
        Escala:
        - > 10 pedidos/90 dias: 100
        - 6-10 pedidos/90 dias: 80
        - 3-5 pedidos/90 dias: 60
        - 1-2 pedidos/90 dias: 40
        - 0 pedidos/90 dias: 10
        """
        date_90_days_ago = datetime.utcnow() - timedelta(days=90)
        
        pedidos_count = self.db.query(Pedido).filter(
            and_(
                Pedido.cliente_id == cliente.id,
                Pedido.criado_em >= date_90_days_ago
            )
        ).count()
        
        if pedidos_count >= 10:
            return 100.0
        elif pedidos_count >= 6:
            return 80.0
        elif pedidos_count >= 3:
            return 60.0
        elif pedidos_count >= 1:
            return 40.0
        else:
            return 10.0
    
    def calcular_score_monetario(self, cliente: Cliente) -> float:
        """
        Calcula score baseado em valor gasto
        
        Escala baseada em percentil de clientes
        """
        total_gasto = self.db.query(
            func.sum(Pedido.valor_frete)
        ).filter(Pedido.cliente_id == cliente.id).scalar() or 0
        
        avg_gasto = self.db.query(
            func.avg(func.sum(Pedido.valor_frete))
        ).filter(Pedido.cliente_id != None).group_by(Pedido.cliente_id).scalar() or 1
        
        percentual = (total_gasto / avg_gasto) * 100 if avg_gasto > 0 else 50
        
        return min(100, max(10, percentual))
    
    def calcular_score_engajamento(self, cliente: Cliente) -> float:
        """
        Calcula score baseado em interações
        
        Escala:
        - > 8 interações/90 dias: 100
        - 5-8 interações/90 dias: 80
        - 2-4 interações/90 dias: 60
        - 1 interação/90 dias: 40
        - 0 interações/90 dias: 10
        """
        date_90_days_ago = datetime.utcnow() - timedelta(days=90)
        
        interactions_count = self.db.query(CustomerInteraction).filter(
            and_(
                CustomerInteraction.cliente_id == cliente.id,
                CustomerInteraction.data_interacao >= date_90_days_ago
            )
        ).count()
        
        if interactions_count >= 8:
            return 100.0
        elif interactions_count >= 5:
            return 80.0
        elif interactions_count >= 2:
            return 60.0
        elif interactions_count >= 1:
            return 40.0
        else:
            return 10.0
    
    def calcular_score_relacionamento(self, cliente: Cliente) -> float:
        """
        Calcula score baseado em tempo de relacionamento
        
        Escala:
        - > 2 anos: 100
        - 1-2 anos: 80
        - 6-12 meses: 60
        - 3-6 meses: 40
        - < 3 meses: 20
        """
        now = datetime.utcnow()
        days_as_customer = (now - cliente.criado_em).days
        
        if days_as_customer >= 730:
            return 100.0
        elif days_as_customer >= 365:
            return 80.0
        elif days_as_customer >= 180:
            return 60.0
        elif days_as_customer >= 90:
            return 40.0
        else:
            return 20.0
    
    def calcular_health_score(self, cliente: Cliente, salvar: bool = True) -> Dict[str, Any]:
        """
        Calcula health score completo do cliente
        
        Args:
            cliente: Cliente para calcular score
            salvar: Se deve salvar no banco
        
        Returns:
        """
        # Calcular cada fator individualmente
        score_recencia = self.calcular_score_recencia(cliente)
        score_frequencia = self.calcular_score_frequencia(cliente)
        score_monetario = self.calcular_score_monetario(cliente)
        score_engajamento = self.calcular_score_engajamento(cliente)
        score_relacionamento = self.calcular_score_relacionamento(cliente)
        
        # Aplicar pesos e calcular score final (média ponderada)
        score_final = (
            score_recencia * self.PESO_RECENCIA +
            score_frequencia * self.PESO_FREQUENCIA +
            score_monetario * self.PESO_MONETARIO +
            score_engajamento * self.PESO_ENGAJAMENTO +
            score_relacionamento * self.PESO_RELACIONAMENTO
        )
        
        score_anterior = cliente.health_score or 75.0
        variacao = score_final - score_anterior
        
        if score_final >= 80:
            categoria = "excelente"
        elif score_final >= 60:
            categoria = "saudavel"
        elif score_final >= 40:
            categoria = "atencao"
        else:
            categoria = "critico"
        
        fatores = {
            'recencia': round(score_recencia, 2),
            'frequencia': round(score_frequencia, 2),
            'monetario': round(score_monetario, 2),
            'engajamento': round(score_engajamento, 2),
            'relacionamento': round(score_relacionamento, 2)
        }
        
        if salvar:
            cliente.health_score_anterior = score_anterior
            cliente.health_score = round(score_final, 2)
            cliente.health_score_atualizado_em = datetime.utcnow()
            
            log = CustomerHealthScoreLog(
                cliente_id=cliente.id,
                score_anterior=score_anterior,
                score_novo=round(score_final, 2),
                variacao=round(variacao, 2),
                fatores_impacto=fatores
            )
            self.db.add(log)
            self.db.commit()
            
            logger.info(f"Health score atualizado para cliente {cliente.razao_social}: {round(score_final, 2)} ({variacao:+.2f})")
        
        return {
            'score': round(score_final, 2),
            'score_anterior': round(score_anterior, 2),
            'variacao': round(variacao, 2),
            'fatores': fatores,
            'categoria': categoria,
            'peso_fatores': {
                'recencia': self.PESO_RECENCIA,
                'frequencia': self.PESO_FREQUENCIA,
                'monetario': self.PESO_MONETARIO,
                'engajamento': self.PESO_ENGAJAMENTO,
                'relacionamento': self.PESO_RELACIONAMENTO
            }
        }
    
    def recalcular_todos_clientes(self) -> Dict[str, Any]:
        """
        Recalcula health score de todos os clientes ativos
        
        Returns:
            Estatísticas do recálculo
        """
        clientes = self.db.query(Cliente).filter(Cliente.ativo == True).all()
        
        processados = 0
        melhoraram = 0
        pioraram = 0
        mantiveram = 0
        
        for cliente in clientes:
            try:
                resultado = self.calcular_health_score(cliente, salvar=True)
                processados += 1
                
                if resultado['variacao'] > 0:
                    melhoraram += 1
                elif resultado['variacao'] < 0:
                    pioraram += 1
                else:
                    mantiveram += 1
                    
            except Exception as e:
                logger.error(f"Erro ao calcular health score do cliente {cliente.id}: {e}")
        
        return {
            'total_processados': processados,
            'melhoraram': melhoraram,
            'pioraram': pioraram,
            'mantiveram': mantiveram,
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def identificar_clientes_em_risco(self, threshold: float = 40.0) -> List[Dict[str, Any]]:
        """
        Identifica clientes com health score abaixo do threshold
        
        Args:
            threshold: Score mínimo (padrão: 40)
        
        Returns:
            Lista de clientes em risco
        """
        clientes_risco = self.db.query(Cliente).filter(
            and_(
                Cliente.ativo == True,
                Cliente.health_score < threshold
            )
        ).order_by(Cliente.health_score.asc()).all()
        
        resultado = []
        for cliente in clientes_risco:
            score_info = self.calcular_health_score(cliente, salvar=False)
            
            resultado.append({
                'cliente_id': cliente.id,
                'cliente_nome': cliente.razao_social,
                'health_score': cliente.health_score,
                'variacao_recente': score_info['variacao'],
                'categoria': score_info['categoria'],
                'fatores_criticos': [k for k, v in score_info['fatores'].items() if v < 40],
                'responsavel_comercial': cliente.responsavel_comercial.nome if cliente.responsavel_comercial else None,
                'valor_total_gasto': cliente.valor_total_gasto or 0,
                'data_ultimo_contato': cliente.data_ultimo_contato.isoformat() if cliente.data_ultimo_contato else None
            })
        
        return resultado
