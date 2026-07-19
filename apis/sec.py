import requests


def get_tickers_json():
    url = "https://www.sec.gov/files/company_tickers.json"
    headers = {"User-Agent": "StockScreener marius.spill@gmail.com"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()



def get_fundamental_json(cik: str) -> dict:
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
    headers = {"User-Agent": "StockScreener marius.spill@gmail.com"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    