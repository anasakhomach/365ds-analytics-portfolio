# Checkout Flow Optimization

DuckDB and Streamlit implementation of the 365DS Checkout Flow Optimization Analysis with SQL and Tableau project.

## Workflow

```powershell
.\.venv-365ds\Scripts\python.exe projects\checkout-flow-optimization\scripts\pipeline.py
.\.venv-365ds\Scripts\python.exe -m streamlit run projects\checkout-flow-optimization\dashboard\app.py
```

## Contract

- Raw input: `source-datasets/Checkout Flow Optimization Analysis With SQL And Tableau/365_checkout_database.sql`
- Warehouse: `projects/checkout-flow-optimization/warehouse.duckdb`
- Analysis window: `2022-07-01` through `2023-01-31`
- Dashboard source: Gold tables only

## Layer Summary

- Bronze preserves the two MySQL dump tables in DuckDB: `checkout_actions` and `checkout_carts`.
- Silver types and filters checkout carts, checkout attempts, successful attempts, and error attempts.
- Gold exposes dashboard marts for daily/monthly checkout steps, success rates, abandonment rates, errors, devices, KPIs, and quiz support.

## MySQL Fallback

DuckDB is canonical for this repo. If dump compatibility needs validation, use:

```powershell
& "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -h 127.0.0.1 -P 3306 -u root -p
```
