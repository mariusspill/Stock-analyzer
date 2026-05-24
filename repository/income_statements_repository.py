import repository.sqlConnection as db

def exists(company_id: int, year: int):
    """Checks if a statement exists for a given year and returns its checked state."""
    sql = "SELECT checked FROM income_statements WHERE company_id = %s AND year = %s;"
    db.cursor.execute(sql, (company_id, year))
    return db.cursor.fetchone() # Returns (checked,) or None

def add_entry_income_statement(
        company_id: int, year: int, 
        data: dict):
    
    """
    Inserts a new record.
    """
    sql = """INSERT INTO income_statements (company_id, year, revenue, gross_profit,
                   operating_income, net_income, EBIT, EBITDA, cost_of_revenue, operating_expense, interest_cost, taxes) VALUES 
                   (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s) """
    
    params = (
        company_id,
        year,
        data['revenue'],
        data['gross_profit'],
        data['operating_income'],
        data['net_income'],
        data['EBIT'],
        data['EBITDA'],
        data['cost_of_revenue'],
        data['operating_expense'],
        data['interest_cost'],
        data['taxes']
    )

    db.cursor.execute(sql, params)
    db.connection.commit()
