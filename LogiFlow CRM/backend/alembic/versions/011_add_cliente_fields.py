"""Add missing fields to clientes table

Revision ID: 011_add_cliente_fields
Revises: 
Create Date: 2024-01-01

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '011_add_cliente_fields'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """Adiciona campos faltantes na tabela clientes"""
    # Verificar e adicionar colunas que podem não existir
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    existing_columns = [col['name'] for col in inspector.get_columns('clientes')]
    
    columns_to_add = [
        ('razao_social', sa.String(255), True, None),
        ('nome_fantasia', sa.String(255), False, None),
        ('ie', sa.String(20), False, None),
        ('contato_nome', sa.String(255), False, None),
        ('celular', sa.String(20), False, None),
        ('cep', sa.String(10), False, None),
        ('logradouro', sa.String(255), False, None),
        ('numero', sa.String(20), False, None),
        ('complemento', sa.String(100), False, None),
        ('bairro', sa.String(100), False, None),
        ('condicao_pagamento', sa.String(50), False, '30_dias'),
        ('limite_credito', sa.Float, False, 0),
        ('ativo', sa.Boolean, False, True),
        ('observacoes', sa.Text, False, None),
    ]
    
    for col_name, col_type, nullable, default in columns_to_add:
        if col_name not in existing_columns:
            # Criar coluna
            if default is not None:
                op.add_column('clientes', sa.Column(col_name, col_type, nullable=True, server_default=str(default)))
            else:
                op.add_column('clientes', sa.Column(col_name, col_type, nullable=True))
    
    # Se existe coluna 'nome' mas não 'razao_social', copiar dados
    if 'nome' in existing_columns and 'razao_social' not in existing_columns:
        op.execute("UPDATE clientes SET razao_social = nome WHERE razao_social IS NULL")
    
    # Se existe coluna 'endereco' mas não 'logradouro', copiar dados
    if 'endereco' in existing_columns and 'logradouro' not in existing_columns:
        op.execute("UPDATE clientes SET logradouro = endereco WHERE logradouro IS NULL")


def downgrade():
    """Remove campos adicionados"""
    columns_to_remove = [
        'razao_social', 'nome_fantasia', 'ie', 'contato_nome', 'celular',
        'cep', 'logradouro', 'numero', 'complemento', 'bairro',
        'condicao_pagamento', 'limite_credito', 'ativo', 'observacoes'
    ]
    
    for col_name in columns_to_remove:
        try:
            op.drop_column('clientes', col_name)
        except Exception:
            pass
