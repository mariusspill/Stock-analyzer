# Stock Data Platform

A personal, end-to-end data platform for value-investing stock screening — built primarily as a hands-on vehicle for learning real data-engineering practice: ETL pipeline design, schema modeling, data quality handling against messy real-world sources, and (eventually) orchestration and transformation tooling used in industry.

## What it does

Ingests company fundamentals directly from SEC EDGAR's XBRL filings (income statements, balance sheets, cash flow statements — annual and quarterly) into a MySQL database, with a Streamlit frontend for browsing and screening the results.

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for the full data model, pipeline chain, and the reasoning behind non-obvious design decisions (XBRL tag-priority mapping, derivation fallbacks, the `checked`-flag protection for hand-verified data, etc.).

Short version: `tickers -> companies/securities registration -> SEC companyfacts fetch -> JSON data lake -> XBRL tag mapping -> MySQL`, orchestrated by `main.py`.

## Tech stack

- **Python 3.13**, managed with [`uv`](https://github.com/astral-sh/uv)
- **MySQL 8**, schema-versioned with **Alembic** migrations (no ORM — raw `mysql-connector-python`)
- **SEC EDGAR** (`data.sec.gov`) as the fundamentals data source — free, no rate-limit ceiling, official filings
- **yfinance** for price data (planned — not yet wired in)
- **Streamlit** for the frontend
- **Docker Compose** for local MySQL

## Running it

Docker is the only thing you need installed. Python, `uv` and MySQL all live
inside the containers.

```bash
git clone git@github.com:mariusspill/Stock-analyzer.git
cd Stock-analyzer

cp .env.example .env          # then set SQL_CONNECTION_PW
docker compose build
docker compose up -d app      # starts MySQL, waits for it, migrates, then serves
```

The frontend is then on <http://localhost:8502>. The database is published on
`localhost:3307` — not 3306, so it cannot collide with a native MySQL install.

Run a pipeline:

```bash
docker compose run --rm pipeline python main.py
```

Tests and linting (also containerised, so they use the locked dependencies):

```bash
./scripts/test.sh
./scripts/lint.sh
```

### Moving the database between machines

The database is the source of truth for ingested data, so it travels as a dump
rather than being regenerated. Both scripts run `mysqldump`/`mysql` *inside* the
db container and write into the mounted `backups/` directory — no host MySQL
client is needed, and the output never passes through a host shell.

```bash
./scripts/db_dump.sh                      # -> backups/stockdb_<timestamp>.sql.gz
./scripts/db_restore.sh                   # restore the newest dump (destructive)
./scripts/db_restore.sh backups/x.sql.gz  # or a specific one
```

If you are coming from a native MySQL install on this host, import it once:

```bash
./scripts/db_import_native.sh
```

`Data/` (the raw JSON/parquet lake, ~13 GB) is deliberately **not** synced
between machines. It is a cache of SEC's API, not an archive — the fundamentals
cache overwrites each company's previous snapshot anyway — so a new machine
warms it on demand rather than copying it.

Today only the price pipeline can be scoped, via `FETCH_UNIVERSE=djia`.
Scoping every stage to a declared ticker universe is
[issue #5](https://github.com/mariusspill/Stock-analyzer/issues/5).

### Running against a native MySQL instead

Set `SQL_HOST`/`SQL_PORT` in `.env` to point wherever you like and run on the
host with `uv run streamlit run app.py`. Nothing about the connection is
hardcoded.

## Status

Actively in development. Fundamentals ingestion (tickers -> companies/securities -> SEC XBRL mapping for all three statement types) is functional. Daily price ingestion, dbt-based derived metrics (P/E TTM, ROE, etc.), and Airflow orchestration are planned next — see [ARCHITECTURE.md](ARCHITECTURE.md#roadmap-not-yet-built) for sequencing and reasoning, and the [GitHub milestones](https://github.com/mariusspill/Stock-analyzer/milestones) for tracked work.

## Disclaimer

Personal learning project, not production software or investment advice.

