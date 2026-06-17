CREATE SCHEMA IF NOT EXISTS gold;

CREATE OR REPLACE TABLE gold.mart_daily_checkout_steps AS
WITH total_carts_created AS (
    SELECT
        action_date,
        COUNT(*) AS count_total_carts
    FROM silver.checkout_carts
    GROUP BY action_date
),
total_checkout_attempts AS (
    SELECT
        action_date,
        COUNT(*) AS count_total_checkout_attempts
    FROM silver.checkout_attempts
    GROUP BY action_date
),
successful_checkout_attempts AS (
    SELECT
        action_date,
        COUNT(*) AS count_successful_checkout_attempts
    FROM silver.successful_checkout_attempts
    GROUP BY action_date
),
date_spine AS (
    SELECT action_date FROM total_carts_created
    UNION
    SELECT action_date FROM total_checkout_attempts
    UNION
    SELECT action_date FROM successful_checkout_attempts
)
SELECT
    date_spine.action_date,
    COALESCE(total_carts_created.count_total_carts, 0) AS count_total_carts,
    COALESCE(total_checkout_attempts.count_total_checkout_attempts, 0) AS count_total_checkout_attempts,
    COALESCE(successful_checkout_attempts.count_successful_checkout_attempts, 0) AS count_successful_checkout_attempts
FROM date_spine
LEFT JOIN total_carts_created USING (action_date)
LEFT JOIN total_checkout_attempts USING (action_date)
LEFT JOIN successful_checkout_attempts USING (action_date)
ORDER BY date_spine.action_date;

CREATE OR REPLACE TABLE gold.mart_monthly_checkout AS
SELECT
    CAST(date_trunc('month', action_date) AS DATE) AS checkout_month,
    SUM(count_total_carts) AS count_total_carts,
    SUM(count_total_checkout_attempts) AS count_total_checkout_attempts,
    SUM(count_successful_checkout_attempts) AS count_successful_checkout_attempts,
    SUM(count_total_checkout_attempts) - SUM(count_successful_checkout_attempts) AS count_failed_checkout_attempts,
    ROUND(SUM(count_successful_checkout_attempts)::DOUBLE / NULLIF(SUM(count_total_checkout_attempts), 0), 4) AS checkout_success_rate,
    ROUND((SUM(count_total_carts) - SUM(count_total_checkout_attempts))::DOUBLE / NULLIF(SUM(count_total_carts), 0), 4) AS cart_abandonment_rate
FROM gold.mart_daily_checkout_steps
GROUP BY checkout_month
ORDER BY checkout_month;

CREATE OR REPLACE TABLE gold.mart_checkout_errors AS
SELECT
    error_message,
    device,
    COUNT(*) AS attempt_count
FROM silver.checkout_errors
GROUP BY error_message, device;

CREATE OR REPLACE TABLE gold.mart_error_rankings AS
WITH by_error AS (
    SELECT
        error_message,
        SUM(attempt_count) AS total_attempts,
        SUM(CASE WHEN device = 'desktop' THEN attempt_count ELSE 0 END) AS desktop_attempts,
        SUM(CASE WHEN device = 'mobile' THEN attempt_count ELSE 0 END) AS mobile_attempts
    FROM gold.mart_checkout_errors
    GROUP BY error_message
)
SELECT
    ROW_NUMBER() OVER (ORDER BY total_attempts DESC, error_message) AS rank,
    error_message,
    total_attempts,
    desktop_attempts,
    mobile_attempts,
    ROUND(desktop_attempts::DOUBLE / NULLIF(total_attempts, 0), 4) AS desktop_share,
    ROUND(mobile_attempts::DOUBLE / NULLIF(total_attempts, 0), 4) AS mobile_share
FROM by_error
ORDER BY rank;

CREATE OR REPLACE TABLE gold.mart_device_distribution AS
WITH device_counts AS (
    SELECT
        device,
        COUNT(*) AS checkout_attempts
    FROM silver.checkout_attempts
    GROUP BY device
),
totals AS (
    SELECT SUM(checkout_attempts) AS total_attempts FROM device_counts
)
SELECT
    device,
    checkout_attempts,
    ROUND(checkout_attempts::DOUBLE / NULLIF(total_attempts, 0), 4) AS attempt_share
FROM device_counts
CROSS JOIN totals
ORDER BY checkout_attempts DESC;

CREATE OR REPLACE TABLE gold.mart_monthly_error_device AS
SELECT
    CAST(date_trunc('month', action_date) AS DATE) AS checkout_month,
    error_message,
    device,
    COUNT(*) AS attempt_count
FROM silver.checkout_errors
GROUP BY checkout_month, error_message, device;

