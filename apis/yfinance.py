import yfinance as yf
from pandas import DataFrame


def fetch_history(ticker: str, start: str, end: str) -> DataFrame:
    y_ticker = yf.Ticker(ticker)

    return y_ticker.history(start=start, end=end, auto_adjust=False)
