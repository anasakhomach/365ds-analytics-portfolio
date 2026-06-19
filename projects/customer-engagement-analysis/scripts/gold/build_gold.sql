CREATE SCHEMA IF NOT EXISTS gold;

CREATE OR REPLACE TABLE gold.mart_student_engagement AS
SELECT
    student_id,
    student_country,
    country_name,
    date_registered,
    date_watched,
    minutes_watched,
    onboarded,
    paid
FROM silver.student_engagement;

CREATE OR REPLACE TABLE gold.mart_course_performance AS
WITH course_minutes AS (
    SELECT
        course_id,
        course_title,
        ROUND(COALESCE(SUM(minutes_watched), 0), 2) AS total_minutes_watched,
        COUNT(DISTINCT student_id) AS students_started
    FROM silver.course_info
    LEFT JOIN silver.student_learning USING (course_id)
    GROUP BY course_id, course_title
),
course_ratings AS (
    SELECT
        course_id,
        COUNT(*) AS number_of_ratings,
        ROUND(AVG(course_rating), 2) AS average_rating
    FROM silver.course_ratings
    GROUP BY course_id
)
SELECT
    ROW_NUMBER() OVER (ORDER BY total_minutes_watched DESC, course_title) AS course_rank,
    course_id,
    course_title,
    total_minutes_watched,
    ROUND(total_minutes_watched / NULLIF(students_started, 0), 2) AS average_minutes,
    COALESCE(number_of_ratings, 0) AS number_of_ratings,
    COALESCE(average_rating, 0) AS average_rating
FROM course_minutes
LEFT JOIN course_ratings USING (course_id)
ORDER BY course_rank;

CREATE OR REPLACE TABLE gold.mart_monthly_engagement AS
WITH typed_engagement AS (
    SELECT
        'All' AS user_type,
        date_watched,
        student_id,
        minutes_watched
    FROM gold.mart_student_engagement
    WHERE date_watched IS NOT NULL
    UNION ALL
    SELECT
        CASE WHEN paid = 1 THEN 'Paid' ELSE 'Free' END AS user_type,
        date_watched,
        student_id,
        minutes_watched
    FROM gold.mart_student_engagement
    WHERE date_watched IS NOT NULL
)
SELECT
    CAST(date_trunc('month', date_watched) AS DATE) AS watched_month,
    user_type,
    ROUND(SUM(minutes_watched), 2) AS total_minutes_watched,
    COUNT(DISTINCT student_id) AS engaged_students,
    ROUND(SUM(minutes_watched) / NULLIF(COUNT(DISTINCT student_id), 0), 2) AS average_minutes_watched
FROM typed_engagement
GROUP BY watched_month, user_type
ORDER BY watched_month, user_type;

CREATE OR REPLACE TABLE gold.mart_monthly_registrations AS
WITH typed_engagement AS (
    SELECT
        'All' AS user_type,
        date_registered,
        student_id,
        onboarded
    FROM gold.mart_student_engagement
    UNION ALL
    SELECT
        CASE WHEN paid = 1 THEN 'Paid' ELSE 'Free' END AS user_type,
        date_registered,
        student_id,
        onboarded
    FROM gold.mart_student_engagement
)
SELECT
    CAST(date_trunc('month', date_registered) AS DATE) AS registration_month,
    user_type,
    COUNT(DISTINCT student_id) AS registered_students,
    COUNT(DISTINCT CASE WHEN onboarded = 1 THEN student_id END) AS onboarded_students,
    ROUND(
        COUNT(DISTINCT CASE WHEN onboarded = 1 THEN student_id END)::DOUBLE
        / NULLIF(COUNT(DISTINCT student_id), 0),
        4
    ) AS onboarding_rate
FROM typed_engagement
GROUP BY registration_month, user_type
ORDER BY registration_month, user_type;

