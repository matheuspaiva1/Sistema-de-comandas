"""create_products_table

Revision ID: 10f545c66d1b
Revises: 
Create Date: 2026-05-14 18:28:09.163344

"""
from typing import Sequence, Union

import sqlmodel  # noqa: F401
from alembic import op
import sqlalchemy as sa


revision: str = '10f545c66d1b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sqlmodel.sql.sqltypes.AutoString(length=100), nullable=False),
    sa.Column('descricao', sqlmodel.sql.sqltypes.AutoString(length=500), nullable=False),
    sa.Column('categoria', sa.Enum('BEBIDA', 'PRATO_PRINCIPAL', 'ENTRADA', 'SOBREMESA', 'LANCHE', 'OUTRO', name='categoriaenum'), nullable=False),
    sa.Column('preco', sa.Float(), nullable=False),
    sa.Column('ativo', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('products')
