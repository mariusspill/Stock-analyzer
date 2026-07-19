import repository.sqlConnection as db

def add(name: str, cik: str):
    """
    Add a new entry to abstract company database table
    name: Field for long name of company
    """
    db.cursor.execute(f"INSERT INTO companies (name, cik) VALUES (%s, %s);", (name, cik))
    db.connection.commit()
    return db.cursor.lastrowid


def update_cik(company_id: int, cik: str):
    db.cursor.execute("UPDATE companies SET cik = %s WHERE id = %s;", (cik, company_id))
    db.connection.commit()


def get_id_by_cik(cik: str):
    db.cursor.execute("SELECT id FROM companies WHERE cik = %s;", (cik,))
    result = db.cursor.fetchone()
    return result[0] if result else None


def get_companies(company_id: int):
    db.connection.commit()
    
    sql = """
            SELECT * FROM companies WHERE id = %s;
        """
    
    db.cursor.execute(sql, (company_id,))

    return db.cursor.fetchall()


def get_all_companies():
    db.connection.commit()

    sql = """
        SELECT * FROM companies;
"""

    db.cursor.execute(sql,)

    return db.cursor.fetchall()