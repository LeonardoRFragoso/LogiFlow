"""
LogiFlow CRM - SQLAlchemy Models
================================
Modelos de dados persistentes
"""

from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum

from database import Base


def generate_uuid():
    return str(uuid.uuid4())[:8].upper()


# ========================================
# Enums
# ========================================

class StatusEntrega(str, enum.Enum):
    AGUARDANDO_COLETA = "aguardando_coleta"
    COLETADO = "coletado"
    EM_TRANSITO = "em_transito"
    SAIU_PARA_ENTREGA = "saiu_para_entrega"
    ENTREGUE = "entregue"
    DEVOLVIDO = "devolvido"
    CANCELADO = "cancelado"


class StatusPedido(str, enum.Enum):
    AGUARDANDO = "aguardando"
    EM_SEPARACAO = "em_separacao"
    COLETADO = "coletado"
    EM_TRANSITO = "em_transito"
    ENTREGUE = "entregue"
    CANCELADO = "cancelado"


class StatusMotorista(str, enum.Enum):
    DISPONIVEL = "disponivel"
    EM_ROTA = "em_rota"
    INDISPONIVEL = "indisponivel"
    FERIAS = "ferias"


class StatusVeiculo(str, enum.Enum):
    DISPONIVEL = "disponivel"
    EM_USO = "em_uso"
    MANUTENCAO = "manutencao"
    INATIVO = "inativo"


class StatusCotacao(str, enum.Enum):
    PENDENTE = "pendente"
    ENVIADA = "enviada"
    APROVADA = "aprovada"
    RECUSADA = "recusada"
    EXPIRADA = "expirada"


# ========================================
# Models
# ========================================

class Cliente(Base):
    __tablename__ = "clientes"
    
    id = Column(String(8), primary_key=True, default=generate_uuid)
    razao_social = Column(String(200), nullable=False)
    nome_fantasia = Column(String(200))
    cnpj = Column(String(20), unique=True)
    inscricao_estadual = Column(String(20))
    email = Column(String(100))
    telefone = Column(String(20))
    celular = Column(String(20))
    endereco = Column(String(200))
    bairro = Column(String(100))
    cidade = Column(String(100))
    uf = Column(String(2))
    cep = Column(String(10))
    contato_nome = Column(String(100))
    ativo = Column(Boolean, default=True)
    criado_em = Column(DateTime, default=datetime.utcnow)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    pedidos = relationship("Pedido", back_populates="cliente")
    cotacoes = relationship("Cotacao", back_populates="cliente")


class Motorista(Base):
    __tablename__ = "motoristas"
    
    id = Column(String(8), primary_key=True, default=generate_uuid)
    nome = Column(String(100), nullable=False)
    cpf = Column(String(14), unique=True)
    telefone = Column(String(20))
    email = Column(String(100))
    cnh_numero = Column(String(20))
    cnh_categoria = Column(String(5))
    cnh_validade = Column(String(10))
    status = Column(String(20), default=StatusMotorista.DISPONIVEL.value)
    foto_url = Column(String(500))
    entregas_hoje = Column(Integer, default=0)
    avaliacao = Column(Float, default=5.0)
    ativo = Column(Boolean, default=True)
    criado_em = Column(DateTime, default=datetime.utcnow)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    veiculo_id = Column(String(8), ForeignKey("veiculos.id"), nullable=True)
    veiculo = relationship("Veiculo", back_populates="motorista")
    entregas = relationship("Entrega", back_populates="motorista")
    pedidos = relationship("Pedido", back_populates="motorista")


class Veiculo(Base):
    __tablename__ = "veiculos"
    
    id = Column(String(8), primary_key=True, default=generate_uuid)
    placa = Column(String(10), unique=True, nullable=False)
    tipo = Column(String(50))
    marca = Column(String(50))
    modelo = Column(String(50))
    ano = Column(Integer)
    capacidade_kg = Column(Float)
    capacidade_m3 = Column(Float)
    status = Column(String(20), default=StatusVeiculo.DISPONIVEL.value)
    km_atual = Column(Integer, default=0)
    ultima_manutencao = Column(String(10))
    proxima_manutencao = Column(String(10))
    ativo = Column(Boolean, default=True)
    criado_em = Column(DateTime, default=datetime.utcnow)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    motorista = relationship("Motorista", back_populates="veiculo", uselist=False)


