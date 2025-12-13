"""
LogiFlow CRM - Configurações
"""

from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import List, Union


class Settings(BaseSettings):
    """Configurações da aplicação"""
    
    # App
    DEBUG: bool = True
    SECRET_KEY: str = "change-this-in-production"
    ALLOWED_ORIGINS: Union[List[str], str] = "http://localhost:3000,http://localhost:8080"
    
    @field_validator('ALLOWED_ORIGINS', mode='before')
    @classmethod
    def parse_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(',')]
        return v
    
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
    
    # WhatsApp / Evolution API
    EVOLUTION_API_URL: str = "http://localhost:8080"
    EVOLUTION_API_KEY: str = ""
    EVOLUTION_INSTANCE_NAME: str = "logiflow"
    
    # Google Maps API
    GOOGLE_MAPS_API_KEY: str = ""
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
