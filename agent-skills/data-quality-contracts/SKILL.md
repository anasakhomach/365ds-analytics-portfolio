---
name: data-quality-contracts
description: Define and implement data quality, schema validation, metadata, lineage, file format, and SQL transformation contracts for local analytics pipelines. Use when working on CSV ingestion, DuckDB warehouses, Bronze/Silver/Gold layers, quality check SQL, source schemas, data catalogs, lineage docs, file conversion, or pipeline reliability.
---

# Data Quality Contracts

## Overview

Use this skill to make data pipelines trustworthy and reproducible. It consolidates useful ideas from the upstream data-pipelines skill set: data quality checking, schema validation, metadata extraction, data catalog updates, lineage tracking, file-format conversion, SQL transform helpers, and pipeline monitoring.

## Workflow

1. Define source contracts.
- List each input file/table, expected columns, data types, key fields, date fields, nullable fields, and grain.
- Record source ownership and refresh assumptions when known.
- Preserve raw files under `source-datasets/`; write derived or standardized copies elsewhere.

2. Validate ingestion.
- Check file existence, encoding, delimiter/header assumptions, row counts, duplicate rows, null-heavy columns, and type parse failures.
- For SQL dump sources, document required engine/dialect and whether DuckDB can execute directly or needs translation.
- For workbook/dashboard sources, separate extractable data from visual design artifacts.

3. Create layer quality gates.
- Bronze: load completeness, row counts, raw column preservation.
- Silver: type validity, dedupe, standard names, referential integrity, accepted values, date ranges.
- Gold: fact/dimension grain, unique keys, nonnegative measures, metric reconciliation, dashboard-readiness.

4. Track metadata and lineage.
- Keep a simple catalog with source, layer, object, grain, primary key, description, and upstream dependencies.
- For each derived table, record raw inputs, transform file, output object, and downstream dashboard/report users.
- Update docs when column names, mart names, or layer contracts change.

5. Monitor and recover.
- Make pipeline entrypoints rerunnable.
- Fail visibly on broken contracts rather than silently coercing bad data.
- Save quality check SQL or scripts near the transformed layer they protect.

## DuckDB-Friendly Checks

Use SQL checks for:

- row count comparisons
- duplicate key counts
- null checks on required fields
- orphan foreign keys
- negative revenue/quantity checks
- impossible date ranges
- expected category values
- reconciliation between source totals and modeled totals

## Output Shape

When adding or reviewing a data contract, provide:

- source inventory
- schema contract
- quality checks
- lineage map
- rerun command
- known risks and unresolved assumptions
