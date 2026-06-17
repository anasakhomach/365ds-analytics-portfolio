---
name: dashboard-storytelling
description: Plan analytics dashboards, Tableau/Streamlit layouts, chart choices, report outlines, and stakeholder-ready data stories. Use when a 365DS project asks for Tableau, Streamlit, BI reporting, dashboard skeletons, chart selection, KPI presentation, executive summaries, insight narratives, or report templates.
---

# Dashboard Storytelling

## Overview

Use this skill to turn verified analysis results into a clear business-facing dashboard or report. It consolidates useful ideas from the upstream chart recommender, dashboard layout planner, data story outliner, report template generator, pivot table creator, and visualization best-practices skills.

## Workflow

1. Identify audience and decision.
- Name the stakeholder, question, decision, and expected action.
- Separate exploration outputs from presentation outputs.
- Keep the first screen focused on the highest-value KPI movement or anomaly.

2. Choose the view type.
- KPI cards: current value, comparison period, target, or variance.
- Line chart: trend over time.
- Bar chart: category comparison or ranking.
- Stacked bar: composition when totals still matter.
- Heatmap: cohort retention, calendar patterns, or matrix density.
- Funnel: ordered step conversion and dropoff.
- Scatter/regression: relationship and outlier exploration.
- Table: exact values, audit trail, or exportable detail.

3. Design the layout.
- Start with summary KPIs, then trend/context, then diagnostic breakdowns, then detail table.
- Keep filters near the top and tied to the business question.
- Avoid chart variety for its own sake; repeated comparable views are easier to scan.
- Use dashboard skeleton PDFs or project instructions as constraints when present.

4. Tell the story.
- Lead with the answer, not the method.
- Use a compact narrative: context, evidence, implication, recommendation.
- Call out assumptions, missing data, and uncertainty plainly.
- Pair every recommendation with the metric that supports it.

5. Verify presentation readiness.
- Check chart axes, sort order, labels, units, date ranges, and filter defaults.
- Confirm dashboard numbers match the verified SQL/Python output.
- Ensure the exported report or dashboard can be regenerated from saved analysis artifacts.

## Repo-Specific Notes

- Tableau `.twbx` files may need Tableau Desktop/Public for full editing. If unavailable, inspect accompanying SQL/PDF instructions and produce compatible extracts or documentation.
- Streamlit dashboards should read modeled or final analysis outputs, not raw files with hidden cleaning logic.
- PDF story sketches and dashboard skeletons are design inputs; preserve them as references.

## Output Shape

For dashboard/report work, produce:

- audience and decision statement
- KPI list with definitions
- page or section layout
- chart plan and data source per chart
- validation checklist
- narrative summary
