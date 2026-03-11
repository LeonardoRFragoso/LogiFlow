"""
Script para adicionar tabela de notificações ao banco de dados
Executa independentemente do Alembic
"""
import os
import psycopg2
from loguru import logger

def add_notifications_table():
    """Adiciona tabela de notificações se não existir"""
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        logger.error("DATABASE_URL não definida")
        return
    
    try:
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        logger.info("🔧 Verificando se tabela 'notifications' existe...")
        
        # Verificar se tabela existe
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'notifications'
            );
        """)
        
        table_exists = cursor.fetchone()[0]
        
        if table_exists:
            logger.info("ℹ️  Tabela 'notifications' já existe")
            cursor.close()
            conn.close()
            return
        
        logger.info("➕ Criando tabela 'notifications'...")
        
        # Criar tabela
        cursor.execute("""
            CREATE TABLE notifications (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                tipo VARCHAR(50) NOT NULL,
                titulo VARCHAR(255) NOT NULL,
                mensagem TEXT NOT NULL,
                link VARCHAR(500),
                entity_type VARCHAR(50),
                entity_id INTEGER,
                icon VARCHAR(50),
                color VARCHAR(20),
                lida BOOLEAN NOT NULL DEFAULT FALSE,
                lida_em TIMESTAMP,
                created_at TIMESTAMP NOT NULL DEFAULT NOW()
            );
        """)
        
        logger.info("✅ Tabela 'notifications' criada")
        
        # Criar índices
        logger.info("➕ Criando índices...")
        
        cursor.execute("CREATE INDEX ix_notifications_user_id ON notifications(user_id);")
        cursor.execute("CREATE INDEX ix_notifications_tipo ON notifications(tipo);")
        cursor.execute("CREATE INDEX ix_notifications_lida ON notifications(lida);")
        cursor.execute("CREATE INDEX ix_notifications_created_at ON notifications(created_at);")
        
        logger.info("✅ Índices criados")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        logger.success("✅ Tabela 'notifications' adicionada com sucesso!")
        
    except Exception as e:
        logger.error(f"❌ Erro ao adicionar tabela 'notifications': {e}")
        raise


if __name__ == "__main__":
    add_notifications_table()
