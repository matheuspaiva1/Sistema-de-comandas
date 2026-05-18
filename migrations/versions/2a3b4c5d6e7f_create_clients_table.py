"""create_clients_table

Revision ID: 2a3b4c5d6e7f
Revises: 10f545c66d1b
Create Date: 2026-05-17 18:30:00.000000

"""
from typing import Sequence, Union

import sqlmodel
from alembic import op
import sqlalchemy as sa


revision: str = '2a3b4c5d6e7f'
down_revision: Union[str, None] = '10f545c66d1b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('clients',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(length=100), nullable=False),
    sa.Column('phone', sqlmodel.sql.sqltypes.AutoString(length=20), nullable=True),
    sa.Column('email', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=True),
    sa.Column('tax_id', sqlmodel.sql.sqltypes.AutoString(length=20), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_clients_name'), 'clients', ['name'], unique=False)
    op.create_index(op.f('ix_clients_email'), 'clients', ['email'], unique=False)
    op.create_index(op.f('ix_clients_tax_id'), 'clients', ['tax_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_clients_tax_id'), table_name='clients')
    op.drop_index(op.f('ix_clients_email'), table_name='clients')
    op.drop_index(op.f('ix_clients_name'), table_name='clients')
    op.drop_table('clients')
