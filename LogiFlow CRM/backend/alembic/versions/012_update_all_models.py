"""Update all models with new fields for MVP

Revision ID: 012_update_all_models
Revises: 011_add_cliente_fields
Create Date: 2024-01-01

"""
from alembic import op
import sqlalchemy as sa


revision = '012_update_all_models'
down_revision = '011_add_cliente_fields'
branch_labels = None
depends_on = None


def upgrade():
    """Adiciona campos faltantes em todas as tabelas principais"""
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    
    # ========================================
    # Tabela: motoristas
    # ========================================
    if 'motoristas' in inspector.get_table_names():
        existing = [col['name'] for col in inspector.get_columns('motoristas')]
        
        motorista_columns = [
            ('rg', sa.String(20)),
            ('data_nascimento', sa.String(20)),
            ('cnh_numero', sa.String(20)),
            ('cnh_categoria', sa.String(5)),
            ('cnh_validade', sa.String(20)),
            ('celular', sa.String(20)),
            ('cep', sa.String(10)),
            ('endereco', sa.String(255)),
            ('cidade', sa.String(100)),
            ('uf', sa.String(2)),
            ('data_admissao', sa.String(20)),
            ('observacoes', sa.Text),
            ('foto_url', sa.String(500)),
            ('veiculo_padrao_id', sa.Integer),
        ]
        
        for col_name, col_type in motorista_columns:
            if col_name not in existing:
                op.add_column('motoristas', sa.Column(col_name, col_type, nullable=True))
    
    # ========================================
    # Tabela: veiculos
    # ========================================
    if 'veiculos' in inspector.get_table_names():
        existing = [col['name'] for col in inspector.get_columns('veiculos')]
        
        veiculo_columns = [
            ('renavam', sa.String(20)),
            ('chassi', sa.String(50)),
            ('ano_fabricacao', sa.Integer),
            ('ano_modelo', sa.Integer),
            ('cor', sa.String(50)),
            ('tipo_carroceria', sa.String(50)),
            ('tipo_propriedade', sa.String(50)),
            ('capacidade_kg', sa.Float),
            ('capacidade_m3', sa.Float),
            ('eixos', sa.Integer),
            ('km_atual', sa.Integer),
            ('rntrc', sa.String(50)),
            ('antt', sa.String(50)),
            ('proprietario_nome', sa.String(255)),
            ('proprietario_documento', sa.String(20)),
            ('licenciamento_validade', sa.String(20)),
            ('seguro_apolice', sa.String(50)),
            ('seguro_validade', sa.String(20)),
            ('seguro_valor', sa.Float),
            ('observacoes', sa.Text),
            ('foto_url', sa.String(500)),
            ('motorista_padrao_id', sa.Integer),
        ]
        
        for col_name, col_type in veiculo_columns:
            if col_name not in existing:
                op.add_column('veiculos', sa.Column(col_name, col_type, nullable=True))
    
    # ========================================
    # Tabela: cotacoes
    # ========================================
    if 'cotacoes' in inspector.get_table_names():
        existing = [col['name'] for col in inspector.get_columns('cotacoes')]
        
        cotacao_columns = [
            ('cliente_nome', sa.String(255)),
            ('origem_cep', sa.String(10)),
            ('origem_logradouro', sa.String(255)),
            ('destino_cep', sa.String(10)),
            ('destino_logradouro', sa.String(255)),
            ('tipo_carga', sa.String(50)),
            ('modal', sa.String(50)),
            ('cubagem_m3', sa.Float),
            ('quantidade_volumes', sa.Integer),
            ('prazo_estimado', sa.Integer),
            ('valor_seguro', sa.Float),
            ('valor_adicional', sa.Float),
            ('urgente', sa.Boolean),
        ]
        
        for col_name, col_type in cotacao_columns:
            if col_name not in existing:
                op.add_column('cotacoes', sa.Column(col_name, col_type, nullable=True))


def downgrade():
    """Remove campos adicionados"""
    pass
