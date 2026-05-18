"""create_item_commands_table

Revision ID: 5d6e7f8g9h0i
Revises: 4c5d6e7f8g9h
Create Date: 2026-05-17 18:33:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


revision: str = '5d6e7f8g9h0i'
down_revision: Union[str, None] = '4c5d6e7f8g9h'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('item_commands',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('command_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('unit_price', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['command_id'], ['commands.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_item_commands_command_id'), 'item_commands', ['command_id'], unique=False)
    op.create_index(op.f('ix_item_commands_product_id'), 'item_commands', ['product_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_item_commands_product_id'), table_name='item_commands')
    op.drop_index(op.f('ix_item_commands_command_id'), table_name='item_commands')
    op.drop_table('item_commands')
