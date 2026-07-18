import os
import json
import glob
from datetime import datetime, timedelta
from pathlib import Path

today = datetime.today()
today_str = today.strftime('%Y-%m-%d')
threshold_date = (today - timedelta(days=today.weekday())).date()

RAW_DATA_PATH = Path(__file__).resolve().parent.parent / "Data" / "MetaData"

def update_meta(type: str) -> bool:
    """
    Determines if a local raw JSON file requires a fresh API update.
    """

    update = False

    search_pattern = os.path.join(RAW_DATA_PATH, f"*{type}*")
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


def save_json_meta_raw(data: dict, type: str):

    if not os.path.exists(RAW_DATA_PATH):
        os.makedirs(RAW_DATA_PATH)

    search_pattern = os.path.join(RAW_DATA_PATH, f"*{type}*")
    for old_file in glob.glob(search_pattern):
            os.remove(old_file)

    filepath = RAW_DATA_PATH / f"{type}_{today_str}.json"

    with open(filepath, "w") as file:
        file.write(json.dumps(data))


def read_json_meta_raw(type: str) -> dict:
    """
    Returns a json object
    """
    search_pattern = os.path.join(RAW_DATA_PATH, f"*{type}*")

    matching_files = glob.glob(search_pattern)

    if len(matching_files) > 0:
        file_path = matching_files[0]
    else:
        # No files for that type
        return {}

    with open(file_path, "r") as file:
        return json.load(file)
