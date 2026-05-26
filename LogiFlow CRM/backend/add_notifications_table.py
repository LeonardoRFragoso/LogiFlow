"""
Migration: cria a tabela de notificações se não existir.
Executado no startup da aplicação — idempotente.
"""
import logging

logger = logging.getLogger(__name__)


def add_notifications_table():
    try:
        from sqlalchemy import text
        from database import engine

        create_sql = text("""
        CREATE TABLE IF NOT EXISTS notifications (
            id          SERIAL PRIMARY KEY,
            tenant_id   VARCHAR(100),
            user_id     INTEGER,
            titulo      VARCHAR(255) NOT NULL,
            mensagem    TEXT,
            icon        VARCHAR(10) DEFAULT '🔔',
            lida        BOOLEAN DEFAULT FALSE,
            criado_em   TIMESTAMP DEFAULT NOW()
        )
        """)
        index_sql = text("""
        CREATE INDEX IF NOT EXISTS idx_notifications_tenant
            ON notifications (tenant_id, lida, criado_em DESC)
        """)
        with engine.connect() as conn:
            try:
                conn.execute(create_sql)
                conn.execute(index_sql)
                conn.commit()
                logger.info("✅ Tabela notifications verificada/criada")
            except Exception as e:
                logger.debug(f"Tabela notifications já existe ou ignorado: {e}")
    except Exception as e:
        logger.warning(f"Migração notifications ignorada (DB indisponível?): {e}")
