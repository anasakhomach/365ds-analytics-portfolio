CREATE SCHEMA IF NOT EXISTS silver;

CREATE OR REPLACE TABLE silver.course_info AS
SELECT
    course_id,
    course_title
FROM bronze.course_info;

CREATE OR REPLACE TABLE silver.course_ratings AS
SELECT
    course_id,
    student_id,
    course_rating,
    date_rated
FROM bronze.course_ratings;

CREATE OR REPLACE TABLE silver.student_info AS
SELECT
    student_id,
    student_country,
    COALESCE(country_name, student_country) AS country_name,
    date_registered
FROM bronze.student_info
LEFT JOIN tmp_country_lookup USING (student_country);

CREATE OR REPLACE TABLE silver.student_learning AS
SELECT
    student_id,
    course_id,
    ROUND(minutes_watched, 2) AS minutes_watched,
    date_watched
FROM bronze.student_learning;

CREATE OR REPLACE TABLE silver.student_purchases AS
SELECT
    purchase_id,
    student_id,
    purchase_type,
    date_purchased
FROM bronze.student_purchases;

CREATE OR REPLACE TABLE silver.purchases_info AS
SELECT
    purchase_id,
    student_id,
    purchase_type,
    date_purchased AS date_start,
    CASE purchase_type
        WHEN 'Monthly' THEN date_purchased + INTERVAL 1 MONTH
        WHEN 'Quarterly' THEN date_purchased + INTERVAL 3 MONTH
        WHEN 'Annual' THEN date_purchased + INTERVAL 12 MONTH
    END::DATE AS date_end
FROM silver.student_purchases;

CREATE OR REPLACE TABLE silver.student_engagement AS
WITH engagement_base AS (
    SELECT
        student_id,
        student_country,
        country_name,
        date_registered,
        date_watched,
        COALESCE(minutes_watched, 0.0) AS minutes_watched,
        CASE WHEN date_watched IS NULL THEN 0 ELSE 1 END AS onboarded
    FROM silver.student_info
    LEFT JOIN silver.student_learning USING (student_id)
),
engagement_with_paid AS (
    SELECT
        engagement_base.*,
        CASE
            WHEN date_watched BETWEEN date_start AND date_end THEN 1
            ELSE 0
        END AS paid_flag
    FROM engagement_base
    LEFT JOIN silver.purchases_info USING (student_id)
)
SELECT
    student_id,
    student_country,
    country_name,
    date_registered,
    date_watched,
    ROUND(minutes_watched, 2) AS minutes_watched,
    onboarded,
    MAX(paid_flag) AS paid
FROM engagement_with_paid
GROUP BY
    student_id,
    student_country,
    country_name,
    date_registered,
    date_watched,
    minutes_watched,
    onboarded;
