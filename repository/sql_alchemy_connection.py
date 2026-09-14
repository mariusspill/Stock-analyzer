"""SQLAlchemy access used by the newer price/dividend/split repositories.

`Base` is available immediately (the ORM classes subclass it at import time),
while `engine` and `Session` are built on first use, for the same reason
`sqlConnection` defers its connect: importing a repository must not require a
running database.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

import repository.db_config as config

Base = declarative_base()

_engine = None
_session_factory = None


def _build():
    global _engine, _session_factory
    if _engine is None:
        _engine = create_engine(config.sqlalchemy_url())
        _session_factory = sessionmaker(bind=_engine)
    return _engine, _session_factory


def __getattr__(name: str):
    """Resolve `engine` / `Session` lazily on first attribute access."""
    if name not in ("engine", "Session"):
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    engine, session_factory = _build()
    return engine if name == "engine" else session_factory
