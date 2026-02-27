"""
LogiFlow CRM - Database Configuration
=====================================
SQLAlchemy + PostgreSQL via psycopg2
Lazy connection - only connects when needed (not at import time)
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool, NullPool
import os

# Importar configurações
from config import Settings

settings = Settings()

# Base declarativa (não requer conexão)
Base = declarative_base()

# Engine e SessionLocal são criados sob demanda (lazy)
_engine = None
_SessionLocal = None


def get_engine():
    """Retorna engine, criando se necessário (lazy initialization)"""
    global _engine
    if _engine is None:
        DATABASE_URL = settings.get_database_url()
        
        # Configurar pool baseado no ambiente
        is_production = os.getenv("ENVIRONMENT", "development") == "production"
        
        if is_production:
            # Produção: usar QueuePool com limite de conexões
            pool_config = {
                "poolclass": QueuePool,
                "pool_size": 10,           # Conexões permanentes
                "max_overflow": 20,        # Conexões adicionais
                "pool_pre_ping": True,     # Verificar conexão antes de usar
                "pool_recycle": 3600,      # Reciclar a cada 1h
                "pool_timeout": 30,        # Timeout para obter conexão
            }
        else:
            # Desenvolvimento: usar NullPool (sem limite)
            pool_config = {
                "poolclass": NullPool,
                "echo": False
            }
        
        _engine = create_engine(DATABASE_URL, **pool_config)
    return _engine


def get_session_local():
    """Retorna SessionLocal, criando se necessário"""
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_engine())
    return _SessionLocal


# Compatibilidade com código existente que faz: from database import engine, SessionLocal
# Criamos uma classe que atua como proxy lazy
class _LazyEngine:
    """Proxy que retorna o engine real quando acessado"""
    def __getattr__(self, name):
        return getattr(get_engine(), name)
    
    def __call__(self, *args, **kwargs):
        return get_engine()(*args, **kwargs)


class _LazySessionLocal:
    """Proxy que retorna SessionLocal real quando chamado"""
    def __call__(self, *args, **kwargs):
        return get_session_local()(*args, **kwargs)
    
    def __getattr__(self, name):
        return getattr(get_session_local(), name)


# Exports para compatibilidade
engine = _LazyEngine()
SessionLocal = _LazySessionLocal()


def get_db():
    """Dependency para injetar sessão do DB"""
    SessionLocal = get_session_local()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Cria todas as tabelas"""
    from models.cte import CTe
    from models.mdfe import MDFe
    from models.configuracao_fiscal import ConfiguracaoFiscal
    from models.tenant_credentials import TenantCredentials
    from models.whatsapp_message import WhatsAppMessage, WhatsAppConversation, WhatsAppConfig
    Base.metadata.create_all(bind=get_engine())
