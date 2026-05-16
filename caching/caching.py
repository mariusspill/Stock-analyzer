import yfinance as yf
import json
import os

def cache_market_caps(tickers: list[str]):
    mcaps = dict()
    for ticker in tickers:
        try:
            mcaps[ticker] = yf.Ticker(ticker).info["marketCap"]
        except:
            print(ticker)

    os.remove("./caching/market_caps.json")
    with open("./caching/market_caps.json", "w") as f:
        json.dump(mcaps, f)


def get_market_caps():
    result = dict()
    with open("./caching/market_caps.json", "r") as f:
        result = json.load(f)
    return result