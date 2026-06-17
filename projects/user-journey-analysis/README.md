# User Journey Analysis

DuckDB and Streamlit implementation of the 365DS User Journey Analysis in Python project.

## Run

From the repository root:

```powershell
.\.venv-365ds\Scripts\python.exe projects\user-journey-analysis\scripts\pipeline.py
.\.venv-365ds\Scripts\streamlit.exe run projects\user-journey-analysis\dashboard\app.py
```

## Structure

- `scripts/bronze/`: loads the immutable raw CSV into DuckDB.
- `scripts/silver/`: validates sessions and creates grouped, duplicate-cleaned journeys.
- `scripts/gold/`: creates dashboard-ready journey metrics and writes the Markdown report.
- `scripts/journey_tools.py`: public journey preprocessing and metric helpers required by the brief.
- `dashboard/`: Streamlit dashboard that reads Gold tables only.
- `tests/`: SQL quality checks run by the pipeline.
- `docs/`: data flow and naming notes.

Generated runtime files such as `warehouse.duckdb` are ignored by git.
