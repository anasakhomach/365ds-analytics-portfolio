WITH checks AS (
    SELECT
        'bronze_checkout_actions_row_count' AS check_name,
        CASE WHEN (SELECT COUNT(*) FROM bronze.checkout_actions) = 12542 THEN 0 ELSE 1 END AS failures
    UNION ALL
    SELECT
        'bronze_checkout_carts_row_count',
        CASE WHEN (SELECT COUNT(*) FROM bronze.checkout_carts) = 5946 THEN 0 ELSE 1 END
    UNION ALL
    SELECT
        'bronze_checkout_actions_min_date',
        CASE WHEN (SELECT MIN(action_date) FROM bronze.checkout_actions) = DATE '2022-07-01' THEN 0 ELSE 1 END
    UNION ALL
    SELECT
        'bronze_checkout_actions_max_date',
        CASE WHEN (SELECT MAX(action_date) FROM bronze.checkout_actions) = DATE '2023-01-31' THEN 0 ELSE 1 END
    UNION ALL
    SELECT
        'bronze_checkout_carts_min_date',
        CASE WHEN (SELECT MIN(action_date) FROM bronze.checkout_carts) = DATE '2022-07-01' THEN 0 ELSE 1 END
    UNION ALL
    SELECT
        'bronze_checkout_carts_max_date',
        CASE WHEN (SELECT MAX(action_date) FROM bronze.checkout_carts) = DATE '2023-03-31' THEN 0 ELSE 1 END
    UNION ALL
    SELECT
        'silver_analysis_window_end',
        CASE WHEN (SELECT MAX(action_date) FROM silver.checkout_carts) = DATE '2023-01-31' THEN 0 ELSE 1 END
    UNION ALL
    SELECT
        'valid_devices',
        (SELECT COUNT(*) FROM silver.checkout_actions WHERE device NOT IN ('desktop', 'mobile'))
    UNION ALL
    SELECT
        'gold_month_count',
        CASE WHEN (SELECT COUNT(*) FROM gold.mart_monthly_checkout) = 7 THEN 0 ELSE 1 END
    UNION ALL
    SELECT
        'gold_month_min',
        CASE WHEN (SELECT MIN(checkout_month) FROM gold.mart_monthly_checkout) = DATE '2022-07-01' THEN 0 ELSE 1 END
    UNION ALL
    SELECT
        'gold_month_max',
        CASE WHEN (SELECT MAX(checkout_month) FROM gold.mart_monthly_checkout) = DATE '2023-01-01' THEN 0 ELSE 1 END
    UNION ALL
    SELECT
        'dashboard_kpi_row',
        CASE WHEN (SELECT COUNT(*) FROM gold.mart_summary_kpis) = 1 THEN 0 ELSE 1 END
    UNION ALL
    SELECT
        'quiz_answer_count',
        CASE WHEN (SELECT COUNT(*) FROM gold.mart_quiz_answers) = 8 THEN 0 ELSE 1 END
)
SELECT check_name, failures
FROM checks
ORDER BY check_name;
