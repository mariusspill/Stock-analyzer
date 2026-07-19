import repository.sqlConnection as db

def exists(company_id: int, year: int, type:str, quarter: str = None):
    """Checks if a statement exists for a given year and returns its checked state."""
    sql = "SELECT checked FROM income_statements WHERE company_id = %s AND year = %s AND type = %s AND quarter <=> %s;"
    db.cursor.execute(sql, (company_id, year, type, quarter))
    return db.cursor.fetchone() # Returns (checked,) or None

def add_entry_income_statement(data: dict,
        company_id: int, year: int, type: str, quarter: str = None,
        ):
    
    """
    Inserts a new record.
    """
    sql = """INSERT INTO income_statements (company_id, year ,type, quarter, revenue, gross_profit,
                   operating_income, net_income, EBIT, EBITDA, cost_of_revenue, operating_expense, interest_cost, taxes,
                   pretax_income, eps_diluted, weighted_avg_diluted_shares) VALUES 
                   (%s,%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s) """
    
    params = (
        company_id,
        year,
        type,
        quarter,
        data['revenue'],
        data['gross_profit'],   
        data['operating_income'],
        data['net_income'],
        data['EBIT'],
        data['EBITDA'],
        data['cost_of_revenue'],
        data['operating_expense'],
        data['interest_cost'],
        data['taxes'],
        data['pretax_income'], 
        data['eps_diluted'], 
        data['weighted_avg_diluted_shares']
    )

    db.cursor.execute(sql, params)
    db.connection.commit()


def get_income_statements(company_id: int):
    db.connection.commit()
    sql = """
            SELECT * FROM income_statements WHERE company_id = %s;
        """
    
    db.cursor.execute(sql, (company_id,))

    return db.cursor.fetchall()