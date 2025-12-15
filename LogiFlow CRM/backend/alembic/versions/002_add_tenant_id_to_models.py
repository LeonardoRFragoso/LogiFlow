"""add tenant_id to models

Revision ID: 002_add_tenant_id
Revises: 001_initial
Create Date: 2024-12-15 14:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '002_add_tenant_id'
down_revision = '001_initial'
branch_labels = None
depends_on = None


def upgrade():
    """
    Adiciona campo tenant_id em todas as tabelas principais
    """
    # Lista de tabelas que precisam de tenant_id
    tables = [
        'users',
        'refresh_tokens',
        'tenant_credentials',
        # Adicionar outras tabelas conforme forem criadas:
        # 'entregas',
        # 'cotacoes',
        # 'pedidos',
        # 'motoristas',
        # 'veiculos',
        # 'clientes',
        # 'ocorrencias',
    ]
    
    for table in tables:
        # Verificar se a coluna já existe
        conn = op.get_bind()
        inspector = sa.inspect(conn)
        
        if table not in inspector.get_table_names():
            print(f"Tabela {table} não existe, pulando...")
            continue
        
        columns = [c['name'] for c in inspector.get_columns(table)]
        
        if 'tenant_id' not in columns:
            # Adicionar coluna tenant_id
            op.add_column(
                table,
                sa.Column('tenant_id', sa.Integer(), nullable=True)
            )
            
            # Criar índice para performance
            op.create_index(
                f'ix_{table}_tenant_id',
                table,
                ['tenant_id']
            )
            
            # Adicionar foreign key para tenants (se a tabela existir)
            if 'tenants' in inspector.get_table_names():
                op.create_foreign_key(
                    f'fk_{table}_tenant_id',
                    table,
                    'tenants',
                    ['tenant_id'],
                    ['id'],
                    ondelete='CASCADE'
                )
            
            print(f"✓ Coluna tenant_id adicionada em {table}")
        else:
            print(f"✓ Coluna tenant_id já existe em {table}")


def downgrade():
    """
    Remove campo tenant_id das tabelas
    """
    tables = [
        'users',
        'refresh_tokens',
        'tenant_credentials',
    ]
    
    for table in tables:
        conn = op.get_bind()
        inspector = sa.inspect(conn)
        
        if table not in inspector.get_table_names():
            continue
        
        columns = [c['name'] for c in inspector.get_columns(table)]
        
        if 'tenant_id' in columns:
            # Remover foreign key
            op.drop_constraint(f'fk_{table}_tenant_id', table, type_='foreignkey')
            
            # Remover índice
            op.drop_index(f'ix_{table}_tenant_id', table_name=table)
            
            # Remover coluna
            op.drop_column(table, 'tenant_id')
            
            print(f"✓ Coluna tenant_id removida de {table}")

