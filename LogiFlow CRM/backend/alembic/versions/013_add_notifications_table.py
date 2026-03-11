"""add notifications table

Revision ID: 013
Revises: 012
Create Date: 2026-03-11 18:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '013'
down_revision = '012'
branch_labels = None
depends_on = None


def upgrade():
    # Create notifications table
    op.create_table(
        'notifications',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('tipo', sa.String(50), nullable=False),
        sa.Column('titulo', sa.String(255), nullable=False),
        sa.Column('mensagem', sa.Text(), nullable=False),
        sa.Column('link', sa.String(500), nullable=True),
        sa.Column('entity_type', sa.String(50), nullable=True),
        sa.Column('entity_id', sa.Integer(), nullable=True),
        sa.Column('icon', sa.String(50), nullable=True),
        sa.Column('color', sa.String(20), nullable=True),
        sa.Column('lida', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('lida_em', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes
    op.create_index('ix_notifications_user_id', 'notifications', ['user_id'])
    op.create_index('ix_notifications_tipo', 'notifications', ['tipo'])
    op.create_index('ix_notifications_lida', 'notifications', ['lida'])
    op.create_index('ix_notifications_created_at', 'notifications', ['created_at'])


def downgrade():
    op.drop_index('ix_notifications_created_at', table_name='notifications')
    op.drop_index('ix_notifications_lida', table_name='notifications')
    op.drop_index('ix_notifications_tipo', table_name='notifications')
    op.drop_index('ix_notifications_user_id', table_name='notifications')
    op.drop_table('notifications')
