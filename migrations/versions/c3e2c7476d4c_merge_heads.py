"""merge heads

Revision ID: c3e2c7476d4c
Revises: 6e7f8g9h0i1j, 8654e9649bff
Create Date: 2026-05-17 18:49:56.759741

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c3e2c7476d4c'
down_revision: Union[str, None] = ('6e7f8g9h0i1j', '8654e9649bff')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
