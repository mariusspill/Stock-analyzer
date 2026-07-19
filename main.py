import threading
import logging

import pipelines.sec_tickers_api_to_json as meta_json
import pipelines.metadata_json_to_db as meta_db

import pipelines.sec_fundamentals_api_to_json as fund_json
import pipelines.sec_income_statements_json_to_db as income_pipe

logging.basicConfig(  
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def mainFunction():
    meta_json.fetch_meta_data()
    meta_db.pipeline()

    fund_json.fetch_fundamentals()
    income_pipe.pipeline()

def frontend():
    pass

if __name__ == "__main__":

    t1 = threading.Thread(target=frontend)
    t2 = threading.Thread(target=mainFunction)

    t1.start()
    t2.start()
    t1.join()
    t2.join()