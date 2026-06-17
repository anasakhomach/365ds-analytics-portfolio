# Real Estate Market Analysis

DuckDB and Streamlit implementation of the 365DS Real Estate Market Analysis project.

## Run

From the repository root:

```powershell
.\.venv-365ds\Scripts\python.exe projects\real-estate-market-analysis\scripts\pipeline.py
.\.venv-365ds\Scripts\streamlit.exe run projects\real-estate-market-analysis\dashboard\app.py
```

## Structure

- `scripts/bronze/`: loads immutable raw CSVs into DuckDB.
- `scripts/silver/`: cleans names, types, dates, prices, customer joins, and derived fields.
- `scripts/gold/`: creates dashboard-ready marts and writes the Markdown report.
- `dashboard/`: Streamlit dashboard that reads Gold tables only.
- `tests/`: SQL quality checks run by the pipeline.
- `docs/`: data flow and naming notes.

Generated runtime files such as `warehouse.duckdb` are ignored by git.
