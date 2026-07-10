import helpers.tickers as tickers
import caching.caching as cch
import threading
from pipelines.fundamentals_api_to_json import fetch_data
import pipelines.fundamentals_json_to_db as pfj

tckrs = tickers.getTickers("./helpers/list.txt")
sp500 = tickers.getTickers("./Data/Indices/s&p500.txt")

def daily_fetch():
    fetch_data()


def daily_cache():
    cch.cache_market_caps(sp500)


def mainFunction():
    # daily_fetch()
    # daily_cache()
    pfj.testing()

def frontend():
    pass

if __name__ == "__main__":
    t1 = threading.Thread(target=frontend)
    t2 = threading.Thread(target=mainFunction)

    t1.start()
    t2.start()
    t1.join()
    t2.join()