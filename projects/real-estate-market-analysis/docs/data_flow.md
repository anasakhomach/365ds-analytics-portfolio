# Data Flow

## Sources

Raw inputs live under `source-datasets/Real Estate Market Analysis With Python/`:

- `customers.csv`: one row per customer profile.
- `properties.csv`: one row per property listing or sale record.

## Layers

1. Bronze loads both CSVs as raw tables with row counts preserved.
2. Silver removes source index columns, normalizes names, trims text values, parses dates and prices, joins sold properties to customers, and derives age, date, and interval fields.
3. Gold creates reporting marts for KPIs, building performance, geography, age, price, revenue, sales by year, and correlation.
4. Streamlit reads only Gold marts from `warehouse.duckdb`.

## Rerun Contract

Run `python projects/real-estate-market-analysis/scripts/pipeline.py` from the repository root. The command rebuilds the warehouse from raw source files and rewrites the Markdown report.
