import repository.companies_repository as companies
import repository.securities_repository  as securities
import storage.sec_local_cache as slc
import json
import logging

logger = logging.getLogger(__name__)


def companies_data_pipeline():
    sec_tickers = slc.read_json_meta_raw("SEC_TICKERS")

    for entry in sec_tickers.values():
        cik = str(entry['cik_str']).zfill(10)
        if companies.get_id_by_cik(cik) == None:
            cid = companies.add(entry['title'], cik)
            logger.info(f"Create new Company {entry['title']} with cik {cik}")
        else:
            cid = companies.get_id_by_cik(cik)
            logger.info(f"Company {entry['title']} already exists")

        if securities.get_id_by_ticker(entry['ticker']) == None:
            securities.add_entry_securities(cid, entry['ticker'], None, None)
            logger.info(f"Create new Security {entry['ticker']} with id {cid}")




def cik_pipeline():
    cdata = companies.get_all_companies()
    sec_tickers = slc.read_json_meta_raw("SEC_TICKERS")

    for company in cdata:
        cid = company[0]
        ticker = securities.get_securities(company[0])[0][2]
        cik = None

        for entry in sec_tickers.values():
            if entry['ticker'] == ticker:
                cik = str(entry['cik_str']).zfill(10)

        if company[2] == None:
            companies.update_cik(cid, cik)
            logger.info(f"Updated {cid} with cik {cik}")



def pipeline():
    companies_data_pipeline()
    cik_pipeline()


pipeline()