---
name: analytics-sql-patterns
description: Design and implement reusable SQL analytics patterns for metrics, KPIs, aggregations, date ranges, joins, CTEs, window functions, funnels, cohorts, retention, A/B tests, and query optimization. Use when a 365DS project asks for SQL analysis, business metrics, checkout funnels, engagement cohorts, customer behavior, sales trends, or DuckDB-backed analytics.
---

# Analytics SQL Patterns

## Overview

Use this skill to convert a business question into auditable SQL analysis. It consolidates useful ideas from the upstream data-analytics skill set: aggregation helpers, CTE builders, complex joins, date-range analysis, funnel analysis, KPI definition, metrics, retention/cohorts, SQL optimization, statistical significance, and window functions.

## Workflow

1. Define the metric contract.
- Name the grain: user, session, order, product, day, cohort, or funnel step.
- State numerator, denominator, filters, date window, timezone assumption, and null handling.
- Separate count metrics, rate metrics, monetary metrics, and time-to-event metrics.

2. Inspect source shape before writing final SQL.
- Identify candidate primary keys, join keys, date columns, event columns, and known duplicate risks.
- Check row counts and date min/max per table or CSV.
- Prefer CTEs that expose each business stage over a single dense query.

3. Pick the pattern.
- Aggregation: group at the final grain only after dedupe and filtering.
- CTE pipeline: use one CTE per semantic step, with names like `sessions`, `orders`, `step_events`, `cohorts`, and `final`.
- Complex join: assert key uniqueness before joining; document expected one-to-one, one-to-many, or many-to-many behavior.
- Window functions: use for ranking, rolling metrics, first/last events, session paths, cohort age, and running totals.
- Funnel: produce one row per entity with boolean or timestamp columns for each ordered step, then aggregate conversion and dropoff.
- Cohort/retention: define cohort date, activity date, period index, active count, cohort size, and retention rate.
- A/B test: define exposure, assignment unit, outcome window, conversion metric, sample size, and statistical test assumptions.

4. Validate the SQL.
- Reconcile totals back to raw row counts or known source totals.
- Add sanity checks for impossible rates, negative amounts, duplicate keys, orphan joins, and date leakage outside the requested window.
- For DuckDB, run queries against a local `.duckdb`/`.db` file or directly over CSVs when that is the simplest reproducible route.

5. Package the result.
- Save reusable SQL in a project-specific folder or layer file.
- Put assumptions next to the query.
- Include final tables that can feed Python, Excel, Tableau, or Streamlit without hidden transformation logic.

## Output Shape

When answering or creating SQL, include:

- business question
- source tables/files
- metric definitions
- SQL query or transformation path
- validation checks
- interpretation notes and caveats

## Guardrails

- Do not trust a metric until its grain and denominator are explicit.
- Do not hide dedupe in final aggregation; make it visible.
- Do not optimize before correctness checks pass.
- Do not mutate raw source files under `source-datasets/`.
