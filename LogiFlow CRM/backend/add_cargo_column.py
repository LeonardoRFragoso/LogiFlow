"""
Migration: adiciona colunas de cargo/leads que podem estar faltando no banco.
Executado no startup da aplicação — idempotente.
"""
import logging
from database import engine

logger = logging.getLogger(__name__)


def add_all_lead_columns():
    columns = [
        ("leads", "cargo", "VARCHAR(255)"),
        ("leads", "empresa", "VARCHAR(255)"),
        ("leads", "telefone", "VARCHAR(50)"),
        ("leads", "origem", "VARCHAR(100)"),
        ("leads", "observacoes", "TEXT"),
    ]
    with engine.connect() as conn:
        for table, col, col_type in columns:
            try:
                conn.execute(
                    f"ALTER TABLE {table} ADD COLUMN IF NOT EXISTS {col} {col_type}"
                )
                conn.commit()
            except Exception as e:
                logger.debug(f"Coluna {table}.{col} já existe ou erro ignorado: {e}")
    logger.info("✅ Colunas de leads verificadas/criadas")
