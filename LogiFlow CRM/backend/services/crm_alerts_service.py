"""
LogiFlow CRM - Serviço de Alertas Comerciais
============================================
Identificação automática de situações que requerem ação comercial
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from datetime import datetime, timedelta
from typing import List, Dict, Any
from loguru import logger

from models import (
    Opportunity, CustomerInteraction, Cliente,
    Pedido, Lead, SalesStage, StatusLead
)


class CRMAlertsService:
    """
    Serviço de alertas e ações comerciais
    
    Alertas implementados:
    - Clientes sem contato há X dias
    - Oportunidades paradas no funil
    - Leads sem follow-up
    - Oportunidades com data de fechamento vencida
    - Clientes com valor alto sem atividade recente
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_inactive_customers(
        self,
        days_without_contact: int = 30,
        minimum_revenue: float = 0
    ) -> List[Dict[str, Any]]:
        """
        Identifica clientes sem contato há X dias
        
        Args:
            days_without_contact: Número de dias sem interação
            minimum_revenue: Valor mínimo de receita para incluir no alerta
        
        Returns:
            Lista de clientes com alertas de inatividade
        """
        cutoff_date = datetime.utcnow() - timedelta(days=days_without_contact)
        
        last_interactions = self.db.query(
            CustomerInteraction.cliente_id,
            func.max(CustomerInteraction.data_interacao).label('last_interaction')
        ).group_by(CustomerInteraction.cliente_id).subquery()
        
        last_orders = self.db.query(
            Pedido.cliente_id,
            func.max(Pedido.criado_em).label('last_order')
        ).group_by(Pedido.cliente_id).subquery()
        
        inactive_clients = self.db.query(Cliente).outerjoin(
            last_interactions,
            Cliente.id == last_interactions.c.cliente_id
        ).outerjoin(
            last_orders,
            Cliente.id == last_orders.c.cliente_id
        ).filter(
            and_(
                Cliente.ativo == True,
                or_(
                    last_interactions.c.last_interaction < cutoff_date,
                    last_interactions.c.last_interaction == None
                ),
                or_(
                    last_orders.c.last_order < cutoff_date,
                    last_orders.c.last_order == None
                )
            )
        ).all()
        
        alerts = []
        for client in inactive_clients:
            total_revenue = self.db.query(
                func.sum(Pedido.valor_frete)
            ).filter(Pedido.cliente_id == client.id).scalar() or 0
            
            if total_revenue < minimum_revenue:
                continue
            
            last_int = self.db.query(
                func.max(CustomerInteraction.data_interacao)
            ).filter(CustomerInteraction.cliente_id == client.id).scalar()
            
            last_ord = self.db.query(
                func.max(Pedido.criado_em)
            ).filter(Pedido.cliente_id == client.id).scalar()
            
            last_activity = max([d for d in [last_int, last_ord] if d is not None], default=None)
            
            days_inactive = (datetime.utcnow() - last_activity).days if last_activity else 999
            
            alerts.append({
                'alert_type': 'inactive_customer',
                'priority': 'high' if days_inactive > 60 else 'medium',
                'cliente_id': client.id,
                'cliente_nome': client.razao_social,
                'cliente_email': client.email,
                'cliente_telefone': client.telefone,
                'days_without_contact': days_inactive,
                'total_revenue': round(float(total_revenue), 2),
                'last_activity_date': last_activity.isoformat() if last_activity else None,
                'suggested_action': 'Agendar contato de reativação',
                'created_at': datetime.utcnow().isoformat()
            })
        
        return alerts
    
    def get_stalled_opportunities(
        self,
        days_in_stage: int = 15
    ) -> List[Dict[str, Any]]:
        """
        Identifica oportunidades paradas no funil há X dias no mesmo estágio
        
        Args:
            days_in_stage: Número de dias parada no mesmo estágio
        
        Returns:
            Lista de oportunidades estagnadas
        """
        cutoff_date = datetime.utcnow() - timedelta(days=days_in_stage)
        
        opportunities = self.db.query(Opportunity).filter(
            and_(
                Opportunity.sales_stage.notin_([SalesStage.GANHO.value, SalesStage.PERDIDO.value]),
                Opportunity.atualizado_em < cutoff_date
            )
        ).all()
        
        alerts = []
        for opp in opportunities:
            last_stage_change = self.db.query(OpportunityStageHistory).filter(
                OpportunityStageHistory.oportunidade_id == opp.id
            ).order_by(OpportunityStageHistory.data_mudanca.desc()).first()
            
            days_in_current_stage = (datetime.utcnow() - (last_stage_change.data_mudanca if last_stage_change else opp.criado_em)).days
            
            priority = 'critical' if days_in_current_stage > 30 else ('high' if days_in_current_stage > 20 else 'medium')
            
            alerts.append({
                'alert_type': 'stalled_opportunity',
                'priority': priority,
                'oportunidade_id': opp.id,
                'oportunidade_nome': opp.nome,
                'cliente_id': opp.cliente_id,
                'cliente_nome': opp.cliente.razao_social if opp.cliente else None,
                'current_stage': opp.sales_stage,
                'days_in_stage': days_in_current_stage,
                'valor_estimado': round(float(opp.valor_estimado), 2),
                'responsavel_nome': opp.responsavel.nome if opp.responsavel else 'Não atribuído',
                'proximo_passo': opp.proximo_passo,
                'suggested_action': 'Revisar próximos passos e reativar negociação',
                'created_at': datetime.utcnow().isoformat()
            })
        
        return alerts
    
    def get_leads_without_followup(
        self,
        days_since_creation: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Identifica leads sem follow-up há X dias
        
        Args:
            days_since_creation: Número de dias desde a criação sem follow-up
        
        Returns:
            Lista de leads sem acompanhamento
        """
        cutoff_date = datetime.utcnow() - timedelta(days=days_since_creation)
        
        leads = self.db.query(Lead).filter(
            and_(
                Lead.status.in_([StatusLead.NOVO.value, StatusLead.CONTATADO.value]),
                Lead.created_at < cutoff_date,
                Lead.assigned_to == None
            )
        ).all()
        
        alerts = []
        for lead in leads:
            days_waiting = (datetime.utcnow() - lead.created_at).days
            
            priority = 'critical' if days_waiting > 7 else ('high' if days_waiting > 5 else 'medium')
            
            alerts.append({
                'alert_type': 'lead_without_followup',
                'priority': priority,
                'lead_id': lead.id,
                'lead_name': lead.name,
                'lead_email': lead.email,
                'lead_phone': lead.phone,
                'lead_company': lead.company,
                'days_waiting': days_waiting,
                'source': lead.source,
                'status': lead.status,
                'suggested_action': 'Atribuir vendedor e realizar primeiro contato',
                'created_at': datetime.utcnow().isoformat()
            })
        
        return alerts
    
    def get_overdue_opportunities(self) -> List[Dict[str, Any]]:
        """
        Identifica oportunidades com data prevista de fechamento vencida
        
        Returns:
            Lista de oportunidades atrasadas
        """
        now = datetime.utcnow()
        
        overdue_opps = self.db.query(Opportunity).filter(
            and_(
                Opportunity.sales_stage.notin_([SalesStage.GANHO.value, SalesStage.PERDIDO.value]),
                Opportunity.data_prevista_fechamento < now,
                Opportunity.data_prevista_fechamento != None
            )
        ).all()
        
        alerts = []
        for opp in overdue_opps:
            days_overdue = (now - opp.data_prevista_fechamento).days
            
            priority = 'critical' if days_overdue > 14 else ('high' if days_overdue > 7 else 'medium')
            
            alerts.append({
                'alert_type': 'overdue_opportunity',
                'priority': priority,
                'oportunidade_id': opp.id,
                'oportunidade_nome': opp.nome,
                'cliente_id': opp.cliente_id,
                'cliente_nome': opp.cliente.razao_social if opp.cliente else None,
                'current_stage': opp.sales_stage,
                'valor_estimado': round(float(opp.valor_estimado), 2),
                'data_prevista_fechamento': opp.data_prevista_fechamento.isoformat(),
                'days_overdue': days_overdue,
                'responsavel_nome': opp.responsavel.nome if opp.responsavel else 'Não atribuído',
                'suggested_action': 'Revisar forecast e atualizar data prevista ou acelerar negociação',
                'created_at': datetime.utcnow().isoformat()
            })
        
        return alerts
    
    def get_high_value_inactive_customers(
        self,
        minimum_revenue: float = 50000,
        days_inactive: int = 45
    ) -> List[Dict[str, Any]]:
        """
        Identifica clientes de alto valor sem atividade recente
        
        Args:
            minimum_revenue: Receita mínima para ser considerado alto valor
            days_inactive: Dias sem atividade
        
        Returns:
            Lista de clientes de alto valor inativos
        """
        cutoff_date = datetime.utcnow() - timedelta(days=days_inactive)
        
        high_value_clients = self.db.query(
            Cliente.id,
            Cliente.razao_social,
            Cliente.email,
            Cliente.telefone,
            func.sum(Pedido.valor_frete).label('total_revenue')
        ).join(Pedido).group_by(
            Cliente.id, Cliente.razao_social, Cliente.email, Cliente.telefone
        ).having(
            func.sum(Pedido.valor_frete) >= minimum_revenue
        ).all()
        
        alerts = []
        for client in high_value_clients:
            last_order = self.db.query(
                func.max(Pedido.criado_em)
            ).filter(Pedido.cliente_id == client.id).scalar()
            
            if last_order and last_order > cutoff_date:
                continue
            
            last_interaction = self.db.query(
                func.max(CustomerInteraction.data_interacao)
            ).filter(CustomerInteraction.cliente_id == client.id).scalar()
            
            if last_interaction and last_interaction > cutoff_date:
                continue
            
            last_activity = max([d for d in [last_order, last_interaction] if d is not None], default=None)
            days_since_activity = (datetime.utcnow() - last_activity).days if last_activity else 999
            
            alerts.append({
                'alert_type': 'high_value_inactive',
                'priority': 'critical',
                'cliente_id': client.id,
                'cliente_nome': client.razao_social,
                'cliente_email': client.email,
                'cliente_telefone': client.telefone,
                'total_revenue': round(float(client.total_revenue), 2),
                'days_inactive': days_since_activity,
                'last_activity_date': last_activity.isoformat() if last_activity else None,
                'suggested_action': 'Contato imediato - Cliente de alto valor em risco de churn',
                'created_at': datetime.utcnow().isoformat()
            })
        
        return alerts
    
    def get_all_alerts(self) -> Dict[str, Any]:
        """
        Retorna todos os alertas consolidados
        
        Returns:
            Dicionário com todos os tipos de alertas e estatísticas
        """
        inactive_customers = self.get_inactive_customers(days_without_contact=30)
        stalled_opportunities = self.get_stalled_opportunities(days_in_stage=15)
        leads_no_followup = self.get_leads_without_followup(days_since_creation=3)
        overdue_opportunities = self.get_overdue_opportunities()
        high_value_inactive = self.get_high_value_inactive_customers()
        
        all_alerts = (
            inactive_customers +
            stalled_opportunities +
            leads_no_followup +
            overdue_opportunities +
            high_value_inactive
        )
        
        critical_count = len([a for a in all_alerts if a['priority'] == 'critical'])
        high_count = len([a for a in all_alerts if a['priority'] == 'high'])
        medium_count = len([a for a in all_alerts if a['priority'] == 'medium'])
        
        return {
            'summary': {
                'total_alerts': len(all_alerts),
                'critical': critical_count,
                'high': high_count,
                'medium': medium_count
            },
            'alerts_by_type': {
                'inactive_customers': inactive_customers,
                'stalled_opportunities': stalled_opportunities,
                'leads_without_followup': leads_no_followup,
                'overdue_opportunities': overdue_opportunities,
                'high_value_inactive': high_value_inactive
            },
            'all_alerts': sorted(all_alerts, key=lambda x: {'critical': 0, 'high': 1, 'medium': 2}[x['priority']]),
            'generated_at': datetime.utcnow().isoformat()
        }
