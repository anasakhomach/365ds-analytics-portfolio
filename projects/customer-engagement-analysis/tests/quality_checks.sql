WITH checks AS (
    SELECT
        'bronze_course_info_row_count' AS check_name,
        CASE WHEN (SELECT COUNT(*) FROM bronze.course_info) = 46 THEN 0 ELSE 1 END AS failures
    UNION ALL
    SELECT
        'bronze_course_ratings_row_count',
        CASE WHEN (SELECT COUNT(*) FROM bronze.course_ratings) = 2500 THEN 0 ELSE 1 END
    UNION ALL
    SELECT
        'bronze_student_info_row_count',
        CASE WHEN (SELECT COUNT(*) FROM bronze.student_info) = 35230 THEN 0 ELSE 1 END
    UNION ALL
    SELECT
        'bronze_student_learning_row_count',
        CASE WHEN (SELECT COUNT(*) FROM bronze.student_learning) = 64458 THEN 0 ELSE 1 END
    UNION ALL
    SELECT
        'bronze_student_purchases_row_count',
        CASE WHEN (SELECT COUNT(*) FROM bronze.student_purchases) = 3041 THEN 0 ELSE 1 END
    UNION ALL
    SELECT
        'student_learning_insert_blocks',
        CASE WHEN (SELECT insert_blocks FROM bronze.load_metadata WHERE source_table = 'student_learning') = 2 THEN 0 ELSE 1 END
    UNION ALL
    SELECT
        'purchases_info_row_count',
        CASE WHEN (SELECT COUNT(*) FROM silver.purchases_info) = 3041 THEN 0 ELSE 1 END
    UNION ALL
    SELECT
        'student_engagement_row_count',
        CASE WHEN (SELECT COUNT(*) FROM silver.student_engagement) = 81532 THEN 0 ELSE 1 END
    UNION ALL
    SELECT
        'student_learning_minutes_reconcile',
        CASE
            WHEN (SELECT ROUND(SUM(minutes_watched), 2) FROM silver.student_learning)
               = (SELECT ROUND(SUM(minutes_watched), 2) FROM silver.student_engagement)
             AND (SELECT ROUND(SUM(minutes_watched), 2) FROM silver.student_learning) = 1835588.10
            THEN 0 ELSE 1
        END
    UNION ALL
    SELECT
        'date_registered_min',
        CASE WHEN (SELECT MIN(date_registered) FROM silver.student_engagement) = DATE '2022-01-01' THEN 0 ELSE 1 END
    UNION ALL
    SELECT
        'date_registered_max',
        CASE WHEN (SELECT MAX(date_registered) FROM silver.student_engagement) = DATE '2022-10-20' THEN 0 ELSE 1 END
    UNION ALL
    SELECT
        'date_watched_min',
        CASE WHEN (SELECT MIN(date_watched) FROM silver.student_engagement) = DATE '2022-01-01' THEN 0 ELSE 1 END
    UNION ALL
    SELECT
        'date_watched_max',
        CASE WHEN (SELECT MAX(date_watched) FROM silver.student_engagement) = DATE '2022-10-20' THEN 0 ELSE 1 END
    UNION ALL
    SELECT
        'valid_paid_values',
        (SELECT COUNT(*) FROM silver.student_engagement WHERE paid NOT IN (0, 1))
    UNION ALL
    SELECT
        'valid_onboarded_values',
        (SELECT COUNT(*) FROM silver.student_engagement WHERE onboarded NOT IN (0, 1))
    UNION ALL
    SELECT
        'gold_course_mart_row_count',
        CASE WHEN (SELECT COUNT(*) FROM gold.mart_course_performance) = 46 THEN 0 ELSE 1 END
    UNION ALL
    SELECT
        'quiz_q1_second_course',
        CASE WHEN EXISTS (
            SELECT 1 FROM gold.mart_quiz_answers
            WHERE question_number = 1 AND answer_value = 'SQL'
        ) THEN 0 ELSE 1 END
    UNION ALL
    SELECT
        'quiz_q2_august_top_country',
        CASE WHEN EXISTS (
            SELECT 1 FROM gold.mart_quiz_answers
            WHERE question_number = 2 AND answer_value LIKE 'India,%' AND support_value = '996'
        ) THEN 0 ELSE 1 END
    UNION ALL
    SELECT
        'quiz_q3_september_fifth_country',
        CASE WHEN EXISTS (
            SELECT 1 FROM gold.mart_quiz_answers
            WHERE question_number = 3 AND answer_value = 'Nigeria'
        ) THEN 0 ELSE 1 END
    UNION ALL
    SELECT
        'quiz_q6_highest_paid_average',
        CASE WHEN EXISTS (
            SELECT 1 FROM gold.mart_quiz_answers
            WHERE question_number = 6 AND ROUND(CAST(answer_value AS DOUBLE), 2) = 291.47
        ) THEN 0 ELSE 1 END
    UNION ALL
    SELECT
        'quiz_q7_highest_free_minutes',
        CASE WHEN EXISTS (
            SELECT 1 FROM gold.mart_quiz_answers
            WHERE question_number = 7 AND ROUND(CAST(answer_value AS DOUBLE), 1) = 146258.9
        ) THEN 0 ELSE 1 END
    UNION ALL
    SELECT
        'quiz_q8_lowest_onboarding_month',
        CASE WHEN EXISTS (
            SELECT 1 FROM gold.mart_quiz_answers
            WHERE question_number = 8 AND answer_value = 'June 2022'
        ) THEN 0 ELSE 1 END
    UNION ALL
    SELECT
        'quiz_q9_onboarding_rate',
        CASE WHEN EXISTS (
            SELECT 1 FROM gold.mart_quiz_answers
            WHERE question_number = 9 AND ROUND(CAST(answer_value AS DOUBLE), 4) = 0.5154
        ) THEN 0 ELSE 1 END
    UNION ALL
    SELECT
        'quiz_q10_paid_free_ratio',
        CASE WHEN EXISTS (
            SELECT 1 FROM gold.mart_quiz_answers
            WHERE question_number = 10 AND ROUND(CAST(answer_value AS DOUBLE), 2) = 23.12
        ) THEN 0 ELSE 1 END
)
SELECT check_name, failures
FROM checks
ORDER BY check_name;
