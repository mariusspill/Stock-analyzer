import os
import json
import glob
from datetime import datetime

date = datetime.today().strftime('%Y-%m-%d')
threshold_string = "2025-12-31"
threshold_date = datetime.strptime(threshold_string, "%Y-%m-%d").date()

RAW_DATA_PATH = "D:\\Data\\Programming\\GitHub\\StockScreener\\Data\\RawData\\"


def update_file(ticker: str, type: str) -> bool:
    """
    Determines if a local raw JSON file requires a fresh API update.

    Args:
        ticker (str): Stock ticker using standard 
        type (str): incomeStatement, cashFlow or balanceSheet

    Returns:
        bool:   True if newest raw json should be updated (older than threshold or in old format)
                False if newest json should not be updated (newer than threshold)
    """
    update = False

    TICKER_DATA_PATH = RAW_DATA_PATH + ticker

    search_pattern = os.path.join(TICKER_DATA_PATH, f"*{type}*")

    matching_files = glob.glob(search_pattern)

    if len(matching_files) > 0:
        file = matching_files[0]
    else:
        return True

    file_comps = file.split("_")

    if file_comps[-1] == f"{type}.json":
        update = True
    else:
        date_components = file_comps[-1].split('.')
        if datetime.strptime(date_components[0], "%Y-%m-%d").date() <= threshold_date:
            update = True

    return update


def save_json_raw(ticker: str, data: dict, type: str):
    if "Note" in data.keys() or "Information" in data.keys() or "False" in data.keys():
        return 0

    result = 1

    TICKER_DATA_PATH = RAW_DATA_PATH + ticker

    if not os.path.exists(TICKER_DATA_PATH):
        os.makedirs(TICKER_DATA_PATH)

    search_pattern = os.path.join(TICKER_DATA_PATH, f"*{type}*")
    for old_file in glob.glob(search_pattern):
        result = 0
        os.remove(old_file)

    filepath = TICKER_DATA_PATH + "\\" + ticker + "_" + type + "_" + date + ".json"

    with open(filepath, "w") as file:
        file.write(json.dumps(data))
    
    return result
