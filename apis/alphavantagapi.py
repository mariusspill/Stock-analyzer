import requests
import os
from datetime import datetime
from dotenv import load_dotenv

date = datetime.today().strftime('%Y-%m-%d')

load_dotenv()
APIKEY = os.getenv("ALPHAVANTAGE_API_KEY")

def get_testData(function: str) -> dict:
    url = "https://www.alphavantage.co/query"

    params = {
        "function": function,
        "symbol": "IBM",
        "apikey": "demo"
    }

    response = requests.get(url, params)

    data = response.json()

    return data


def get_financial_data(ticker: str, type: str, key: str = APIKEY):
    url = "https://www.alphavantage.co/query"

    params = {
        "function": type,
        "symbol": ticker,
        "apikey": key
    }

    response = requests.get(url, params)

    data = response.json()

    return data