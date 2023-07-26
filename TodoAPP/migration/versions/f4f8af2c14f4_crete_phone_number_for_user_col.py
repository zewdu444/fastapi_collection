"""Crete phone number for user col

Revision ID: f4f8af2c14f4
Revises:
Create Date: 2023-07-26 23:40:11.543616

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f4f8af2c14f4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
     op.add_column("users", sa.Column("phone_number", sa.String(20)))


def downgrade() -> None:
    pass
