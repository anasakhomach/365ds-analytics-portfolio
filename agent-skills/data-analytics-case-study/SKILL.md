---
name: data-analytics-case-study
description: Execute 365 Data Science style analytics case studies in this repo. Use when working from project-instructions/*.md or source-datasets/* on SQL, Excel, Python, Tableau, LangChain, cohort, funnel, engagement, real-estate, dashboard, notebook, report, or reproducible data analysis deliverables.
---

# Data Analytics Case Study

## Overview

Use this skill to turn a project brief plus raw data into a reproducible analytics deliverable. The current repo contains 365DS project briefs in `project-instructions/` and raw sources in `source-datasets/`.

## Workflow

1. Match the brief to the data.
- Read the relevant `project-instructions/*.md` file first.
- Locate the matching folder or file under `source-datasets/`.
- Inventory file types, sizes, schemas, and obvious external-tool requirements.

2. Define the delivery contract.
- State the questions to answer, expected outputs, toolchain, and assumptions.
- For SQL/Tableau projects, decide whether analysis should be SQL-only, DuckDB-backed, or dashboard-oriented.
- For Python projects, prefer reproducible `.py` scripts plus Markdown outputs unless the user requests notebooks.
- For Excel work, preserve formulas and workbook semantics when creating `.xlsx` outputs.

3. Profile the raw data.
- Inspect row counts, columns, data types, nulls, duplicates, keys, date ranges, and category cardinality.
- Use structured readers such as DuckDB, pandas, openpyxl, or SQL parsers instead of ad hoc text manipulation.
- Do not edit files under `source-datasets/`; treat them as immutable raw inputs.

4. Build the analysis.
- Create a project-specific output folder when new deliverables are needed.
- Keep transformations reproducible and rerunnable from raw inputs.
- Separate extraction, cleaning, modeling, analysis, and presentation code when the work grows beyond one small script.
- Make charts and tables answer the business question directly; avoid decorative output that does not support a finding.

5. Verify.
- Re-run the script/query/notebook from a clean entrypoint.
- Check totals against source row counts and known business invariants.
- Confirm exported reports, charts, dashboards, or workbooks open and contain the expected outputs.
- Record exact commands and verification results in the final response and memory artifact when useful.

## Standards

- Keep raw data immutable and derived artifacts clearly named.
- Prefer small, auditable SQL and Python files over large opaque notebooks.
- Document assumptions next to the analysis, especially date filters, attribution logic, joins, and excluded records.
- If a project uses proprietary formats such as `.twbx`, inspect what is possible locally and state any tool limitation plainly.
