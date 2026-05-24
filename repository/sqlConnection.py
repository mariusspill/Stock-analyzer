import mysql.connector as sqlc

connection = sqlc.connect(
    user = "root",
    host = "localhost",
    database = "stockdb",
    passwd = "OpenPassword123"
)

cursor = connection.cursor()
