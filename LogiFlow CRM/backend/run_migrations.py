#!/usr/bin/env python3
"""
Script para executar migrations do Alembic
"""

import os
import sys
from pathlib import Path

# Adicionar o diretório ao path
sys.path.insert(0, str(Path(__file__).parent))

from alembic.config import Config
from alembic import command
from loguru import logger

def run_migrations():
    """Executa todas as migrations pendentes"""
    try:
        # Configurar alembic
        alembic_cfg = Config("alembic.ini")
        
        # Executar migrations
        logger.info("🔄 Executando migrations...")
        command.upgrade(alembic_cfg, "head")
        
        logger.success("✅ Migrations executadas com sucesso!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro ao executar migrations: {e}")
        return False

if __name__ == "__main__":
    success = run_migrations()
    sys.exit(0 if success else 1)
