import repository.companies_repository as companies
import repository.income_statements_repository as incomes
import storage.sec_fundamentals_cache as sfc
import logging
import pipelines.xbrl_utils as xbrl

logger = logging.getLogger(__name__)


def get_financial_number(company_id: int, number: str, year: int, type: str = "annual", quarter: int = None):
    unit = "USD"
    if number == "revenue":
        prioList = ["RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues", "SalesRevenueNet"]
    elif number == 'gross_profit':
        prioList = ["GrossProfit"]
    elif number == 'operating_income':
        prioList = ["OperatingIncomeLoss"]
    elif number == 'net_income':
        prioList = ["NetIncomeLoss", "ProfitLoss"]
    elif number == 'cost_of_revenue':
        prioList = ["CostOfRevenue", "CostOfGoodsAndServicesSold", "CostOfGoodsSold"]
    elif number == 'operating_expense':
        prioList = ["OperatingExpenses", "CostsAndExpenses"]
    elif number == 'interest_cost':
        prioList = ["InterestExpense"]
    elif number == 'taxes':
        prioList = ["IncomeTaxExpenseBenefit"]
    elif number == 'pretax_income':
        prioList = ["IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest",
                    "IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments"]
    elif number == 'eps_diluted':
        prioList = ["EarningsPerShareDiluted"]
        unit = "USD/shares"
    elif number == 'weighted_avg_diluted_shares':
        prioList = ["WeightedAverageNumberOfDilutedSharesOutstanding"]
        unit = "shares"
    elif number == 'Depreciation':
        prioList = ["Depreciation"]
    elif number == "Amortization":
        prioList = ["AmortizationOfIntangibleAssets"]
    elif number == 'sga':
        prioList = ["SellingGeneralAndAdministrativeExpense"]
    elif number == 'rd':
        prioList = ["ResearchAndDevelopmentExpense"]


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
    
    cik = companies.get_companies(company_id)[0][2]

    return xbrl.get_tag_value(sfc.read_json_fundamental_raw(cik, "fundamentals"), prioList , fy=year, fp=fp, unit=unit)



def get_one_statement(company_id: int, year: int, type: str, quarter: str = None):
    data = dict()
    data['revenue'] = get_financial_number(company_id, "revenue", year, type, quarter)
    data['gross_profit'] = get_financial_number(company_id, "gross_profit", year, type, quarter)
    data['operating_income'] = get_financial_number(company_id, "operating_income", year, type, quarter)
    data['net_income'] = get_financial_number(company_id, "net_income", year, type, quarter)
    data['cost_of_revenue'] = get_financial_number(company_id, "cost_of_revenue", year, type, quarter)
    data['operating_expense'] = get_financial_number(company_id, "operating_expense", year, type, quarter)
    data['interest_cost'] = get_financial_number(company_id, "interest_cost", year, type, quarter)
    data['taxes'] = get_financial_number(company_id, "taxes", year, type, quarter)
    data['pretax_income'] = get_financial_number(company_id, "pretax_income", year, type, quarter)
    data['eps_diluted'] = get_financial_number(company_id, "eps_diluted", year, type, quarter)
    data['weighted_avg_diluted_shares'] = get_financial_number(company_id, "weighted_avg_diluted_shares", year, type, quarter)

    if data['gross_profit'] is None and data['revenue'] is not None and data['cost_of_revenue'] is not None:
        data['gross_profit'] = data['revenue'] - data['cost_of_revenue']


    if data['net_income'] is not None and data['interest_cost'] is not None and data['taxes'] is not None:
        data['EBIT'] = data['net_income'] + data['interest_cost'] + data['taxes']
        dep = get_financial_number(company_id, "Depreciation", year, type, quarter)
        amort = get_financial_number(company_id, "Amortization", year, type, quarter)
        if dep is not None and amort is not None:
            data['EBITDA'] = data['EBIT'] + dep + amort
        else:
            data['EBITDA'] = None
    else:
        data['EBIT'] = None
        data['EBITDA'] = None

    sga = get_financial_number(company_id, "sga", year, type, quarter)
    rd = get_financial_number(company_id, "rd", year, type, quarter)
    if rd is None:
        rd = 0

    if sga is not None and data['gross_profit'] is not None:
        data['operating_expense'] = sga + rd
        data['operating_income'] = data['gross_profit'] - data['operating_expense']
    else:
        data['operating_expense'] = None
        data['operating_income'] = None

    return data

def pipeline():
    companies_list = companies.get_all_companies()

    for company in companies_list:
        company_id = company[0]

        cik = company[2]

        if cik == None:
            continue

        for year in range(2007, 2027):
            type = "annual"
            data = get_one_statement(company_id, year, type)
            if not (data['revenue'] is None and data['net_income'] is None): 
                if incomes.exists(company_id, year, type):
                    incomes.update_entry_income_statement(data, company_id, year, type)
                    logger.info(f"{company_id}, {year} updated")
                else:
                    incomes.add_entry_income_statement(data, company_id, year, type)
                    logger.info(f"{company_id}, {year} created")

            for quarter in range(1, 5):
                type = "quarter"
                data = get_one_statement(company_id, year, type, quarter)
                if data['revenue'] is None and data['net_income'] is None: continue
                if incomes.exists(company_id, year, type, quarter):
                    incomes.update_entry_income_statement(data, company_id, year, type, quarter)
                    logger.info(f"{company_id}, {year}, {quarter} updated")
                else:
                    incomes.add_entry_income_statement(data, company_id, year, type, quarter)
                    logger.info(f"{company_id}, {year}, {quarter} created")
