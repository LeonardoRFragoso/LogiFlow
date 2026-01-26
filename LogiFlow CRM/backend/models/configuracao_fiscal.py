"""
LogiFlow CRM - Model Configuração Fiscal
Armazena configurações fiscais do tenant
"""

from sqlalchemy import Column, String, Integer, Float, Boolean, JSON, DateTime, Text
from datetime import datetime
from database import Base


class ConfiguracaoFiscal(Base):
    """Configurações fiscais por tenant"""
    
    __tablename__ = "configuracoes_fiscais"
    
    id = Column(String(36), primary_key=True)
    tenant_id = Column(String(100), unique=True, nullable=False, index=True)
    
    # Dados do Emitente
    emitente_cnpj = Column(String(18), nullable=False)
    emitente_razao_social = Column(String(255), nullable=False)
    emitente_nome_fantasia = Column(String(255), nullable=True)
    emitente_ie = Column(String(20), nullable=False)
    emitente_im = Column(String(20), nullable=True)
    emitente_cnae = Column(String(10), nullable=True)
    emitente_crt = Column(String(1), default="1")
    
    # Endereço do Emitente
    emitente_endereco = Column(String(255), nullable=False)
    emitente_numero = Column(String(20), nullable=False)
    emitente_complemento = Column(String(100), nullable=True)
    emitente_bairro = Column(String(100), nullable=False)
    emitente_cidade = Column(String(100), nullable=False)
    emitente_uf = Column(String(2), nullable=False)
    emitente_cep = Column(String(10), nullable=False)
    emitente_telefone = Column(String(20), nullable=True)
    emitente_email = Column(String(255), nullable=True)
    
    # Configurações CT-e
    cte_serie_padrao = Column(String(10), default="1")
    cte_proximo_numero = Column(Integer, default=1)
    cte_ambiente = Column(String(20), default="homologacao")
    
    # Configurações MDF-e
    mdfe_serie_padrao = Column(String(10), default="1")
    mdfe_proximo_numero = Column(Integer, default=1)
    mdfe_ambiente = Column(String(20), default="homologacao")
    
    # RNTRC/ANTT
    rntrc = Column(String(20), nullable=True)
    antt = Column(String(20), nullable=True)
    
    # Tabela ICMS (JSON com alíquotas por UF)
    tabela_icms = Column(JSON, nullable=True, default={
        "AC": 12.0, "AL": 12.0, "AP": 12.0, "AM": 12.0,
        "BA": 12.0, "CE": 12.0, "DF": 12.0, "ES": 12.0,
        "GO": 12.0, "MA": 12.0, "MT": 12.0, "MS": 12.0,
        "MG": 12.0, "PA": 12.0, "PB": 12.0, "PR": 12.0,
        "PE": 12.0, "PI": 12.0, "RJ": 12.0, "RN": 12.0,
        "RS": 12.0, "RO": 12.0, "RR": 12.0, "SC": 12.0,
        "SP": 12.0, "SE": 12.0, "TO": 12.0
    })
    
    # Certificado Digital
    certificado_arquivo = Column(Text, nullable=True)
    certificado_senha = Column(String(255), nullable=True)
    certificado_validade = Column(DateTime, nullable=True)
    
    # Integração Focus NFe
    focusnfe_token = Column(String(255), nullable=True)
    focusnfe_ambiente = Column(String(20), default="homologacao")
    focusnfe_ativo = Column(Boolean, default=False)
    
    # Configurações de Emissão
    emitir_automatico_cte = Column(Boolean, default=False)
    agrupar_automatico_mdfe = Column(Boolean, default=False)
    enviar_email_apos_emissao = Column(Boolean, default=True)
    enviar_whatsapp_apos_emissao = Column(Boolean, default=False)
    
    # Mensagens Padrão
    mensagem_email_cte = Column(Text, nullable=True)
    mensagem_whatsapp_cte = Column(Text, nullable=True)
    
    # Validações
    validar_dados_antes_emissao = Column(Boolean, default=True)
    exigir_rntrc = Column(Boolean, default=True)
    exigir_ciot = Column(Boolean, default=False)
    
    # Observações Padrão
    obs_padrao_cte = Column(Text, nullable=True)
    obs_padrao_mdfe = Column(Text, nullable=True)
    
    # Status
    ativo = Column(Boolean, default=True)
    configurado = Column(Boolean, default=False)
    
    # Auditoria
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String(100), nullable=True)
    
    def __repr__(self):
        return f"<ConfiguracaoFiscal(tenant_id={self.tenant_id}, cnpj={self.emitente_cnpj})>"
    
    def to_dict(self):
        """Converte para dicionário"""
        return {
            "id": self.id,
            "tenant_id": self.tenant_id,
            "emitente_cnpj": self.emitente_cnpj,
            "emitente_razao_social": self.emitente_razao_social,
            "emitente_nome_fantasia": self.emitente_nome_fantasia,
            "emitente_ie": self.emitente_ie,
            "emitente_im": self.emitente_im,
            "emitente_cnae": self.emitente_cnae,
            "emitente_crt": self.emitente_crt,
            "emitente_endereco": self.emitente_endereco,
            "emitente_numero": self.emitente_numero,
            "emitente_complemento": self.emitente_complemento,
            "emitente_bairro": self.emitente_bairro,
            "emitente_cidade": self.emitente_cidade,
            "emitente_uf": self.emitente_uf,
            "emitente_cep": self.emitente_cep,
            "emitente_telefone": self.emitente_telefone,
            "emitente_email": self.emitente_email,
            "cte_serie_padrao": self.cte_serie_padrao,
            "cte_proximo_numero": self.cte_proximo_numero,
            "cte_ambiente": self.cte_ambiente,
            "mdfe_serie_padrao": self.mdfe_serie_padrao,
            "mdfe_proximo_numero": self.mdfe_proximo_numero,
            "mdfe_ambiente": self.mdfe_ambiente,
            "rntrc": self.rntrc,
            "antt": self.antt,
            "tabela_icms": self.tabela_icms,
            "certificado_validade": self.certificado_validade.isoformat() if self.certificado_validade else None,
            "focusnfe_ativo": self.focusnfe_ativo,
            "focusnfe_ambiente": self.focusnfe_ambiente,
            "emitir_automatico_cte": self.emitir_automatico_cte,
            "agrupar_automatico_mdfe": self.agrupar_automatico_mdfe,
            "enviar_email_apos_emissao": self.enviar_email_apos_emissao,
            "enviar_whatsapp_apos_emissao": self.enviar_whatsapp_apos_emissao,
            "validar_dados_antes_emissao": self.validar_dados_antes_emissao,
            "exigir_rntrc": self.exigir_rntrc,
            "exigir_ciot": self.exigir_ciot,
            "obs_padrao_cte": self.obs_padrao_cte,
            "obs_padrao_mdfe": self.obs_padrao_mdfe,
            "ativo": self.ativo,
            "configurado": self.configurado,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
