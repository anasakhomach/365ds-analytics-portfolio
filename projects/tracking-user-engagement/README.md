# Tracking User Engagement

This project implements the 365 Data Science **Tracking User Engagement with SQL, Excel, and Python** brief using the repo-standard DuckDB and Streamlit workflow.

## Workflow

- Python orchestrates the pipeline.
- SQL defines Bronze, Silver, and relational Gold tables.
- Python creates the brief's statistical and regression outputs.
- Streamlit reads Gold tables only.

## Run

```powershell
.\.venv-365ds\Scripts\python.exe projects\tracking-user-engagement\scripts\pipeline.py
.\.venv-365ds\Scripts\streamlit.exe run projects\tracking-user-engagement\dashboard\app.py
```

## Outputs

- `warehouse.duckdb`: generated local warehouse, ignored by git.
- `reports/tracking_user_engagement_report.md`: generated business report.
- Gold marts for Q2 engagement, outlier removal, confidence intervals, t-tests, correlation, regression, probabilities, and quiz support.

## Source Contract

Raw input remains immutable under `source-datasets/Tracking User Engagement With SQL Excel And Python/`.