CREATE OR REPLACE TABLE gold.mart_summary_kpis AS
WITH kpi AS (
    SELECT
        SUM(count_total_carts) AS total_carts,
        SUM(count_total_checkout_attempts) AS total_checkout_attempts,
        SUM(count_successful_checkout_attempts) AS successful_checkout_attempts
    FROM gold.mart_monthly_checkout
),
errors AS (
    SELECT
        error_message AS most_common_error,
        total_attempts AS most_common_error_attempts
    FROM gold.mart_error_rankings
    WHERE rank = 1
)
SELECT
    total_carts,
    total_checkout_attempts,
    successful_checkout_attempts,
    total_checkout_attempts - successful_checkout_attempts AS failed_checkout_attempts,
    ROUND(successful_checkout_attempts::DOUBLE / NULLIF(total_checkout_attempts, 0), 4) AS checkout_success_rate,
    ROUND((total_carts - total_checkout_attempts)::DOUBLE / NULLIF(total_carts, 0), 4) AS cart_abandonment_rate,
    most_common_error,
    most_common_error_attempts
FROM kpi
CROSS JOIN errors;

CREATE OR REPLACE TABLE gold.mart_quiz_answers AS
WITH highest_attempts AS (
    SELECT * FROM gold.mart_monthly_checkout
    ORDER BY count_total_checkout_attempts DESC, checkout_month
    LIMIT 1
),
lowest_attempts AS (
    SELECT * FROM gold.mart_monthly_checkout
    ORDER BY count_total_checkout_attempts ASC, checkout_month
    LIMIT 1
),
highest_carts AS (
    SELECT * FROM gold.mart_monthly_checkout
    ORDER BY count_total_carts DESC, checkout_month
    LIMIT 1
),
highest_abandonment AS (
    SELECT
        string_agg(strftime(checkout_month, '%B %Y'), ' and ' ORDER BY cart_abandonment_rate DESC, checkout_month) AS answer_value,
        string_agg(CAST(cart_abandonment_rate AS VARCHAR), ', ' ORDER BY cart_abandonment_rate DESC, checkout_month) AS support_value
    FROM (
        SELECT *
        FROM gold.mart_monthly_checkout
        ORDER BY cart_abandonment_rate DESC, checkout_month
        LIMIT 2
    )
),
september_desktop_error AS (
    SELECT
        error_message,
        SUM(attempt_count) AS attempts
    FROM gold.mart_monthly_error_device
    WHERE checkout_month = DATE '2022-09-01'
      AND device = 'desktop'
    GROUP BY error_message
    ORDER BY attempts DESC, error_message
    LIMIT 1
),
third_overall_error AS (
    SELECT * FROM gold.mart_error_rankings WHERE rank = 3
),
third_desktop_error AS (
    SELECT
        error_message,
        ROW_NUMBER() OVER (ORDER BY SUM(attempt_count) DESC, error_message) AS desktop_rank
    FROM gold.mart_checkout_errors
    WHERE device = 'desktop'
    GROUP BY error_message
    QUALIFY desktop_rank = 3
)
SELECT
    1 AS question_number,
    'Highest monthly checkout attempts' AS question,
    strftime(checkout_month, '%B %Y') AS answer_value,
    CAST(count_total_checkout_attempts AS VARCHAR) AS support_value,
    'data-derived' AS answer_basis
FROM highest_attempts
UNION ALL
SELECT
    2,
    'Lowest monthly checkout attempts',
    strftime(checkout_month, '%B %Y') || ', ' || CAST(count_total_checkout_attempts AS VARCHAR) || ' attempts',
    CAST(count_total_checkout_attempts AS VARCHAR),
    'data-derived'
FROM lowest_attempts
UNION ALL
SELECT
    3,
    'Highest monthly purchase carts',
    strftime(checkout_month, '%B %Y'),
    CAST(count_total_carts AS VARCHAR),
    'data-derived'
FROM highest_carts
UNION ALL
SELECT
    4,
    'Two highest monthly cart abandonment rates',
    answer_value,
    support_value,
    'data-derived'
FROM highest_abandonment
UNION ALL
SELECT
    5,
    'Most frequent desktop error in September 2022',
    error_message,
    CAST(attempts AS VARCHAR),
    'data-derived'
FROM september_desktop_error
UNION ALL
SELECT
    6,
    'Third most common overall error',
    error_message,
    CAST(total_attempts AS VARCHAR),
    'data-derived'
FROM third_overall_error
UNION ALL
SELECT
    7,
    'Third most common desktop error',
    error_message,
    CAST(desktop_rank AS VARCHAR),
    'data-derived'
FROM third_desktop_error
UNION ALL
SELECT
    8,
    'Opportunity size using prompt assumptions',
    '$648',
    '((0.40 - 0.34) * 360 * 30)',
    'course-prompt-assumption';
