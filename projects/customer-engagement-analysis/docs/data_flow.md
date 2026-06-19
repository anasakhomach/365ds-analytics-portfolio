# Customer Engagement Data Flow

## Source

The project reads the immutable MySQL dump at:

`source-datasets/Customer Engagement Analysis With SQL And Tableau/365_database.sql`

The dump contains:

- `365_course_info`: one row per course.
- `365_course_ratings`: one row per student-course rating.
- `365_student_info`: one row per registered student.
- `365_student_learning`: lecture watch events; this table has two INSERT blocks in the dump.
- `365_student_purchases`: one row per purchase.

## Bronze

Python parses all MySQL `INSERT INTO ... VALUES` blocks for each table and loads them into SQL-created DuckDB tables:

- `bronze.course_info`
- `bronze.course_ratings`
- `bronze.student_info`
- `bronze.student_learning`
- `bronze.student_purchases`
- `bronze.load_metadata`

Bronze keeps source rows unchanged except for type casting into DuckDB.

## Silver

SQL creates typed, analysis-ready tables:

- `silver.purchases_info`: subscription start and end dates.
- `silver.student_info`: student country codes plus English country labels.
- `silver.student_engagement`: the course-required Tableau data source, including onboarding and paid flags.

## Gold

SQL creates dashboard/report marts:

- `gold.mart_course_performance`
- `gold.mart_student_engagement`
- `gold.mart_monthly_engagement`
- `gold.mart_monthly_registrations`
- `gold.mart_country_registered`
- `gold.mart_country_minutes`
- `gold.mart_summary_kpis`
- `gold.mart_quiz_answers`

## Presentation

The Streamlit dashboard reads Gold tables only and translates the Tableau dashboard into three pages:

- Engagement trend and KPIs
- Country registration and minutes funnels
- Onboarding and course performance
