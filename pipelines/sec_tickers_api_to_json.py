import logging
from storage.sec_local_cache import *
from apis.sec import *

logger = logging.getLogger(__name__)

def fetch_meta_data():
    type = "SEC_TICKERS"
    if update_meta("SEC_TICKERS"):
        data = get_tickers_json()
        logger.info(f"Send out API request for: {type}")
        save_json_meta_raw(data, type)
    else:
        logger.info(f"{type} already up to date")