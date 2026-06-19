CREATE SCHEMA IF NOT EXISTS silver;

CREATE OR REPLACE TABLE silver.student_certificates AS
SELECT
    certificate_id,
    student_id,
    date_issued
FROM bronze.student_certificates;

CREATE OR REPLACE TABLE silver.student_info AS
SELECT
    student_id,
    date_registered
FROM bronze.student_info;

CREATE OR REPLACE TABLE silver.student_purchases AS
SELECT
    purchase_id,
    student_id,
    plan_id,
    date_purchased,
    date_refunded
FROM bronze.student_purchases;

CREATE OR REPLACE TABLE silver.student_video_watched AS
SELECT
    student_id,
    course_id,
    seconds_watched,
    date_watched
FROM bronze.student_video_watched;

CREATE OR REPLACE TABLE silver.purchases_info AS
WITH plan_windows AS (
    SELECT
        purchase_id,
        student_id,
        plan_id,
        date_purchased AS date_start,
        CASE plan_id
            WHEN 0 THEN date_purchased + INTERVAL 1 MONTH
            WHEN 1 THEN date_purchased + INTERVAL 3 MONTH
            WHEN 2 THEN date_purchased + INTERVAL 12 MONTH
            WHEN 3 THEN NULL
        END::DATE AS planned_date_end,
        date_refunded
    FROM silver.student_purchases
)
SELECT
    purchase_id,
    student_id,
    plan_id,
    CASE plan_id
        WHEN 0 THEN 'Monthly'
        WHEN 1 THEN 'Quarterly'
        WHEN 2 THEN 'Annual'
        WHEN 3 THEN 'Lifetime'
        ELSE 'Unknown'
    END AS plan_name,
    date_start,
    CASE
        WHEN date_refunded IS NOT NULL THEN date_refunded
        ELSE planned_date_end
    END AS date_end,
    date_refunded
FROM plan_windows;

CREATE OR REPLACE TABLE silver.q2_minutes_watched AS
SELECT
    EXTRACT(year FROM date_watched)::INTEGER AS engagement_year,
    student_id,
    ROUND(SUM(seconds_watched) / 60.0, 2) AS minutes_watched
FROM silver.student_video_watched
WHERE date_watched BETWEEN DATE '2021-04-01' AND DATE '2021-06-30'
   OR date_watched BETWEEN DATE '2022-04-01' AND DATE '2022-06-30'
GROUP BY engagement_year, student_id;

CREATE OR REPLACE TABLE silver.q2_paid_flags AS
WITH year_windows AS (
    SELECT 2021 AS engagement_year, DATE '2021-04-01' AS window_start, DATE '2021-06-30' AS window_end
    UNION ALL
    SELECT 2022, DATE '2022-04-01', DATE '2022-06-30'
),
active_paid AS (
    SELECT DISTINCT
        year_windows.engagement_year,
        purchases_info.student_id
    FROM year_windows
    INNER JOIN silver.purchases_info AS purchases_info
        ON purchases_info.date_start <= year_windows.window_end
       AND COALESCE(purchases_info.date_end, DATE '2999-12-31') >= year_windows.window_start
)
SELECT
    q2_minutes_watched.engagement_year,
    q2_minutes_watched.student_id,
    CASE WHEN active_paid.student_id IS NULL THEN 0 ELSE 1 END AS paid
FROM silver.q2_minutes_watched AS q2_minutes_watched
LEFT JOIN active_paid
    ON q2_minutes_watched.engagement_year = active_paid.engagement_year
   AND q2_minutes_watched.student_id = active_paid.student_id;

CREATE OR REPLACE TABLE silver.q2_engagement_segments AS
SELECT
    q2_minutes_watched.engagement_year,
    q2_paid_flags.paid,
    CASE WHEN q2_paid_flags.paid = 1 THEN 'Paid' ELSE 'Free' END AS student_plan,
    CAST(q2_minutes_watched.engagement_year AS VARCHAR)
        || '_paid_'
        || CAST(q2_paid_flags.paid AS VARCHAR) AS segment_key,
    q2_minutes_watched.student_id,
    q2_minutes_watched.minutes_watched
FROM silver.q2_minutes_watched AS q2_minutes_watched
INNER JOIN silver.q2_paid_flags AS q2_paid_flags
    ON q2_minutes_watched.engagement_year = q2_paid_flags.engagement_year
   AND q2_minutes_watched.student_id = q2_paid_flags.student_id;

CREATE OR REPLACE TABLE silver.certificates_minutes AS
WITH certificates AS (
    SELECT
        student_id,
        COUNT(*) AS certificates_issued
    FROM silver.student_certificates
    GROUP BY student_id
),
minutes AS (
    SELECT
        student_id,
        ROUND(SUM(seconds_watched) / 60.0, 2) AS minutes_watched
    FROM silver.student_video_watched
    GROUP BY student_id
)
SELECT
    certificates.student_id,
    COALESCE(minutes.minutes_watched, 0.0) AS minutes_watched,
    certificates.certificates_issued
FROM certificates
LEFT JOIN minutes USING (student_id);
