# Customer Engagement Analysis

DuckDB and Streamlit implementation of the 365DS Customer Engagement Analysis with SQL and Tableau project.

## Workflow

```powershell
.\.venv-365ds\Scripts\python.exe projects\customer-engagement-analysis\scripts\pipeline.py
.\.venv-365ds\Scripts\python.exe -m streamlit run projects\customer-engagement-analysis\dashboard\app.py
```

## Contract

- Raw input: `source-datasets/Customer Engagement Analysis With SQL And Tableau/365_database.sql`
- Warehouse: `projects/customer-engagement-analysis/warehouse.duckdb`
- Dashboard source: Gold tables only
- Tableau workbook and Hyper extracts are references only

## Layer Summary

- Bronze preserves the five MySQL dump tables in DuckDB and records insert-block counts.
- Silver creates typed source tables, subscription windows, country labels, and the course-required student engagement extract.
- Gold exposes dashboard marts for course performance, monthly engagement, registration/onboarding, country funnels, KPIs, and quiz support.

## MySQL Fallback

DuckDB is canonical for this repo. If dump compatibility needs validation, use:

```powershell
& "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -h 127.0.0.1 -P 3306 -u root -p
```
