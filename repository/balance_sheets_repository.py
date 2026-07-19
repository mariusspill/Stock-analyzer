import repository.sqlConnection as db

def exists(company_id: int, year: int, type: str, quarter: str = None):
    """Checks if a balance sheet exists for a given period and returns its checked state."""
    sql = "SELECT checked FROM balance_sheets WHERE company_id = %s AND year = %s AND type = %s AND quarter <=> %s;"
    db.cursor.execute(sql, (company_id, year, type, quarter))
    return db.cursor.fetchone()

def add_entry_balance_sheets(data: dict, company_id: int, year: int, type: str, quarter: str = None):
    """
    Add a new entry to balance_sheets database table
    """

    sql = """INSERT INTO balance_sheets (company_id, year, type, quarter, total_assets, total_current_assets, cash, receivables, 
                inventories, properties_plant_equipment, intangible_assets, total_liabilities_and_equity, 
                short_debt, long_debt, total_debt, total_liabilities, total_equity, retained_earnings, 
                total_shares, treasury_shares, shares_outstanding, total_current_liabilities, goodwill) VALUES 
                (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    
    params = (
        company_id,
        year,
        type,
        quarter,
        data['total_assets'],
        data['total_current_assets'],
        data['cash'],
        data['receivables'],
        data['inventories'],
        data['ppn'],
        data['intangibles'],
        data['total_liabilities_equity'],
        data['short_debt'],
        data['long_debt'],
        data['total_debt'],
        data['total_liabilities'],
        data['total_equity'],
        data['retained_earnings'],
        data['total_shares'],
        data['treasury_shares'],
        data['shares_outstanding'],
        data['total_current_liabilities'],
        data['goodwill']
    )
    db.cursor.execute(sql, params)
    db.connection.commit()


def update_entry_balance_sheets(data: dict, company_id: int, year: int, type: str, quarter: str = None):
    """
    Updates an existing balance sheet record with fresh data. Only call this when checked = 0.
    """
    sql = """UPDATE balance_sheets SET total_assets = %s, total_current_assets = %s, cash = %s, receivables = %s,
                inventories = %s, properties_plant_equipment = %s, intangible_assets = %s, total_liabilities_and_equity = %s,
                short_debt = %s, long_debt = %s, total_debt = %s, total_liabilities = %s, total_equity = %s,
                retained_earnings = %s, total_shares = %s, treasury_shares = %s, shares_outstanding = %s,
                total_current_liabilities = %s, goodwill = %s
             WHERE company_id = %s AND year = %s AND type = %s AND quarter <=> %s AND checked != 1"""

    params = (
        data['total_assets'], data['total_current_assets'], data['cash'], data['receivables'],
        data['inventories'], data['ppn'], data['intangibles'], data['total_liabilities_equity'],
        data['short_debt'], data['long_debt'], data['total_debt'], data['total_liabilities'],
        data['total_equity'], data['retained_earnings'], data['total_shares'],
        data['treasury_shares'], data['shares_outstanding'],
        data['total_current_liabilities'], data['goodwill'],
        company_id, year, type, quarter
    )

    db.cursor.execute(sql, params)
    db.connection.commit()

def get_balance_sheets(company_id: int):
    db.connection.commit()

    sql = """
            SELECT * FROM balance_sheets WHERE company_id = %s;
        """
    
    db.cursor.execute(sql, (company_id,))

    return db.cursor.fetchall()