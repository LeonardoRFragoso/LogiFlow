#!/usr/bin/env python3
"""
LogiFlow CRM - Script para executar migrations Alembic
======================================================
Uso:
    python scripts/run_migrations.py upgrade      # Aplicar todas as migrations
    python scripts/run_migrations.py downgrade    # Reverter última migration
    python scripts/run_migrations.py current      # Ver versão atual
    python scripts/run_migrations.py history      # Ver histórico de migrations
"""
import subprocess
import sys
import os

# Garantir que estamos no diretório do backend
BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(BACKEND_DIR)

# Detectar executável do Alembic (venv ou global)
VENV_ALEMBIC = os.path.join(BACKEND_DIR, "venv", "Scripts", "alembic.exe")
if os.path.exists(VENV_ALEMBIC):
    ALEMBIC_CMD = [VENV_ALEMBIC]
else:
    # Fallback: tentar importar diretamente
    ALEMBIC_CMD = [sys.executable, "-c", "from alembic.config import main; main()"]


def run_alembic(command: str, *args):
    """Executa comando Alembic"""
    cmd = ALEMBIC_CMD + [command, *args]
    print(f"Executando: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=BACKEND_DIR)
    return result.returncode


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("\nComandos disponíveis:")
        print("  upgrade     - Aplica todas as migrations pendentes")
        print("  downgrade   - Reverte a última migration")
        print("  current     - Mostra versão atual do banco")
        print("  history     - Mostra histórico de migrations")
        print("  heads       - Mostra as migrations mais recentes")
        print("  generate    - Gera nova migration (autogenerate)")
        return 1
    
    command = sys.argv[1].lower()
    
    if command == "upgrade":
        target = sys.argv[2] if len(sys.argv) > 2 else "head"
        return run_alembic("upgrade", target)
    
    elif command == "downgrade":
        target = sys.argv[2] if len(sys.argv) > 2 else "-1"
        return run_alembic("downgrade", target)
    
    elif command == "current":
        return run_alembic("current")
    
    elif command == "history":
        return run_alembic("history", "--verbose")
    
    elif command == "heads":
        return run_alembic("heads")
    
    elif command == "generate":
        if len(sys.argv) < 3:
            print("Erro: Forneça uma mensagem para a migration")
            print("Uso: python scripts/run_migrations.py generate 'descricao da migration'")
            return 1
        message = sys.argv[2]
        return run_alembic("revision", "--autogenerate", "-m", message)
    
    else:
        print(f"Comando desconhecido: {command}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
