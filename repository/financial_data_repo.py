import helpers.tickers as tickers
from storage.local_cache import save_json_raw
from apis.alphavantagapi import get_financial_data
from storage.local_cache import update_file

def fetch_data():
    tckrs = tickers.getTickers("./Data/Indices/s&p500.txt")

    for ticker in tckrs:
        if not update_file(ticker, 'incomeStatement'):
            print("Skip because current: " + ticker)
            continue

        data = get_financial_data(ticker, "INCOME_STATEMENT")
        print("Fetch new json: " + ticker)
        result = save_json_raw(ticker, data, "incomeStatement")

        if result == 1:
            with open("./helpers/list.txt", "a") as file:
                text = "\n" + ticker
                file.write(text)