"""create_tables_table

Revision ID: 3b4c5d6e7f8g
Revises: 2a3b4c5d6e7f
Create Date: 2026-05-17 18:31:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


revision: str = '3b4c5d6e7f8g'
down_revision: Union[str, None] = '2a3b4c5d6e7f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('tables',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('number', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('seats', sa.Integer(), nullable=True),
    sa.Column('location', sa.String(), nullable=True),
    sa.Column('status', sa.Enum('LIVRE', 'OCUPADA', name='tablestatus'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tables_number'), 'tables', ['number'], unique=False)
    op.create_index(op.f('ix_tables_status'), 'tables', ['status'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_tables_status'), table_name='tables')
    op.drop_index(op.f('ix_tables_number'), table_name='tables')
    op.drop_table('tables')
