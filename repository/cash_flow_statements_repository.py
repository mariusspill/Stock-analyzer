import repository.sqlConnection as db


import repository.sqlConnection as db

def exists(company_id: int, year: int, type:str, quarter: str = None):
    """Checks if a statement exists for a given year and returns its checked state."""
    sql = "SELECT checked FROM cash_flow_statements WHERE company_id = %s AND year = %s AND type = %s AND quarter <=> %s;"
    db.cursor.execute(sql, (company_id, year, type, quarter))
    return db.cursor.fetchone() # Returns (checked,) or None

def add_entry_cash_flow_statement(data: dict,
        company_id: int, year: int, type: str, quarter: str = None,
        ):
    
    """
    Inserts a new record.
    """
    sql = """INSERT INTO cash_flow_statements (company_id, year,type, quarter,
      operating_cash_flow, capital_expenditures, investing_cash_flow, financing_cash_flow, dividends_paid, depreciation_amortization)
       VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """
    
    params = (
        company_id, year, type, quarter,
        data['operating_cash_flow'], 
        data['capital_expenditures'], 
        data['investing_cash_flow'],
        data['financing_cash_flow'], 
        data['dividends_paid'], 
        data['depreciation_amortization']
    )

    db.cursor.execute(sql, params)
    db.connection.commit()


def update_entry_cash_flow_statement(data: dict, company_id: int, year: int, type: str, quarter: str = None):
    """
    Updates an existing cash flow statement record with fresh data. Only call this when checked = 0.
    """
    sql = """UPDATE cash_flow_statements SET operating_cash_flow = %s, capital_expenditures = %s,
                investing_cash_flow = %s, financing_cash_flow = %s, dividends_paid = %s, depreciation_amortization = %s
             WHERE company_id = %s AND year = %s AND type = %s AND quarter <=> %s AND checked != 1"""

    params = (
        data['operating_cash_flow'], data['capital_expenditures'], data['investing_cash_flow'],
        data['financing_cash_flow'], data['dividends_paid'], data['depreciation_amortization'],
        company_id, year, type, quarter
    )

    db.cursor.execute(sql, params)
    db.connection.commit()



def get_cash_flow_statements(company_id: int):
    db.connection.commit()
    sql = """
            SELECT * FROM cash_flow_statements WHERE company_id = %s;
        """
    
    db.cursor.execute(sql, (company_id,))

    return db.cursor.fetchall()