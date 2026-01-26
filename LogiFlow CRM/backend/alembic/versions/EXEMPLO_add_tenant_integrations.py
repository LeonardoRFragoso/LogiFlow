"""Add tenant_integrations table

Revision ID: EXEMPLO_XXXXXX
Revises: (anterior)
Create Date: 2026-01-23 10:45:00.000000

IMPORTANTE: Este é um arquivo de EXEMPLO.
Para criar a migration real, execute:
    alembic revision --autogenerate -m "Add tenant_integrations table"

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'EXEMPLO_XXXXXX'
down_revision = None  # Substituir pelo ID da última migration
branch_labels = None
depends_on = None


def upgrade():
    """Cria tabela tenant_integrations"""
    op.create_table(
        'tenant_integrations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('tenant_id', sa.Integer(), nullable=False),
        sa.Column('integration_type', sa.String(length=50), nullable=False),
        sa.Column('api_key', sa.Text(), nullable=True),
        sa.Column('api_secret', sa.Text(), nullable=True),
        sa.Column('access_token', sa.Text(), nullable=True),
        sa.Column('refresh_token', sa.Text(), nullable=True),
        sa.Column('config', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True, default=True),
        sa.Column('is_valid', sa.Boolean(), nullable=True, default=False),
        sa.Column('last_validation', sa.DateTime(), nullable=True),
        sa.Column('validation_error', sa.Text(), nullable=True),
        sa.Column('environment', sa.String(length=20), nullable=True, default='production'),
        sa.Column('request_count', sa.Integer(), nullable=True, default=0),
        sa.Column('last_request', sa.DateTime(), nullable=True),
        sa.Column('monthly_limit', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('created_by', sa.Integer(), nullable=True),
        
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], )
    )
    
    # Índices para performance
    op.create_index(
        'ix_tenant_integrations_tenant_id',
        'tenant_integrations',
        ['tenant_id']
    )
    
    op.create_index(
        'ix_tenant_integrations_integration_type',
        'tenant_integrations',
        ['integration_type']
    )
    
    # Índice composto para busca rápida tenant + tipo
    op.create_index(
        'ix_tenant_integrations_tenant_type',
        'tenant_integrations',
        ['tenant_id', 'integration_type'],
        unique=False
    )


def downgrade():
    """Remove tabela tenant_integrations"""
    op.drop_index('ix_tenant_integrations_tenant_type', table_name='tenant_integrations')
    op.drop_index('ix_tenant_integrations_integration_type', table_name='tenant_integrations')
    op.drop_index('ix_tenant_integrations_tenant_id', table_name='tenant_integrations')
    op.drop_table('tenant_integrations')
