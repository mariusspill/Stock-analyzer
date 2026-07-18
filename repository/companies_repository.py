import repository.sqlConnection as db

def add(name: str, cik: str):
    """
    Add a new entry to abstract company database table
    name: Field for long name of company
    """
    db.cursor.execute(f"INSERT INTO companies (name) VALUES (%s, %s);", (name, cik))
    db.connection.commit()


def get_companies(company_id: int):
    db.connection.commit()
    
    sql = """
            SELECT * FROM companies WHERE id = %s;
        """
    
    db.cursor.execute(sql, (company_id,))

    return db.cursor.fetchall()