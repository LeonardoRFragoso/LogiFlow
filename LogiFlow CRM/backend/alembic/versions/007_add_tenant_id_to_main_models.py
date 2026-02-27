"""Add tenant_id to main models (Cliente, Motorista, Veiculo, Pedido, Entrega)

Revision ID: 007_add_tenant_id_main_models
Revises: 006_create_clean_architecture_tables
Create Date: 2026-02-27 08:30:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '007_add_tenant_id_main_models'
down_revision = '006_create_clean_architecture_tables'
branch_labels = None
depends_on = None


def upgrade():
    """
    Adiciona campo tenant_id aos modelos principais para multi-tenancy
    """
    # Lista de tabelas que precisam de tenant_id
    tables_to_update = [
        'clientes',
        'motoristas',
        'veiculos',
        'pedidos',
        'entregas',
    ]
    
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    
    for table in tables_to_update:
        # Verificar se a tabela existe
        if table not in inspector.get_table_names():
            print(f"⚠️  Tabela {table} não existe, pulando...")
            continue
        
        # Verificar se a coluna já existe
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
            
            # Adicionar foreign key para tenants
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
    
    # Remover constraints UNIQUE que conflitam com multi-tenancy
    # (ex: cnpj, cpf, placa, numero, codigo devem ser únicos por tenant, não globalmente)
    
    # Para Cliente: remover unique constraint de cnpj
    try:
        if 'clientes' in inspector.get_table_names():
            constraints = inspector.get_unique_constraints('clientes')
            for constraint in constraints:
                if 'cnpj' in constraint['column_names']:
                    op.drop_constraint(constraint['name'], 'clientes', type_='unique')
                    print(f"✓ Removido constraint UNIQUE de cnpj em clientes")
    except Exception as e:
        print(f"⚠️  Erro ao remover constraint de cnpj: {e}")
    
    # Para Motorista: remover unique constraint de cpf
    try:
        if 'motoristas' in inspector.get_table_names():
            constraints = inspector.get_unique_constraints('motoristas')
            for constraint in constraints:
                if 'cpf' in constraint['column_names']:
                    op.drop_constraint(constraint['name'], 'motoristas', type_='unique')
                    print(f"✓ Removido constraint UNIQUE de cpf em motoristas")
    except Exception as e:
        print(f"⚠️  Erro ao remover constraint de cpf: {e}")
    
    # Para Veiculo: remover unique constraint de placa
    try:
        if 'veiculos' in inspector.get_table_names():
            constraints = inspector.get_unique_constraints('veiculos')
            for constraint in constraints:
                if 'placa' in constraint['column_names']:
                    op.drop_constraint(constraint['name'], 'veiculos', type_='unique')
                    print(f"✓ Removido constraint UNIQUE de placa em veiculos")
    except Exception as e:
        print(f"⚠️  Erro ao remover constraint de placa: {e}")
    
    # Para Pedido: remover unique constraint de numero
    try:
        if 'pedidos' in inspector.get_table_names():
            constraints = inspector.get_unique_constraints('pedidos')
            for constraint in constraints:
                if 'numero' in constraint['column_names']:
                    op.drop_constraint(constraint['name'], 'pedidos', type_='unique')
                    print(f"✓ Removido constraint UNIQUE de numero em pedidos")
    except Exception as e:
        print(f"⚠️  Erro ao remover constraint de numero: {e}")
    
    # Para Entrega: remover unique constraint de codigo
    try:
        if 'entregas' in inspector.get_table_names():
            constraints = inspector.get_unique_constraints('entregas')
            for constraint in constraints:
                if 'codigo' in constraint['column_names']:
                    op.drop_constraint(constraint['name'], 'entregas', type_='unique')
                    print(f"✓ Removido constraint UNIQUE de codigo em entregas")
    except Exception as e:
        print(f"⚠️  Erro ao remover constraint de codigo: {e}")


def downgrade():
    """
    Remove campo tenant_id dos modelos principais
    """
    tables_to_update = [
        'clientes',
        'motoristas',
        'veiculos',
        'pedidos',
        'entregas',
    ]
    
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    
    for table in tables_to_update:
        if table not in inspector.get_table_names():
            continue
        
        columns = [c['name'] for c in inspector.get_columns(table)]
        
        if 'tenant_id' in columns:
            # Remover foreign key
            try:
                op.drop_constraint(f'fk_{table}_tenant_id', table, type_='foreignkey')
            except Exception:
                pass
            
            # Remover índice
            try:
                op.drop_index(f'ix_{table}_tenant_id', table_name=table)
            except Exception:
                pass
            
            # Remover coluna
            op.drop_column(table, 'tenant_id')
            
            print(f"✓ Coluna tenant_id removida de {table}")
