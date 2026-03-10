"""Add db_name, db_user, db_password to tenants table

Revision ID: 010_add_tenant_db_columns
Revises: 009_add_strategic_indices
Create Date: 2026-03-10 12:20:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '010_add_tenant_db_columns'
down_revision = '009_add_strategic_indices'
branch_labels = None
depends_on = None


def upgrade():
    """
    Adiciona colunas de banco de dados dedicado à tabela tenants
    """
    # Verificar se as colunas já existem antes de adicionar
    conn = op.get_bind()
    
    # Adicionar db_name se não existir
    result = conn.execute(sa.text("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name='tenants' AND column_name='db_name'
    """))
    if not result.fetchone():
        op.execute("""
            ALTER TABLE tenants 
            ADD COLUMN db_name VARCHAR(100)
        """)
        print("✅ Coluna db_name adicionada")
    
    # Adicionar db_user se não existir
    result = conn.execute(sa.text("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name='tenants' AND column_name='db_user'
    """))
    if not result.fetchone():
        op.execute("""
            ALTER TABLE tenants 
            ADD COLUMN db_user VARCHAR(100)
        """)
        print("✅ Coluna db_user adicionada")
    
    # Adicionar db_password se não existir
    result = conn.execute(sa.text("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name='tenants' AND column_name='db_password'
    """))
    if not result.fetchone():
        op.execute("""
            ALTER TABLE tenants 
            ADD COLUMN db_password VARCHAR(255)
        """)
        print("✅ Coluna db_password adicionada")
    
    # Adicionar trial_ends_at se não existir
    result = conn.execute(sa.text("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name='tenants' AND column_name='trial_ends_at'
    """))
    if not result.fetchone():
        op.execute("""
            ALTER TABLE tenants 
            ADD COLUMN trial_ends_at TIMESTAMP
        """)
        print("✅ Coluna trial_ends_at adicionada")
    
    # Adicionar max_users se não existir
    result = conn.execute(sa.text("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name='tenants' AND column_name='max_users'
    """))
    if not result.fetchone():
        op.execute("""
            ALTER TABLE tenants 
            ADD COLUMN max_users INTEGER DEFAULT 5
        """)
        print("✅ Coluna max_users adicionada")
    
    # Adicionar max_vehicles se não existir
    result = conn.execute(sa.text("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name='tenants' AND column_name='max_vehicles'
    """))
    if not result.fetchone():
        op.execute("""
            ALTER TABLE tenants 
            ADD COLUMN max_vehicles INTEGER DEFAULT 10
        """)
        print("✅ Coluna max_vehicles adicionada")
    
    # Adicionar max_orders_per_month se não existir
    result = conn.execute(sa.text("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name='tenants' AND column_name='max_orders_per_month'
    """))
    if not result.fetchone():
        op.execute("""
            ALTER TABLE tenants 
            ADD COLUMN max_orders_per_month INTEGER DEFAULT 500
        """)
        print("✅ Coluna max_orders_per_month adicionada")
    
    # Adicionar cancelled_at se não existir
    result = conn.execute(sa.text("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name='tenants' AND column_name='cancelled_at'
    """))
    if not result.fetchone():
        op.execute("""
            ALTER TABLE tenants 
            ADD COLUMN cancelled_at TIMESTAMP
        """)
        print("✅ Coluna cancelled_at adicionada")
    
    # Criar índice único para db_name se não existir
    op.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS idx_tenants_db_name 
        ON tenants(db_name) 
        WHERE db_name IS NOT NULL
    """)
    print("✅ Índice único criado para db_name")


def downgrade():
    """
    Remove as colunas adicionadas
    """
    op.execute("DROP INDEX IF EXISTS idx_tenants_db_name")
    op.execute("ALTER TABLE tenants DROP COLUMN IF EXISTS db_name")
    op.execute("ALTER TABLE tenants DROP COLUMN IF EXISTS db_user")
    op.execute("ALTER TABLE tenants DROP COLUMN IF EXISTS db_password")
    op.execute("ALTER TABLE tenants DROP COLUMN IF EXISTS trial_ends_at")
    op.execute("ALTER TABLE tenants DROP COLUMN IF EXISTS max_users")
    op.execute("ALTER TABLE tenants DROP COLUMN IF EXISTS max_vehicles")
    op.execute("ALTER TABLE tenants DROP COLUMN IF EXISTS max_orders_per_month")
    op.execute("ALTER TABLE tenants DROP COLUMN IF EXISTS cancelled_at")
