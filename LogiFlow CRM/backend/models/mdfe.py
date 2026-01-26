"""
LogiFlow CRM - Model MDF-e
Armazena informações dos MDF-es emitidos
"""

from sqlalchemy import Column, String, Float, DateTime, Integer, Text, JSON, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from database import Base


class StatusMDFe(str, enum.Enum):
    """Status possíveis do MDF-e"""
    RASCUNHO = "rascunho"
    PROCESSANDO = "processando"
    AUTORIZADO = "autorizado"
    REJEITADO = "rejeitado"
    ENCERRADO = "encerrado"
    CANCELADO = "cancelado"


class MDFe(Base):
    """Model para MDF-e (Manifesto de Documentos Fiscais Eletrônico)"""
    
    __tablename__ = "mdfes"
    
    id = Column(String(36), primary_key=True)
    tenant_id = Column(String(100), nullable=False, index=True)
    
    # Identificação
    numero = Column(Integer, nullable=False)
    serie = Column(String(10), default="1")
    chave = Column(String(44), unique=True, index=True)
    ref = Column(String(100), unique=True, index=True)
    
    # Status e datas
    status = Column(SQLEnum(StatusMDFe), default=StatusMDFe.RASCUNHO, index=True)
    data_emissao = Column(DateTime, default=datetime.utcnow)
    data_autorizacao = Column(DateTime, nullable=True)
    data_encerramento = Column(DateTime, nullable=True)
    protocolo = Column(String(50), nullable=True)
    protocolo_encerramento = Column(String(50), nullable=True)
    
    # Modal e tipo
    modal = Column(String(1), default="1")
    tipo_emitente = Column(String(1), default="1")
    
    # Percurso (UFs)
    percurso = Column(JSON, nullable=False)
    
    # Local de carregamento
    uf_carregamento = Column(String(2), nullable=True)
    cidade_carregamento = Column(String(100), nullable=True)
    
    # Local de descarregamento
    uf_descarregamento = Column(String(2), nullable=True)
    cidade_descarregamento = Column(String(100), nullable=True)
    cidade_codigo_ibge = Column(String(10), nullable=True)
    
    # Totalizadores
    quantidade_ctes = Column(Integer, default=0)
    valor_total_carga = Column(Float, default=0.00)
    peso_total_kg = Column(Float, default=0.00)
    
    # Veículo
    veiculo_placa = Column(String(10), nullable=False)
    veiculo_uf = Column(String(2), nullable=False)
    veiculo_dados = Column(JSON, nullable=True)
    
    # Condutores
    condutores = Column(JSON, nullable=False)
    
    # Documentos vinculados (CT-es)
    documentos = Column(JSON, nullable=False)
    
    # URLs e arquivos
    url_damdfe = Column(String(500), nullable=True)
    url_xml = Column(String(500), nullable=True)
    
    # Cancelamento
    motivo_cancelamento = Column(Text, nullable=True)
    data_cancelamento = Column(DateTime, nullable=True)
    
    # Encerramento
    motivo_encerramento = Column(Text, nullable=True)
    
    # Mensagens de erro
    mensagem_erro = Column(Text, nullable=True)
    
    # Dados completos (JSON)
    dados_completos = Column(JSON, nullable=True)
    
    # Auditoria
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String(100), nullable=True)
    
    # Relacionamento com CT-es
    ctes = relationship("CTe", back_populates="mdfe", foreign_keys="CTe.mdfe_id")
    
    def __repr__(self):
        return f"<MDFe(numero={self.numero}, serie={self.serie}, status={self.status})>"
    
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
            "data_encerramento": self.data_encerramento.isoformat() if self.data_encerramento else None,
            "protocolo": self.protocolo,
            "protocolo_encerramento": self.protocolo_encerramento,
            "modal": self.modal,
            "tipo_emitente": self.tipo_emitente,
            "percurso": self.percurso,
            "uf_carregamento": self.uf_carregamento,
            "cidade_carregamento": self.cidade_carregamento,
            "uf_descarregamento": self.uf_descarregamento,
            "cidade_descarregamento": self.cidade_descarregamento,
            "cidade_codigo_ibge": self.cidade_codigo_ibge,
            "quantidade_ctes": self.quantidade_ctes,
            "valor_total_carga": self.valor_total_carga,
            "peso_total_kg": self.peso_total_kg,
            "veiculo_placa": self.veiculo_placa,
            "veiculo_uf": self.veiculo_uf,
            "veiculo_dados": self.veiculo_dados,
            "condutores": self.condutores,
            "documentos": self.documentos,
            "url_damdfe": self.url_damdfe,
            "url_xml": self.url_xml,
            "motivo_cancelamento": self.motivo_cancelamento,
            "data_cancelamento": self.data_cancelamento.isoformat() if self.data_cancelamento else None,
            "motivo_encerramento": self.motivo_encerramento,
            "mensagem_erro": self.mensagem_erro,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "created_by": self.created_by,
            "ctes_vinculados": len(self.ctes) if self.ctes else 0
        }
