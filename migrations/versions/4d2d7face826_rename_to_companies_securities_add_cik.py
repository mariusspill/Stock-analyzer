"""rename to companies/securities, add cik

Revision ID: 4d2d7face826
Revises: f558a661d6a3
Create Date: 2026-07-18 17:11:24.537374

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4d2d7face826'
down_revision: Union[str, Sequence[str], None] = 'f558a661d6a3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.rename_table('company', 'companies')
    op.add_column('companies', sa.Column('cik', sa.CHAR(10), nullable=True))

    op.rename_table('company_identifiers', 'securities')

    # company_id was both PK and FK (1:1 with company) — drop that FK/PK,
    # add a surrogate PK so a company can have multiple securities.
    op.drop_constraint('securities_ibfk_1', 'securities', type_='foreignkey')
    op.execute('ALTER TABLE securities DROP PRIMARY KEY')
    op.add_column('securities', sa.Column('id', sa.Integer, primary_key=True, autoincrement=True, nullable=False))
    op.alter_column('securities', 'company_id', nullable=False)
    op.create_foreign_key('fk_securities_company_id', 'securities', 'companies', ['company_id'], ['id'])


def downgrade() -> None:
    op.drop_constraint('fk_securities_company_id', 'securities', type_='foreignkey')
    op.drop_column('securities', 'id')
    op.execute('ALTER TABLE securities ADD PRIMARY KEY (company_id)')
    op.create_foreign_key('company_identifiers_ibfk_1', 'securities', 'companies', ['company_id'], ['id'])
    op.rename_table('securities', 'company_identifiers')

    op.drop_column('companies', 'cik')
    op.rename_table('companies', 'company')
