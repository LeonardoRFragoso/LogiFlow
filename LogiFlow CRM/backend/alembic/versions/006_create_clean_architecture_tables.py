"""Create Clean Architecture tables (clientes, cotacoes, pedidos)

Revision ID: 006
Revises: 005_create_gps_tables
Create Date: 2026-01-26

Tabelas para nova arquitetura em camadas (Domain-Driven Design).
Estas tabelas usam UUID como primary key e são otimizadas para PostgreSQL.
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '006_clean_architecture'
down_revision = '005_create_gps'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ===========================================
    # Tabela: clientes (v2 - Clean Architecture)
    # ===========================================
    op.create_table(
        'clientes_v2',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('razao_social', sa.String(200), nullable=False, index=True),
        sa.Column('nome_fantasia', sa.String(200), nullable=True),
        sa.Column('documento', sa.String(14), nullable=False, unique=True, index=True),
        sa.Column('email', sa.String(255), nullable=True, index=True),
        sa.Column('telefone', sa.String(20), nullable=True),
        sa.Column('inscricao_estadual', sa.String(20), nullable=True),
        sa.Column('ativo', sa.Boolean(), nullable=False, default=True),
        sa.Column('observacoes', sa.Text(), nullable=True),
        sa.Column('endereco', postgresql.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
    )
    
    # Índice composto para busca por status + nome
    op.create_index('ix_clientes_v2_ativo_razao', 'clientes_v2', ['ativo', 'razao_social'])
    
    # ===========================================
    # Tabela: cotacoes (v2 - Clean Architecture)
    # ===========================================
    op.create_table(
        'cotacoes_v2',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('numero', sa.String(50), nullable=False, unique=True, index=True),
        sa.Column('cliente_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('clientes_v2.id'), nullable=False, index=True),
        sa.Column('origem', postgresql.JSON(), nullable=False),
        sa.Column('destino', postgresql.JSON(), nullable=False),
        sa.Column('itens', postgresql.JSON(), nullable=False),
        sa.Column('tipo_frete', sa.String(10), nullable=False, default='CIF'),
        sa.Column('tipo_carga', sa.String(20), nullable=False, default='fracionada'),
        sa.Column('status', sa.String(20), nullable=False, default='rascunho', index=True),
        sa.Column('valor_frete', sa.Numeric(12, 2), nullable=False, default=0),
        sa.Column('valor_seguro', sa.Numeric(12, 2), nullable=False, default=0),
        sa.Column('valor_outros', sa.Numeric(12, 2), nullable=False, default=0),
        sa.Column('desconto', sa.Numeric(12, 2), nullable=False, default=0),
        sa.Column('validade', sa.Date(), nullable=True),
        sa.Column('observacoes', sa.Text(), nullable=True),
        sa.Column('criado_por', sa.String(100), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
    )
    
    # Índice composto para busca por cliente + status
    op.create_index('ix_cotacoes_v2_cliente_status', 'cotacoes_v2', ['cliente_id', 'status'])
    
    # Índice para cotações expiradas
    op.create_index('ix_cotacoes_v2_validade', 'cotacoes_v2', ['validade', 'status'])
    
    # ===========================================
    # Tabela: pedidos (v2 - Clean Architecture)
    # ===========================================
    op.create_table(
        'pedidos_v2',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('numero', sa.String(50), nullable=False, unique=True, index=True),
        sa.Column('cliente_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('clientes_v2.id'), nullable=False, index=True),
        sa.Column('cotacao_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('cotacoes_v2.id'), nullable=True),
        sa.Column('origem', postgresql.JSON(), nullable=False),
        sa.Column('destino', postgresql.JSON(), nullable=False),
        sa.Column('status', sa.String(30), nullable=False, default='aguardando_coleta', index=True),
        sa.Column('peso_kg', sa.Numeric(12, 3), nullable=False, default=0),
        sa.Column('volume_m3', sa.Numeric(12, 3), nullable=False, default=0),
        sa.Column('valor_mercadoria', sa.Numeric(12, 2), nullable=False, default=0),
        sa.Column('descricao_carga', sa.Text(), nullable=True),
        sa.Column('valor_frete', sa.Numeric(12, 2), nullable=False, default=0),
        sa.Column('valor_seguro', sa.Numeric(12, 2), nullable=False, default=0),
        sa.Column('valor_total', sa.Numeric(12, 2), nullable=False, default=0),
        sa.Column('data_coleta_prevista', sa.DateTime(), nullable=True),
        sa.Column('data_coleta_realizada', sa.DateTime(), nullable=True),
        sa.Column('data_entrega_prevista', sa.DateTime(), nullable=True),
        sa.Column('data_entrega_realizada', sa.DateTime(), nullable=True),
        sa.Column('motorista_id', postgresql.UUID(as_uuid=True), nullable=True, index=True),
        sa.Column('veiculo_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('cte_numero', sa.String(50), nullable=True),
        sa.Column('cte_chave', sa.String(50), nullable=True),
        sa.Column('nfe_chave', sa.String(50), nullable=True),
        sa.Column('observacoes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
    )
    
    # Índice composto para busca por cliente + status
    op.create_index('ix_pedidos_v2_cliente_status', 'pedidos_v2', ['cliente_id', 'status'])
    
    # Índice para pedidos em trânsito
    op.create_index('ix_pedidos_v2_motorista_status', 'pedidos_v2', ['motorista_id', 'status'])
    
    # Índice para tracking por datas
    op.create_index('ix_pedidos_v2_datas', 'pedidos_v2', ['data_coleta_prevista', 'data_entrega_prevista'])


def downgrade() -> None:
    # Remover índices compostos
    op.drop_index('ix_pedidos_v2_datas', 'pedidos_v2')
    op.drop_index('ix_pedidos_v2_motorista_status', 'pedidos_v2')
    op.drop_index('ix_pedidos_v2_cliente_status', 'pedidos_v2')
    op.drop_index('ix_cotacoes_v2_validade', 'cotacoes_v2')
    op.drop_index('ix_cotacoes_v2_cliente_status', 'cotacoes_v2')
    op.drop_index('ix_clientes_v2_ativo_razao', 'clientes_v2')
    
    # Remover tabelas (ordem inversa por causa das FKs)
    op.drop_table('pedidos_v2')
    op.drop_table('cotacoes_v2')
    op.drop_table('clientes_v2')
