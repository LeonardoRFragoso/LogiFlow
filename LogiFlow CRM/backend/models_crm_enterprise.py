"""
LogiFlow CRM - Models Enterprise Adicionais
============================================
Models complementares para CRM nível Enterprise
"""

from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from database import Base


def generate_uuid():
    return str(uuid.uuid4())[:8].upper()


class LeadStatusHistory(Base):
    """Histórico de mudanças de status de leads (auditoria)"""
    __tablename__ = "lead_status_history"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=False, index=True)
    
    status_anterior = Column(String(20), nullable=True)
    status_novo = Column(String(20), nullable=False)
    
    usuario_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    motivo = Column(Text, nullable=True)
    
    data_mudanca = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    lead = relationship("Lead", back_populates="historico_status")
    usuario = relationship("User", foreign_keys=[usuario_id])


class OpportunityNote(Base):
    """Notas e anotações em oportunidades"""
    __tablename__ = "opportunity_notes"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    oportunidade_id = Column(String(8), ForeignKey("opportunities.id"), nullable=False, index=True)
    
    conteudo = Column(Text, nullable=False)
    tipo = Column(String(30), default="note")
    
    autor_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    
    criado_em = Column(DateTime, default=datetime.utcnow, index=True)
    editado_em = Column(DateTime, nullable=True)
    
    # Relationships
    oportunidade = relationship("Opportunity", foreign_keys=[oportunidade_id])
    autor = relationship("User", foreign_keys=[autor_id])


class OpportunityProduct(Base):
    """Produtos/Serviços associados a uma oportunidade"""
    __tablename__ = "opportunity_products"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    oportunidade_id = Column(String(8), ForeignKey("opportunities.id"), nullable=False, index=True)
    
    produto_nome = Column(String(255), nullable=False)
    descricao = Column(Text)
    quantidade = Column(Float, default=1)
    valor_unitario = Column(Float, nullable=False)
    valor_total = Column(Float, nullable=False)
    
    desconto_percentual = Column(Float, default=0)
    desconto_valor = Column(Float, default=0)
    
    criado_em = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    oportunidade = relationship("Opportunity", foreign_keys=[oportunidade_id])


class SalesActivity(Base):
    """Atividades planejadas no processo de vendas"""
    __tablename__ = "sales_activities"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    oportunidade_id = Column(String(8), ForeignKey("opportunities.id"), nullable=True, index=True)
    cliente_id = Column(String(8), ForeignKey("clientes.id"), nullable=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=True, index=True)
    
    tipo = Column(String(30), nullable=False, index=True)
    assunto = Column(String(255), nullable=False)
    descricao = Column(Text)
    
    responsavel_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    
    data_planejada = Column(DateTime, nullable=False, index=True)
    data_conclusao = Column(DateTime, nullable=True)
    
    status = Column(String(20), default="planejada", index=True)
    prioridade = Column(String(20), default="media")
    
    resultado = Column(Text, nullable=True)
    
    criado_em = Column(DateTime, default=datetime.utcnow)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    oportunidade = relationship("Opportunity", foreign_keys=[oportunidade_id])
    cliente = relationship("Cliente", foreign_keys=[cliente_id])
    lead = relationship("Lead", foreign_keys=[lead_id])
    responsavel = relationship("User", foreign_keys=[responsavel_id])


class SalesForecast(Base):
    """Previsões de vendas mensais"""
    __tablename__ = "sales_forecasts"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    ano = Column(Integer, nullable=False, index=True)
    mes = Column(Integer, nullable=False, index=True)
    
    responsavel_id = Column(String(36), ForeignKey("users.id"), nullable=True, index=True)
    
    valor_previsto = Column(Float, nullable=False)
    valor_comprometido = Column(Float, default=0)
    valor_upside = Column(Float, default=0)
    valor_realizado = Column(Float, default=0)
    
    numero_oportunidades = Column(Integer, default=0)
    
    criado_em = Column(DateTime, default=datetime.utcnow)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    responsavel = relationship("User", foreign_keys=[responsavel_id])


class CustomerHealthScoreLog(Base):
    """Log de mudanças no health score do cliente"""
    __tablename__ = "customer_health_score_log"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    cliente_id = Column(String(8), ForeignKey("clientes.id"), nullable=False, index=True)
    
    score_anterior = Column(Float, nullable=True)
    score_novo = Column(Float, nullable=False)
    variacao = Column(Float, nullable=False)
    
    fatores_impacto = Column(JSON)
    
    data_calculo = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    cliente = relationship("Cliente", foreign_keys=[cliente_id])


class OpportunitySLALog(Base):
    """Log de SLA e aging de oportunidades"""
    __tablename__ = "opportunity_sla_log"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    oportunidade_id = Column(String(8), ForeignKey("opportunities.id"), nullable=False, index=True)
    
    estagio = Column(String(30), nullable=False)
    dias_no_estagio = Column(Integer, nullable=False)
    sla_estagio_dias = Column(Integer, nullable=False)
    
    status_sla = Column(String(20), nullable=False, index=True)
    
    verificado_em = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    oportunidade = relationship("Opportunity", foreign_keys=[oportunidade_id])


class ClienteSegmentacao(Base):
    """Segmentação avançada de clientes"""
    __tablename__ = "cliente_segmentacao"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    cliente_id = Column(String(8), ForeignKey("clientes.id"), nullable=False, unique=True, index=True)
    
    rfm_score = Column(Integer, default=0)
    recency_score = Column(Integer, default=0)
    frequency_score = Column(Integer, default=0)
    monetary_score = Column(Integer, default=0)
    
    segmento_rfm = Column(String(50))
    
    ltv_estimado = Column(Float, default=0)
    
    risco_churn = Column(String(20), default="baixo", index=True)
    probabilidade_churn = Column(Float, default=0)
    
    propensao_upsell = Column(Float, default=0)
    propensao_cross_sell = Column(Float, default=0)
    
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    cliente = relationship("Cliente", foreign_keys=[cliente_id])


class EmailTemplate(Base):
    """Templates de email para automação comercial"""
    __tablename__ = "email_templates"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    nome = Column(String(255), nullable=False)
    tipo = Column(String(50), nullable=False, index=True)
    
    assunto = Column(String(255), nullable=False)
    corpo_html = Column(Text, nullable=False)
    corpo_texto = Column(Text)
    
    variaveis_disponiveis = Column(JSON)
    
    ativo = Column(Boolean, default=True)
    
    criado_por = Column(String(36), ForeignKey("users.id"), nullable=True)
    criado_em = Column(DateTime, default=datetime.utcnow)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    criador = relationship("User", foreign_keys=[criado_por])
