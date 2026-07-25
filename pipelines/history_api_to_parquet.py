from datetime import datetime
import time
import logging
import os
import storage.yfinance_history as storage_history
import apis.yfinance as apiyf
import repository.securities_repository as securities

DJIA_TICKERS = {
    "AAPL", "AMGN", "AMZN", "AXP", "BA", "CAT", "CRM", "CSCO", "CVX",
    "DIS", "GS", "HD", "HON", "IBM", "JNJ", "JPM", "KO", "MCD", "MMM",
    "MRK", "MSFT", "NKE", "NVDA", "PG", "SHW", "TRV", "UNH", "V", "VZ", "WMT",
}

logger = logging.getLogger(__name__)

today = datetime.today()
today_str = today.strftime('%Y-%m-%d')

FETCH_UNIVERSE = os.getenv("FETCH_UNIVERSE", "full")


def get_target_securities():
    all_securities = securities.get_all_securities()
    if FETCH_UNIVERSE == "djia":
        return [s for s in all_securities if s[2] in DJIA_TICKERS]
    return all_securities


def fetch_history(full_time: bool = True):
    security_list = get_target_securities()

    for security in security_list:
        ticker = security[2]
        try:
            start = storage_history.get_latest_cached_date(ticker)
            if start == None:
                if full_time:
                    start = "1950-01-01"
                else:
                    start = "2010-01-01"
            df = apiyf.fetch_history(ticker, start, today_str)
            if df.empty:
                logger.warning(f"{ticker}: no data returned, skipping")
                continue
            logger.info(f"{ticker} fetched")
            storage_history.save_parquet_raw(ticker, df)
        except Exception:
            logger.exception(f"{ticker} failed")
        time.sleep(1)
