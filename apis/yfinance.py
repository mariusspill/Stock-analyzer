from pandas import DataFrame
import yfinance as yf


def fetch_history(ticker: str, start: str, end: str) -> DataFrame:
    y_ticker = yf.Ticker(ticker)

    return y_ticker.history(start=start, end=end, auto_adjust=False)
