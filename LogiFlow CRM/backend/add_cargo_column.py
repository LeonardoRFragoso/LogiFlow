"""
Migration: adiciona colunas de cargo/leads que podem estar faltando no banco.
Executado no startup da aplicação — idempotente.
"""
import logging

logger = logging.getLogger(__name__)


def add_all_lead_columns():
    try:
        from sqlalchemy import text
        from database import engine

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
                    conn.execute(text(
                        f"ALTER TABLE {table} ADD COLUMN IF NOT EXISTS {col} {col_type}"
                    ))
                    conn.commit()
                except Exception as e:
                    logger.debug(f"Coluna {table}.{col} já existe ou ignorado: {e}")
        logger.info("✅ Colunas de leads verificadas/criadas")
    except Exception as e:
        logger.warning(f"Migração add_cargo_column ignorada (DB indisponível?): {e}")
