SELECT 'bronze_customers_row_count' AS check_name,
       CASE WHEN (SELECT COUNT(*) FROM bronze.raw_customers) = 162 THEN 0 ELSE 1 END AS failures
UNION ALL
SELECT 'bronze_properties_row_count' AS check_name,
       CASE WHEN (SELECT COUNT(*) FROM bronze.raw_properties) = 267 THEN 0 ELSE 1 END AS failures
UNION ALL
SELECT 'sold_properties_have_customer_id' AS check_name,
       COUNT(*) AS failures
FROM silver.cleaned_properties
WHERE sold_flag AND customer_id IS NULL
UNION ALL
SELECT 'sold_properties_have_sale_date' AS check_name,
       COUNT(*) AS failures
FROM silver.cleaned_properties
WHERE sold_flag AND sale_date IS NULL
UNION ALL
SELECT 'no_negative_property_prices' AS check_name,
       COUNT(*) AS failures
FROM silver.cleaned_properties
WHERE price < 0
UNION ALL
SELECT 'no_orphan_sold_customers' AS check_name,
       COUNT(*) AS failures
FROM silver.cleaned_properties p
LEFT JOIN silver.cleaned_customers c USING (customer_id)
WHERE p.sold_flag AND c.customer_id IS NULL
UNION ALL
SELECT 'gold_summary_exists' AS check_name,
       CASE WHEN (SELECT COUNT(*) FROM gold.mart_summary_kpis) = 1 THEN 0 ELSE 1 END AS failures
UNION ALL
SELECT 'age_price_correlation_in_range' AS check_name,
       COUNT(*) AS failures
FROM gold.mart_correlation_metrics
WHERE correlation IS NOT NULL AND (correlation < -1 OR correlation > 1);
