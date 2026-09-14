"""Importing a repository module must not require a database.

This is what lets the app container start before MySQL is ready, and what makes
the code importable in tests and CI at all."""

import importlib


def test_repositories_import_without_a_database(monkeypatch):
    monkeypatch.delenv("SQL_CONNECTION_PW", raising=False)
    for module in (
        "repository.companies_repository",
        "repository.securities_repository",
        "repository.income_statements_repository",
        "repository.balance_sheets_repository",
        "repository.cash_flow_statements_repository",
        "repository.daily_ohlc_repository",
        "repository.dividends_repository",
        "repository.stock_splits_repository",
    ):
        importlib.import_module(module)


def test_unknown_attribute_still_raises_attribute_error():
    import repository.sqlConnection as db

    for name in ("nope", "cursors"):
        try:
            getattr(db, name)
        except AttributeError:
            continue
        raise AssertionError(f"{name} should not resolve")
