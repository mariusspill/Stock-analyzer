import repository.company_repository as company
import repository.company_identifiers_repository  as company_identifier
import repository.income_statements_repository as income
import repository.balance_sheets_repository as balance

def pipeline():
    print(income.exists(company_identifier.get_id_by_ticker("IBM"), 2025))