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
- **Priority is multi-machine database sync** (2026-09-15). The user will be
  travelling with limited access to the desktop. The database must move between
  machines the way code does, so that work done on a laptop is not lost and
  there is never more than one dataset. A laptop cannot host the 13 GB lake, so
  the database has to carry everything that matters.
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
- **Database migrated into Docker.** The native MySQL on :3306 was exported,
  restored into the container on :3307, and verified: 200,122 / 197,892 /
  197,513 rows in the three statement tables, 8,027 companies, 10,442
  securities, and all 82 `checked = 1` rows intact — counts identical on both
  sides. `alembic current` reports head, so there is no migration drift. `.env`
  now points at the container and host-side code reaches it. Retiring the native
  service is #2 and still open.

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

In priority order:

1. **#8** — how the database dump travels between machines. This is the point of
   the whole exercise; everything else is subordinate to it. **Blocked on an
   unresolved design question, below.**
2. **#11** — load parquet prices into `daily_ohlc`. Reclassified as a
   prerequisite, not a nice-to-have: prices exist only in the lake, the lake does
   not travel, so without this a second machine has no price data at all.
3. **#2** — finish retiring the native MySQL (`.env` is already switched; what
   remains is stopping the Windows service and confirming nothing breaks).
4. **#5–#7** — the universe work. Lower priority now; it scopes *cache warming*,
   which matters less once the database carries everything.

### Open design question blocking #8

"The database travels like git" breaks down the moment two machines both write.
A SQL dump is an opaque blob — git cannot merge two divergent databases, so if
pipelines run on the laptop *and* the desktop, one side's work is silently lost.
That is precisely the outcome the priority above exists to prevent, so it has to
be answered before building the sync.

Three shapes, not yet decided:

- **Single-writer discipline.** Dump-sync as planned, plus a rule that only one
  machine ingests at a time. Free and simple; enforced by humans, so it will
  eventually be violated.
- **One hosted database both machines connect to.** No sync, no dumps, no
  conflicts — `SQL_HOST` already makes this a config change rather than a code
  change. Costs money and needs network access while travelling.
- **Append-only reconciliation.** Merge by re-deriving rather than replacing.
  Most robust, by far the most work, and the `checked = 1` rows complicate it.

## Revisit later

Not issues yet, deliberately — see `ARCHITECTURE.md` for the longer-form ones.

- The two DB access styles (raw connector vs SQLAlchemy) should converge
  eventually. Not urgent; no behaviour depends on the split.
- `main.py` orchestrates by commented-out lines. Fine until there is a scheduler.
- 21 lint findings remain in `pipelines/` (star imports, `== None`). Fixing them
  means touching pipeline logic, so it wants its own pass.
