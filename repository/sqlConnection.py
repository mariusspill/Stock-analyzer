import mysql.connector as sqlc
from dotenv import load_dotenv
import os

load_dotenv()
SQL_PASSWORD = os.getenv("SQL_CONNECTION_PW")

connection = sqlc.connect(
    user = "root",
    host = "localhost",
    database = "stockdb",
    passwd = SQL_PASSWORD
)

cursor = connection.cursor()
