import repository.companies_repository as companies
import repository.securities_repository  as securities
import repository.income_statements_repository as income
import repository.balance_sheets_repository as balance
import storage.local_cache as lc
import json
import logging

logger = logging.getLogger(__name__)

def pipeline(indices: list[str]):

    # Income statements pipeline
    for ticker in indices:
        comp_id = securities.get_id_by_ticker(ticker)
        if comp_id is None:
            logger.warning(f"⚠️ {ticker} cannot be processed. Reason: Registry ID missing.")
            continue
        try:
            data = lc.read_json_raw(ticker, "incomeStatement")
        except json.JSONDecodeError:
            logger.warning(f"⚠️ {ticker} cannot be processed. Reason: read json failed")
            continue

        if data == {}:
            logger.warning(f"⚠️ {ticker} cannot be processed. Reason: data dict empty.")
            continue

        for record in data:
            year = int(record["fiscalDateEnding"][0:4])
            if income.exists(comp_id, year) == None:
                insert_data = {
                    'revenue': _to_int(record.get('totalRevenue')),
                    'gross_profit': _to_int(record.get('grossProfit')),
                    'operating_income': _to_int(record.get('operatingIncome')),
                    'net_income': _to_int(record.get('netIncome')),
                    'EBIT': _to_int(record.get('ebit')),
                    'EBITDA': _to_int(record.get('ebitda')),
                    'cost_of_revenue': _to_int(record.get('costOfRevenue')),
                    'operating_expense': _to_int(record.get('operatingExpenses')),
                    'interest_cost': _to_int(record.get('interestExpense')),
                    'taxes': _to_int(record.get('incomeTaxExpense'))
                }

                income.add_entry_income_statement(comp_id, year, insert_data)

                logger.info(f"add record for {ticker} {year}")
            else:
                logger.debug(f"record exists {ticker} {year}")
                
def _to_int(value):
    """AlphaVantage returns every number as a string, and 'None' (literally) when a company didn't report it."""
    if value in (None, "None"):
        return None
    return int(value)
