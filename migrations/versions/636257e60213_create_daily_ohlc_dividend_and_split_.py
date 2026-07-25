"""Create daily_ohlc, dividend and split tables

Revision ID: 636257e60213
Revises: 98796683500b
Create Date: 2026-07-25 14:30:04.214846

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '636257e60213'
down_revision: Union[str, Sequence[str], None] = '98796683500b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("daily_ohlc",
                    sa.Column('security_id', sa.Integer, sa.ForeignKey('securities.id'),primary_key=True, nullable=False),
                    sa.Column('date', sa.Date, primary_key=True, nullable=False),
                    sa.Column('open', sa.DECIMAL(12, 4)),
                    sa.Column('high', sa.DECIMAL(12, 4)),
                    sa.Column('low', sa.DECIMAL(12, 4)),
                    sa.Column('close', sa.DECIMAL(12, 4)),
                    sa.Column('volume', sa.BigInteger))
    op.create_table("dividends",
                    sa.Column('security_id', sa.Integer, sa.ForeignKey('securities.id'),primary_key=True, nullable=False),
                    sa.Column('ex_date', sa.Date, primary_key=True, nullable=False),
                    sa.Column('amount', sa.DECIMAL(12, 4), nullable=False))
    op.create_table("stock_splits",
                    sa.Column('security_id', sa.Integer, sa.ForeignKey('securities.id'),primary_key=True, nullable=False),
                    sa.Column('date', sa.Date, primary_key=True, nullable=False),
                    sa.Column('old_amount', sa.Integer, nullable=False),
                    sa.Column('new_amount', sa.Integer, nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("daily_ohlc")
    op.drop_table("dividends")
    op.drop_table("stock_splits")
