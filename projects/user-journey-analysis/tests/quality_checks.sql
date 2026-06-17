WITH cleaned_sequence_failures AS (
    SELECT
        scenario,
        user_id,
        string_split(user_journey, '-') AS pages
    FROM silver.grouped_journeys
),
duplicate_failures AS (
    SELECT COUNT(*) AS failures
    FROM cleaned_sequence_failures,
         range(1, len(pages)) AS idx(i)
    WHERE pages[i] = pages[i + 1]
)
SELECT 'bronze_raw_row_count' AS check_name,
       CASE WHEN (SELECT COUNT(*) FROM bronze.raw_user_journeys) = 9935 THEN 0 ELSE 1 END AS failures
UNION ALL
SELECT 'bronze_unique_users' AS check_name,
       CASE WHEN (SELECT COUNT(DISTINCT user_id) FROM bronze.raw_user_journeys) = 1350 THEN 0 ELSE 1 END AS failures
UNION ALL
SELECT 'bronze_unique_sessions' AS check_name,
       CASE WHEN (SELECT COUNT(DISTINCT session_id) FROM bronze.raw_user_journeys) = 9935 THEN 0 ELSE 1 END AS failures
UNION ALL
SELECT 'valid_subscription_types' AS check_name,
       COUNT(*) AS failures
FROM silver.cleaned_sessions
WHERE subscription_type NOT IN ('Annual', 'Monthly', 'Quarterly')
UNION ALL
SELECT 'no_consecutive_duplicate_pages' AS check_name,
       failures
FROM duplicate_failures
UNION ALL
SELECT 'first_three_grouped_record_count' AS check_name,
       CASE WHEN (
           SELECT COUNT(*)
           FROM silver.grouped_journeys
           WHERE scenario = 'first_3_sessions'
       ) = 1350 THEN 0 ELSE 1 END AS failures
UNION ALL
SELECT 'quarterly_third_page_is_sign_up' AS check_name,
       CASE WHEN (
           SELECT page
           FROM gold.mart_page_count
           WHERE scenario = 'all_sessions'
             AND subscription_type = 'Quarterly'
             AND rank = 3
       ) = 'Sign up' THEN 0 ELSE 1 END AS failures
UNION ALL
SELECT 'pricing_fourth_destination_is_courses' AS check_name,
       CASE WHEN (
           SELECT next_page
           FROM gold.mart_page_destinations
           WHERE scenario = 'all_sessions'
             AND subscription_type = 'All'
             AND source_page = 'Pricing'
             AND rank = 4
       ) = 'Courses' THEN 0 ELSE 1 END AS failures
UNION ALL
SELECT 'last_three_avg_length_is_3_6' AS check_name,
       CASE WHEN (
           SELECT avg_journey_length
           FROM gold.mart_journey_length
           WHERE scenario = 'last_3_sessions'
             AND subscription_type = 'All'
       ) = 3.6 THEN 0 ELSE 1 END AS failures
UNION ALL
SELECT 'last_three_fourth_presence_is_homepage' AS check_name,
       CASE WHEN (
           SELECT page
           FROM gold.mart_page_presence
           WHERE scenario = 'last_3_sessions'
             AND subscription_type = 'All'
             AND rank = 4
       ) = 'Homepage' THEN 0 ELSE 1 END AS failures
UNION ALL
SELECT 'last_three_top_four_sequence_count_is_49' AS check_name,
       CASE WHEN (
           SELECT journey_count
           FROM gold.mart_page_sequences
           WHERE scenario = 'last_3_sessions'
             AND subscription_type = 'All'
             AND sequence_length = 4
             AND rank = 1
       ) = 49 THEN 0 ELSE 1 END AS failures;
