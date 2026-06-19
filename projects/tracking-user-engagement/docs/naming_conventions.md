# Tracking User Engagement Naming Conventions

## Layers

- `bronze.*`: typed raw source tables loaded from the SQL dump.
- `silver.*`: cleaned, typed, and course-specific analysis extracts.
- `gold.*`: dashboard, report, statistics, and quiz-supporting marts.

## Table Names

- Use `student_*` for direct source entities.
- Use `q2_*` for Q2 2021 vs Q2 2022 engagement comparisons.
- Use `mart_*` for Gold reporting tables.
- Use `*_no_outliers` only for tables where the brief's 99th-percentile filtering has been applied.

## Metrics

- `minutes_watched` is always `seconds_watched / 60`, rounded to two decimals for course-aligned extracts.
- `paid = 1` means a student had a subscription overlapping the relevant Q2 window.
- Lifetime purchases keep `date_end` null and are treated as open-ended for overlap checks.
- `filtered_students` counts rows after keeping values lower than the segment-specific 99th percentile.
