"""
LogiFlow CRM - Database Configuration
=====================================
SQLAlchemy + SQLite para desenvolvimento
Pode ser alterado para PostgreSQL em produção
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# SQLite para desenvolvimento (arquivo local)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./logiflow.db")

# Para PostgreSQL em produção:
# DATABASE_URL = "postgresql://user:password@localhost/logiflow"

engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
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
