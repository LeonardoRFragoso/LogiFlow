"""add lead cargo column

Revision ID: 011_add_lead_cargo
Revises: 010_add_tenant_db_columns
Create Date: 2026-03-10 14:50:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '011_add_lead_cargo'
down_revision = '010_add_tenant_db_columns'
branch_labels = None
depends_on = None


def upgrade():
    """Add cargo column to leads table if it doesn't exist"""
    
    # Check if column exists before adding
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    columns = [col['name'] for col in inspector.get_columns('leads')]
    
    if 'cargo' not in columns:
        op.add_column('leads', sa.Column('cargo', sa.String(length=100), nullable=True))
        print("✅ Coluna 'cargo' adicionada à tabela 'leads'")
    else:
        print("ℹ️ Coluna 'cargo' já existe na tabela 'leads'")


def downgrade():
    """Remove cargo column from leads table"""
    op.drop_column('leads', 'cargo')
