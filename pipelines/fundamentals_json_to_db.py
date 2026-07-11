import repository.company_repository as company
import repository.company_identifiers_repository  as company_identifier
import repository.income_statements_repository as income
import repository.balance_sheets_repository as balance
import storage.local_cache as lc
import json
import logging

logger = logging.getLogger(__name__)

def pipeline(indices: list[str]):

    # Income statements pipeline
    for ticker in indices:
        comp_id = company_identifier.get_id_by_ticker(ticker)
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
                logger.info(f"add record for {ticker} {year}")
            else:
                logger.debug(f"record exists {ticker} {year}")
                

def testing():
    dic = lc.read_json_raw("IBM", "incomeStatement")
    record = dic[0]

    data = {
        'revenue': record["totalRevenue"],
        'gross_profit': 0,
        'operating_income': 0,
        'net_income': 0,
        'EBIT': 0,
        'EBITDA': 0,
        'cost_of_revenue': 0,
        'operating_expense': record["operatingExpenses"],
        'interest_cost': record["interestExpense"],
        'taxes': 0
    }

    print(record)


def test_repository():
    ticker = "MMM"
    year = 2025
    data = {
        'revenue':  24948000000,
        'gross_profit': 9868000000,
        'operating_income': 4563000000,
        'net_income': 3250000000,
        'EBIT': 4973000000,
        'EBITDA': 5851000000,
        'cost_of_revenue': 15080000000,
        'operating_expense': 3997000000,
        'interest_cost': -714000000,
        'taxes': 1003000000
    }

    income.add_entry_income_statement(company_identifier.get_id_by_ticker(ticker), year, data)