"""
Module to access specific keynumbers from database like net income
"""

import databases.sqlConnection as sql

def get_net_income(ticker: int, year: int):
    """
    Returns net_income for company for specified year
    """
    sql.cursor.execute(f"""SELECT company.id, company_identifiers.ticker, income_statements.net_income
                   FROM Company INNER JOIN Company_Identifiers ON Company.id = Company_Identifiers.company_id
                   INNER JOIN income_statements ON company.id = income_statements.company_id
                   WHERE company_identifiers.ticker = '{ticker}' AND income_statements.year = {year};""")
    data = sql.cursor.fetchall()
    try:
        return data[0][2]
    except:
        return 0
