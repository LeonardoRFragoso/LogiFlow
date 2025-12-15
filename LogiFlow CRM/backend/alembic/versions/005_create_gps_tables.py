"""Create GPS tracking tables

Revision ID: 005
Revises: 004
Create Date: 2025-12-15 16:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '005'
down_revision = '004'
branch_labels = None
depends_on = None


def upgrade():
    # GPSPosition table
    op.create_table(
        'gps_positions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('tenant_id', sa.String(length=50), nullable=False),
        sa.Column('placa', sa.String(length=10), nullable=False),
        sa.Column('veiculo_id', sa.String(length=50), nullable=True),
        sa.Column('provider', sa.String(length=50), nullable=False),
        sa.Column('provider_vehicle_id', sa.String(length=100), nullable=True),
        sa.Column('latitude', sa.Float(), nullable=False),
        sa.Column('longitude', sa.Float(), nullable=False),
        sa.Column('altitude', sa.Float(), nullable=True),
        sa.Column('precisao_metros', sa.Float(), nullable=True),
        sa.Column('velocidade_kmh', sa.Float(), nullable=True),
        sa.Column('direcao_graus', sa.Integer(), nullable=True),
        sa.Column('ignicao', sa.Boolean(), nullable=True),
        sa.Column('em_movimento', sa.Boolean(), nullable=True),
        sa.Column('endereco_completo', sa.String(length=500), nullable=True),
        sa.Column('cidade', sa.String(length=100), nullable=True),
        sa.Column('estado', sa.String(length=2), nullable=True),
        sa.Column('alertas', sa.Text(), nullable=True),
        sa.Column('odometro_km', sa.Float(), nullable=True),
        sa.Column('horimetro_horas', sa.Float(), nullable=True),
        sa.Column('data_gps', sa.DateTime(), nullable=False),
        sa.Column('data_recebimento', sa.DateTime(), nullable=True),
        sa.Column('payload_original', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_gps_positions_tenant_id', 'gps_positions', ['tenant_id'])
    op.create_index('ix_gps_positions_placa', 'gps_positions', ['placa'])
    op.create_index('ix_gps_positions_provider', 'gps_positions', ['provider'])
    op.create_index('ix_gps_positions_em_movimento', 'gps_positions', ['em_movimento'])
    op.create_index('ix_gps_positions_data_gps', 'gps_positions', ['data_gps'])
    op.create_index('ix_gps_positions_data_recebimento', 'gps_positions', ['data_recebimento'])
    
    # GPSRoute table
    op.create_table(
        'gps_routes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('tenant_id', sa.String(length=50), nullable=False),
        sa.Column('placa', sa.String(length=10), nullable=False),
        sa.Column('rota_nome', sa.String(length=200), nullable=True),
        sa.Column('origem_lat', sa.Float(), nullable=True),
        sa.Column('origem_lng', sa.Float(), nullable=True),
        sa.Column('origem_endereco', sa.String(length=500), nullable=True),
        sa.Column('destino_lat', sa.Float(), nullable=True),
        sa.Column('destino_lng', sa.Float(), nullable=True),
        sa.Column('destino_endereco', sa.String(length=500), nullable=True),
        sa.Column('distancia_total_km', sa.Float(), nullable=True),
        sa.Column('duracao_minutos', sa.Integer(), nullable=True),
        sa.Column('velocidade_media_kmh', sa.Float(), nullable=True),
        sa.Column('velocidade_maxima_kmh', sa.Float(), nullable=True),
        sa.Column('total_paradas', sa.Integer(), nullable=True),
        sa.Column('tempo_parado_minutos', sa.Integer(), nullable=True),
        sa.Column('pontos_rota', sa.Text(), nullable=True),
        sa.Column('provider', sa.String(length=50), nullable=False),
        sa.Column('data_inicio', sa.DateTime(), nullable=False),
        sa.Column('data_fim', sa.DateTime(), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_gps_routes_tenant_id', 'gps_routes', ['tenant_id'])
    op.create_index('ix_gps_routes_placa', 'gps_routes', ['placa'])
    op.create_index('ix_gps_routes_data_inicio', 'gps_routes', ['data_inicio'])
    op.create_index('ix_gps_routes_data_fim', 'gps_routes', ['data_fim'])


def downgrade():
    op.drop_table('gps_routes')
    op.drop_table('gps_positions')

