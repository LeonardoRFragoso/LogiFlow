"""
Database Configuration - Configuração do SQLAlchemy para PostgreSQL
Reutiliza engine e Base do database.py principal para consistência.
"""
from typing import Generator

from sqlalchemy.orm import Session

# Reutilizar configurações do database.py principal
from database import engine, SessionLocal, Base, get_db as _get_db


def get_db() -> Generator[Session, None, None]:
    """
    Dependency que fornece sessão do banco de dados.
    Uso com FastAPI:
        @router.get("/items")
        def get_items(db: Session = Depends(get_db)):
            ...
    """
    return _get_db()


def init_db() -> None:
    """Cria todas as tabelas no banco de dados via Alembic"""
    # Usar alembic upgrade head para criar tabelas
    # Base.metadata.create_all() não é recomendado com Alembic
    pass


__all__ = ["get_db", "engine", "SessionLocal", "Base", "init_db"]
