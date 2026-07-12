"""baseline schema

Revision ID: f558a661d6a3
Revises: 
Create Date: 2026-07-12 12:05:59.616622

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f558a661d6a3'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'company',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True, nullable=False),
        sa.Column('name', sa.VARCHAR(255))
    )

    op.create_table(
        'company_identifiers',
        sa.Column('company_id', sa.Integer, sa.ForeignKey('company.id'), primary_key=True, nullable=False),
        sa.Column('ticker', sa.VARCHAR(10)),
        sa.Column('isin', sa.VARCHAR(12)),
        sa.Column('wkn', sa.VARCHAR(6))
    )

    op.create_table('income_statements',
                    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True, nullable=False),
                    sa.Column('company_id', sa.Integer, sa.ForeignKey('company.id'), nullable=False),
                    sa.Column('year', sa.Integer),
                    sa.Column('revenue', sa.BigInteger),
                    sa.Column('gross_profit', sa.BigInteger),
                    sa.Column('operating_income', sa.BigInteger),
                    sa.Column('net_income', sa.BigInteger),
                    sa.Column('EBIT', sa.BigInteger),
                    sa.Column('EBITDA', sa.BigInteger),
                    sa.Column('cost_of_revenue', sa.BigInteger),
                    sa.Column('operating_expense', sa.BigInteger),
                    sa.Column('interest_cost', sa.BigInteger),
                    sa.Column('taxes', sa.BigInteger),
                    sa.Column('checked', sa.Boolean, server_default='0')
                    )

    op.create_table('balance_sheets',
                    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True, nullable=False),
                    sa.Column('company_id', sa.Integer, sa.ForeignKey('company.id'), nullable=False),
                    sa.Column('year', sa.Integer, nullable=False),
                    sa.Column('type', sa.Enum('quarter', 'annual'), nullable=False),
                    sa.Column('total_assets', sa.BigInteger),
                    sa.Column('total_current_assets', sa.BigInteger),
                    sa.Column('cash', sa.BigInteger),
                    sa.Column('receivables', sa.BigInteger),
                    sa.Column('inventories', sa.BigInteger),
                    sa.Column('properties_plant_equipment', sa.BigInteger),
                    sa.Column('intangible_assets', sa.BigInteger),
                    sa.Column('total_liabilities_and_equity', sa.BigInteger),
                    sa.Column('short_debt', sa.BigInteger),
                    sa.Column('long_debt', sa.BigInteger),
                    sa.Column('total_debt', sa.BigInteger),
                    sa.Column('total_liabilities', sa.BigInteger),
                    sa.Column('total_equity', sa.BigInteger),
                    sa.Column('retained_earnings', sa.BigInteger),
                    sa.Column('total_shares', sa.BigInteger),
                    sa.Column('treasury_shares', sa.BigInteger),
                    sa.Column('shares_outstanding', sa.BigInteger),
                    sa.Column('checked', sa.Boolean, server_default='0'),
                    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('balance_sheets')

    op.drop_table('income_statements')

    op.drop_table('company_identifiers')

    op.drop_table('company')
