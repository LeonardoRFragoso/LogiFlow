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


class StatusLead(str, enum.Enum):
    NOVO = "novo"
    CONTATADO = "contatado"
    QUALIFICADO = "qualificado"
    CONVERTIDO = "convertido"
    PERDIDO = "perdido"


class StatusTenant(str, enum.Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    CANCELLED = "cancelled"
    TRIAL = "trial"


class PlanType(str, enum.Enum):
    STARTER = "starter"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"


class SubscriptionStatus(str, enum.Enum):
    ACTIVE = "active"
    PAST_DUE = "past_due"
    CANCELLED = "cancelled"
    TRIAL = "trial"


class PaymentGateway(str, enum.Enum):
    STRIPE = "stripe"
    ASAAS = "asaas"
    MERCADOPAGO = "mercadopago"


class NPSCategory(str, enum.Enum):
    PROMOTOR = "promotor"  # 9-10
    NEUTRO = "neutro"      # 7-8
    DETRATOR = "detrator"  # 0-6


class SurveyStatus(str, enum.Enum):
    ENVIADA = "enviada"
    RESPONDIDA = "respondida"
    EXPIRADA = "expirada"
    CANCELADA = "cancelada"


class ChurnRiskLevel(str, enum.Enum):
    BAIXO = "baixo"        # Verde
    MEDIO = "medio"        # Amarelo
    ALTO = "alto"          # Vermelho
    CRITICO = "critico"    # Roxo


# ========================================
# Auth Models
# ========================================


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(120), unique=True, nullable=False, index=True)
    nome = Column(String(120), nullable=False)
    senha_hash = Column(String(255), nullable=False)
    tipo = Column(String(50), default="operador")
    status = Column(String(50), default="ativo")
    telefone = Column(String(30))
    cargo = Column(String(100))
    ultimo_acesso = Column(DateTime)
    criado_em = Column(DateTime, default=datetime.utcnow)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    token = Column(String(255), primary_key=True, index=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    expire_at = Column(DateTime, nullable=False)
    revoked = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


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


# ========================================
# SaaS / Multi-Tenant Models
# ========================================

class Lead(Base):
    """Leads capturados do site de divulgação"""
    __tablename__ = "leads"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    email = Column(String(150), nullable=False, unique=True, index=True)
    phone = Column(String(20), nullable=False)
    company = Column(String(150), nullable=False)
    vehicles = Column(String(20))
    message = Column(Text)
    
    status = Column(String(20), default=StatusLead.NOVO.value, index=True)
    source = Column(String(50), default="site")
    assigned_to = Column(Integer, nullable=True)  # ID do vendedor
    
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    converted_at = Column(DateTime, nullable=True)
    
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=True)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="leads")


class Tenant(Base):
    """Clientes SaaS (multi-tenant)"""
    __tablename__ = "tenants"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    subdomain = Column(String(50), nullable=False, unique=True, index=True)
    company_name = Column(String(150), nullable=False)
    contact_name = Column(String(150), nullable=False)
    contact_email = Column(String(150), nullable=False, index=True)
    contact_phone = Column(String(20))
    
    # Banco de dados dedicado
    db_name = Column(String(100), nullable=False, unique=True)
    db_user = Column(String(100), nullable=False)
    db_password = Column(String(255), nullable=False)
    
    # Storage
    s3_bucket = Column(String(100))
    
    # Status
    status = Column(String(20), default=StatusTenant.TRIAL.value, index=True)
    trial_ends_at = Column(DateTime, nullable=True)
    
    # Plano e Limites
    plan = Column(String(20), default=PlanType.STARTER.value)
    max_users = Column(Integer, default=5)
    max_vehicles = Column(Integer, default=10)
    max_orders_per_month = Column(Integer, default=500)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    cancelled_at = Column(DateTime, nullable=True)
    
    # Relationships
    leads = relationship("Lead", back_populates="tenant")
    subscriptions = relationship("Subscription", back_populates="tenant")


class Subscription(Base):
    """Assinaturas e pagamentos recorrentes"""
    __tablename__ = "subscriptions"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    
    plan = Column(String(20), nullable=False)
    status = Column(String(20), default=SubscriptionStatus.TRIAL.value, index=True)
    
    # Valores
    amount = Column(Float, nullable=False)
    currency = Column(String(3), default="BRL")
    billing_cycle = Column(String(20), default="monthly")
    
    # Datas
    current_period_start = Column(DateTime, nullable=False)
    current_period_end = Column(DateTime, nullable=False, index=True)
    trial_ends_at = Column(DateTime, nullable=True)
    cancelled_at = Column(DateTime, nullable=True)
    
    # Gateway de pagamento
    payment_gateway = Column(String(20), default=PaymentGateway.ASAAS.value)
    gateway_subscription_id = Column(String(255))
    gateway_customer_id = Column(String(255))
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="subscriptions")


