import os
import json
import glob
from datetime import datetime, timedelta
from pathlib import Path

today = datetime.today()
today_str = today.strftime('%Y-%m-%d')
threshold_date = (today - timedelta(days=30)).date()

RAW_DATA_PATH = Path(__file__).resolve().parent.parent / "Data" / "Fundamentals"

def update_fundamentals(cik:str, type: str) -> bool:
    """
    Determines if a local raw JSON file requires a fresh API update.
    """

    update = False
    CIK_DATA_PATH = RAW_DATA_PATH / cik

    
    search_pattern = os.path.join(CIK_DATA_PATH, f"*{type}*")

    matching_files = glob.glob(search_pattern)

    if len(matching_files) > 0:
        file = matching_files[0]
    else:
        return True

    file_comps = file.split("_")


    date_components = file_comps[-1].split('.')
    if datetime.strptime(date_components[0], "%Y-%m-%d").date() <= threshold_date:
        update = True

    return update


def save_json_fundamental_raw(data: dict, cik:str, type: str):
    CIK_DATA_PATH = RAW_DATA_PATH / cik

    if not os.path.exists(CIK_DATA_PATH):
        os.makedirs(CIK_DATA_PATH)

    search_pattern = os.path.join(CIK_DATA_PATH, f"*{type}*")
    for old_file in glob.glob(search_pattern):
            os.remove(old_file)

    filepath = CIK_DATA_PATH / f"{type}_{today_str}.json"

    with open(filepath, "w") as file:
        file.write(json.dumps(data))


def read_json_fundamental_raw(cik:str, type: str) -> dict:
    """
    Returns a json object
    """
    CIK_DATA_PATH = RAW_DATA_PATH / cik

    if not os.path.exists(CIK_DATA_PATH):
        # CIK doesn't exists in datalake
        return {}
    
    search_pattern = os.path.join(CIK_DATA_PATH, f"*{type}*")

    matching_files = glob.glob(search_pattern)

    if len(matching_files) > 0:
        file_path = matching_files[0]
    else:
        # No files for that type
        return {}

    with open(file_path, "r") as file:
        return json.load(file)