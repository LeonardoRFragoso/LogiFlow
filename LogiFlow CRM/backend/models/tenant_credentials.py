"""
LogiFlow CRM - Modelo de Credenciais por Tenant
Armazena credenciais de integrações (ERP, GPS, Frete) de forma segura por tenant
"""

from sqlalchemy import Column, String, Boolean, DateTime, Text, Integer
from sqlalchemy.sql import func
from datetime import datetime
import json
from cryptography.fernet import Fernet
import os

from database import Base


class TenantCredentials(Base):
    """
    Modelo para armazenar credenciais de integrações por tenant
    
    Credenciais são criptografadas antes de serem salvas no banco
    """
    
    __tablename__ = "tenant_credentials"
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(String(50), nullable=False, index=True)
    
    # Tipo de integração
    integration_type = Column(String(50), nullable=False)  # 'erp', 'gps', 'freight'
    provider = Column(String(50), nullable=False)  # 'omie', 'bling', 'tiny', 'sascar', etc
    
    # Credenciais criptografadas (JSON)
    encrypted_credentials = Column(Text, nullable=False)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_validated = Column(Boolean, default=False)
    last_validation = Column(DateTime, nullable=True)
    
    # Metadados
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    created_by = Column(String(100))
    
    @staticmethod
    def get_encryption_key():
        """Obtém chave de criptografia do ambiente"""
        key = os.getenv('CREDENTIALS_ENCRYPTION_KEY')
        if not key:
            # Gerar chave se não existir (desenvolvimento)
            key = Fernet.generate_key().decode()
            print(f"⚠️ AVISO: Gere uma chave e adicione ao .env: CREDENTIALS_ENCRYPTION_KEY={key}")
        return key.encode() if isinstance(key, str) else key
    
    @staticmethod
    def encrypt_credentials(credentials: dict) -> str:
        """Criptografa credenciais"""
        f = Fernet(TenantCredentials.get_encryption_key())
        json_str = json.dumps(credentials)
        encrypted = f.encrypt(json_str.encode())
        return encrypted.decode()
    
    @staticmethod
    def decrypt_credentials(encrypted_data: str) -> dict:
        """Descriptografa credenciais"""
        f = Fernet(TenantCredentials.get_encryption_key())
        decrypted = f.decrypt(encrypted_data.encode())
        return json.loads(decrypted.decode())


# Schemas de credenciais por provider

ERP_CREDENTIALS_SCHEMAS = {
    "omie": {
        "fields": ["app_key", "app_secret"],
        "required": ["app_key", "app_secret"],
        "display_name": "Omie ERP"
    },
    "bling": {
        "fields": ["access_token"],
        "required": ["access_token"],
        "display_name": "Bling ERP"
    },
    "tiny": {
        "fields": ["token"],
        "required": ["token"],
        "display_name": "Tiny ERP"
    }
}

GPS_CREDENTIALS_SCHEMAS = {
    "sascar": {
        "fields": ["api_key", "api_secret"],
        "required": ["api_key", "api_secret"],
        "display_name": "Sascar GPS"
    },
    "autotrac": {
        "fields": ["username", "password"],
        "required": ["username", "password"],
        "display_name": "Autotrac GPS"
    },
    "onixsat": {
        "fields": ["api_token"],
        "required": ["api_token"],
        "display_name": "Onixsat GPS"
    }
}

FREIGHT_CREDENTIALS_SCHEMAS = {
    "melhor_envio": {
        "fields": ["token", "sandbox"],
        "required": ["token"],
        "display_name": "Melhor Envio"
    },
    "frenet": {
        "fields": ["token"],
        "required": ["token"],
        "display_name": "Frenet"
    }
}

ALL_CREDENTIALS_SCHEMAS = {
    "erp": ERP_CREDENTIALS_SCHEMAS,
    "gps": GPS_CREDENTIALS_SCHEMAS,
    "freight": FREIGHT_CREDENTIALS_SCHEMAS
}
