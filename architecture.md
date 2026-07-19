# Architecture

A personal value-investing stock screener. Fundamentals and prices are ingested from free public sources into MySQL, with a Streamlit frontend for screening. No ORM — raw `mysql-connector-python` throughout.

## Data model

**Companies vs. Securities (1:many).** A `companies` row is one legal entity, keyed by `cik` (SEC's zero-padded 10-digit Central Index Key — the true identity key, not ticker or name, since tickers can be reused/delisted and companies can have multiple securities). A `securities` row is one tradeable instrument (`ticker`, `isin`, `wkn`) belonging to a company — this exists to handle dual-class shares and ADRs, which the original 1:1 schema couldn't represent.

**Fundamentals tables**: `income_statements`, `balance_sheets`, `cash_flow_statements`. All three share the same period-identity shape:
- `company_id`, `year`, `type` (`"annual"` / `"quarter"`), `quarter` (`"1"`–`"4"`, `NULL` for annual)
- `checked` (boolean) — protects hand-researched rows. Set to `1` for figures manually verified when no API had them (some genuinely required digging through old filings by hand). Any pipeline `UPDATE` includes `AND checked != 1` in its `WHERE` clause — checked rows are never silently overwritten by automated ingestion. `INSERT`s are unaffected (a checked row already existing means the row isn't re-inserted, just skipped for updates).

Lookups use `quarter <=> %s` (MySQL's NULL-safe equality) since `quarter` is nullable and `=` doesn't match `NULL` against `NULL`.

## Ingestion pipeline chain

1. `sec_tickers_api_to_json.fetch_meta_data()` — ticker list -> JSON cache (weekly staleness)
2. `metadata_json_to_db.pipeline()` — registers companies + securities, CIK-keyed
3. `sec_fundamentals_api_to_json.fetch_fundamentals()` — SEC companyfacts -> JSON cache per CIK (monthly staleness)
4. JSON -> DB mapping (independent once step 3's cache is populated):
   - `sec_income_statements_json_to_db.pipeline()` -> `income_statements`
   - `sec_balance_sheets_json_to_db.pipeline()` -> `balance_sheets`
   - `sec_cash_flow_statements_json_to_db.pipeline()` -> `cash_flow_statements`



Each arrow is a real boundary: the fetch stage hits the network and caches to disk; everything downstream reads only from that local cache, never re-hits the API. This is why the fetch stage is rate-limited/slow (SEC fair-use pacing) while the JSON->DB mapping stage is fast (local disk + DB only) — they're scheduled independently.

**Why SEC EDGAR, not AlphaVantage**: AlphaVantage capped at 25 calls/day, which doesn't scale to ~8,000 companies. SEC's `companyfacts` API (`data.sec.gov/api/xbrl/companyfacts/CIK##########.json`) is free, has no daily cap, and returns *all* historical facts for a company in one call — a single request replaces what would've been dozens of AlphaVantage calls.

## Data lake

`storage/sec_local_cache.py` (ticker list) and `storage/sec_fundamentals_cache.py` (companyfacts JSON) cache raw API responses to `Data/Fundamentals/{cik}/{type}_{date}.json`. Staleness windows: weekly for the ticker list, monthly for fundamentals (SEC filings only change a few times a year per company, so daily refetching would be pure waste). This is the project's single source of truth for raw data — all downstream tables are derived from it and can, in principle, be rebuilt from it without hitting SEC again.

## XBRL tag mapping — the core complexity

SEC's `companyfacts` JSON is keyed by US-GAAP XBRL tag (e.g. `Revenues`, `Assets`, `NetIncomeLoss`), not by a fixed schema — and **the same concept is often reported under different tags by different companies, or by the same company in different years**, because of accounting-standard transitions (ASC 606 revenue recognition, ASC 842 lease accounting) and inconsistent filer conventions. `pipelines/xbrl_utils.py::get_tag_value()` handles this with a **priority list**: for each field, a list of candidate tag names in preference order, first match wins. Example — revenue tries `RevenueFromContractWithCustomerExcludingAssessedTax` (post-ASC-606), then `Revenues`, then `SalesRevenueNet` (older conventions).

`get_tag_value` also cross-checks each candidate entry's `end` date against the target fiscal year, because SEC's `fy`/`fp` metadata reflects the *filing's own* fiscal context — a filing can carry a prior-year comparative figure tagged under a `fy` that doesn't match the period the number actually describes.

**When no tag matches at all** (not a naming issue — the company genuinely doesn't report that line item, e.g. Gap Inc. blends all opex into one line with no separate SG&A tag; some companies never separately tag Q4 since there's no 10-Q for Q4), the field is left `None` rather than guessed at. Where a field is cleanly re-derivable from other already-fetched fields, a fallback derivation is applied instead of leaving it `None` — e.g. `gross_profit = revenue - cost_of_revenue` when `GrossProfit` isn't directly tagged (verified against IBM's own reported figures to within $1M, i.e. rounding).

**Standardized `operating_income` definition**: rather than trust each company's own `OperatingIncomeLoss` tag (definitions vary — Compustat-style OIADP vs. others), this project standardizes on the classic CFA-curriculum formula: `operating_income = gross_profit - SG&A - R&D`. Missing R&D defaults to `0` (a huge share of companies — retailers, financials, utilities — simply don't do R&D and never tag it, so absence means zero, not missing data). Missing SG&A does *not* default to anything — SG&A is close to universally reported by operating companies, so its absence more likely means genuinely unavailable data than a real zero, and `operating_income`/`operating_expense` are left `None` in that case (e.g. Gap Inc., which blends SG&A into one undifferentiated opex line).

**`EBIT`/`EBITDA`** are computed as `net_income + interest_cost + taxes` and `EBIT + Depreciation + Amortization`, both guarded so any missing input yields `None` rather than a misleading `0` (a `0` looks like real data; `None` doesn't).

**Q4 is not stored as its own row.** SEC filers submit 10-Qs for Q1–Q3 only; Q4 has no standalone filing, and most companies never tag discrete Q4 figures. `Q4 = FY - Q1 - Q2 - Q3` is trivial to derive on demand (e.g. in a future dbt model) from data already in the DB, so there's no need to pre-compute and store it.

## Running the pipelines

Each JSON->DB pipeline module exposes `pipeline(full=True, update=True)`:
- `full=True` backfills from 2007 (roughly when SEC's XBRL mandate phased in); `full=False` only touches the last two years, for fast routine reruns.
- `update=True` refreshes existing non-`checked` rows; `update=False` only inserts new periods, leaving existing rows untouched.

Each period fetch is wrapped in `try/except` — one company/period with bad data (e.g. an out-of-range `eps_diluted` value) logs an error and the run continues, rather than one bad row killing an ~8,000-company backfill.

Run the full chain via `main.py`, or any pipeline module standalone via `python -m pipelines.<module_name>` for testing against one or a few companies.

## Known limitations / open questions

- `total_debt` has no direct XBRL tag anywhere — always derived as `short_debt + long_debt`.
- Dividend/capex figures are stored as SEC reports them (`PaymentsOfDividendsCommonStock`, `PaymentsToAcquirePropertyPlantAndEquipment` — both positive numbers representing cash outflows), not sign-flipped to negative.
- No automated test suite yet for the repository layer or tag-mapping logic — correctness is currently verified by manual spot-checks against real 10-Ks (see e.g. the IBM/Gap Inc./ASC 842 lease-reclassification investigations that shaped several of the derivation-fallback decisions above).
- Balance sheet / cash flow field priority lists have had less real-world validation than income statements so far — worth spot-checking more companies as the full backfill runs.

## Roadmap (not yet built)

Daily OHLC prices (yfinance) -> dbt derived metrics (P/E TTM, 3yr avg P/E, ROE) -> Airflow orchestration of the full chain. Sequenced in that order because P/E-based metrics need price data that doesn't exist yet, and orchestrating unfinished pipelines makes debugging harder, not easier.
