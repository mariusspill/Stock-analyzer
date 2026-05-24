import sqlConnection as db

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

    db.cursor.execute(sql, params)
    db.connection.commit()
