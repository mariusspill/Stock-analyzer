"""Single source of truth for how this project reaches MySQL.

Every consumer -- the raw mysql-connector layer, the SQLAlchemy layer and
Alembic's env.py -- reads its settings from here. A new machine therefore only
has to supply environment variables; nothing about the connection is baked into
the code. This is what lets the same checkout talk to a native MySQL on one
machine and a container on another.
"""

import os

from dotenv import load_dotenv
from sqlalchemy.engine import URL

load_dotenv()

HOST = os.getenv("SQL_HOST", "localhost")
PORT = int(os.getenv("SQL_PORT", "3306"))
USER = os.getenv("SQL_USER", "root")
DATABASE = os.getenv("SQL_DATABASE", "stockdb")


def password() -> str:
    """The DB password, or a clear error if the machine isn't configured yet."""
    value = os.getenv("SQL_CONNECTION_PW")
    if not value:
        raise RuntimeError(
            "SQL_CONNECTION_PW is not set. Copy .env.example to .env and fill it in."
        )
    return value


def connector_kwargs() -> dict:
    """Keyword arguments for `mysql.connector.connect()`."""
    return {
        "host": HOST,
        "port": PORT,
        "user": USER,
        "password": password(),
        "database": DATABASE,
    }


def sqlalchemy_url() -> URL:
    return URL.create(
        "mysql+mysqlconnector",
        username=USER,
        password=password(),
        host=HOST,
        port=PORT,
        database=DATABASE,
    )


def describe() -> str:
    """Connection target without the password -- safe to log."""
    return f"{USER}@{HOST}:{PORT}/{DATABASE}"
