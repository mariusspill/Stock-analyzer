import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

db_url = URL.create(
    "mysql+mysqlconnector",
    username="root",
    password=os.getenv("SQL_CONNECTION_PW"),
    host=os.getenv("SQL_HOST", "localhost"),
    database="stockdb",
)

engine = create_engine(db_url)
Session = sessionmaker(bind=engine)
Base = declarative_base()
