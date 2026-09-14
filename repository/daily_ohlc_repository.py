from dataclasses import dataclass
from datetime import date

import sqlalchemy as sa

import repository.sql_alchemy_connection as db


class DailyOhlc(db.Base):
    __tablename__ = "daily_ohlc"
    security_id = sa.Column(sa.Integer, sa.ForeignKey("securities.id"), primary_key=True)
    date = sa.Column(sa.Date, primary_key=True)
    open = sa.Column(sa.DECIMAL(12, 4))
    high = sa.Column(sa.DECIMAL(12, 4))
    low = sa.Column(sa.DECIMAL(12, 4))
    close = sa.Column(sa.DECIMAL(12, 4))
    volume = sa.Column(sa.BigInteger)

@dataclass
class OhlcDto():
    security_id: int
    date_: date
    open: float
    high: float
    low: float
    close: float
    volume: int

def map_dto_to_orm(ohlc: OhlcDto) -> DailyOhlc:
    result = DailyOhlc()
    result.security_id = ohlc.security_id
    result.date = ohlc.date_
    result.open = ohlc.open
    result.high = ohlc.high
    result.low = ohlc.low
    result.close = ohlc.close
    result.volume = ohlc.volume

    return result

def upsert_daily_ohlc(ohlc: OhlcDto):
    data = map_dto_to_orm(ohlc)
    with db.Session() as session:
        session.merge(data)
        session.commit()


def get_daily_ohlc(security_id: int):
    with db.Session() as session:
        return (
            session.query(DailyOhlc).filter_by(security_id=security_id).order_by(DailyOhlc.date).all()
        )
