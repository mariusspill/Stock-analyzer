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

1. Start the database:

docker compose up -d db

2. Create a `.env` file at the repo root with at least:

SQL_CONNECTION_PW=<your password>
SQL_HOST=localhost

(matches the port/user defaults in `docker-compose.yml` / `repository/sqlConnection.py`)
3. Apply migrations:

uv run alembic upgrade head

4. Run the ingestion chain:
uv run python main.py

5. Launch the frontend:
uv run streamlit run app.py


## Status

Actively in development. Fundamentals ingestion (tickers -> companies/securities -> SEC XBRL mapping for all three statement types) is functional. Daily price ingestion, dbt-based derived metrics (P/E TTM, ROE, etc.), and Airflow orchestration are planned next — see [ARCHITECTURE.md](ARCHITECTURE.md#roadmap-not-yet-built) for sequencing and reasoning.

## Disclaimer

Personal learning project, not production software or investment advice.

