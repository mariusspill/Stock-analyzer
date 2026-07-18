import requests


def get_tickers_json():
    url = "https://www.sec.gov/files/company_tickers.json"
    headers = {"User-Agent": "StockScreener marius.spill@gmail.com"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
