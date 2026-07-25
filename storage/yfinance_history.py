import os
import json
import glob
import pandas as pd
from datetime import date
from datetime import datetime, timedelta
from pathlib import Path

RAW_DATA_PATH = Path(__file__).resolve().parent.parent / "Data" / "Histories"

def get_latest_cached_date(ticker: str) -> date | None:
    TICKER_DATA_PATH = RAW_DATA_PATH / ticker
    search_pattern = os.path.join(TICKER_DATA_PATH, "*history*")
    files = glob.glob(search_pattern)

    if not files:
        return None 

    latest_file = max(files) 
    df = pd.read_parquet(latest_file)
    return df.index.max().date()


def save_parquet_raw(ticker: str, df: pd.DataFrame):
    TICKER_DATA_PATH = RAW_DATA_PATH / ticker

    if not os.path.exists(TICKER_DATA_PATH):
        os.makedirs(TICKER_DATA_PATH)

    dt = df.index.max().date().isoformat()

    filepath = TICKER_DATA_PATH / f"history_{dt}.parquet"

    df.to_parquet(filepath)


def read_parquet_raw(filepath) -> pd.DataFrame:
    return pd.read_parquet(filepath)

def read_all_history(ticker: str) -> pd.DataFrame | None:
    TICKER_DATA_PATH = RAW_DATA_PATH / ticker
    search_pattern = os.path.join(TICKER_DATA_PATH, "*history*")
    files = sorted(glob.glob(search_pattern))

    if not files:
        return None

    dfs = [read_parquet_raw(f) for f in files]
    combined = pd.concat(dfs)
    combined = combined[~combined.index.duplicated(keep="last")]
    return combined.sort_index()

