"""
LogiFlow CRM - Configurações
"""

from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import List, Union, Optional


class Settings(BaseSettings):
    """Configurações da aplicação"""
    
    # App
    DEBUG: bool = True
    SECRET_KEY: str = "change-this-in-production"
    API_PREFIX: str = "/api"
    API_VERSION: str = "v1"
    ALLOWED_ORIGINS: Union[List[str], str] = "http://localhost:3000,http://localhost:8080,https://logi-flow-blush.vercel.app"
    
    @field_validator('ALLOWED_ORIGINS', mode='before')
    @classmethod
    def parse_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(',')]
        return v
    
    # Database (suporta DATABASE_URL do Render ou vars individuais)
    DATABASE_URL: Optional[str] = None  # URL completa (Render)
    DB_HOST: str = "db"
    DB_NAME: str = "logiflow"
    DB_USER: str = "logiflow"
    DB_PASSWORD: str = "logiflow123"
    DB_PORT: int = 5432
    
    def get_database_url(self) -> str:
        """Retorna URL do banco com driver psycopg2"""
        if self.DATABASE_URL:
            return self.DATABASE_URL
        # Construir URL com psycopg2
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    # Redis (suporta REDIS_URL do Railway/Render ou vars individuais)
    REDIS_URL: Optional[str] = None  # URL completa (Railway/Render)
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = "redis123"
    
    def get_redis_config(self) -> dict:
        """Retorna configuração do Redis parseando REDIS_URL se disponível"""
        if self.REDIS_URL:
            # Parse redis://default:password@host:port
            from urllib.parse import urlparse
            parsed = urlparse(self.REDIS_URL)
            return {
                "host": parsed.hostname or "localhost",
                "port": parsed.port or 6379,
                "password": parsed.password or None,
                "decode_responses": True
            }
        return {
            "host": self.REDIS_HOST,
            "port": self.REDIS_PORT,
            "password": self.REDIS_PASSWORD if self.REDIS_PASSWORD else None,
            "decode_responses": True
        }
    
    # WhatsApp / Evolution API
    EVOLUTION_API_URL: str = "http://localhost:8080"
    EVOLUTION_API_KEY: str = ""
    EVOLUTION_INSTANCE_NAME: str = "logiflow"
    
    # Google Maps API
    GOOGLE_MAPS_API_KEY: str = ""
    GOOGLE_MAPS_DISTANCE_MATRIX_KEY: str = ""
    
    # Mercado Pago (Pagamentos)
    MERCADOPAGO_ACCESS_TOKEN: str = ""
    MERCADOPAGO_PUBLIC_KEY: str = ""
    MERCADOPAGO_WEBHOOK_URL: str = ""
    CHECKOUT_SUCCESS_URL: str = "http://localhost:3001/checkout/success"
    CHECKOUT_FAILURE_URL: str = "http://localhost:3001/checkout/failure"
    CHECKOUT_PENDING_URL: str = "http://localhost:3001/checkout/pending"

    # Focus NFe (CT-e/MDF-e)
    FOCUSNFE_TOKEN: str = ""
    FOCUSNFE_ENVIRONMENT: str = "homologacao"  # homologacao ou producao
    
    # Frete - Melhor Envio / Frenet
    MELHOR_ENVIO_TOKEN: str = ""
    MELHOR_ENVIO_SANDBOX: bool = True
    FRENET_TOKEN: str = ""
    
    # Rastreadores GPS - Simulation Modes
    SASCAR_SIMULATION_MODE: bool = True
    AUTOTRAC_SIMULATION_MODE: bool = True
    ONIXSAT_SIMULATION_MODE: bool = True
    
    # Email SMTP
    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    FROM_EMAIL: str = "noreply@logiflow.com.br"
    FROM_NAME: str = "LogiFlow CRM"
    SALES_EMAIL: str = "vendas@logiflow.com.br"
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Ignorar variáveis extras no .env


settings = Settings()
