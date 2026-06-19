# Tracking User Engagement Data Flow

## Source

- Raw input: `source-datasets/Tracking User Engagement With SQL Excel And Python/data_scientist_project.sql`
- Source grain:
  - `student_certificates`: one row per issued certificate.
  - `student_info`: one row per registered student.
  - `student_purchases`: one row per subscription purchase.
  - `student_video_watched`: one row per watched-course event.

## Bronze

Bronze parses the MySQL dump into DuckDB tables without business transformations. The parser supports multiple `INSERT` blocks per table and stores block counts in `bronze.load_metadata`.

Expected row counts:

- `bronze.student_certificates`: 1,751
- `bronze.student_info`: 270,275
- `bronze.student_purchases`: 18,207
- `bronze.student_video_watched`: 86,035

## Silver

Silver standardizes typed source tables and creates the course-required analytical extracts:

- `silver.purchases_info`: subscription start/end dates, including refund override and lifetime/open-ended handling.
- `silver.q2_minutes_watched`: one row per student and engagement year for Q2 2021 or Q2 2022.
- `silver.q2_paid_flags`: paid/free status based on subscription overlap with the Q2 window.
- `silver.q2_engagement_segments`: paid/free/year segments used for outlier removal and hypothesis tests.
- `silver.certificates_minutes`: certificate holders with total watched minutes and certificate counts.

## Gold

Gold exposes dashboard/report-ready marts:

- Q2 engagement segments and raw segment summaries.
- 99th-percentile filtered engagement rows and segment statistics.
- Hypothesis test outputs for free-plan and paid students.
- Certificate correlation and linear regression outputs.
- Watching-event probability/dependence summary.
- Summary KPIs and quiz-supporting answers.

The Streamlit dashboard reads Gold tables only.
