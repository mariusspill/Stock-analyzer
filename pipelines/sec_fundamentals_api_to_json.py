import logging
import time

import repository.companies_repository as companies
from apis.sec import *
from storage.sec_fundamentals_cache import *

logger = logging.getLogger(__name__)

def fetch_fundamentals():
    type = "fundamentals"
    
    companies_list = companies.get_all_companies()

    for company in companies_list:
        cik = company[2]
        if cik is None:
            continue

        if update_fundamentals(cik, type):
            data = get_fundamental_json(cik)
            if data is not None:
                logger.info(f"Send out API request for: {cik}")
                save_json_fundamental_raw(data, cik, type)
            time.sleep(0.2)
        else:
            logger.info(f"{cik} already up to date")
            continue