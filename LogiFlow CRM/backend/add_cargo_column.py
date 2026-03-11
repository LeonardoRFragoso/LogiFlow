"""
Script para adicionar TODAS as colunas faltantes na tabela 'leads'.
Executa diretamente no banco de dados, sem usar Alembic.
"""
import os
import psycopg2
from urllib.parse import urlparse

def add_all_lead_columns():
    # Obter URL do banco de dados
    database_url = os.getenv('DATABASE_URL')
    
    if not database_url:
        print("❌ DATABASE_URL não definida")
        return
    
    # Parse da URL
    result = urlparse(database_url)
    
    # Lista de colunas a adicionar
    columns_to_add = [
        ('cargo', 'VARCHAR(100)'),
        ('website', 'VARCHAR(255)'),
        ('linkedin', 'VARCHAR(255)'),
        ('necessidade_descrita', 'TEXT'),
        ('source_details', 'VARCHAR(255)'),
        ('lead_score', 'INTEGER DEFAULT 0'),
        ('estagio_maturidade', "VARCHAR(50) DEFAULT 'frio'"),
        ('primeiro_contato_em', 'TIMESTAMP'),
        ('ultimo_contato_em', 'TIMESTAMP'),
        ('proximo_followup_em', 'TIMESTAMP'),
        ('converted_to_cliente_id', 'INTEGER'),
        ('motivo_descarte', 'TEXT'),
    ]
    
    try:
        # Conectar ao banco
        conn = psycopg2.connect(
            database=result.path[1:],
            user=result.username,
            password=result.password,
            host=result.hostname,
            port=result.port
        )
        
        cursor = conn.cursor()
        
        print("🔧 Adicionando colunas faltantes à tabela 'leads'...")
        
        # Adicionar cada coluna se não existir
        for column_name, column_type in columns_to_add:
            cursor.execute(f"""
                DO $$ 
                BEGIN 
                    IF NOT EXISTS (
                        SELECT 1 FROM information_schema.columns 
                        WHERE table_name='leads' AND column_name='{column_name}'
                    ) THEN
                        ALTER TABLE leads ADD COLUMN {column_name} {column_type};
                        RAISE NOTICE 'Coluna {column_name} adicionada com sucesso';
                    END IF;
                END $$;
            """)
            conn.commit()
            
            print(f"✅ Coluna '{column_name}' adicionada à tabela 'leads' com sucesso!")
            
    except Exception as e:
        print(f"❌ Erro ao adicionar coluna: {e}")
        raise
    finally:
        if conn:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    print("🔧 Adicionando todas as colunas faltantes à tabela 'leads'...")
    add_all_lead_columns()
    print("✅ Script concluído!")
