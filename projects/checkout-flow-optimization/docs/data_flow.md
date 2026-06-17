# Checkout Flow Data Flow

## Source

The project reads the immutable MySQL dump at:

`source-datasets/Checkout Flow Optimization Analysis With SQL And Tableau/365_checkout_database.sql`

The dump contains:

- `checkout_actions`: checkout and non-checkout action events.
- `checkout_carts`: carts created by users.

## Bronze

Python parses the MySQL `INSERT INTO ... VALUES` blocks and loads them into DuckDB tables created from SQL DDL:

- `bronze.checkout_actions`
- `bronze.checkout_carts`

Bronze keeps the full dump period. No business filtering happens here.

## Silver

SQL creates typed, analysis-ready tables for `2022-07-01` through `2023-01-31`:

- `silver.checkout_actions`
- `silver.checkout_carts`
- `silver.checkout_attempts`
- `silver.successful_checkout_attempts`
- `silver.checkout_errors`

## Gold

SQL creates dashboard/report marts:

- `gold.mart_daily_checkout_steps`
- `gold.mart_monthly_checkout`
- `gold.mart_checkout_errors`
- `gold.mart_error_rankings`
- `gold.mart_device_distribution`
- `gold.mart_summary_kpis`
- `gold.mart_quiz_answers`

## Presentation

The Streamlit dashboard reads Gold tables only and translates the Tableau story into three pages:

- Checkout success
- Cart abandonment
- Error and device diagnostics
