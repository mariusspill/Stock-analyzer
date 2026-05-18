import helpers.tickers as tickers
import apis.alphavantagapi as ava
import caching.caching as cch
import webinterface.webmain as wm
import threading
from repository.financial_data_repo import fetch_data

tckrs = tickers.getTickers("./helpers/list.txt")

def daily_fetch():
    fetch_data()


def daily_cache():
    cch.cache_market_caps(tckrs)


def mainFunction():
    daily_fetch()
    daily_cache()    

if __name__ == "__main__":
    t1 = threading.Thread(target=wm.runFlask)
    t2 = threading.Thread(target=mainFunction)

    t1.start()
    t2.start()
    t1.join()
    t2.join()