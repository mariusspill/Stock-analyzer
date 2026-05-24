"""
Module to store and retrieve data from DB
"""

import mysql.connector as sqlc
import apis.alphavantagedata as dt
import yfinance as yf
import pandas as pd

pd.set_option('display.max_rows', None)



connection = sqlc.connect(
    user = "root",
    host = "localhost",
    database = "stockdb",
    passwd = "OpenPassword123"
)

cursor = connection.cursor()

def add_entry_company(name: str):
    """
    Add a new entry to abstract company database table
    name: Field for long name of company
    """
    cursor.execute(f"INSERT INTO company (name) VALUES (%s);", (name,))
    connection.commit()


def add_entry_company_identifiers(id: int, ticker: str, isin: str, wkn: str):
    """
    Add a new entry to company_identifier database table
    id: company_id from abstract table, isin: isin, wkn: german Wertpapierkennnummer
    """
    cursor.execute(f"INSERT INTO company_identifiers (company_id, ticker, isin, wkn) VALUES ({id}, '{ticker}', '{isin}', '{wkn}');")
    connection.commit()


def add_entry_balance_sheets(company_id: int, year: int, type: str, total_assets: int = None, total_current_assets: int = None, cash: int = None, receivables: int = None,
                             inventories: int = None, ppn: int = None, intangibles: int = None, total_liabilities_equity: int = None, short_debt: int = None, long_debt: int = None,
                             total_debt: int = None, total_liabilities: int = None, total_equity: int = None, retained_earnings: int = None, total_shares: int = None,
                             treasury_shares: int = None, shares_outstanding: int = None):
    """
    Add a new entry to balance_sheets database table
    """

    sql = """INSERT INTO balance_sheets (company_id, year, type, total_assets, total_current_assets, cash, receivables, 
                inventories, properties_plant_equipment, intangible_assets, total_liabilities_and_equity, 
                short_debt, long_debt, total_debt, total_liabilities, total_equity, retained_earnings, 
                total_shares, treasury_shares, shares_outstanding) VALUES 
                (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    
    params = (
        company_id,
        year,
        type,
        total_assets,
        total_current_assets,
        cash,
        receivables,
        inventories,
        ppn,
        intangibles,
        total_liabilities_equity,
        short_debt,
        long_debt,
        total_debt,
        total_liabilities,
        total_equity,
        retained_earnings,
        total_shares,
        treasury_shares,
        shares_outstanding
    )
    cursor.execute(sql, params)
    connection.commit()


def add_entry_income_statement(company_id: int, year: int, revenue: int = None, gross_profit:int = None, 
                               operating_income: int = None, net_income: int = None, EBIT: int = None, EBITDA: int = None,
                               cost_of_revenue:int = None, operating_expense: int = None, interest_cost: int = None, taxes: int = None):
    """
    Add a new entry to income_statements database table
    """
    sql = """INSERT INTO income_statements (company_id, year, revenue, gross_profit,
                   operating_income, net_income, EBIT, EBITDA, cost_of_revenue, operating_expense, interest_cost, taxes) VALUES 
                   (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    
    params = (
        company_id,
        year,
        revenue,
        gross_profit,
        operating_income,
        net_income,
        EBIT,
        EBITDA,
        cost_of_revenue,
        operating_expense,
        interest_cost,
        taxes
    )

    cursor.execute(sql, params)
    connection.commit()


def update_entry_income_statement(id: int, column: str, value: int):
    """
    Updates entry in income_statements database table
    """
    cursor.execute(f"UPDATE income_statements SET {column} = {value} WHERE id = {id};")
    connection.commit()


def get_data_identifiers():
    """
    Returns my id and other identifiers for all companies in db
    """
    cursor.execute(f"""SELECT Company.id,
                    Company.name, 
                    Company_Identifiers.ticker, 
                    Company_Identifiers.isin, 
                    Company_Identifiers.wkn 
                    FROM Company JOIN Company_Identifiers ON Company.id = Company_Identifiers.company_id;""")
    return cursor.fetchall()


def get_id_by_ticker(ticker: int):
    """
    Returns my id for specified company
    """
    cursor.execute(f"""SELECT Company.id,
                    Company_Identifiers.ticker
                    FROM Company JOIN Company_Identifiers ON Company.id = Company_Identifiers.company_id
                    WHERE Company_Identifiers.ticker = '{ticker}';""")
    try:
        return cursor.fetchall()[0][0]
    except:
        return "No data for company"
    

def automate_data_insertion_balance_sheet(ticker: str, year: int = 2024):
    company_id = get_id_by_ticker(ticker)

    if isinstance(company_id, int) and ticker is not None:
        cursor.execute(f"""SELECT company.id, company_identifiers.ticker, balance_sheets.*
                    FROM Company INNER JOIN Company_Identifiers ON Company.id = Company_Identifiers.company_id
                    INNER JOIN balance_sheets ON company.id = balance_sheets.company_id
                    WHERE company_identifiers.ticker = '{ticker}' AND balance_sheets.year = {year};""")
        data = cursor.fetchall()

        balance_sheet = yf.Ticker(ticker).balancesheet.iloc[:, 0]
        year = int(str(balance_sheet.name)[:4])
        print(balance_sheet)

        if data == []:
            print("I would insert")
            """
            sql.add_entry_balance_sheets(
                company_id,
                year,
                "annual",
                4002814000000,
                2179723000000,
                23372000000,
                101223000000,
                0,
                32223000000,
                64560000000,
                4002814000000,
                52893000000,
                401418000000,
                454311000000,
                3658056000000,
                344758000000,
                376166000000,
                4104933895,
                1307313494,
                2797620401
            )
            """
        else:
            if data[0][21] == 1:
                print("record checked handly")
            else:
                print("update possible")



def automate_data_insertion(ticker: str):
    """
    Datapipeline for income_statements table: alphavantaga raw json -> database
    """
    # does this entry exist:
    company_id = get_id_by_ticker(ticker)

    if isinstance(company_id, int) and ticker is not None:

        years = dt.get_years_covered(ticker)

        print(ticker)

        for year in years:
            try:
                revenue = dt.get_revenue(ticker, year)
                net_income = dt.get_netIncome(ticker, year)
                gross_profit = dt.get_gross_profit(ticker, year)
                taxes = dt.get_taxes_paid(ticker, year)
                interest = dt.get_interest_paid(ticker, year)

                if revenue == None:
                    revenue = 0

                cost_of_revenue = int(revenue) - int(gross_profit)

                if not "None" in net_income:
                    net_income = int(net_income)
                else:
                    net_income = 0

                if not "None" in interest:
                    interest = int(interest)
                else:
                    interest = 0

                if not "None" in taxes:
                    taxes = int(taxes)
                else:
                    taxes = 0

                ebit = int(net_income) + int(taxes) + int(interest)


                da = dt.get_depreciation_and_amortization(ticker, year)
                if not "None" in da:
                    ebitda = ebit + int(da)
                else:
                    ebitda = ebit
                operating_income = dt.get_operating_income(ticker, year)
                operating_expenses = dt.get_operating_expenses(ticker, year)

                cursor.execute(f"""SELECT company.id, company_identifiers.ticker, income_statements.*
                            FROM Company INNER JOIN Company_Identifiers ON Company.id = Company_Identifiers.company_id
                            INNER JOIN income_statements ON company.id = income_statements.company_id
                            WHERE company_identifiers.ticker = '{ticker}' AND income_statements.year = {year};""")
                data = cursor.fetchall()

                if data == []:
                    add_entry_income_statement(company_id, year, revenue, gross_profit, net_income=net_income, EBIT=ebit, EBITDA=ebitda, cost_of_revenue=cost_of_revenue, interest_cost=interest, taxes=taxes)
                else:
                    if data[0][15] == 1:
                        print("record checked handly")
                    else:
                        print("update possible")
            except:
                continue

    else:
        print("no company data for ", ticker)


def fetch_sp500_from_alpha_advantage():
    """
    automated pipeline for all s&p500 companies
    """
    tickers = dt.get_sp500_tickers()

    for ticker in tickers:
        if "CDW" in ticker:
            continue
        if "DXCM" in ticker:
            continue
        automate_data_insertion(ticker)