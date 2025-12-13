"""
LogiFlow CRM - Configurações
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Configurações da aplicação"""
    
    # App
    DEBUG: bool = True
    SECRET_KEY: str = "change-this-in-production"
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080"]
    
    # Database
    DB_HOST: str = "db"
    DB_NAME: str = "logiflow_crm"
    DB_USER: str = "logiflow"
    DB_PASSWORD: str = "logiflow123"
    DB_PORT: int = 3306
    
    # Redis
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = "redis123"
    
    # SuiteCRM
    SUITECRM_URL: str = "http://logiflow_suitecrm:8080"
    SUITECRM_CLIENT_ID: str = ""
    SUITECRM_CLIENT_SECRET: str = ""
    
    # Focus NFe
    FOCUSNFE_TOKEN: str = ""
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
