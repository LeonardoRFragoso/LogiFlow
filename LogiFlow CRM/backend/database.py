"""
LogiFlow CRM - Database Configuration
=====================================
SQLAlchemy + MySQL via PyMySQL
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Importar configurações
from config import Settings

settings = Settings()

# Usar método que garante PyMySQL
DATABASE_URL = settings.get_database_url()

# Engine com configuração correta
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Verificar conexão antes de usar
    pool_recycle=3600,   # Reciclar conexões a cada 1h
    echo=False  # True para debug SQL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependency para injetar sessão do DB"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Cria todas as tabelas"""
    Base.metadata.create_all(bind=engine)
