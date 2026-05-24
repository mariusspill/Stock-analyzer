import sqlConnection as db

def add_entry_company_identifiers(id: int, ticker: str, isin: str, wkn: str):
    """
    Add a new entry to company_identifier database table
    id: company_id from abstract table, isin: isin, wkn: german Wertpapierkennnummer
    """
    db.cursor.execute(f"INSERT INTO company_identifiers (company_id, ticker, isin, wkn) VALUES ({id}, '{ticker}', '{isin}', '{wkn}');")
    db.connection.commit()