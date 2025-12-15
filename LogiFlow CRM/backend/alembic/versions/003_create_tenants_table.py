"""create tenants table

Revision ID: 003_create_tenants
Revises: 002_add_tenant_id
Create Date: 2024-12-15 14:10:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql, postgresql

# revision identifiers, used by Alembic.
revision = '003_create_tenants'
down_revision = '002_add_tenant_id'
branch_labels = None
depends_on = None


def upgrade():
    """
    Cria tabela de tenants com informações de plano e billing
    """
    op.create_table(
        'tenants',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nome', sa.String(200), nullable=False),
        sa.Column('slug', sa.String(100), nullable=False, unique=True),
        sa.Column('cnpj', sa.String(20), nullable=True),
        sa.Column('email', sa.String(200), nullable=False),
        sa.Column('telefone', sa.String(20), nullable=True),
        
        # Endereço
        sa.Column('endereco', sa.String(300), nullable=True),
        sa.Column('cidade', sa.String(100), nullable=True),
        sa.Column('uf', sa.String(2), nullable=True),
        sa.Column('cep', sa.String(10), nullable=True),
        
        # Plano e Billing
        sa.Column('plano', sa.String(50), nullable=False, server_default='free'),
        sa.Column('status', sa.String(50), nullable=False, server_default='active'),
        sa.Column('data_inicio', sa.DateTime(), nullable=True),
        sa.Column('data_fim', sa.DateTime(), nullable=True),
        sa.Column('data_cancelamento', sa.DateTime(), nullable=True),
        
        # Mercado Pago
        sa.Column('mercadopago_subscription_id', sa.String(100), nullable=True),
        sa.Column('mercadopago_customer_id', sa.String(100), nullable=True),
        
        # Configurações
        sa.Column('configuracoes', sa.JSON(), nullable=True),
        
        # Metadados
        sa.Column('ativo', sa.Boolean(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=True, onupdate=sa.text('CURRENT_TIMESTAMP')),
        
        sa.PrimaryKeyConstraint('id')
    )
    
    # Índices
    op.create_index('ix_tenants_slug', 'tenants', ['slug'], unique=True)
    op.create_index('ix_tenants_email', 'tenants', ['email'])
    op.create_index('ix_tenants_plano', 'tenants', ['plano'])
    op.create_index('ix_tenants_status', 'tenants', ['status'])
    op.create_index('ix_tenants_ativo', 'tenants', ['ativo'])
    
    print("✓ Tabela 'tenants' criada com sucesso")


def downgrade():
    """
    Remove tabela de tenants
    """
    op.drop_table('tenants')
    print("✓ Tabela 'tenants' removida")

