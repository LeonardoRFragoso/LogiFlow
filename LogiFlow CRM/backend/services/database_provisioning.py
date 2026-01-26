"""
Serviço de Provisionamento de Banco de Dados Isolado
Cria e configura banco de dados separado para cada tenant
"""

from loguru import logger
import os
from typing import Dict, Optional
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError


class DatabaseProvisioningService:
    """Serviço para provisionar bancos de dados isolados para tenants"""
    
    def __init__(self):
        self.db_host = os.getenv("DB_HOST", "localhost")
        self.db_port = int(os.getenv("DB_PORT", "5432"))
        self.db_root_user = os.getenv("DB_ROOT_USER", "root")
        self.db_root_password = os.getenv("DB_ROOT_PASSWORD", "")
    
    def create_tenant_database(
        self,
        db_name: str,
        db_user: str,
        db_password: str
    ) -> Dict[str, any]:
        """
        Cria um banco de dados isolado para o tenant
        """
        raise NotImplementedError(
            "Provisionamento automático de banco por tenant estava implementado apenas para MySQL/MariaDB. "
            "O projeto foi padronizado para PostgreSQL (ADR-002). "
            "Implemente a versão PostgreSQL (CREATE DATABASE/ROLE + GRANT) via psycopg2 ou remova o uso deste serviço."
        )
    
    def _run_migrations(self, db_name: str, db_user: str, db_password: str):
        """
        Executa migrations no banco do tenant
        """
        raise NotImplementedError(
            "Execução de migrations por tenant precisa ser adaptada para PostgreSQL (ADR-002)."
        )
    
    def delete_tenant_database(self, db_name: str, db_user: str) -> bool:
        """
        Remove banco de dados e usuário do tenant
        """
        raise NotImplementedError(
            "Remoção de banco por tenant estava implementada apenas para MySQL/MariaDB. "
            "O projeto foi padronizado para PostgreSQL (ADR-002)."
        )
    
    def backup_tenant_database(self, db_name: str, backup_path: str) -> bool:
        """
        Cria backup do banco de dados do tenant
        """
        raise NotImplementedError(
            "Backup por tenant estava implementado via mysqldump (MySQL/MariaDB). "
            "Para PostgreSQL use pg_dump/pg_restore (ADR-002)."
        )
    
    def restore_tenant_database(self, db_name: str, backup_path: str) -> bool:
        """
        Restaura banco de dados do tenant a partir de backup
        """
        raise NotImplementedError(
            "Restore por tenant estava implementado via mysql CLI (MySQL/MariaDB). "
            "Para PostgreSQL use pg_restore/psql (ADR-002)."
        )
    
    def get_database_size(self, db_name: str) -> Optional[float]:
        """
        Retorna o tamanho do banco de dados em MB
        """
        raise NotImplementedError(
            "Cálculo de tamanho estava implementado via information_schema do MySQL. "
            "Para PostgreSQL use pg_database_size/pg_total_relation_size (ADR-002)."
        )
    
    def test_connection(self, db_name: str, db_user: str, db_password: str) -> bool:
        """
        Testa conexão com o banco do tenant
        """
        raise NotImplementedError(
            "Teste de conexão estava implementado via PyMySQL (MySQL/MariaDB). "
            "Para PostgreSQL implemente com psycopg2 (ADR-002)."
        )


# Instância global do serviço
db_provisioning_service = DatabaseProvisioningService()


# Funções helper
def create_tenant_database(db_name: str, db_user: str, db_password: str) -> Dict[str, any]:
    """Helper para criar banco do tenant"""
    return db_provisioning_service.create_tenant_database(db_name, db_user, db_password)


def delete_tenant_database(db_name: str, db_user: str) -> bool:
    """Helper para deletar banco do tenant"""
    return db_provisioning_service.delete_tenant_database(db_name, db_user)


def backup_tenant_database(db_name: str, backup_path: str) -> bool:
    """Helper para backup do banco do tenant"""
    return db_provisioning_service.backup_tenant_database(db_name, backup_path)
