#!/usr/bin/env python3
"""
Script para inicializar/atualizar o banco de dados do LogiFlow CRM
Executa as migrations e cria dados iniciais se necessário
"""

import sys
import os
import logging

# Adiciona o diretório pai ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'
)
logger = logging.getLogger(__name__)

# Funções auxiliares para simular loguru
def log_info(msg): print(f"ℹ️  {msg}")
def log_success(msg): print(f"✅ {msg}")
def log_error(msg): print(f"❌ {msg}")

try:
    from sqlalchemy import create_engine, inspect, text
    from sqlalchemy.orm import sessionmaker
    from database import engine, Base
    from models_main import Tenant, User, Cliente, Motorista, Veiculo, Pedido, Entrega, Cotacao, Ocorrencia, Lead
except ImportError as e:
    print(f"❌ Erro de importação: {e}")
    print("💡 Execute: pip install sqlalchemy")
    sys.exit(1)


def create_tables():
    """Cria todas as tabelas no banco de dados"""
    log_info("Criando tabelas no banco de dados...")
    
    try:
        Base.metadata.create_all(bind=engine)
        log_success("Tabelas criadas com sucesso!")
        return True
    except Exception as e:
        log_error(f"Erro ao criar tabelas: {e}")
        return False


def check_tables():
    """Verifica quais tabelas existem"""
    from database import get_engine
    real_engine = get_engine()
    inspector = inspect(real_engine)
    tables = inspector.get_table_names()
    
    log_info(f"Tabelas existentes: {len(tables)}")
    for table in sorted(tables):
        columns = [col['name'] for col in inspector.get_columns(table)]
        print(f"   - {table}: {len(columns)} colunas")
    
    return tables


def create_demo_tenant():
    """Cria um tenant de demonstração se não existir"""
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Verifica se já existe
        existing = session.query(Tenant).filter(Tenant.subdomain == 'demo').first()
        if existing:
            log_info("Tenant demo já existe")
            return existing.id
        
        # Cria tenant demo
        tenant = Tenant(
            subdomain='demo',
            company_name='Transportadora Demo',
            contact_name='Administrador',
            contact_email='admin@demo.logiflow.com.br',
            contact_phone='(11) 99999-9999',
            db_name='logiflow_demo',
            db_user='demo_user',
            db_password='demo_pass',
            status='active'
        )
        
        session.add(tenant)
        session.commit()
        
        log_success(f"Tenant demo criado (ID: {tenant.id})")
        return tenant.id
        
    except Exception as e:
        session.rollback()
        log_error(f"Erro ao criar tenant demo: {e}")
        return None
    finally:
        session.close()


def create_demo_user(tenant_id):
    """Cria um usuário admin de demonstração"""
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Verifica se já existe
        existing = session.query(User).filter(User.email == 'admin@demo.logiflow.com.br').first()
        if existing:
            log_info("Usuário admin demo já existe")
            return existing.id
        
        # Hash da senha 'admin123' - usando hashlib se passlib não disponível
        try:
            from passlib.context import CryptContext
            pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
            hashed_password = pwd_context.hash("admin123")
        except ImportError:
            import hashlib
            hashed_password = hashlib.sha256("admin123".encode()).hexdigest()
        
        user = User(
            email='admin@demo.logiflow.com.br',
            hashed_password=hashed_password,
            full_name='Administrador Demo',
            role='admin',
            is_active=True,
            tenant_id=tenant_id
        )
        
        session.add(user)
        session.commit()
        
        log_success(f"Usuário admin demo criado (ID: {user.id})")
        print("   📧 Email: admin@demo.logiflow.com.br")
        print("   🔑 Senha: admin123")
        return user.id
        
    except Exception as e:
        session.rollback()
        log_error(f"Erro ao criar usuário demo: {e}")
        return None
    finally:
        session.close()


def main():
    """Função principal"""
    print("=" * 50)
    print("🚀 LogiFlow CRM - Inicialização do Banco de Dados")
    print("=" * 50)
    
    # 1. Criar tabelas
    if not create_tables():
        log_error("Falha ao criar tabelas. Abortando.")
        sys.exit(1)
    
    # 2. Verificar tabelas
    tables = check_tables()
    
    # 3. Criar tenant demo
    tenant_id = create_demo_tenant()
    
    # 4. Criar usuário demo
    if tenant_id:
        create_demo_user(tenant_id)
    
    print("=" * 50)
    log_success("Inicialização concluída!")
    print("=" * 50)


if __name__ == "__main__":
    main()
