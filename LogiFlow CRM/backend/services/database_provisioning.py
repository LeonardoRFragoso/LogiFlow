"""
Serviço de Provisionamento de Banco de Dados Isolado
Cria e configura banco de dados separado para cada tenant
"""

from loguru import logger
import pymysql
import os
from typing import Dict, Optional
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError


class DatabaseProvisioningService:
    """Serviço para provisionar bancos de dados isolados para tenants"""
    
    def __init__(self):
        self.db_host = os.getenv("DB_HOST", "localhost")
        self.db_port = int(os.getenv("DB_PORT", "3306"))
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
        try:
            logger.info(f"🗄️  Criando banco de dados: {db_name}")
            
            # Conectar como root
            connection = pymysql.connect(
                host=self.db_host,
                port=self.db_port,
                user=self.db_root_user,
                password=self.db_root_password,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            
            with connection.cursor() as cursor:
                # Criar banco de dados
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
                logger.success(f"   ✅ Banco de dados '{db_name}' criado")
                
                # Criar usuário
                cursor.execute(f"CREATE USER IF NOT EXISTS '{db_user}'@'%' IDENTIFIED BY '{db_password}'")
                logger.success(f"   ✅ Usuário '{db_user}' criado")
                
                # Conceder permissões
                cursor.execute(f"GRANT ALL PRIVILEGES ON `{db_name}`.* TO '{db_user}'@'%'")
                cursor.execute("FLUSH PRIVILEGES")
                logger.success(f"   ✅ Permissões concedidas")
            
            connection.commit()
            connection.close()
            
            # Executar migrations no novo banco
            self._run_migrations(db_name, db_user, db_password)
            
            return {
                "success": True,
                "db_name": db_name,
                "db_user": db_user,
                "db_host": self.db_host,
                "db_port": self.db_port
            }
            
        except Exception as e:
            logger.error(f"❌ Erro ao criar banco de dados: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _run_migrations(self, db_name: str, db_user: str, db_password: str):
        """
        Executa migrations no banco do tenant
        """
        try:
            logger.info(f"🔄 Executando migrations no banco '{db_name}'...")
            
            # Criar engine para o banco do tenant
            db_url = f"mysql+pymysql://{db_user}:{db_password}@{self.db_host}:{self.db_port}/{db_name}"
            engine = create_engine(db_url)
            
            # Importar modelos
            from models import Base
            
            # Criar todas as tabelas
            Base.metadata.create_all(engine)
            
            logger.success(f"   ✅ Migrations executadas com sucesso")
            
        except Exception as e:
            logger.error(f"❌ Erro ao executar migrations: {e}")
            raise
    
    def delete_tenant_database(self, db_name: str, db_user: str) -> bool:
        """
        Remove banco de dados e usuário do tenant
        """
        try:
            logger.warning(f"🗑️  Removendo banco de dados: {db_name}")
            
            connection = pymysql.connect(
                host=self.db_host,
                port=self.db_port,
                user=self.db_root_user,
                password=self.db_root_password,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            
            with connection.cursor() as cursor:
                # Remover banco de dados
                cursor.execute(f"DROP DATABASE IF EXISTS `{db_name}`")
                logger.info(f"   ✅ Banco de dados '{db_name}' removido")
                
                # Remover usuário
                cursor.execute(f"DROP USER IF EXISTS '{db_user}'@'%'")
                cursor.execute("FLUSH PRIVILEGES")
                logger.info(f"   ✅ Usuário '{db_user}' removido")
            
            connection.commit()
            connection.close()
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao remover banco de dados: {e}")
            return False
    
    def backup_tenant_database(self, db_name: str, backup_path: str) -> bool:
        """
        Cria backup do banco de dados do tenant
        """
        try:
            logger.info(f"💾 Criando backup do banco '{db_name}'...")
            
            import subprocess
            
            # Comando mysqldump
            cmd = [
                'mysqldump',
                f'--host={self.db_host}',
                f'--port={self.db_port}',
                f'--user={self.db_root_user}',
                f'--password={self.db_root_password}',
                '--single-transaction',
                '--quick',
                '--lock-tables=false',
                db_name
            ]
            
            # Executar backup
            with open(backup_path, 'w') as f:
                subprocess.run(cmd, stdout=f, check=True)
            
            logger.success(f"   ✅ Backup criado: {backup_path}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao criar backup: {e}")
            return False
    
    def restore_tenant_database(self, db_name: str, backup_path: str) -> bool:
        """
        Restaura banco de dados do tenant a partir de backup
        """
        try:
            logger.info(f"♻️  Restaurando banco '{db_name}' do backup...")
            
            import subprocess
            
            # Comando mysql
            cmd = [
                'mysql',
                f'--host={self.db_host}',
                f'--port={self.db_port}',
                f'--user={self.db_root_user}',
                f'--password={self.db_root_password}',
                db_name
            ]
            
            # Executar restore
            with open(backup_path, 'r') as f:
                subprocess.run(cmd, stdin=f, check=True)
            
            logger.success(f"   ✅ Banco restaurado com sucesso")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao restaurar backup: {e}")
            return False
    
    def get_database_size(self, db_name: str) -> Optional[float]:
        """
        Retorna o tamanho do banco de dados em MB
        """
        try:
            connection = pymysql.connect(
                host=self.db_host,
                port=self.db_port,
                user=self.db_root_user,
                password=self.db_root_password,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            
            with connection.cursor() as cursor:
                query = """
                    SELECT 
                        ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) as size_mb
                    FROM information_schema.TABLES
                    WHERE table_schema = %s
                """
                cursor.execute(query, (db_name,))
                result = cursor.fetchone()
                
                if result and result['size_mb']:
                    return float(result['size_mb'])
                return 0.0
            
        except Exception as e:
            logger.error(f"❌ Erro ao obter tamanho do banco: {e}")
            return None
    
    def test_connection(self, db_name: str, db_user: str, db_password: str) -> bool:
        """
        Testa conexão com o banco do tenant
        """
        try:
            connection = pymysql.connect(
                host=self.db_host,
                port=self.db_port,
                user=db_user,
                password=db_password,
                database=db_name,
                charset='utf8mb4'
            )
            connection.close()
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao testar conexão: {e}")
            return False


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
