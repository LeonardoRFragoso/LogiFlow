"""Create NPS, CSAT and Churn Alert tables

Revision ID: 004
Revises: 003
Create Date: 2025-12-15 14:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision = '004'
down_revision = '003'
branch_labels = None
depends_on = None


def upgrade():
    # NPSSurvey table
    op.create_table(
        'nps_surveys',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('tenant_id', sa.String(length=50), nullable=False),
        sa.Column('cliente_id', sa.String(length=50), nullable=False),
        sa.Column('tipo', sa.String(length=20), nullable=False),
        sa.Column('pergunta', sa.Text(), nullable=True),
        sa.Column('score', sa.Integer(), nullable=True),
        sa.Column('categoria', sa.String(length=20), nullable=True),
        sa.Column('feedback_texto', sa.Text(), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('data_criacao', sa.DateTime(), nullable=True),
        sa.Column('data_expiracao', sa.DateTime(), nullable=False),
        sa.Column('data_resposta', sa.DateTime(), nullable=True),
        sa.Column('data_envio_email', sa.DateTime(), nullable=True),
        sa.Column('link_pesquisa', sa.String(length=500), nullable=True),
        sa.Column('ip_resposta', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_nps_surveys_tenant_id', 'nps_surveys', ['tenant_id'])
    op.create_index('ix_nps_surveys_cliente_id', 'nps_surveys', ['cliente_id'])
    op.create_index('ix_nps_surveys_status', 'nps_surveys', ['status'])
    op.create_index('ix_nps_surveys_data_criacao', 'nps_surveys', ['data_criacao'])
    
    # CSATSurvey table
    op.create_table(
        'csat_surveys',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('tenant_id', sa.String(length=50), nullable=False),
        sa.Column('cliente_id', sa.String(length=50), nullable=False),
        sa.Column('ticket_id', sa.String(length=50), nullable=False),
        sa.Column('pergunta', sa.Text(), nullable=True),
        sa.Column('score', sa.Integer(), nullable=True),
        sa.Column('comentario', sa.Text(), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('data_criacao', sa.DateTime(), nullable=True),
        sa.Column('data_expiracao', sa.DateTime(), nullable=False),
        sa.Column('data_resposta', sa.DateTime(), nullable=True),
        sa.Column('data_envio_email', sa.DateTime(), nullable=True),
        sa.Column('link_pesquisa', sa.String(length=500), nullable=True),
        sa.Column('ip_resposta', sa.String(length=50), nullable=True),
        sa.Column('atendente_responsavel', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_csat_surveys_tenant_id', 'csat_surveys', ['tenant_id'])
    op.create_index('ix_csat_surveys_cliente_id', 'csat_surveys', ['cliente_id'])
    op.create_index('ix_csat_surveys_ticket_id', 'csat_surveys', ['ticket_id'])
    op.create_index('ix_csat_surveys_status', 'csat_surveys', ['status'])
    op.create_index('ix_csat_surveys_data_criacao', 'csat_surveys', ['data_criacao'])
    
    # ChurnAlert table
    op.create_table(
        'churn_alerts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('tenant_id', sa.String(length=50), nullable=False),
        sa.Column('cliente_id', sa.String(length=50), nullable=False),
        sa.Column('health_score', sa.Float(), nullable=False),
        sa.Column('health_score_anterior', sa.Float(), nullable=True),
        sa.Column('nivel_risco', sa.String(length=20), nullable=False),
        sa.Column('probabilidade_churn', sa.Float(), nullable=False),
        sa.Column('motivos', sa.Text(), nullable=True),
        sa.Column('metricas_criticas', sa.Text(), nullable=True),
        sa.Column('acao_requerida', sa.Boolean(), nullable=True),
        sa.Column('acao_sugerida', sa.Text(), nullable=True),
        sa.Column('prazo_acao_dias', sa.Integer(), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=True),
        sa.Column('atribuido_a', sa.String(length=100), nullable=True),
        sa.Column('data_resolucao', sa.DateTime(), nullable=True),
        sa.Column('acoes_tomadas', sa.Text(), nullable=True),
        sa.Column('resultado', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('notificado_em', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_churn_alerts_tenant_id', 'churn_alerts', ['tenant_id'])
    op.create_index('ix_churn_alerts_cliente_id', 'churn_alerts', ['cliente_id'])
    op.create_index('ix_churn_alerts_health_score', 'churn_alerts', ['health_score'])
    op.create_index('ix_churn_alerts_nivel_risco', 'churn_alerts', ['nivel_risco'])
    op.create_index('ix_churn_alerts_acao_requerida', 'churn_alerts', ['acao_requerida'])
    op.create_index('ix_churn_alerts_status', 'churn_alerts', ['status'])
    op.create_index('ix_churn_alerts_created_at', 'churn_alerts', ['created_at'])
    
    # CustomerSuccessAction table
    op.create_table(
        'cs_actions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('tenant_id', sa.String(length=50), nullable=False),
        sa.Column('cliente_id', sa.String(length=50), nullable=False),
        sa.Column('origem_tipo', sa.String(length=50), nullable=False),
        sa.Column('origem_id', sa.String(length=50), nullable=True),
        sa.Column('tipo', sa.String(length=50), nullable=False),
        sa.Column('titulo', sa.String(length=200), nullable=False),
        sa.Column('descricao', sa.Text(), nullable=True),
        sa.Column('responsavel', sa.String(length=100), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=True),
        sa.Column('prioridade', sa.String(length=20), nullable=True),
        sa.Column('data_criacao', sa.DateTime(), nullable=True),
        sa.Column('prazo', sa.DateTime(), nullable=True),
        sa.Column('data_conclusao', sa.DateTime(), nullable=True),
        sa.Column('resultado', sa.Text(), nullable=True),
        sa.Column('notas', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_cs_actions_tenant_id', 'cs_actions', ['tenant_id'])
    op.create_index('ix_cs_actions_cliente_id', 'cs_actions', ['cliente_id'])
    op.create_index('ix_cs_actions_status', 'cs_actions', ['status'])
    op.create_index('ix_cs_actions_data_criacao', 'cs_actions', ['data_criacao'])
    op.create_index('ix_cs_actions_prazo', 'cs_actions', ['prazo'])


def downgrade():
    op.drop_table('cs_actions')
    op.drop_table('churn_alerts')
    op.drop_table('csat_surveys')
    op.drop_table('nps_surveys')

