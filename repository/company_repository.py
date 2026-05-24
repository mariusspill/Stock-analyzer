import sqlConnection as db

def add(name: str):
    """
    Add a new entry to abstract company database table
    name: Field for long name of company
    """
    db.cursor.execute(f"INSERT INTO company (name) VALUES (%s);", (name,))
    db.connection.commit()
