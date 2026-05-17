"""create_commands_table

Revision ID: 4c5d6e7f8g9h
Revises: 3b4c5d6e7f8g
Create Date: 2026-05-17 18:32:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


revision: str = '4c5d6e7f8g9h'
down_revision: Union[str, None] = '3b4c5d6e7f8g'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('commands',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code', sa.Integer(), nullable=False),
    sa.Column('client_id', sa.Integer(), nullable=False),
    sa.Column('status', sa.Enum('ABERTA', 'FECHADA', 'CANCELADA', name='commandstatus'), nullable=False),
    sa.Column('opened_at', sa.DateTime(), nullable=False),
    sa.Column('closed_at', sa.DateTime(), nullable=True),
    sa.Column('total_amount', sa.Float(), nullable=False),
    sa.Column('table_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['client_id'], ['clients.id'], ),
    sa.ForeignKeyConstraint(['table_id'], ['tables.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_commands_code'), 'commands', ['code'], unique=False)
    op.create_index(op.f('ix_commands_client_id'), 'commands', ['client_id'], unique=False)
    op.create_index(op.f('ix_commands_status'), 'commands', ['status'], unique=False)
    op.create_index(op.f('ix_commands_table_id'), 'commands', ['table_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_commands_table_id'), table_name='commands')
    op.drop_index(op.f('ix_commands_status'), table_name='commands')
    op.drop_index(op.f('ix_commands_client_id'), table_name='commands')
    op.drop_index(op.f('ix_commands_code'), table_name='commands')
    op.drop_table('commands')
