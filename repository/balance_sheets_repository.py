import sqlConnection as db

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
    db.cursor.execute(sql, params)
    db.connection.commit()