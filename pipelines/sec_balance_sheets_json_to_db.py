import repository.companies_repository as companies
import repository.balance_sheets_repository as balances
import storage.sec_fundamentals_cache as sfc
import logging
import pipelines.xbrl_utils as xbrl

logger = logging.getLogger(__name__)

def get_financial_number(facts: dict, number: str, year: int, type: str = "annual", quarter: int = None):
    unit = "USD"
    if number == "total_assets":
        prioList = ["Assets"]
    elif number == "total_current_assets":
        prioList = ["AssetsCurrent"]
    elif number == "cash":
        prioList = ["CashAndCashEquivalentsAtCarryingValue", "CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents", "Cash"]
    elif number == "receivables":
        prioList = ["AccountsReceivableNetCurrent", "AccountsAndOtherReceivablesNetCurrent"]
    elif number == "inventories":
        prioList = ["InventoryNet"]
    elif number == "ppn":
        prioList = ["PropertyPlantAndEquipmentNet", "PropertyPlantAndEquipmentAndFinanceLeaseRightOfUseAssetAfterAccumulatedDepreciationAndAmortization"]
    elif number == "intangibles":
        prioList = ["IntangibleAssetsNetExcludingGoodwill", "FiniteLivedIntangibleAssetsNet"]
    elif number == "total_liabilities_equity":
        prioList = ["LiabilitiesAndStockholdersEquity"]
    elif number == "short_debt":
        prioList = ["DebtCurrent", "ShortTermBorrowings", "LongTermDebtCurrent"]
    elif number == "long_debt":
        prioList = ["LongTermDebtNoncurrent", "LongTermDebt"]
    elif number == "total_liabilities":
        prioList = ["Liabilities"]
    elif number == "total_equity":
        prioList = ["StockholdersEquity", "StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest"]
    elif number == "retained_earnings":
        prioList = ["RetainedEarningsAccumulatedDeficit"]
    elif number == "total_shares":
        prioList = ["CommonStockSharesIssued"]
        unit = "shares"
    elif number == "treasury_shares":
        prioList = ["TreasuryStockShares", "TreasuryStockCommonShares"]
        unit = "shares"
    elif number == "shares_outstanding":
        prioList = ["CommonStockSharesOutstanding"]
        unit = "shares"
    elif number == "total_current_liabilities":
        prioList = ["LiabilitiesCurrent"]
    elif number == "goodwill":
        prioList = ["Goodwill"]
    
    if type == "annual":
        fp = "FY"
    elif type == "quarter":
        if quarter == 1:
            fp = "Q1"
        elif quarter == 2:
            fp = "Q2"
        elif quarter == 3:
            fp = "Q3"
        elif quarter == 4:
            fp = "Q4"

    return xbrl.get_tag_value(facts, prioList , fy=year, fp=fp, unit=unit)

def get_one_statement(facts: dict, year: int, type: str, quarter: str = None):
    data = dict()

    data['total_assets'] = get_financial_number(facts, "total_assets", year, type, quarter)
    data['total_current_assets'] = get_financial_number(facts, "total_current_assets", year, type, quarter)
    data['cash'] = get_financial_number(facts, "cash", year, type, quarter)
    data['receivables'] = get_financial_number(facts, "receivables", year, type, quarter)
    data['inventories'] = get_financial_number(facts, "inventories", year, type, quarter)
    data['ppn'] = get_financial_number(facts, "ppn", year, type, quarter)
    data['intangibles'] = get_financial_number(facts, "intangibles", year, type, quarter)
    data['total_liabilities_equity'] = get_financial_number(facts, "total_liabilities_equity", year, type, quarter)
    data['short_debt'] = get_financial_number(facts, "short_debt", year, type, quarter)
    data['long_debt'] = get_financial_number(facts, "long_debt", year, type, quarter)
    data['total_liabilities'] = get_financial_number(facts, "total_liabilities", year, type, quarter)
    data['total_equity'] = get_financial_number(facts, "total_equity", year, type, quarter)
    data['retained_earnings'] = get_financial_number(facts, "retained_earnings", year, type, quarter)
    data['total_shares'] = get_financial_number(facts, "total_shares", year, type, quarter)
    data['treasury_shares'] = get_financial_number(facts, "treasury_shares", year, type, quarter)
    data['shares_outstanding'] = get_financial_number(facts, "shares_outstanding", year, type, quarter)
    data['total_current_liabilities'] = get_financial_number(facts, "total_current_liabilities", year, type, quarter)
    data['goodwill'] = get_financial_number(facts, "goodwill", year, type, quarter)


    if data['short_debt'] is not None and data['long_debt'] is not None:
        data['total_debt'] = data['short_debt'] + data['long_debt']
    else:
        data['total_debt'] = None

    return data

def pipeline(full=True, update=True):
    companies_list = companies.get_all_companies()

    for company in companies_list:
        company_id = company[0]

        cik = company[2]

        if cik == None:
            continue
        
        facts = sfc.read_json_fundamental_raw(cik, "fundamentals")

        if full:
            start = 2007
        else:
            start = 2025

        for year in range(start, 2027):
            type = "annual"
            data = get_one_statement(facts, year, type)
            if not (data['total_assets'] is None and data['total_liabilities'] is None): 
                try:
                    if balances.exists(company_id, year, type):
                        if update:
                            balances.update_entry_balance_sheets(data, company_id, year, type)
                            logger.info(f"{company_id}, {year} updated")
                        else:
                            logger.info(f"{company_id}, {year} skipped")
                    else:
                        balances.add_entry_balance_sheets(data, company_id, year, type)
                        logger.info(f"{company_id}, {year} created")
                except Exception as e:
                    logger.error(f"{company_id}, {year} failed: {e}")

            for quarter in range(1, 5):
                type = "quarter"
                data = get_one_statement(facts, year, type, quarter)
                if data['total_assets'] is None and data['total_liabilities'] is None: continue
                try:
                    if balances.exists(company_id, year, type, quarter):
                        if update:
                            balances.update_entry_balance_sheets(data, company_id, year, type, quarter)
                            logger.info(f"{company_id}, {year}, {quarter} updated")
                        else:
                            logger.info(f"{company_id}, {year}, {quarter} skipped")
                    else:
                        balances.add_entry_balance_sheets(data, company_id, year, type, quarter)
                        logger.info(f"{company_id}, {year}, {quarter} created")
                except Exception as e:
                    logger.error(f"{company_id}, {year}, {quarter} failed: {e}")