# ========================================
# NPS e Satisfação
# ========================================

class NPSSurvey(Base):
    """Pesquisas NPS (Net Promoter Score)"""
    __tablename__ = "nps_surveys"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenant_id = Column(String(50), nullable=False, index=True)
    cliente_id = Column(String(50), nullable=False, index=True)
    
    # Tipo de pesquisa
    tipo = Column(String(20), nullable=False)  # "30_dias" ou "90_dias"
    
    # Pergunta
    pergunta = Column(Text, default="Em uma escala de 0 a 10, quanto você recomendaria o LogiFlow CRM para um amigo ou colega?")
    
    # Resposta
    score = Column(Integer, nullable=True)  # 0-10
    categoria = Column(String(20), nullable=True)  # promotor, neutro, detrator
    feedback_texto = Column(Text, nullable=True)
    
    # Status
    status = Column(String(20), default=SurveyStatus.ENVIADA.value, index=True)
    
    # Datas
    data_criacao = Column(DateTime, default=datetime.utcnow, index=True)
    data_expiracao = Column(DateTime, nullable=False)
    data_resposta = Column(DateTime, nullable=True)
    data_envio_email = Column(DateTime, nullable=True)
    
    # Metadados
    link_pesquisa = Column(String(500), nullable=True)
    ip_resposta = Column(String(50), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class CSATSurvey(Base):
    """Pesquisas CSAT (Customer Satisfaction) - Pós-Suporte"""
    __tablename__ = "csat_surveys"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenant_id = Column(String(50), nullable=False, index=True)
    cliente_id = Column(String(50), nullable=False, index=True)
    ticket_id = Column(String(50), nullable=False, index=True)
    
    # Pergunta
    pergunta = Column(Text, default="Como você avalia o atendimento recebido?")
    
    # Resposta
    score = Column(Integer, nullable=True)  # 1-5
    comentario = Column(Text, nullable=True)
    
    # Status
    status = Column(String(20), default=SurveyStatus.ENVIADA.value, index=True)
    
    # Datas
    data_criacao = Column(DateTime, default=datetime.utcnow, index=True)
    data_expiracao = Column(DateTime, nullable=False)
    data_resposta = Column(DateTime, nullable=True)
    data_envio_email = Column(DateTime, nullable=True)
    
    # Metadados
    link_pesquisa = Column(String(500), nullable=True)
    ip_resposta = Column(String(50), nullable=True)
    atendente_responsavel = Column(String(100), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ChurnAlert(Base):
    """Alertas de Risco de Churn"""
    __tablename__ = "churn_alerts"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenant_id = Column(String(50), nullable=False, index=True)
    cliente_id = Column(String(50), nullable=False, index=True)
    
    # Health Score
    health_score = Column(Float, nullable=False, index=True)
    health_score_anterior = Column(Float, nullable=True)
    
    # Risco
    nivel_risco = Column(String(20), nullable=False, index=True)  # baixo, medio, alto, critico
    probabilidade_churn = Column(Float, nullable=False)  # 0-100%
    
    # Motivos
    motivos = Column(Text, nullable=True)  # JSON array de motivos
    metricas_criticas = Column(Text, nullable=True)  # JSON array de métricas problemáticas
    
    # Ações
    acao_requerida = Column(Boolean, default=False, index=True)
    acao_sugerida = Column(Text, nullable=True)
    prazo_acao_dias = Column(Integer, nullable=True)
    
    # Status
    status = Column(String(20), default="ativo", index=True)  # ativo, resolvido, ignorado
    atribuido_a = Column(String(100), nullable=True)  # CS responsável
    
    # Resolução
    data_resolucao = Column(DateTime, nullable=True)
    acoes_tomadas = Column(Text, nullable=True)  # JSON array de ações
    resultado = Column(String(50), nullable=True)  # sucesso, churn_ocorreu, falso_positivo
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    notificado_em = Column(DateTime, nullable=True)


class CustomerSuccessAction(Base):
    """Ações de Customer Success"""
    __tablename__ = "cs_actions"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenant_id = Column(String(50), nullable=False, index=True)
    cliente_id = Column(String(50), nullable=False, index=True)
    
    # Origem
    origem_tipo = Column(String(50), nullable=False)  # nps_detrator, csat_baixo, churn_alert, manual
    origem_id = Column(String(50), nullable=True)  # ID da pesquisa ou alerta
    
    # Ação
    tipo = Column(String(50), nullable=False)  # contato_telefone, email, reuniao, treinamento, etc
    titulo = Column(String(200), nullable=False)
    descricao = Column(Text, nullable=True)
    
    # Responsável
    responsavel = Column(String(100), nullable=False)
    
    # Status
    status = Column(String(20), default="pendente", index=True)  # pendente, em_progresso, concluida, cancelada
    prioridade = Column(String(20), default="media")  # baixa, media, alta, urgente
    
    # Datas
    data_criacao = Column(DateTime, default=datetime.utcnow, index=True)
    prazo = Column(DateTime, nullable=True, index=True)
    data_conclusao = Column(DateTime, nullable=True)
    
    # Resultado
    resultado = Column(Text, nullable=True)
    notas = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# ========================================
# GPS Tracking
# ========================================

class GPSPosition(Base):
    """Posições GPS em tempo real (recebidas via webhook)"""
    __tablename__ = "gps_positions"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenant_id = Column(String(50), nullable=False, index=True)
    
    # Veículo
    placa = Column(String(10), nullable=False, index=True)
    veiculo_id = Column(String(50), nullable=True)
    
    # Provider GPS
    provider = Column(String(50), nullable=False, index=True)  # sascar, autotrac, onixsat
    provider_vehicle_id = Column(String(100), nullable=True)
    
    # Posição
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    altitude = Column(Float, nullable=True)
    precisao_metros = Column(Float, nullable=True)
    
    # Velocidade e direção
    velocidade_kmh = Column(Float, nullable=True)
    direcao_graus = Column(Integer, nullable=True)  # 0-359
    
    # Status
    ignicao = Column(Boolean, nullable=True)
    em_movimento = Column(Boolean, nullable=True, index=True)
    
    # Endereço (se disponível)
    endereco_completo = Column(String(500), nullable=True)
    cidade = Column(String(100), nullable=True)
    estado = Column(String(2), nullable=True)
    
    # Sensores/Alertas
    alertas = Column(Text, nullable=True)  # JSON array
    odometro_km = Column(Float, nullable=True)
    horimetro_horas = Column(Float, nullable=True)
    
    # Datas
    data_gps = Column(DateTime, nullable=False, index=True)  # Data do GPS
    data_recebimento = Column(DateTime, default=datetime.utcnow, index=True)  # Data que recebemos
    
    # Metadados
    payload_original = Column(Text, nullable=True)  # JSON do payload original
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)


class GPSRoute(Base):
    """Rotas GPS (histórico consolidado)"""
    __tablename__ = "gps_routes"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenant_id = Column(String(50), nullable=False, index=True)
    
    # Veículo e rota
    placa = Column(String(10), nullable=False, index=True)
    rota_nome = Column(String(200), nullable=True)
    
    # Origem/Destino
    origem_lat = Column(Float, nullable=True)
    origem_lng = Column(Float, nullable=True)
    origem_endereco = Column(String(500), nullable=True)
    
    destino_lat = Column(Float, nullable=True)
    destino_lng = Column(Float, nullable=True)
    destino_endereco = Column(String(500), nullable=True)
    
    # Estatísticas da rota
    distancia_total_km = Column(Float, nullable=True)
    duracao_minutos = Column(Integer, nullable=True)
    velocidade_media_kmh = Column(Float, nullable=True)
    velocidade_maxima_kmh = Column(Float, nullable=True)
    
    # Paradas
    total_paradas = Column(Integer, default=0)
    tempo_parado_minutos = Column(Integer, default=0)
    
    # Pontos da rota (JSON array de lat/lng)
    pontos_rota = Column(Text, nullable=True)  # JSON [{lat, lng, timestamp, velocidade}]
    
    # Provider
    provider = Column(String(50), nullable=False)
    
    # Datas
    data_inicio = Column(DateTime, nullable=False, index=True)
    data_fim = Column(DateTime, nullable=False, index=True)
    
    # Status
    status = Column(String(20), default="em_andamento")  # em_andamento, finalizada, cancelada
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
