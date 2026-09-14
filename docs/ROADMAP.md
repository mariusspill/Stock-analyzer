# Roadmap

Coarse-grained milestones. Near-term entries are decomposed into concrete tasks;
farther-out ones stay deliberately vague until their turn comes. Completed
milestones link to a retrospective in `docs/milestones/`.

## M1 — Portable environment *(in progress)*

Make the repo runnable on any machine with Docker and nothing else.

- [x] Central connection config with `SQL_PORT` support (`repository/db_config.py`)
- [x] Connections open lazily, so importing code no longer requires a database
- [x] `.env.example` documents every setting
- [x] Compose stack with a DB healthcheck and a migration step that runs before the app
- [x] Dump/restore scripts that run entirely inside the container
- [x] `pandas`/`pyarrow` promoted from accidental transitive deps to declared ones
- [x] First tests covering config and lazy imports
- [ ] `uv lock` + `docker compose build` verified green
- [ ] README rewritten around the container workflow

## M2 — Database into Docker

Retire the native MySQL install on port 3306.

- [ ] Run `./scripts/db_import_native.sh` and restore into the container
- [ ] Verify row counts and `checked=1` counts match the native database
- [ ] Confirm `alembic current` agrees with `head` after restore
- [ ] Switch `.env` to the container and re-run the Streamlit app
- [ ] Delete the unrestorable UTF-16 backup from `Data/backups/`

## M3 — Same version on every machine

The remaining half of "publishable everywhere". Code and schema already travel
via git; data does not.

- [ ] Decide where database dumps live (git-lfs vs. object storage vs. manual)
- [ ] Decide how the 13 GB `Data/` lake is shared, rather than refetched per machine
- [ ] Write the second-machine bootstrap into the README and verify it end to end

## M4 — CI

- [ ] GitHub Actions: build the image and run the test suite on push and PR
- [ ] Nothing beyond build + test until there is something to deploy

## M5 — Trust the pipelines *(coarse)*

Test `ARCHITECTURE.md`'s claim that the warehouse is rebuildable from the lake:
rebuild into a scratch database and diff against the real one. Expected to fail
on `checked=1` rows; the point is to find out what *else* differs. TBD.

## M6 — Prices into the warehouse *(coarse)*

`pipelines/history_api_to_parquet.py` currently stops at parquet. Load it into
`daily_ohlc` / `dividends` / `stock_splits`, which the schema already has. TBD.

## M7 — Analytics layer *(coarse)*

Derived metrics (P/E TTM, 3yr avg P/E, ROE) via dbt, then Airflow orchestration
of the full chain. Sequenced after M6 because the P/E metrics need price data.
See `ARCHITECTURE.md` for the reasoning. TBD.