CREATE OR REPLACE TABLE gold.mart_country_registered AS
WITH typed_engagement AS (
    SELECT
        'All' AS user_type,
        student_id,
        student_country,
        country_name,
        date_registered
    FROM gold.mart_student_engagement
    UNION ALL
    SELECT
        CASE WHEN paid = 1 THEN 'Paid' ELSE 'Free' END AS user_type,
        student_id,
        student_country,
        country_name,
        date_registered
    FROM gold.mart_student_engagement
)
SELECT
    CAST(date_trunc('month', date_registered) AS DATE) AS registration_month,
    user_type,
    student_country,
    country_name,
    COUNT(DISTINCT student_id) AS registered_students
FROM typed_engagement
GROUP BY registration_month, user_type, student_country, country_name;

CREATE OR REPLACE TABLE gold.mart_country_minutes AS
WITH typed_engagement AS (
    SELECT
        'All' AS user_type,
        student_id,
        student_country,
        country_name,
        date_registered,
        minutes_watched
    FROM gold.mart_student_engagement
    WHERE date_watched IS NOT NULL
    UNION ALL
    SELECT
        CASE WHEN paid = 1 THEN 'Paid' ELSE 'Free' END AS user_type,
        student_id,
        student_country,
        country_name,
        date_registered,
        minutes_watched
    FROM gold.mart_student_engagement
    WHERE date_watched IS NOT NULL
)
SELECT
    CAST(date_trunc('month', date_registered) AS DATE) AS registration_month,
    user_type,
    student_country,
    country_name,
    ROUND(SUM(minutes_watched), 2) AS total_minutes_watched,
    COUNT(DISTINCT student_id) AS engaged_students
FROM typed_engagement
GROUP BY registration_month, user_type, student_country, country_name;

CREATE OR REPLACE TABLE gold.mart_summary_kpis AS
WITH totals AS (
    SELECT
        COUNT(DISTINCT student_id) AS registered_students,
        COUNT(DISTINCT CASE WHEN onboarded = 1 THEN student_id END) AS onboarded_students,
        COUNT(DISTINCT CASE WHEN date_watched IS NOT NULL THEN student_id END) AS engaged_students,
        ROUND(SUM(minutes_watched), 2) AS total_minutes_watched,
        ROUND(
            SUM(minutes_watched) / NULLIF(COUNT(DISTINCT CASE WHEN date_watched IS NOT NULL THEN student_id END), 0),
            2
        ) AS average_minutes_watched,
        ROUND(
            COUNT(DISTINCT CASE WHEN onboarded = 1 THEN student_id END)::DOUBLE
            / NULLIF(COUNT(DISTINCT student_id), 0),
            4
        ) AS onboarding_rate
    FROM gold.mart_student_engagement
),
by_type AS (
    SELECT
        SUM(CASE WHEN paid = 1 THEN minutes_watched ELSE 0 END)
        / NULLIF(COUNT(DISTINCT CASE WHEN paid = 1 AND date_watched IS NOT NULL THEN student_id END), 0)
            AS paid_average_minutes_watched_raw,
        SUM(CASE WHEN paid = 0 THEN minutes_watched ELSE 0 END)
        / NULLIF(COUNT(DISTINCT CASE WHEN paid = 0 AND date_watched IS NOT NULL THEN student_id END), 0)
            AS free_average_minutes_watched_raw
    FROM gold.mart_student_engagement
)
SELECT
    registered_students,
    onboarded_students,
    engaged_students,
    total_minutes_watched,
    average_minutes_watched,
    onboarding_rate,
    ROUND(paid_average_minutes_watched_raw, 2) AS paid_average_minutes_watched,
    ROUND(free_average_minutes_watched_raw, 2) AS free_average_minutes_watched,
    ROUND(paid_average_minutes_watched_raw / NULLIF(free_average_minutes_watched_raw, 0), 2) AS paid_to_free_average_ratio
FROM totals
CROSS JOIN by_type;

