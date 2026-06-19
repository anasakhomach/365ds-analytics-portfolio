CREATE SCHEMA IF NOT EXISTS gold;

CREATE OR REPLACE TABLE gold.mart_q2_engagement_segments AS
SELECT
    engagement_year,
    paid,
    student_plan,
    segment_key,
    student_id,
    minutes_watched
FROM silver.q2_engagement_segments;

CREATE OR REPLACE TABLE gold.mart_q2_segment_summary_raw AS
SELECT
    engagement_year,
    paid,
    student_plan,
    segment_key,
    COUNT(*) AS raw_students,
    ROUND(AVG(minutes_watched), 4) AS raw_mean_minutes,
    ROUND(median(minutes_watched), 4) AS raw_median_minutes,
    ROUND(quantile_cont(minutes_watched, 0.99), 4) AS q99_minutes,
    ROUND(MAX(minutes_watched), 4) AS max_minutes
FROM gold.mart_q2_engagement_segments
GROUP BY engagement_year, paid, student_plan, segment_key
ORDER BY engagement_year, paid;

CREATE OR REPLACE TABLE gold.mart_certificates_minutes AS
SELECT
    student_id,
    minutes_watched,
    certificates_issued
FROM silver.certificates_minutes;

CREATE OR REPLACE TABLE gold.mart_watch_probability AS
WITH watched_2021 AS (
    SELECT DISTINCT student_id
    FROM silver.q2_minutes_watched
    WHERE engagement_year = 2021
),
watched_2022 AS (
    SELECT DISTINCT student_id
    FROM silver.q2_minutes_watched
    WHERE engagement_year = 2022
),
universe AS (
    SELECT student_id FROM watched_2021
    UNION
    SELECT student_id FROM watched_2022
),
counts AS (
    SELECT
        (SELECT COUNT(*) FROM universe) AS universe_students,
        (SELECT COUNT(*) FROM watched_2021) AS watched_2021_students,
        (SELECT COUNT(*) FROM watched_2022) AS watched_2022_students,
        (
            SELECT COUNT(*)
            FROM watched_2021
            INNER JOIN watched_2022 USING (student_id)
        ) AS watched_both_students
)
SELECT
    universe_students,
    watched_2021_students,
    watched_2022_students,
    watched_both_students,
    ROUND(watched_2021_students::DOUBLE / NULLIF(universe_students, 0), 4) AS probability_watched_2021,
    ROUND(watched_2022_students::DOUBLE / NULLIF(universe_students, 0), 4) AS probability_watched_2022,
    ROUND(watched_both_students::DOUBLE / NULLIF(universe_students, 0), 4) AS probability_watched_both,
    ROUND(watched_both_students::DOUBLE / NULLIF(watched_2022_students, 0), 4) AS probability_2021_given_2022,
    ROUND(
        (
            watched_2021_students::DOUBLE / NULLIF(universe_students, 0)
        )
        * (
            watched_2022_students::DOUBLE / NULLIF(universe_students, 0)
        ),
        4
    ) AS independent_product_probability,
    CASE
        WHEN ABS(
            watched_both_students::DOUBLE / NULLIF(universe_students, 0)
            - (
                watched_2021_students::DOUBLE / NULLIF(universe_students, 0)
            )
            * (
                watched_2022_students::DOUBLE / NULLIF(universe_students, 0)
            )
        ) > 0.0001 THEN 1
        ELSE 0
    END AS events_are_dependent
FROM counts;
