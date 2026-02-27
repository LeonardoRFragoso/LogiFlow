"""Add tenant_id to main models - Standalone Migration

Revision ID: 008_add_tenant_id_standalone
Revises: None
Create Date: 2026-02-27 09:15:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '008_add_tenant_id_standalone'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """
    Cria tabelas base e adiciona campo tenant_id para multi-tenancy
    """
    # Criar tabela tenants
    op.execute("""
        CREATE TABLE IF NOT EXISTS tenants (
            id SERIAL PRIMARY KEY,
            company_name VARCHAR(255) NOT NULL,
            contact_name VARCHAR(255),
            contact_email VARCHAR(255),
            contact_phone VARCHAR(20),
            subdomain VARCHAR(100) UNIQUE,
            status VARCHAR(50) DEFAULT 'active',
            plan VARCHAR(50) DEFAULT 'starter',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Criar tabela users se não existir
    op.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            nome VARCHAR(255),
            senha_hash VARCHAR(255),
            tipo VARCHAR(50),
            status VARCHAR(50) DEFAULT 'ativo',
            tenant_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE
        )
    """)
    
    # Criar tabela clientes se não existir
    op.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(255) NOT NULL,
            email VARCHAR(255),
            telefone VARCHAR(20),
            cnpj VARCHAR(20),
            endereco TEXT,
            cidade VARCHAR(100),
            uf VARCHAR(2),
            tenant_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE
        )
    """)
    
    # Criar tabela motoristas se não existir
    op.execute("""
        CREATE TABLE IF NOT EXISTS motoristas (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(255) NOT NULL,
            cpf VARCHAR(20),
            cnh VARCHAR(20),
            email VARCHAR(255),
            telefone VARCHAR(20),
            status VARCHAR(50),
            disponibilidade VARCHAR(50),
            tipo_contrato VARCHAR(50),
            tenant_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE
        )
    """)
    
    # Criar tabela veiculos se não existir
    op.execute("""
        CREATE TABLE IF NOT EXISTS veiculos (
            id SERIAL PRIMARY KEY,
            placa VARCHAR(20) UNIQUE NOT NULL,
            marca VARCHAR(100),
            modelo VARCHAR(100),
            ano INTEGER,
            status VARCHAR(50),
            disponibilidade VARCHAR(50),
            tipo VARCHAR(50),
            tipo_carroceria VARCHAR(50),
            tipo_propriedade VARCHAR(50),
            capacidade_kg FLOAT,
            tenant_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE
        )
    """)
    
    # Criar tabela pedidos se não existir
    op.execute("""
        CREATE TABLE IF NOT EXISTS pedidos (
            id SERIAL PRIMARY KEY,
            cliente_id INTEGER,
            cliente_nome VARCHAR(255),
            status VARCHAR(50),
            prioridade VARCHAR(50),
            tipo_frete VARCHAR(50),
            peso_total_kg FLOAT,
            volume_total_m3 FLOAT,
            valor_mercadoria FLOAT,
            motorista_id INTEGER,
            veiculo_id INTEGER,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            tenant_id INTEGER,
            FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE
        )
    """)
    
    # Criar tabela entregas se não existir
    op.execute("""
        CREATE TABLE IF NOT EXISTS entregas (
            id SERIAL PRIMARY KEY,
            codigo VARCHAR(100),
            cliente_id INTEGER,
            cliente_nome VARCHAR(255),
            endereco_entrega TEXT,
            cidade VARCHAR(100),
            uf VARCHAR(2),
            status VARCHAR(50),
            data_entrega TIMESTAMP,
            tenant_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE
        )
    """)
    
    # Criar tabela leads se não existir
    op.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255),
            phone VARCHAR(20),
            company VARCHAR(255),
            vehicles VARCHAR(255),
            message TEXT,
            status VARCHAR(50),
            source VARCHAR(50),
            assigned_to INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            converted_at TIMESTAMP,
            tenant_id INTEGER,
            FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE
        )
    """)
    
    # Criar índices para performance
    op.execute("CREATE INDEX IF NOT EXISTS idx_users_tenant_id ON users(tenant_id)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_clientes_tenant_id ON clientes(tenant_id)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_motoristas_tenant_id ON motoristas(tenant_id)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_veiculos_tenant_id ON veiculos(tenant_id)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_pedidos_tenant_id ON pedidos(tenant_id)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_entregas_tenant_id ON entregas(tenant_id)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_leads_tenant_id ON leads(tenant_id)")


def downgrade():
    """
    Remove tenant_id dos modelos
    """
    tables_to_update = [
        'users',
        'clientes',
        'motoristas',
        'veiculos',
        'pedidos',
        'entregas',
        'leads',
    ]
    
    # Remover constraints e colunas
    for table in tables_to_update:
        op.execute(f"""
            ALTER TABLE {table}
            DROP CONSTRAINT IF EXISTS fk_{table}_tenant_id
        """)
        
        op.execute(f"""
            DROP INDEX IF EXISTS idx_{table}_tenant_id
        """)
        
        op.execute(f"""
            ALTER TABLE {table}
            DROP COLUMN IF EXISTS tenant_id
        """)
    
    # Remover tabela tenants
    op.execute("DROP TABLE IF EXISTS tenants")
