"""
Script para adicionar coluna cargo à tabela leads
Executa diretamente no banco de dados sem usar Alembic
"""
import os
from sqlalchemy import create_engine, text
from config import settings

def add_cargo_column():
    """Adiciona coluna cargo à tabela leads se não existir"""
    
    # Criar engine
    engine = create_engine(settings.DATABASE_URL)
    
    try:
        with engine.connect() as conn:
            # Verificar se coluna já existe
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'leads' 
                AND column_name = 'cargo'
            """))
            
            if result.fetchone():
                print("ℹ️ Coluna 'cargo' já existe na tabela 'leads'")
                return
            
            # Adicionar coluna
            conn.execute(text("""
                ALTER TABLE leads 
                ADD COLUMN cargo VARCHAR(100)
            """))
            conn.commit()
            
            print("✅ Coluna 'cargo' adicionada à tabela 'leads' com sucesso!")
            
    except Exception as e:
        print(f"❌ Erro ao adicionar coluna: {e}")
        raise
    finally:
        engine.dispose()

if __name__ == "__main__":
    print("🔧 Adicionando coluna 'cargo' à tabela 'leads'...")
    add_cargo_column()
    print("✅ Script concluído!")
