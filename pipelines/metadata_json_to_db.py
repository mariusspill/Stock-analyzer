import repository.companies_repository as companies
import repository.securities_repository  as securities
import storage.sec_local_cache as slc
import json
import logging

logger = logging.getLogger(__name__)


def pipeline():
    cdata = companies.get_all_companies()
    for company in cdata:
        print(company)
        print(securities.get_securities(company[0]))

    sec_tickers = slc.read_json_meta_raw("SEC_TICKERS")

    for entry in sec_tickers.values():
        pass


pipeline()