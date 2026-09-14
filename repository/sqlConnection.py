"""Raw mysql-connector access used by the older repository modules.

`connection` and `cursor` are created on first *use* rather than at import
time. Importing a repository module no longer requires a live database, which
is what lets the app container start before MySQL has finished booting, and
lets tests import this code with no database at all.

Call sites are unchanged: `db.cursor` and `db.connection` still work.
"""

import mysql.connector as sqlc

import repository.db_config as config

_connection = None
_cursor = None


def _connect():
    global _connection, _cursor
    if _connection is None:
        _connection = sqlc.connect(**config.connector_kwargs())
        _cursor = _connection.cursor()
    return _connection, _cursor


def __getattr__(name: str):
    """Resolve `connection` / `cursor` lazily on first attribute access."""
    if name not in ("connection", "cursor"):
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    connection, cursor = _connect()
    return connection if name == "connection" else cursor
