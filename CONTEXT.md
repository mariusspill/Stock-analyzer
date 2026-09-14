# Context

Rolling state of the project. Read this first; `ARCHITECTURE.md` explains *why*
the data model and pipelines look the way they do, and does not need updating
as often.

## Project Overview

A personal value-investing stock screener and data platform. SEC EDGAR XBRL
filings and yfinance price history are ingested into MySQL through a chain of
explicit pipeline stages, with a Streamlit frontend on top. Built primarily as a
hands-on vehicle for learning real data-engineering practice.

Stack: Python 3.13 (`uv`), MySQL 8, Alembic migrations, no ORM on the older
tables (raw `mysql-connector-python`) and SQLAlchemy on the newer ones,
Streamlit, Docker Compose.

## Workflow Mode

learning

## Current Architecture & Module Status

| Area | Location | State |
| --- | --- | --- |
| Connection settings | `repository/db_config.py` | Single source of truth. Host, port, user, database and password all come from the environment. |
| Raw MySQL access | `repository/sqlConnection.py` | Connects lazily on first attribute access, not at import. |
| SQLAlchemy access | `repository/sql_alchemy_connection.py` | `Base` eager, `engine`/`Session` lazy. |
| Repositories | `repository/*_repository.py` | Two styles coexist: raw connector (companies, securities, the three statement tables) and SQLAlchemy ORM (daily_ohlc, dividends, stock_splits). Deliberately not unified yet. |
| Fundamentals pipelines | `pipelines/sec_*` | Working. SEC companyfacts -> JSON lake -> MySQL. |
| Price pipeline | `pipelines/history_api_to_parquet.py` | Fetches to parquet only. Nothing loads parquet into `daily_ohlc` yet. |
| Schema | `migrations/versions/` | 4 revisions; `env.py` reads its URL from `db_config`. |
| Orchestration | `main.py` | Manual: stages are commented in and out by hand. |

## Decisions in force

- **The database is the source of truth for ingested data** (2026-09-14). Dumps
  in `backups/` are how it moves between machines. Pipelines are not trusted to
  reproduce it, because the `checked=1` hand-verified rows cannot be regenerated
  by any pipeline.
- **The raw data lake is a cache, not an archive** (2026-09-15), and is not
  synced between machines. `storage/sec_fundamentals_cache.py` already deletes
  the previous snapshot when writing a new one, so it holds the latest response
  from a re-callable API rather than a record of what was filed when. It gets
  warmed on demand, scoped by universe.
- **A universe is declared, never discovered** (2026-09-15). It comes from a
  tracked ticker-list file selected by the `UNIVERSE` env var — never inferred
  from what is already on disk, since a pipeline that fetches only what it
  already has can never grow.
- **Planning lives in GitHub**, not in the repo. Milestones and issues are the
  source of truth for what is planned and in progress; this file holds rolling
  state; `ARCHITECTURE.md` holds coarse direction not yet ready to be an issue.

## Recent Changes

- **Portable environment.** Central `db_config` with `SQL_PORT` support, lazy
  connections so importing code no longer needs a live database, `.env.example`,
  healthchecked compose stack with a migration step that runs before the app,
  dump/restore scripts that never pass through a host shell, `pandas`/`pyarrow`
  promoted to declared dependencies, first tests, LF line endings and exec bits
  forced so scripts survive a Windows checkout into a Linux container.
- **Database migration into Docker (in progress).** Images build. The native
  MySQL on :3306 has been exported to a 21 MB gzipped dump — ASCII, all 9 tables
  in the current schema, `alembic_version` at head. Restore and row-count
  verification still outstanding.

## Build & Verification Commands

Docker is the only required local dependency.

```bash
cp .env.example .env          # then fill in SQL_CONNECTION_PW
uv lock                       # regenerate the lockfile after dependency changes
docker compose build

docker compose up -d db       # database only
docker compose up -d app      # runs migrations first, then Streamlit on :8502

./scripts/test.sh             # pytest, inside the container
./scripts/lint.sh             # ruff, inside the container

./scripts/db_dump.sh          # backups/stockdb_<timestamp>.sql.gz
./scripts/db_restore.sh       # restore newest dump (destructive, prompts)
./scripts/db_import_native.sh # one-time: native MySQL on :3306 -> container

docker compose run --rm pipeline python main.py
```

## Next Immediate Tasks

Tracked in [GitHub milestones](https://github.com/mariusspill/Stock-analyzer/milestones).
Currently in flight:

1. **#1** — restore `backups/native_import_*.sql.gz` and verify row counts, and
   especially `checked=1` counts, match the native database.
2. **#2** — point `.env` at the container (`SQL_HOST=localhost`,
   `SQL_PORT=3307`) and retire the native MySQL install.
3. **#5–#7** — the universe work, once the database migration is closed out.

## Revisit later

Not issues yet, deliberately — see `ARCHITECTURE.md` for the longer-form ones.

- The two DB access styles (raw connector vs SQLAlchemy) should converge
  eventually. Not urgent; no behaviour depends on the split.
- `main.py` orchestrates by commented-out lines. Fine until there is a scheduler.
- 21 lint findings remain in `pipelines/` (star imports, `== None`). Fixing them
  means touching pipeline logic, so it wants its own pass.
