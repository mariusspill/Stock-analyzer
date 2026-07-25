from dataclasses import dataclass
from datetime import date

import repository.sql_alchemy_connection as db
import sqlalchemy as sa

class StockSplit(db.Base):
    __tablename__ = "stock_splits"
    security_id = sa.Column(sa.Integer, sa.ForeignKey("securities.id"), primary_key=True)
    date = sa.Column(sa.Date, primary_key=True)
    old_amount = sa.Column( sa.Integer, nullable=False)
    new_amount = sa.Column( sa.Integer, nullable=False)

@dataclass
class StockSplitDto():
    security_id: int
    date_: date
    old_amount: int
    new_amount: int

def map_dto_to_orm(stock_split: StockSplitDto) -> StockSplit:
    result = StockSplit()
    result.security_id = stock_split.security_id
    result.date = stock_split.date_
    result.old_amount = stock_split.old_amount
    result.new_amount = stock_split.new_amount

    return result

def upsert_stock_splits(stock_split: StockSplitDto):
    data = map_dto_to_orm(stock_split)
    with db.Session() as session:
        session.merge(data)
        session.commit()


def get_stock_splits(security_id: int):
    with db.Session() as session:
        return (
            session.query(StockSplit).filter_by(security_id=security_id).order_by(StockSplit.date).all()
        )
