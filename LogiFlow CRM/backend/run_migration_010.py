#!/usr/bin/env python3
"""
Script para executar migration 010 - Adicionar colunas ao tenants
Uso: python run_migration_010.py
"""
import os
import sys
from alembic import command
from alembic.config import Config

def run_migration():
    """Executa a migration 010"""
    print("=" * 60)
    print("🔧 Executando Migration 010 - Tenant DB Columns")
    print("=" * 60)
    
    # Configurar Alembic
    alembic_cfg = Config("alembic.ini")
    
    try:
        # Executar upgrade para a versão 010
        print("\n📦 Aplicando migration 010_add_tenant_db_columns...")
        command.upgrade(alembic_cfg, "010_add_tenant_db_columns")
        print("✅ Migration 010 aplicada com sucesso!")
        
        # Mostrar versão atual
        print("\n📊 Verificando versão atual...")
        command.current(alembic_cfg)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erro ao executar migration: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = run_migration()
    sys.exit(0 if success else 1)
