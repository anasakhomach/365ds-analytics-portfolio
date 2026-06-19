WITH checks AS (
    SELECT
        'bronze_student_certificates_row_count' AS check_name,
        CASE WHEN (SELECT COUNT(*) FROM bronze.student_certificates) = 1751 THEN 0 ELSE 1 END AS failures
    UNION ALL
    SELECT
        'bronze_student_info_row_count',
        CASE WHEN (SELECT COUNT(*) FROM bronze.student_info) = 270275 THEN 0 ELSE 1 END
    UNION ALL
    SELECT
        'bronze_student_purchases_row_count',
        CASE WHEN (SELECT COUNT(*) FROM bronze.student_purchases) = 18207 THEN 0 ELSE 1 END
    UNION ALL
    SELECT
        'bronze_student_video_watched_row_count',
        CASE WHEN (SELECT COUNT(*) FROM bronze.student_video_watched) = 86035 THEN 0 ELSE 1 END
    UNION ALL
    SELECT
        'student_info_insert_blocks',
        CASE WHEN (SELECT insert_blocks FROM bronze.load_metadata WHERE source_table = 'student_info') = 6 THEN 0 ELSE 1 END
    UNION ALL
    SELECT
        'student_video_watched_insert_blocks',
        CASE WHEN (SELECT insert_blocks FROM bronze.load_metadata WHERE source_table = 'student_video_watched') = 3 THEN 0 ELSE 1 END
    UNION ALL
    SELECT
        'student_info_date_range',
        CASE
            WHEN (SELECT MIN(date_registered) FROM bronze.student_info) = DATE '2020-01-01'
             AND (SELECT MAX(date_registered) FROM bronze.student_info) = DATE '2022-06-30'
            THEN 0 ELSE 1
        END
    UNION ALL
    SELECT
        'student_video_watched_date_range',
        CASE
            WHEN (SELECT MIN(date_watched) FROM bronze.student_video_watched) = DATE '2021-04-01'
             AND (SELECT MAX(date_watched) FROM bronze.student_video_watched) = DATE '2022-06-30'
            THEN 0 ELSE 1
        END
    UNION ALL
    SELECT
        'valid_plan_ids',
        (SELECT COUNT(*) FROM silver.student_purchases WHERE plan_id NOT IN (0, 1, 2, 3))
    UNION ALL
    SELECT
        'nonnegative_seconds_watched',
        (SELECT COUNT(*) FROM silver.student_video_watched WHERE seconds_watched < 0)
    UNION ALL
    SELECT
        'purchases_info_row_count',
        CASE WHEN (SELECT COUNT(*) FROM silver.purchases_info) = 18207 THEN 0 ELSE 1 END
    UNION ALL
    SELECT
        'q2_2021_watcher_count',
        CASE WHEN (
            SELECT COUNT(*) FROM silver.q2_minutes_watched WHERE engagement_year = 2021
        ) = 7639 THEN 0 ELSE 1 END
    UNION ALL
    SELECT
        'q2_2022_watcher_count',
        CASE WHEN (
            SELECT COUNT(*) FROM silver.q2_minutes_watched WHERE engagement_year = 2022
        ) = 8841 THEN 0 ELSE 1 END
    UNION ALL
    SELECT
        'q2_paid_values',
        (SELECT COUNT(*) FROM silver.q2_paid_flags WHERE paid NOT IN (0, 1))
    UNION ALL
    SELECT
        'split_2021_free_count',
        CASE WHEN (
            SELECT COUNT(*) FROM silver.q2_engagement_segments WHERE engagement_year = 2021 AND paid = 0
        ) = 5334 THEN 0 ELSE 1 END
    UNION ALL
    SELECT
        'split_2022_free_count',
        CASE WHEN (
            SELECT COUNT(*) FROM silver.q2_engagement_segments WHERE engagement_year = 2022 AND paid = 0
        ) = 6055 THEN 0 ELSE 1 END
    UNION ALL
    SELECT
        'split_2021_paid_count',
        CASE WHEN (
            SELECT COUNT(*) FROM silver.q2_engagement_segments WHERE engagement_year = 2021 AND paid = 1
        ) = 2305 THEN 0 ELSE 1 END
    UNION ALL
    SELECT
        'split_2022_paid_count',
        CASE WHEN (
            SELECT COUNT(*) FROM silver.q2_engagement_segments WHERE engagement_year = 2022 AND paid = 1
        ) = 2786 THEN 0 ELSE 1 END
    UNION ALL
    SELECT
        'certificates_minutes_row_count',
        CASE WHEN (SELECT COUNT(*) FROM silver.certificates_minutes) = 658 THEN 0 ELSE 1 END
    UNION ALL
    SELECT
        'no_outliers_2021_free_count',
        CASE WHEN (
            SELECT COUNT(*) FROM gold.mart_q2_engagement_no_outliers WHERE engagement_year = 2021 AND paid = 0
        ) = 5280 THEN 0 ELSE 1 END
    UNION ALL
    SELECT
        'no_outliers_2022_free_count',
        CASE WHEN (
            SELECT COUNT(*) FROM gold.mart_q2_engagement_no_outliers WHERE engagement_year = 2022 AND paid = 0
        ) = 5994 THEN 0 ELSE 1 END
    UNION ALL
    SELECT
        'no_outliers_2021_paid_count',
        CASE WHEN (
            SELECT COUNT(*) FROM gold.mart_q2_engagement_no_outliers WHERE engagement_year = 2021 AND paid = 1
        ) = 2281 THEN 0 ELSE 1 END
    UNION ALL
    SELECT
        'no_outliers_2022_paid_count',
        CASE WHEN (
            SELECT COUNT(*) FROM gold.mart_q2_engagement_no_outliers WHERE engagement_year = 2022 AND paid = 1
        ) = 2758 THEN 0 ELSE 1 END
    UNION ALL
    SELECT
        'free_t_statistic',
        CASE WHEN EXISTS (
            SELECT 1 FROM gold.mart_hypothesis_tests
            WHERE student_plan = 'Free' AND ROUND(t_statistic, 4) = -3.9512
        ) THEN 0 ELSE 1 END
    UNION ALL
    SELECT
        'paid_t_statistic',
        CASE WHEN EXISTS (
            SELECT 1 FROM gold.mart_hypothesis_tests
            WHERE student_plan = 'Paid' AND ROUND(t_statistic, 4) = 5.1544
        ) THEN 0 ELSE 1 END
    UNION ALL
    SELECT
        'certificate_correlation',
        CASE WHEN EXISTS (
            SELECT 1 FROM gold.mart_correlation
            WHERE ROUND(correlation_coefficient, 4) = 0.5126
        ) THEN 0 ELSE 1 END
    UNION ALL
    SELECT
        'regression_r_squared',
        CASE WHEN EXISTS (
            SELECT 1 FROM gold.mart_regression
            WHERE ROUND(r_squared, 4) = 0.4678
        ) THEN 0 ELSE 1 END
    UNION ALL
    SELECT
        'regression_prediction_1200',
        CASE WHEN EXISTS (
            SELECT 1 FROM gold.mart_regression
            WHERE predicted_certificates_rounded_up = 4
        ) THEN 0 ELSE 1 END
    UNION ALL
    SELECT
        'probability_2021_given_2022',
        CASE WHEN EXISTS (
            SELECT 1 FROM gold.mart_watch_probability
            WHERE probability_2021_given_2022 = 0.0724
        ) THEN 0 ELSE 1 END
    UNION ALL
    SELECT
        'quiz_answer_count',
        CASE WHEN (SELECT COUNT(*) FROM gold.mart_quiz_answers) = 14 THEN 0 ELSE 1 END
)
SELECT check_name, failures
FROM checks
ORDER BY check_name;
