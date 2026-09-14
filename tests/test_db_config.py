"""The connection settings are the whole reason this project was machine-bound,
so they are worth pinning down: defaults must be sane, and every setting must be
overridable from the environment alone."""

import importlib

import pytest

import repository.db_config as db_config


def reload_with(monkeypatch, **env):
    for key in ("SQL_HOST", "SQL_PORT", "SQL_USER", "SQL_DATABASE", "SQL_CONNECTION_PW"):
        monkeypatch.delenv(key, raising=False)
    for key, value in env.items():
        monkeypatch.setenv(key, value)
    # Reloading re-runs `from dotenv import load_dotenv`, so the patch has to
    # land on the dotenv module itself. Without it, load_dotenv would refill the
    # variables this helper just deleted from a developer's real .env file.
    monkeypatch.setattr("dotenv.load_dotenv", lambda *a, **k: None)
    return importlib.reload(db_config)


def test_defaults_point_at_a_local_database(monkeypatch):
    config = reload_with(monkeypatch)
    assert (config.HOST, config.PORT, config.USER, config.DATABASE) == (
        "localhost",
        3306,
        "root",
        "stockdb",
    )


def test_every_setting_comes_from_the_environment(monkeypatch):
    config = reload_with(
        monkeypatch,
        SQL_HOST="db",
        SQL_PORT="3307",
        SQL_USER="screener",
        SQL_DATABASE="other",
        SQL_CONNECTION_PW="secret",
    )
    assert config.connector_kwargs() == {
        "host": "db",
        "port": 3307,
        "user": "screener",
        "password": "secret",
        "database": "other",
    }


def test_missing_password_names_the_fix(monkeypatch):
    config = reload_with(monkeypatch)
    with pytest.raises(RuntimeError, match=r"\.env\.example"):
        config.connector_kwargs()


def test_describe_never_leaks_the_password(monkeypatch):
    config = reload_with(monkeypatch, SQL_CONNECTION_PW="hunter2")
    assert "hunter2" not in config.describe()
