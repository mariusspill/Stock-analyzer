import logging

logger = logging.getLogger(__name__)


def get_tag_value(facts: dict, tag_candidates: list, fy: int, fp: str, unit: str = "USD"):
    """
    Walks a priority list of XBRL tags and returns the first one that has
    a reported value for the given fiscal year + fiscal period (e.g. fy=2024,
    fp="FY" or "Q1"). Cross-checks the fact's own 'end' date against fy to
    avoid matching a comparative prior-year figure mistakenly tagged with a
    later filing's fy. Returns None if no candidate tag has data for that period.
    """
    us_gaap = facts.get("facts", {}).get("us-gaap", {})

    for tag in tag_candidates:
        tag_data = us_gaap.get(tag)
        if not tag_data:
            continue
        entries = tag_data.get("units", {}).get(unit, [])
        for entry in entries:
            end_year = int(entry.get("end", "0000")[:4])
            if entry.get("fy") == fy and entry.get("fp") == fp and end_year == fy:
                return entry.get("val")

    return None
