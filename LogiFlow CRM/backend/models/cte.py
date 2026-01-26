"""
LogiFlow CRM - Model CT-e
Armazena informações dos CT-es emitidos
"""

from sqlalchemy import Column, String, Float, DateTime, Integer, Text, JSON, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from database import Base


class StatusCTe(str, enum.Enum):
    """Status possíveis do CT-e"""
    RASCUNHO = "rascunho"
    PROCESSANDO = "processando"
    AUTORIZADO = "autorizado"
    REJEITADO = "rejeitado"
    CANCELADO = "cancelado"
    DENEGADO = "denegado"


class CTe(Base):
    """Model para CT-e (Conhecimento de Transporte Eletrônico)"""
    
    __tablename__ = "ctes"
    
    id = Column(String(36), primary_key=True)
    tenant_id = Column(String(100), nullable=False, index=True)
    
    # Identificação
    numero = Column(Integer, nullable=False)
    serie = Column(String(10), default="1")
    chave = Column(String(44), unique=True, index=True)
    ref = Column(String(100), unique=True, index=True)
    
    # Status e datas
    status = Column(SQLEnum(StatusCTe), default=StatusCTe.RASCUNHO, index=True)
    data_emissao = Column(DateTime, default=datetime.utcnow)
    data_autorizacao = Column(DateTime, nullable=True)
    protocolo = Column(String(50), nullable=True)
    
    # Relacionamentos
    pedido_id = Column(String(36), nullable=True, index=True)
    mdfe_id = Column(String(36), ForeignKey("mdfes.id"), nullable=True, index=True)
    
    # Valores
    valor_total = Column(Float, nullable=False)
    valor_receber = Column(Float, nullable=False)
    valor_carga = Column(Float, nullable=True)
    peso_kg = Column(Float, nullable=False)
    
    # Modal e tipo
    modal = Column(String(2), default="01")
    tipo_servico = Column(String(1), default="0")
    natureza_operacao = Column(String(255), default="PRESTACAO DE SERVICO DE TRANSPORTE")
    
    # Dados fiscais
    tomador_tipo = Column(String(1), nullable=False)
    tomador_cnpj = Column(String(18), nullable=False)
    tomador_nome = Column(String(255), nullable=False)
    tomador_dados = Column(JSON, nullable=True)
    
    remetente_cnpj = Column(String(18), nullable=False)
    remetente_nome = Column(String(255), nullable=False)
    remetente_dados = Column(JSON, nullable=True)
    
    destinatario_cnpj = Column(String(18), nullable=False)
    destinatario_nome = Column(String(255), nullable=False)
    destinatario_dados = Column(JSON, nullable=True)
    
    # ICMS
    icms_situacao = Column(String(2), default="00")
    icms_aliquota = Column(Float, default=0.00)
    icms_valor = Column(Float, default=0.00)
    
    # Veículo
    veiculo_placa = Column(String(10), nullable=False)
    veiculo_uf = Column(String(2), nullable=False)
    veiculo_dados = Column(JSON, nullable=True)
    
    # RNTRC e CIOT
    rntrc = Column(String(20), nullable=True)
    ciot = Column(String(20), nullable=True)
    
    # URLs e arquivos
    url_danfe = Column(String(500), nullable=True)
    url_xml = Column(String(500), nullable=True)
    
    # Cancelamento
    motivo_cancelamento = Column(Text, nullable=True)
    data_cancelamento = Column(DateTime, nullable=True)
    
    # Mensagens de erro
    mensagem_erro = Column(Text, nullable=True)
    
    # Dados completos (JSON)
    dados_completos = Column(JSON, nullable=True)
    
    # Auditoria
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String(100), nullable=True)
    
    # Relacionamento com MDF-e
    mdfe = relationship("MDFe", back_populates="ctes", foreign_keys=[mdfe_id])
    
    def __repr__(self):
        return f"<CTe(numero={self.numero}, serie={self.serie}, status={self.status})>"
    
    def to_dict(self):
        """Converte para dicionário"""
        return {
            "id": self.id,
            "tenant_id": self.tenant_id,
            "numero": self.numero,
            "serie": self.serie,
            "chave": self.chave,
            "ref": self.ref,
            "status": self.status.value if self.status else None,
            "data_emissao": self.data_emissao.isoformat() if self.data_emissao else None,
            "data_autorizacao": self.data_autorizacao.isoformat() if self.data_autorizacao else None,
            "protocolo": self.protocolo,
            "pedido_id": self.pedido_id,
            "mdfe_id": self.mdfe_id,
            "valor_total": self.valor_total,
            "valor_receber": self.valor_receber,
            "valor_carga": self.valor_carga,
            "peso_kg": self.peso_kg,
            "modal": self.modal,
            "tipo_servico": self.tipo_servico,
            "natureza_operacao": self.natureza_operacao,
            "tomador_tipo": self.tomador_tipo,
            "tomador_cnpj": self.tomador_cnpj,
            "tomador_nome": self.tomador_nome,
            "tomador_dados": self.tomador_dados,
            "remetente_cnpj": self.remetente_cnpj,
            "remetente_nome": self.remetente_nome,
            "remetente_dados": self.remetente_dados,
            "destinatario_cnpj": self.destinatario_cnpj,
            "destinatario_nome": self.destinatario_nome,
            "destinatario_dados": self.destinatario_dados,
            "icms_situacao": self.icms_situacao,
            "icms_aliquota": self.icms_aliquota,
            "icms_valor": self.icms_valor,
            "veiculo_placa": self.veiculo_placa,
            "veiculo_uf": self.veiculo_uf,
            "veiculo_dados": self.veiculo_dados,
            "rntrc": self.rntrc,
            "ciot": self.ciot,
            "url_danfe": self.url_danfe,
            "url_xml": self.url_xml,
            "motivo_cancelamento": self.motivo_cancelamento,
            "data_cancelamento": self.data_cancelamento.isoformat() if self.data_cancelamento else None,
            "mensagem_erro": self.mensagem_erro,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "created_by": self.created_by
        }
