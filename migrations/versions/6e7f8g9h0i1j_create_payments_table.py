"""create_payments_table

Revision ID: 6e7f8g9h0i1j
Revises: 5d6e7f8g9h0i
Create Date: 2026-05-17 18:34:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


revision: str = '6e7f8g9h0i1j'
down_revision: Union[str, None] = '5d6e7f8g9h0i'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('payments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('command_id', sa.Integer(), nullable=True),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('method', sa.Enum('DINHEIRO', 'CARTAO', 'PIX', name='paymentmethod'), nullable=False),
    sa.Column('status', sa.Enum('PENDENTE', 'PAGO', 'ESTORNADO', name='paymentstatus'), nullable=False),
    sa.Column('paid_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['command_id'], ['commands.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_payments_command_id'), 'payments', ['command_id'], unique=False)
    op.create_index(op.f('ix_payments_status'), 'payments', ['status'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_payments_status'), table_name='payments')
    op.drop_index(op.f('ix_payments_command_id'), table_name='payments')
    op.drop_table('payments')
