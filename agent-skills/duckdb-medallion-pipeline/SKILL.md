---
name: duckdb-medallion-pipeline
description: Build, repair, or standardize local DuckDB data engineering projects that use Bronze, Silver, and Gold layers with Python orchestration, SQL transformations, quality checks, and Streamlit dashboards. Use when working on medallion pipelines, local warehouses, marts, star schemas, ETL scripts, or dashboard data contracts.
---

# DuckDB Medallion Pipeline

## Overview

Use this skill for local analytics engineering projects modeled after the sibling repos:

- `C:\Users\Nitro\data-analytics-project\maven-fuzzy-factory`
- `C:\Users\Nitro\data-analytics-project\baraa-warehouse-example`

Both use a portable warehouse pattern: raw CSVs, DuckDB, Python orchestration, SQL models, quality checks, and Streamlit dashboards.

## Target Contract

Prefer this structure when creating or standardizing a pipeline:

```text
datasets/                    # raw sources
scripts/
  bronze/setup_warehouse.py  # setup_bronze()
  silver/build_silver.py     # build_silver()
  silver/*.sql               # cleaned semantic models
  gold/build_gold.py         # build_gold()
  gold/*.sql                 # reporting marts or star schema
  pipeline.py                # run_pipeline()
dashboard/app.py             # Streamlit reads gold only
tests/quality_checks_*.sql   # SQL quality checks
docs/data_flow.md
docs/naming_conventions.md
```

## Workflow

1. Map sources and contracts.
- Identify raw source files, primary keys, date fields, grain, and business questions.
- Decide the warehouse filename (`warehouse.duckdb` or `warehouse.db`) and keep it consistent.
- Preserve legacy folders only as lineage; put active runtime code under `scripts/`, `dashboard/`, `tests/`, and `docs/`.

2. Build Bronze.
- Load raw CSVs without business transformations.
- Keep source columns traceable and record load counts.
- Resolve source paths predictably, usually `datasets/` first and legacy raw folders only as fallback.

3. Build Silver.
- Clean, standardize, deduplicate, type, and normalize data.
- Put repeatable SQL in `scripts/silver/*.sql` and Python orchestration in `scripts/silver/build_silver.py`.
- Assert key uniqueness, referential joins, and date parsing before gold marts depend on the data.

4. Build Gold.
- Create fact/dimension tables, marts, or analytics views at reporting grain.
- Name marts by business purpose, such as `mart_conversion_funnels`, `mart_product_performance`, or `mart_traffic_growth`.
- Keep dashboards and reports reading gold objects only.

5. Orchestrate and verify.
- Run the whole pipeline from `python scripts/pipeline.py`.
- Run focused quality SQL files against the DuckDB warehouse.
- Launch `streamlit run dashboard/app.py` only after gold outputs exist.
- Record command results, failing checks, and row-count evidence.

## Guardrails

- Use the project `.venv` when present; avoid conda/global environments for pipeline runs.
- Do not hand-roll CSV parsing when DuckDB or pandas can load sources safely.
- Do not let Streamlit query raw or silver tables unless explicitly building a diagnostic view.
- Update docs when layer contracts, mart names, commands, or dashboard data sources change.
