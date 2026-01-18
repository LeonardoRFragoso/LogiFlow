"""
LogiFlow CRM - Serviço de Métricas Comerciais
==============================================
Cálculo de indicadores comerciais nativos
"""

from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, extract
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from loguru import logger

from models import (
    Opportunity, OpportunityStageHistory, CustomerInteraction,
    Cliente, Pedido, Cotacao, Lead, SalesStage
)


class CRMMetricsService:
    """
    Serviço de cálculo de métricas comerciais
    
    Métricas implementadas:
    - Taxa de conversão por estágio do funil
    - Tempo médio em cada fase do funil
    - Valor potencial vs. valor realizado
    - Clientes ativos vs. inativos
    - Pipeline ponderado (weighted pipeline)
    - Velocity do pipeline
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_funnel_conversion_rates(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Calcula taxa de conversão entre estágios do funil
        
        Returns:
            {
                'lead_to_qualified': 45.5,
                'qualified_to_proposal': 62.3,
                'proposal_to_negotiation': 78.9,
                'negotiation_to_won': 55.2,
                'overall_conversion': 12.4,
                'total_leads': 150,
                'total_won': 18
            }
        """
        if not start_date:
            start_date = datetime.utcnow() - timedelta(days=90)
        if not end_date:
            end_date = datetime.utcnow()
        
        query = self.db.query(Opportunity).filter(
            Opportunity.criado_em.between(start_date, end_date)
        )
        
        total_opps = query.count()
        
        lead_count = query.filter(Opportunity.sales_stage == SalesStage.LEAD.value).count()
        qualified_count = query.filter(
            or_(
                Opportunity.sales_stage == SalesStage.QUALIFICADO.value,
                Opportunity.sales_stage == SalesStage.PROPOSTA.value,
                Opportunity.sales_stage == SalesStage.NEGOCIACAO.value,
                Opportunity.sales_stage == SalesStage.GANHO.value
            )
        ).count()
        proposal_count = query.filter(
            or_(
                Opportunity.sales_stage == SalesStage.PROPOSTA.value,
                Opportunity.sales_stage == SalesStage.NEGOCIACAO.value,
                Opportunity.sales_stage == SalesStage.GANHO.value
            )
        ).count()
        negotiation_count = query.filter(
            or_(
                Opportunity.sales_stage == SalesStage.NEGOCIACAO.value,
                Opportunity.sales_stage == SalesStage.GANHO.value
            )
        ).count()
        won_count = query.filter(Opportunity.sales_stage == SalesStage.GANHO.value).count()
        
        lead_to_qualified = (qualified_count / lead_count * 100) if lead_count > 0 else 0
        qualified_to_proposal = (proposal_count / qualified_count * 100) if qualified_count > 0 else 0
        proposal_to_negotiation = (negotiation_count / proposal_count * 100) if proposal_count > 0 else 0
        negotiation_to_won = (won_count / negotiation_count * 100) if negotiation_count > 0 else 0
        overall_conversion = (won_count / total_opps * 100) if total_opps > 0 else 0
        
        return {
            'lead_to_qualified': round(lead_to_qualified, 2),
            'qualified_to_proposal': round(qualified_to_proposal, 2),
            'proposal_to_negotiation': round(proposal_to_negotiation, 2),
            'negotiation_to_won': round(negotiation_to_won, 2),
            'overall_conversion': round(overall_conversion, 2),
            'total_leads': lead_count,
            'total_qualified': qualified_count,
            'total_proposals': proposal_count,
            'total_negotiation': negotiation_count,
            'total_won': won_count,
            'total_opportunities': total_opps,
            'period_start': start_date.isoformat(),
            'period_end': end_date.isoformat()
        }
    
    def get_average_stage_duration(self) -> Dict[str, float]:
        """
        Calcula tempo médio (em dias) que oportunidades ficam em cada estágio
        
        Returns:
            {
                'lead': 5.2,
                'qualificado': 8.7,
                'proposta': 12.4,
                'negociacao': 15.8,
                'avg_total_cycle': 42.1
            }
        """
        stage_durations = {}
        
        for stage in SalesStage:
            if stage.value in ['ganho', 'perdido']:
                continue
            
            histories = self.db.query(OpportunityStageHistory).filter(
                OpportunityStageHistory.estagio_novo == stage.value
            ).all()
            
            durations = []
            for history in histories:
                next_history = self.db.query(OpportunityStageHistory).filter(
                    and_(
                        OpportunityStageHistory.oportunidade_id == history.oportunidade_id,
                        OpportunityStageHistory.data_mudanca > history.data_mudanca
                    )
                ).order_by(OpportunityStageHistory.data_mudanca.asc()).first()
                
                if next_history:
                    duration = (next_history.data_mudanca - history.data_mudanca).days
                    durations.append(duration)
            
            avg_duration = sum(durations) / len(durations) if durations else 0
            stage_durations[stage.value] = round(avg_duration, 1)
        
        total_cycle = sum(stage_durations.values())
        stage_durations['avg_total_cycle'] = round(total_cycle, 1)
        
        return stage_durations
    
    def get_pipeline_value(self) -> Dict[str, Any]:
        """
        Calcula valor potencial vs. valor realizado
        
        Returns:
            {
                'total_pipeline': 1250000.00,
                'weighted_pipeline': 456000.00,
                'total_won': 320000.00,
                'total_lost': 85000.00,
                'open_opportunities': 45,
                'win_rate': 78.9
            }
        """
        total_pipeline = self.db.query(
            func.sum(Opportunity.valor_estimado)
        ).filter(
            Opportunity.sales_stage.notin_([SalesStage.GANHO.value, SalesStage.PERDIDO.value])
        ).scalar() or 0
        
        weighted_pipeline = self.db.query(
            func.sum(Opportunity.valor_estimado * Opportunity.probabilidade / 100)
        ).filter(
            Opportunity.sales_stage.notin_([SalesStage.GANHO.value, SalesStage.PERDIDO.value])
        ).scalar() or 0
        
        total_won = self.db.query(
            func.sum(Opportunity.valor_estimado)
        ).filter(Opportunity.sales_stage == SalesStage.GANHO.value).scalar() or 0
        
        total_lost = self.db.query(
            func.sum(Opportunity.valor_estimado)
        ).filter(Opportunity.sales_stage == SalesStage.PERDIDO.value).scalar() or 0
        
        open_opportunities = self.db.query(Opportunity).filter(
            Opportunity.sales_stage.notin_([SalesStage.GANHO.value, SalesStage.PERDIDO.value])
        ).count()
        
        won_count = self.db.query(Opportunity).filter(
            Opportunity.sales_stage == SalesStage.GANHO.value
        ).count()
        
        lost_count = self.db.query(Opportunity).filter(
            Opportunity.sales_stage == SalesStage.PERDIDO.value
        ).count()
        
        total_closed = won_count + lost_count
        win_rate = (won_count / total_closed * 100) if total_closed > 0 else 0
        
        return {
            'total_pipeline': round(float(total_pipeline), 2),
            'weighted_pipeline': round(float(weighted_pipeline), 2),
            'total_won': round(float(total_won), 2),
            'total_lost': round(float(total_lost), 2),
            'open_opportunities': open_opportunities,
            'closed_won': won_count,
            'closed_lost': lost_count,
            'win_rate': round(win_rate, 2)
        }
    
    def get_customer_activity_status(self) -> Dict[str, Any]:
        """
        Analisa clientes ativos vs. inativos
        
        Critérios:
        - Ativo: teve pedido ou interação nos últimos 30 dias
        - Em risco: sem atividade entre 30-90 dias
        - Inativo: sem atividade há mais de 90 dias
        
        Returns:
            {
                'active': 45,
                'at_risk': 12,
                'inactive': 8,
                'total_customers': 65,
                'active_percentage': 69.2
            }
        """
        now = datetime.utcnow()
        date_30_days = now - timedelta(days=30)
        date_90_days = now - timedelta(days=90)
        
        active_from_orders = self.db.query(Cliente.id).join(Pedido).filter(
            Pedido.criado_em >= date_30_days
        ).distinct().all()
        
        active_from_interactions = self.db.query(Cliente.id).join(CustomerInteraction).filter(
            CustomerInteraction.data_interacao >= date_30_days
        ).distinct().all()
        
        active_ids = set([c.id for c in active_from_orders] + [c.id for c in active_from_interactions])
        
        at_risk_from_orders = self.db.query(Cliente.id).join(Pedido).filter(
            and_(
                Pedido.criado_em < date_30_days,
                Pedido.criado_em >= date_90_days
            )
        ).filter(Cliente.id.notin_(active_ids)).distinct().all()
        
        at_risk_from_interactions = self.db.query(Cliente.id).join(CustomerInteraction).filter(
            and_(
                CustomerInteraction.data_interacao < date_30_days,
                CustomerInteraction.data_interacao >= date_90_days
            )
        ).filter(Cliente.id.notin_(active_ids)).distinct().all()
        
        at_risk_ids = set([c.id for c in at_risk_from_orders] + [c.id for c in at_risk_from_interactions])
        
        total_customers = self.db.query(Cliente).filter(Cliente.ativo == True).count()
        
        active_count = len(active_ids)
        at_risk_count = len(at_risk_ids)
        inactive_count = total_customers - active_count - at_risk_count
        
        active_percentage = (active_count / total_customers * 100) if total_customers > 0 else 0
        
        return {
            'active': active_count,
            'at_risk': at_risk_count,
            'inactive': max(0, inactive_count),
            'total_customers': total_customers,
            'active_percentage': round(active_percentage, 2),
            'at_risk_percentage': round((at_risk_count / total_customers * 100) if total_customers > 0 else 0, 2),
            'inactive_percentage': round((inactive_count / total_customers * 100) if total_customers > 0 else 0, 2)
        }
    
    def get_sales_performance_by_user(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        """
        Performance de vendas por usuário (responsável)
        
        Returns: Lista de vendedores com suas métricas
        """
        if not start_date:
            start_date = datetime.utcnow() - timedelta(days=90)
        if not end_date:
            end_date = datetime.utcnow()
        
        from models import User
        
        users = self.db.query(User).all()
        performance = []
        
        for user in users:
            user_opps = self.db.query(Opportunity).filter(
                and_(
                    Opportunity.responsavel_id == user.id,
                    Opportunity.criado_em.between(start_date, end_date)
                )
            )
            
            total_opps = user_opps.count()
            won_opps = user_opps.filter(Opportunity.sales_stage == SalesStage.GANHO.value).count()
            total_value_won = user_opps.filter(
                Opportunity.sales_stage == SalesStage.GANHO.value
            ).with_entities(func.sum(Opportunity.valor_estimado)).scalar() or 0
            
            win_rate = (won_opps / total_opps * 100) if total_opps > 0 else 0
            
            interactions_count = self.db.query(CustomerInteraction).filter(
                and_(
                    CustomerInteraction.responsavel_id == user.id,
                    CustomerInteraction.data_interacao.between(start_date, end_date)
                )
            ).count()
            
            performance.append({
                'user_id': user.id,
                'user_name': user.nome,
                'user_email': user.email,
                'total_opportunities': total_opps,
                'won_opportunities': won_opps,
                'total_value_won': round(float(total_value_won), 2),
                'win_rate': round(win_rate, 2),
                'total_interactions': interactions_count,
                'avg_deal_size': round(float(total_value_won / won_opps), 2) if won_opps > 0 else 0
            })
        
        return sorted(performance, key=lambda x: x['total_value_won'], reverse=True)
    
    def get_complete_dashboard(self) -> Dict[str, Any]:
        """
        Retorna dashboard completo com todas as métricas principais
        """
        return {
            'conversion_rates': self.get_funnel_conversion_rates(),
            'stage_durations': self.get_average_stage_duration(),
            'pipeline_value': self.get_pipeline_value(),
            'customer_activity': self.get_customer_activity_status(),
            'sales_performance': self.get_sales_performance_by_user(),
            'generated_at': datetime.utcnow().isoformat()
        }