class Pedido(Base):
    __tablename__ = "pedidos"
    
    id = Column(String(8), primary_key=True, default=generate_uuid)
    numero = Column(String(20), unique=True, nullable=False)
    cliente_id = Column(String(8), ForeignKey("clientes.id"))
    motorista_id = Column(String(8), ForeignKey("motoristas.id"), nullable=True)
    
    origem_endereco = Column(String(200))
    origem_cidade = Column(String(100))
    origem_uf = Column(String(2))
    destino_endereco = Column(String(200))
    destino_cidade = Column(String(100))
    destino_uf = Column(String(2))
    destino_cep = Column(String(10))
    
    peso_kg = Column(Float, default=0)
    volumes = Column(Integer, default=0)
    valor_mercadoria = Column(Float, default=0)
    valor_frete = Column(Float, default=0)
    
    status = Column(String(20), default=StatusPedido.AGUARDANDO.value)
    sla_status = Column(String(20), default="verde")
    previsao_entrega = Column(DateTime)
    data_coleta = Column(DateTime)
    data_entrega = Column(DateTime)
    observacoes = Column(Text)
    
    criado_em = Column(DateTime, default=datetime.utcnow)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    cliente = relationship("Cliente", back_populates="pedidos")
    motorista = relationship("Motorista", back_populates="pedidos")
    entregas = relationship("Entrega", back_populates="pedido")


class Entrega(Base):
    __tablename__ = "entregas"
    
    id = Column(String(8), primary_key=True, default=generate_uuid)
    codigo = Column(String(20), unique=True, nullable=False)
    pedido_id = Column(String(8), ForeignKey("pedidos.id"))
    motorista_id = Column(String(8), ForeignKey("motoristas.id"), nullable=True)
    
    cliente_nome = Column(String(200))
    cliente_telefone = Column(String(20))
    
    endereco_rua = Column(String(200))
    endereco_bairro = Column(String(100))
    endereco_cidade = Column(String(100))
    endereco_uf = Column(String(2))
    endereco_cep = Column(String(10))
    latitude = Column(Float)
    longitude = Column(Float)
    
    volumes = Column(Integer, default=0)
    peso = Column(Float, default=0)
    valor_mercadoria = Column(Float, default=0)
    valor_frete = Column(Float, default=0)
    
    status = Column(String(30), default=StatusEntrega.AGUARDANDO_COLETA.value)
    progresso = Column(Integer, default=0)
    previsao_entrega = Column(DateTime)
    data_coleta = Column(DateTime)
    data_entrega = Column(DateTime)
    
    assinatura_recebedor = Column(Text)
    foto_comprovante = Column(String(500))
    observacoes = Column(Text)
    atrasada = Column(Boolean, default=False)
    
    criado_em = Column(DateTime, default=datetime.utcnow)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    pedido = relationship("Pedido", back_populates="entregas")
    motorista = relationship("Motorista", back_populates="entregas")


class Cotacao(Base):
    __tablename__ = "cotacoes"
    
    id = Column(String(8), primary_key=True, default=generate_uuid)
    numero = Column(String(20), unique=True, nullable=False)
    cliente_id = Column(String(8), ForeignKey("clientes.id"))
    
    origem_cidade = Column(String(100))
    origem_uf = Column(String(2))
    destino_cidade = Column(String(100))
    destino_uf = Column(String(2))
    
    peso_kg = Column(Float, default=0)
    valor_mercadoria = Column(Float, default=0)
    valor_frete = Column(Float, default=0)
    prazo_dias = Column(Integer, default=0)
    
    status = Column(String(20), default=StatusCotacao.PENDENTE.value)
    validade = Column(DateTime)
    observacoes = Column(Text)
    
    criado_em = Column(DateTime, default=datetime.utcnow)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    cliente = relationship("Cliente", back_populates="cotacoes")


class Ocorrencia(Base):
    __tablename__ = "ocorrencias"
    
    id = Column(String(8), primary_key=True, default=generate_uuid)
    entrega_id = Column(String(8), ForeignKey("entregas.id"))
    tipo = Column(String(50))
    titulo = Column(String(200))
    descricao = Column(Text)
    prioridade = Column(String(20), default="media")
    status = Column(String(20), default="aberta")
    data_ocorrencia = Column(DateTime, default=datetime.utcnow)
    
    criado_em = Column(DateTime, default=datetime.utcnow)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
