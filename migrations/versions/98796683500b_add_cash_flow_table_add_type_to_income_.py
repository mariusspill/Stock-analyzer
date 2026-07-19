"""add cash_flow table, add type to income_statements

Revision ID: 98796683500b
Revises: 4d2d7face826
Create Date: 2026-07-19 16:49:27.653460

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '98796683500b'
down_revision: Union[str, Sequence[str], None] = '4d2d7face826'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column('income_statements',
        sa.Column('type', sa.Enum('quarter', 'annual'), nullable=False, server_default='annual')
    )
    op.add_column('income_statements', sa.Column('quarter', sa.Enum("1", "2", "3", "4"), nullable= True))
    op.add_column('income_statements', sa.Column('pretax_income', sa.BigInteger))
    op.add_column('income_statements', sa.Column('eps_diluted', sa.Numeric(10, 4)))
    op.add_column('income_statements', sa.Column('weighted_avg_diluted_shares', sa.BigInteger))

    op.add_column('balance_sheets', sa.Column('quarter', sa.Enum("1", "2", "3", "4"), nullable= True))
    op.add_column('balance_sheets', sa.Column('total_current_liabilities', sa.BigInteger))
    op.add_column('balance_sheets', sa.Column('goodwill', sa.BigInteger))

    op.create_table('cash_flow_statements',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True, nullable=False),
        sa.Column('company_id', sa.Integer, sa.ForeignKey('companies.id'), nullable=False),
        sa.Column('year', sa.Integer, nullable=False),
        sa.Column('type', sa.Enum('quarter', 'annual'), nullable = False),
        sa.Column('quarter', sa.Enum("1", "2", "3", "4"), nullable= True),
        sa.Column('operating_cash_flow', sa.BigInteger),
        sa.Column('capital_expenditures', sa.BigInteger),
        sa.Column('investing_cash_flow', sa.BigInteger),
        sa.Column('financing_cash_flow', sa.BigInteger),
        sa.Column('dividends_paid', sa.BigInteger),
        sa.Column('depreciation_amortization', sa.BigInteger),
        sa.Column('checked', sa.Boolean, server_default='0'),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('cash_flow_statements')
    op.drop_column('balance_sheets', 'goodwill')
    op.drop_column('balance_sheets', 'total_current_liabilities')
    op.drop_column('balance_sheets', 'quarter')
    op.drop_column('income_statements', 'weighted_avg_diluted_shares')
    op.drop_column('income_statements', 'eps_diluted')
    op.drop_column('income_statements', 'pretax_income')
    op.drop_column('income_statements', 'quarter')
    op.drop_column('income_statements', 'type')
