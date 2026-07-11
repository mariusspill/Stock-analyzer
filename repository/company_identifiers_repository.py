import repository.sqlConnection as db

def add_entry_company_identifiers(id: int, ticker: str, isin: str, wkn: str):
    """
    Add a new entry to company_identifier database table
    id: company_id from abstract table, isin: isin, wkn: german Wertpapierkennnummer
    """
    sql = """INSERT INTO company_identifiers (company_id, ticker, isin, wkn) VALUES (%s, %s, %s, %s);"""

    db.cursor.execute(sql, (id, ticker, isin, wkn))
    db.connection.commit()

def get_id_by_ticker(ticker: str):
    """
    Looks up the company_identifiers table to translate a public 
    string ticker into your internal relational integer company_id.
    """
    sql = "SELECT company_id FROM company_identifiers WHERE ticker = %s;"
    db.cursor.execute(sql, (ticker,))
    result = db.cursor.fetchone()
    
    # Returns the integer (e.g. 14) or None if the stock isn't registered yet
    return result[0] if result else None

def get_company_identifiers(company_id: int):
    sql = """
            SELECT * FROM company_identifiers WHERE company_id = %s;
        """
    
    db.cursor.execute(sql, (company_id,))

    return db.cursor.fetchall()