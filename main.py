import helpers.tickers as tickers
import threading
import logging

from pipelines.sec_tickers_api_to_json import fetch_meta_data

logging.basicConfig(  
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def mainFunction():
    fetch_meta_data()

def frontend():
    pass

if __name__ == "__main__":

    t1 = threading.Thread(target=frontend)
    t2 = threading.Thread(target=mainFunction)

    t1.start()
    t2.start()
    t1.join()
    t2.join()