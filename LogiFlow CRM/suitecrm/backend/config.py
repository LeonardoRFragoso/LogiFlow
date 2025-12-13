"""
LogiFlow CRM - Configurações
"""

from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Configurações da aplicação carregadas do ambiente"""
    
    # Ambiente
    ENV: str = "development"
    DEBUG: bool = True
    
    # Banco de Dados
    DB_HOST: str = "db"
    DB_PORT: int = 3306
    DB_NAME: str = "logiflow_crm"
    DB_USER: str = "logiflow"
    DB_PASSWORD: str = "logiflow123"
    
    @property
    def DATABASE_URL(self) -> str:
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    # Redis
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = "redis123"
    
    @property
    def REDIS_URL(self) -> str:
        return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/0"
    
    # JWT
    JWT_SECRET: str = "change-this-secret-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24
    
    # SuiteCRM
    SUITECRM_URL: str = "http://suitecrm"
    SUITECRM_CLIENT_ID: str = ""
    SUITECRM_CLIENT_SECRET: str = ""
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173"
    ]
    
    # Integrações
    FOCUSNFE_TOKEN: str = ""
    FOCUSNFE_ENVIRONMENT: str = "homologacao"
    
    # E-mail
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM_NAME: str = "LogiFlow CRM"
    SMTP_FROM_EMAIL: str = "noreply@logiflow.com.br"
    
    # Storage
    S3_ENDPOINT: str = ""
    S3_ACCESS_KEY: str = ""
    S3_SECRET_KEY: str = ""
    S3_BUCKET: str = "logiflow-uploads"
    S3_REGION: str = "us-east-1"
    
    # Sentry
    SENTRY_DSN: str = ""
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Instância global de configurações
settings = Settings()
