"""Create CRM Enterprise tables

Revision ID: 001_crm_enterprise
Revises: 
Create Date: 2026-01-18 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001_crm_enterprise'
down_revision = '005_create_gps'
branch_labels = None
depends_on = None


def upgrade():
    # Criar tabelas de CRM Enterprise
    
    # Oportunidades
    op.create_table('opportunities',
        sa.Column('id', sa.String(8), primary_key=True),
        sa.Column('cliente_id', sa.String(8), sa.ForeignKey('clientes.id'), nullable=False, index=True),
        sa.Column('nome', sa.String(255), nullable=False),
        sa.Column('descricao', sa.Text),
        sa.Column('valor_estimado', sa.Float, default=0),
        sa.Column('probabilidade', sa.Integer, default=0),
        sa.Column('sales_stage', sa.String(30), default='lead', index=True),
        sa.Column('data_prevista_fechamento', sa.DateTime),
        sa.Column('data_fechamento', sa.DateTime),
        sa.Column('responsavel_id', sa.String(36), sa.ForeignKey('users.id'), index=True),
        sa.Column('origem', sa.String(100)),
        sa.Column('proximo_passo', sa.String(255)),
        sa.Column('motivo_perda', sa.Text),
        sa.Column('concorrente', sa.String(200)),
        sa.Column('criado_em', sa.DateTime, default=sa.func.now(), index=True),
        sa.Column('atualizado_em', sa.DateTime, default=sa.func.now(), onupdate=sa.func.now())
    )
    
    # Histórico de mudanças de estágio
    op.create_table('opportunity_stage_history',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('oportunidade_id', sa.String(8), sa.ForeignKey('opportunities.id'), nullable=False, index=True),
        sa.Column('estagio_anterior', sa.String(30)),
        sa.Column('estagio_novo', sa.String(30), nullable=False),
        sa.Column('usuario_id', sa.String(36), sa.ForeignKey('users.id')),
        sa.Column('motivo', sa.Text),
        sa.Column('data_mudanca', sa.DateTime, default=sa.func.now(), index=True)
    )
    
    # Interações com clientes
    op.create_table('customer_interactions',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('cliente_id', sa.String(8), sa.ForeignKey('clientes.id'), nullable=False, index=True),
        sa.Column('oportunidade_id', sa.String(8), sa.ForeignKey('opportunities.id'), index=True),
        sa.Column('tipo', sa.String(30), nullable=False, index=True),
        sa.Column('assunto', sa.String(255), nullable=False),
        sa.Column('descricao', sa.Text),
        sa.Column('responsavel_id', sa.String(36), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('data_interacao', sa.DateTime, nullable=False, index=True),
        sa.Column('duracao_minutos', sa.Integer),
        sa.Column('resultado', sa.String(50)),
        sa.Column('proxima_acao', sa.String(255)),
        sa.Column('data_proxima_acao', sa.DateTime),
        sa.Column('criado_em', sa.DateTime, default=sa.func.now()),
        sa.Column('atualizado_em', sa.DateTime, default=sa.func.now(), onupdate=sa.func.now())
    )
    
    # Histórico de campos do cliente
    op.create_table('cliente_field_history',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('cliente_id', sa.String(8), sa.ForeignKey('clientes.id'), nullable=False, index=True),
        sa.Column('campo_alterado', sa.String(100), nullable=False),
        sa.Column('valor_anterior', sa.Text),
        sa.Column('valor_novo', sa.Text),
        sa.Column('usuario_id', sa.String(36), sa.ForeignKey('users.id')),
        sa.Column('data_alteracao', sa.DateTime, default=sa.func.now(), index=True),
        sa.Column('motivo', sa.Text)
    )
    
    # Histórico de status de leads
    op.create_table('lead_status_history',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('lead_id', sa.Integer, sa.ForeignKey('leads.id'), nullable=False, index=True),
        sa.Column('status_anterior', sa.String(20)),
        sa.Column('status_novo', sa.String(20), nullable=False),
        sa.Column('usuario_id', sa.String(36), sa.ForeignKey('users.id')),
        sa.Column('motivo', sa.Text),
        sa.Column('data_mudanca', sa.DateTime, default=sa.func.now(), index=True)
    )
    
    # Notas em oportunidades
    op.create_table('opportunity_notes',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('oportunidade_id', sa.String(8), sa.ForeignKey('opportunities.id'), nullable=False, index=True),
        sa.Column('conteudo', sa.Text, nullable=False),
        sa.Column('tipo', sa.String(30), default='note'),
        sa.Column('autor_id', sa.String(36), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('criado_em', sa.DateTime, default=sa.func.now(), index=True),
        sa.Column('editado_em', sa.DateTime)
    )
    
    # Produtos em oportunidades
    op.create_table('opportunity_products',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('oportunidade_id', sa.String(8), sa.ForeignKey('opportunities.id'), nullable=False, index=True),
        sa.Column('produto_nome', sa.String(255), nullable=False),
        sa.Column('descricao', sa.Text),
        sa.Column('quantidade', sa.Float, default=1),
        sa.Column('valor_unitario', sa.Float, nullable=False),
        sa.Column('valor_total', sa.Float, nullable=False),
        sa.Column('desconto_percentual', sa.Float, default=0),
        sa.Column('desconto_valor', sa.Float, default=0),
        sa.Column('criado_em', sa.DateTime, default=sa.func.now())
    )
    
    # Atividades de vendas
    op.create_table('sales_activities',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('oportunidade_id', sa.String(8), sa.ForeignKey('opportunities.id'), index=True),
        sa.Column('cliente_id', sa.String(8), sa.ForeignKey('clientes.id'), index=True),
        sa.Column('lead_id', sa.Integer, sa.ForeignKey('leads.id'), index=True),
        sa.Column('tipo', sa.String(30), nullable=False, index=True),
        sa.Column('assunto', sa.String(255), nullable=False),
        sa.Column('descricao', sa.Text),
        sa.Column('responsavel_id', sa.String(36), sa.ForeignKey('users.id'), nullable=False, index=True),
        sa.Column('data_planejada', sa.DateTime, nullable=False, index=True),
        sa.Column('data_conclusao', sa.DateTime),
        sa.Column('status', sa.String(20), default='planejada', index=True),
        sa.Column('prioridade', sa.String(20), default='media'),
        sa.Column('resultado', sa.Text),
        sa.Column('criado_em', sa.DateTime, default=sa.func.now()),
        sa.Column('atualizado_em', sa.DateTime, default=sa.func.now(), onupdate=sa.func.now())
    )
    
    # Forecast de vendas
    op.create_table('sales_forecasts',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('ano', sa.Integer, nullable=False, index=True),
        sa.Column('mes', sa.Integer, nullable=False, index=True),
        sa.Column('responsavel_id', sa.String(36), sa.ForeignKey('users.id'), index=True),
        sa.Column('valor_previsto', sa.Float, nullable=False),
        sa.Column('valor_comprometido', sa.Float, default=0),
        sa.Column('valor_upside', sa.Float, default=0),
        sa.Column('valor_realizado', sa.Float, default=0),
        sa.Column('numero_oportunidades', sa.Integer, default=0),
        sa.Column('criado_em', sa.DateTime, default=sa.func.now()),
        sa.Column('atualizado_em', sa.DateTime, default=sa.func.now(), onupdate=sa.func.now())
    )
    
    # Log de health score
    op.create_table('customer_health_score_log',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('cliente_id', sa.String(8), sa.ForeignKey('clientes.id'), nullable=False, index=True),
        sa.Column('score_anterior', sa.Float),
        sa.Column('score_novo', sa.Float, nullable=False),
        sa.Column('variacao', sa.Float, nullable=False),
        sa.Column('fatores_impacto', sa.JSON),
        sa.Column('data_calculo', sa.DateTime, default=sa.func.now(), index=True)
    )
    
    # Log de SLA de oportunidades
    op.create_table('opportunity_sla_log',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('oportunidade_id', sa.String(8), sa.ForeignKey('opportunities.id'), nullable=False, index=True),
        sa.Column('estagio', sa.String(30), nullable=False),
        sa.Column('dias_no_estagio', sa.Integer, nullable=False),
        sa.Column('sla_estagio_dias', sa.Integer, nullable=False),
        sa.Column('status_sla', sa.String(20), nullable=False, index=True),
        sa.Column('verificado_em', sa.DateTime, default=sa.func.now(), index=True)
    )
    
    # Segmentação de clientes
    op.create_table('cliente_segmentacao',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('cliente_id', sa.String(8), sa.ForeignKey('clientes.id'), nullable=False, unique=True, index=True),
        sa.Column('rfm_score', sa.Integer, default=0),
        sa.Column('recency_score', sa.Integer, default=0),
        sa.Column('frequency_score', sa.Integer, default=0),
        sa.Column('monetary_score', sa.Integer, default=0),
        sa.Column('segmento_rfm', sa.String(50)),
        sa.Column('ltv_estimado', sa.Float, default=0),
        sa.Column('risco_churn', sa.String(20), default='baixo', index=True),
        sa.Column('probabilidade_churn', sa.Float, default=0),
        sa.Column('propensao_upsell', sa.Float, default=0),
        sa.Column('propensao_cross_sell', sa.Float, default=0),
        sa.Column('atualizado_em', sa.DateTime, default=sa.func.now(), onupdate=sa.func.now())
    )
    
    # Templates de email
    op.create_table('email_templates',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('nome', sa.String(255), nullable=False),
        sa.Column('tipo', sa.String(50), nullable=False, index=True),
        sa.Column('assunto', sa.String(255), nullable=False),
        sa.Column('corpo_html', sa.Text, nullable=False),
        sa.Column('corpo_texto', sa.Text),
        sa.Column('variaveis_disponiveis', sa.JSON),
        sa.Column('ativo', sa.Boolean, default=True),
        sa.Column('criado_por', sa.String(36), sa.ForeignKey('users.id')),
        sa.Column('criado_em', sa.DateTime, default=sa.func.now()),
        sa.Column('atualizado_em', sa.DateTime, default=sa.func.now(), onupdate=sa.func.now())
    )
    
    # Adicionar colunas Enterprise na tabela clientes (SQLite batch mode)
    with op.batch_alter_table('clientes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('cargo_contato', sa.String(100)))
        batch_op.add_column(sa.Column('email_contato_secundario', sa.String(100)))
        batch_op.add_column(sa.Column('telefone_contato_secundario', sa.String(20)))
        batch_op.add_column(sa.Column('segmento', sa.String(100)))
        batch_op.add_column(sa.Column('porte', sa.String(50)))
        batch_op.add_column(sa.Column('status_comercial', sa.String(50), server_default='ativo'))
        batch_op.add_column(sa.Column('classificacao', sa.String(20), server_default='B'))
        batch_op.add_column(sa.Column('health_score', sa.Float, server_default='75.0'))
        batch_op.add_column(sa.Column('health_score_anterior', sa.Float))
        batch_op.add_column(sa.Column('health_score_atualizado_em', sa.DateTime))
        batch_op.add_column(sa.Column('responsavel_comercial_id', sa.String(36)))
        batch_op.add_column(sa.Column('responsavel_cs_id', sa.String(36)))
        batch_op.add_column(sa.Column('data_primeira_compra', sa.DateTime))
        batch_op.add_column(sa.Column('data_ultima_compra', sa.DateTime))
        batch_op.add_column(sa.Column('data_ultimo_contato', sa.DateTime))
        batch_op.add_column(sa.Column('valor_total_gasto', sa.Float, server_default='0'))
        batch_op.add_column(sa.Column('ticket_medio', sa.Float, server_default='0'))
        batch_op.add_column(sa.Column('frequencia_compra_dias', sa.Integer))
        batch_op.add_column(sa.Column('sla_resposta_horas', sa.Integer, server_default='24'))
        batch_op.add_column(sa.Column('prioridade_atendimento', sa.String(20), server_default='normal'))
        batch_op.add_column(sa.Column('tags', sa.Text))
        batch_op.add_column(sa.Column('observacoes_internas', sa.Text))
        batch_op.create_index('idx_cliente_status_comercial', ['status_comercial'])
        batch_op.create_index('idx_cliente_health_score', ['health_score'])
        batch_op.create_index('idx_cliente_responsavel_comercial', ['responsavel_comercial_id'])
        batch_op.create_index('idx_cliente_data_ultimo_contato', ['data_ultimo_contato'])
    
    # Adicionar colunas Enterprise na tabela leads (SQLite batch mode)
    with op.batch_alter_table('leads', schema=None) as batch_op:
        batch_op.add_column(sa.Column('cargo', sa.String(100)))
        batch_op.add_column(sa.Column('website', sa.String(255)))
        batch_op.add_column(sa.Column('linkedin', sa.String(255)))
        batch_op.add_column(sa.Column('necessidade_descrita', sa.Text))
        batch_op.add_column(sa.Column('source_details', sa.String(255)))
        batch_op.add_column(sa.Column('lead_score', sa.Integer, server_default='0'))
        batch_op.add_column(sa.Column('estagio_maturidade', sa.String(50), server_default='frio'))
        batch_op.add_column(sa.Column('primeiro_contato_em', sa.DateTime))
        batch_op.add_column(sa.Column('ultimo_contato_em', sa.DateTime))
        batch_op.add_column(sa.Column('proximo_followup_em', sa.DateTime))
        batch_op.add_column(sa.Column('converted_to_cliente_id', sa.String(8)))
        batch_op.add_column(sa.Column('motivo_descarte', sa.Text))
        batch_op.create_index('idx_lead_score', ['lead_score'])
        batch_op.create_index('idx_lead_source', ['source'])
        batch_op.create_index('idx_lead_proximo_followup', ['proximo_followup_em'])


def downgrade():
    # Remover colunas de leads (SQLite batch mode)
    with op.batch_alter_table('leads', schema=None) as batch_op:
        batch_op.drop_index('idx_lead_proximo_followup')
        batch_op.drop_index('idx_lead_source')
        batch_op.drop_index('idx_lead_score')
        batch_op.drop_column('motivo_descarte')
        batch_op.drop_column('converted_to_cliente_id')
        batch_op.drop_column('proximo_followup_em')
        batch_op.drop_column('ultimo_contato_em')
        batch_op.drop_column('primeiro_contato_em')
        batch_op.drop_column('estagio_maturidade')
        batch_op.drop_column('lead_score')
        batch_op.drop_column('source_details')
        batch_op.drop_column('necessidade_descrita')
        batch_op.drop_column('linkedin')
        batch_op.drop_column('website')
        batch_op.drop_column('cargo')
    
    # Remover colunas de clientes (SQLite batch mode)
    with op.batch_alter_table('clientes', schema=None) as batch_op:
        batch_op.drop_index('idx_cliente_data_ultimo_contato')
        batch_op.drop_index('idx_cliente_responsavel_comercial')
        batch_op.drop_index('idx_cliente_health_score')
        batch_op.drop_index('idx_cliente_status_comercial')
        batch_op.drop_column('observacoes_internas')
        batch_op.drop_column('tags')
        batch_op.drop_column('prioridade_atendimento')
        batch_op.drop_column('sla_resposta_horas')
        batch_op.drop_column('frequencia_compra_dias')
        batch_op.drop_column('ticket_medio')
        batch_op.drop_column('valor_total_gasto')
        batch_op.drop_column('data_ultimo_contato')
        batch_op.drop_column('data_ultima_compra')
        batch_op.drop_column('data_primeira_compra')
        batch_op.drop_column('responsavel_cs_id')
        batch_op.drop_column('responsavel_comercial_id')
        batch_op.drop_column('health_score_atualizado_em')
        batch_op.drop_column('health_score_anterior')
        batch_op.drop_column('health_score')
        batch_op.drop_column('classificacao')
        batch_op.drop_column('status_comercial')
        batch_op.drop_column('porte')
        batch_op.drop_column('segmento')
        batch_op.drop_column('telefone_contato_secundario')
        batch_op.drop_column('email_contato_secundario')
        batch_op.drop_column('cargo_contato')
    
    # Remover tabelas
    op.drop_table('email_templates')
    op.drop_table('cliente_segmentacao')
    op.drop_table('opportunity_sla_log')
    op.drop_table('customer_health_score_log')
    op.drop_table('sales_forecasts')
    op.drop_table('sales_activities')
    op.drop_table('opportunity_products')
    op.drop_table('opportunity_notes')
    op.drop_table('lead_status_history')
    op.drop_table('cliente_field_history')
    op.drop_table('customer_interactions')
    op.drop_table('opportunity_stage_history')
    op.drop_table('opportunities')
