import os
import json
import glob
from datetime import datetime
from pathlib import Path

date = datetime.today().strftime('%Y-%m-%d')
threshold_string = "2025-12-31"
threshold_date = datetime.strptime(threshold_string, "%Y-%m-%d").date()

RAW_DATA_PATH = Path(__file__).resolve().parent.parent / "Data" / "RawData"


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

    TICKER_DATA_PATH = RAW_DATA_PATH / ticker

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
    # Test if no real data and analyze the reason
    note_msg = data.get("Note", "")
    info_msg = data.get("Information", "")
    if "Note" in data.keys() or "Information" in data.keys() or "False" in data.keys():
        if "We have detected" in note_msg or "We have detected" in info_msg:
            print("API key limit reached: " + ticker)
        elif "1 request per second" in note_msg or "1 request per second" in info_msg:
            print("Speed limit warning received, ticker skipped: " + ticker)
        # Return 1 to signal no json was fetched
        return 1

    # Real data / json received
    result = 0

    TICKER_DATA_PATH = RAW_DATA_PATH / ticker

    if not os.path.exists(TICKER_DATA_PATH):
        os.makedirs(TICKER_DATA_PATH)

    search_pattern = os.path.join(TICKER_DATA_PATH, f"*{type}*")
    for old_file in glob.glob(search_pattern):
            os.remove(old_file)

    filepath = TICKER_DATA_PATH / f"{ticker}_{type}_{date}.json"

    with open(filepath, "w") as file:
        file.write(json.dumps(data))
    
    return result


def read_json_raw(ticker: str, type: str, annual: bool = True) -> dict:
    """
    Returns a json object
    """

    TICKER_DATA_PATH = RAW_DATA_PATH / ticker

    if not os.path.exists(TICKER_DATA_PATH):
        # Ticker doesn't exists in datalake
        return {}
    
    search_pattern = os.path.join(TICKER_DATA_PATH, f"*{type}*")

    matching_files = glob.glob(search_pattern)

    if len(matching_files) > 0:
        file_path = matching_files[0]
    else:
        # No files for that type
        return {}

    with open(file_path, "r") as file:
        if annual:
            return json.load(file).get("annualReports", {})
        else:
            return json.load(file)
