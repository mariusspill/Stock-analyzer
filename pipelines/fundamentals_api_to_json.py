import helpers.tickers as tickers
import time
from storage.local_cache import save_json_raw
from apis.alphavantagapi import get_financial_data
from storage.local_cache import update_file
import logging

logger = logging.getLogger(__name__)


def fetch_data():
    tckrs = tickers.getTickers("./Data/Indices/s&p500.txt")

    counter = 0

    for ticker in tckrs:
        if not update_file(ticker, 'incomeStatement'):
            logger.info("Skip because data is up to date: " + ticker)
            continue

        data = get_financial_data(ticker, "INCOME_STATEMENT")
        logger.info("Send out API request for: " + ticker)
        result = save_json_raw(ticker, data, "incomeStatement")

        # AlphaVantage only allows one request every second - sleep to not outspeed rate
        time.sleep(1.5)

        if result == 0:
            counter += 1
            with open("./helpers/list.txt", "a") as file:
                text = "\n" + ticker
                file.write(text)
        elif result == 1:
            # if no json was fetched terminate 
            logger.info(f'{counter} calls have been made')
            return 1
        
        logger.info(f'{counter} calls have been made')
