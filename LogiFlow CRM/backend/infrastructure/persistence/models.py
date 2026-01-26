"""
SQLAlchemy Models - Modelos de persistência para PostgreSQL
"""
from datetime import datetime, date
from decimal import Decimal
from typing import Optional
from uuid import uuid4

from sqlalchemy import (
    Column, String, Text, Boolean, DateTime, Date,
    Numeric, Integer, ForeignKey, JSON, Enum as SQLEnum
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

# Usar Base do database.py principal para compatibilidade com Alembic
from database import Base


class ClienteModel(Base):
    """Modelo de persistência para Cliente (v2 - Clean Architecture)"""
    __tablename__ = "clientes_v2"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    razao_social = Column(String(200), nullable=False, index=True)
    nome_fantasia = Column(String(200), nullable=True)
    documento = Column(String(14), nullable=False, unique=True, index=True)
    email = Column(String(255), nullable=True, index=True)
    telefone = Column(String(20), nullable=True)
    inscricao_estadual = Column(String(20), nullable=True)
    ativo = Column(Boolean, default=True, nullable=False)
    observacoes = Column(Text, nullable=True)
    
    # Endereço (JSON para simplificar)
    endereco = Column(JSON, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relacionamentos
    cotacoes = relationship("CotacaoModel", back_populates="cliente")
    pedidos = relationship("PedidoModel", back_populates="cliente")
    
    def __repr__(self):
        return f"<Cliente {self.razao_social}>"


class CotacaoModel(Base):
    """Modelo de persistência para Cotação (v2 - Clean Architecture)"""
    __tablename__ = "cotacoes_v2"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    numero = Column(String(50), nullable=False, unique=True, index=True)
    cliente_id = Column(UUID(as_uuid=True), ForeignKey("clientes_v2.id"), nullable=False, index=True)
    
    # Endereços (JSON)
    origem = Column(JSON, nullable=False)
    destino = Column(JSON, nullable=False)
    
    # Itens (JSON array)
    itens = Column(JSON, nullable=False)
    
    # Tipo
    tipo_frete = Column(String(10), default="CIF", nullable=False)
    tipo_carga = Column(String(20), default="fracionada", nullable=False)
    status = Column(String(20), default="rascunho", nullable=False, index=True)
    
    # Valores
    valor_frete = Column(Numeric(12, 2), default=0, nullable=False)
    valor_seguro = Column(Numeric(12, 2), default=0, nullable=False)
    valor_outros = Column(Numeric(12, 2), default=0, nullable=False)
    desconto = Column(Numeric(12, 2), default=0, nullable=False)
    
    # Datas
    validade = Column(Date, nullable=True)
    
    # Metadata
    observacoes = Column(Text, nullable=True)
    criado_por = Column(String(100), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relacionamentos
    cliente = relationship("ClienteModel", back_populates="cotacoes")
    pedido = relationship("PedidoModel", back_populates="cotacao", uselist=False)
    
    def __repr__(self):
        return f"<Cotacao {self.numero}>"


class PedidoModel(Base):
    """Modelo de persistência para Pedido (v2 - Clean Architecture)"""
    __tablename__ = "pedidos_v2"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    numero = Column(String(50), nullable=False, unique=True, index=True)
    cliente_id = Column(UUID(as_uuid=True), ForeignKey("clientes_v2.id"), nullable=False, index=True)
    cotacao_id = Column(UUID(as_uuid=True), ForeignKey("cotacoes_v2.id"), nullable=True)
    
    # Endereços (JSON)
    origem = Column(JSON, nullable=False)
    destino = Column(JSON, nullable=False)
    
    # Status
    status = Column(String(30), default="aguardando_coleta", nullable=False, index=True)
    
    # Carga
    peso_kg = Column(Numeric(12, 3), default=0, nullable=False)
    volume_m3 = Column(Numeric(12, 3), default=0, nullable=False)
    valor_mercadoria = Column(Numeric(12, 2), default=0, nullable=False)
    descricao_carga = Column(Text, nullable=True)
    
    # Valores
    valor_frete = Column(Numeric(12, 2), default=0, nullable=False)
    valor_seguro = Column(Numeric(12, 2), default=0, nullable=False)
    valor_total = Column(Numeric(12, 2), default=0, nullable=False)
    
    # Datas
    data_coleta_prevista = Column(DateTime, nullable=True)
    data_coleta_realizada = Column(DateTime, nullable=True)
    data_entrega_prevista = Column(DateTime, nullable=True)
    data_entrega_realizada = Column(DateTime, nullable=True)
    
    # Rastreamento
    motorista_id = Column(UUID(as_uuid=True), nullable=True, index=True)
    veiculo_id = Column(UUID(as_uuid=True), nullable=True)
    
    # Documentos fiscais
    cte_numero = Column(String(50), nullable=True)
    cte_chave = Column(String(50), nullable=True)
    nfe_chave = Column(String(50), nullable=True)
    
    # Metadata
    observacoes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relacionamentos
    cliente = relationship("ClienteModel", back_populates="pedidos")
    cotacao = relationship("CotacaoModel", back_populates="pedido")
    
    def __repr__(self):
        return f"<Pedido {self.numero}>"
