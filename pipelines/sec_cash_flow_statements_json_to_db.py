import repository.companies_repository as companies
import repository.cash_flow_statements_repository as cash_flows
import storage.sec_fundamentals_cache as sfc
import logging
import pipelines.xbrl_utils as xbrl

logger = logging.getLogger(__name__)

def get_financial_number(facts: dict, number: str, year: int, type: str = "annual", quarter: int = None):
    unit = "USD"
    if number == "operating_cash_flow":
        prioList = ["NetCashProvidedByUsedInOperatingActivities", "NetCashProvidedByUsedInOperatingActivitiesContinuingOperations"]
    elif number == "capital_expenditures":
        prioList = ["PaymentsToAcquirePropertyPlantAndEquipment", "PaymentsForProceedsFromProductiveAssets"]
    elif number == "investing_cash_flow":
        prioList = ["NetCashProvidedByUsedInInvestingActivities", "NetCashProvidedByUsedInInvestingActivitiesContinuingOperations"]
    elif number == "financing_cash_flow":
        prioList = ["NetCashProvidedByUsedInFinancingActivities", "NetCashProvidedByUsedInFinancingActivitiesContinuingOperations"]
    elif number == "dividends_paid":
        prioList = ["PaymentsOfDividendsCommonStock", "PaymentsOfDividends"]
    elif number == "depreciation_amortization":
        prioList = ["DepreciationDepletionAndAmortization", "DepreciationAmortizationAndAccretionNet"]
    elif number == "depreciation":
        prioList = ["Depreciation"]
    elif number == "amortization":
        prioList = ["AmortizationOfIntangibleAssets"]

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

    data['operating_cash_flow'] = get_financial_number(facts, "operating_cash_flow", year, type, quarter)
    data['capital_expenditures'] = get_financial_number(facts, "capital_expenditures", year, type, quarter)
    data['investing_cash_flow'] = get_financial_number(facts, "investing_cash_flow", year, type, quarter)
    data['financing_cash_flow'] = get_financial_number(facts, "financing_cash_flow", year, type, quarter)
    data['dividends_paid'] = get_financial_number(facts, "dividends_paid", year, type, quarter)
    data['depreciation_amortization'] = get_financial_number(facts, "depreciation_amortization", year, type, quarter)

    if data['depreciation_amortization'] is None:
        dep = get_financial_number(facts, "depreciation", year, type, quarter)
        amort = get_financial_number(facts, "amortization", year, type, quarter)
        if dep is not None and amort is not None:
            data['depreciation_amortization'] = dep + amort
    
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
            if not (data['operating_cash_flow'] is None and data['investing_cash_flow'] is None): 
                try:
                    if cash_flows.exists(company_id, year, type):
                        if update:
                            cash_flows.update_entry_cash_flow_statement(data, company_id, year, type)
                            logger.info(f"{company_id}, {year} updated")
                        else:
                            logger.info(f"{company_id}, {year} skipped")
                    else:
                        cash_flows.add_entry_cash_flow_statement(data, company_id, year, type)
                        logger.info(f"{company_id}, {year} created")
                except Exception as e:
                    logger.error(f"{company_id}, {year} failed: {e}")

            for quarter in range(1, 5):
                type = "quarter"
                data = get_one_statement(facts, year, type, quarter)
                if data['operating_cash_flow'] is None and data['investing_cash_flow'] is None: continue
                try:
                    if cash_flows.exists(company_id, year, type, quarter):
                        if update:
                            cash_flows.update_entry_cash_flow_statement(data, company_id, year, type, quarter)
                            logger.info(f"{company_id}, {year}, {quarter} updated")
                        else:
                            logger.info(f"{company_id}, {year}, {quarter} skipped")
                    else:
                        cash_flows.add_entry_cash_flow_statement(data, company_id, year, type, quarter)
                        logger.info(f"{company_id}, {year}, {quarter} created")
                except Exception as e:
                    logger.error(f"{company_id}, {year}, {quarter} failed: {e}")