CREATE OR REPLACE TABLE gold.mart_quiz_answers AS
WITH second_course AS (
    SELECT * FROM gold.mart_course_performance WHERE course_rank = 2
),
august_top_country AS (
    SELECT *
    FROM gold.mart_country_registered
    WHERE registration_month = DATE '2022-08-01'
      AND user_type = 'All'
    ORDER BY registered_students DESC, country_name
    LIMIT 1
),
september_fifth_country AS (
    SELECT *
    FROM gold.mart_country_registered
    WHERE registration_month = DATE '2022-09-01'
      AND user_type = 'All'
    ORDER BY registered_students DESC, country_name
    LIMIT 1 OFFSET 4
),
july_free_minutes_country AS (
    SELECT *
    FROM gold.mart_country_minutes
    WHERE registration_month = DATE '2022-07-01'
      AND user_type = 'Free'
    ORDER BY total_minutes_watched DESC, country_name
    LIMIT 1
),
july_paid_minutes_country AS (
    SELECT *
    FROM gold.mart_country_minutes
    WHERE registration_month = DATE '2022-07-01'
      AND user_type = 'Paid'
    ORDER BY total_minutes_watched DESC, country_name
    LIMIT 1
),
highest_paid_average AS (
    SELECT *
    FROM gold.mart_monthly_engagement
    WHERE user_type = 'Paid'
    ORDER BY average_minutes_watched DESC, watched_month
    LIMIT 1
),
highest_free_minutes AS (
    SELECT *
    FROM gold.mart_monthly_engagement
    WHERE user_type = 'Free'
    ORDER BY total_minutes_watched DESC, watched_month
    LIMIT 1
),
lowest_onboarding AS (
    SELECT *
    FROM gold.mart_monthly_registrations
    WHERE user_type = 'All'
    ORDER BY onboarding_rate ASC, registration_month
    LIMIT 1
)
SELECT
    1 AS question_number,
    'Second course by total minutes watched' AS question,
    course_title AS answer_value,
    CAST(total_minutes_watched AS VARCHAR) AS support_value,
    'data-derived' AS answer_basis
FROM second_course
UNION ALL
SELECT
    2,
    'Top country by registered students in August 2022',
    country_name || ', ' || CAST(registered_students AS VARCHAR) || ' students',
    CAST(registered_students AS VARCHAR),
    'data-derived'
FROM august_top_country
UNION ALL
SELECT
    3,
    'Fifth country by registered students in September 2022',
    country_name,
    CAST(registered_students AS VARCHAR),
    'data-derived'
FROM september_fifth_country
UNION ALL
SELECT
    4,
    'Top country by free-plan minutes for July registrations',
    country_name,
    CAST(total_minutes_watched AS VARCHAR),
    'data-derived'
FROM july_free_minutes_country
UNION ALL
SELECT
    5,
    'Top country by paying-student minutes for July registrations',
    country_name,
    CAST(total_minutes_watched AS VARCHAR),
    'data-derived'
FROM july_paid_minutes_country
UNION ALL
SELECT
    6,
    'Highest monthly average minutes watched by paying students',
    CAST(average_minutes_watched AS VARCHAR),
    strftime(watched_month, '%B %Y'),
    'data-derived'
FROM highest_paid_average
UNION ALL
SELECT
    7,
    'Highest monthly minutes watched by free-plan students',
    CAST(total_minutes_watched AS VARCHAR),
    strftime(watched_month, '%B %Y'),
    'data-derived'
FROM highest_free_minutes
UNION ALL
SELECT
    8,
    'Lowest monthly onboarding rate',
    strftime(registration_month, '%B %Y'),
    CAST(onboarding_rate AS VARCHAR),
    'data-derived'
FROM lowest_onboarding
UNION ALL
SELECT
    9,
    'Overall onboarding rate',
    CAST(onboarding_rate AS VARCHAR),
    CAST(onboarded_students AS VARCHAR) || ' / ' || CAST(registered_students AS VARCHAR),
    'data-derived'
FROM gold.mart_summary_kpis
UNION ALL
SELECT
    10,
    'Paying to free-plan average minutes watched ratio',
    CAST(paid_to_free_average_ratio AS VARCHAR),
    'Question text is truncated in the converted brief',
    'data-derived'
FROM gold.mart_summary_kpis;
