from dataclasses import dataclass
from datetime import date

import repository.sql_alchemy_connection as db
import sqlalchemy as sa

class Dividend(db.Base):
    __tablename__ = "dividends"
    security_id = sa.Column(sa.Integer, sa.ForeignKey("securities.id"), primary_key=True)
    ex_date = sa.Column(sa.Date, primary_key=True)
    amount = sa.Column(sa.DECIMAL(12,4), nullable=False)

@dataclass
class DividendDto():
    security_id: int
    date_: date
    amount: float

def map_dto_to_orm(dividend: DividendDto) -> Dividend:
    result = Dividend()
    result.security_id = dividend.security_id
    result.ex_date = dividend.date_
    result.amount = dividend.amount

    return result

def upsert_dividends(dividend: DividendDto):
    data = map_dto_to_orm(dividend)
    with db.Session() as session:
        session.merge(data)
        session.commit()


def get_dividends(security_id: int):
    with db.Session() as session:
        return (
            session.query(Dividend).filter_by(security_id=security_id).order_by(Dividend.ex_date).all()
        )
