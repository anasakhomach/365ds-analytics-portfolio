CREATE SCHEMA IF NOT EXISTS gold;

CREATE OR REPLACE TABLE gold.mart_property_transactions AS
SELECT
    property_id,
    building_id,
    building_label,
    property_number,
    type AS property_type,
    area,
    price,
    status,
    sold_flag,
    customer_id,
    entity,
    sex,
    country,
    state,
    purpose,
    deal_satisfaction,
    has_mortgage,
    sale_date,
    sale_year,
    sale_month,
    revenue,
    age_at_purchase,
    age_interval,
    price_interval
FROM silver.property_transactions;

CREATE OR REPLACE TABLE gold.mart_summary_kpis AS
SELECT
    COUNT(*) AS total_properties,
    SUM(CASE WHEN sold_flag THEN 1 ELSE 0 END) AS sold_properties,
    SUM(CASE WHEN NOT sold_flag THEN 1 ELSE 0 END) AS available_properties,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(AVG(CASE WHEN sold_flag THEN price END), 2) AS avg_sold_price,
    ROUND(AVG(CASE WHEN sold_flag THEN area END), 2) AS avg_sold_area,
    ROUND(AVG(CASE WHEN sold_flag THEN deal_satisfaction END), 2) AS avg_deal_satisfaction,
    ROUND(CORR(age_at_purchase, price), 4) AS age_price_correlation,
    ROUND(COVAR_SAMP(age_at_purchase, price), 2) AS age_price_covariance
FROM silver.property_transactions;

CREATE OR REPLACE TABLE gold.mart_building_performance AS
SELECT
    building_id,
    building_label,
    COUNT(*) AS total_properties,
    SUM(CASE WHEN sold_flag THEN 1 ELSE 0 END) AS sold_properties,
    SUM(CASE WHEN has_mortgage THEN 1 ELSE 0 END) AS mortgage_sales,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(AVG(CASE WHEN sold_flag THEN area END), 2) AS avg_area,
    ROUND(AVG(CASE WHEN sold_flag THEN price END), 2) AS avg_price,
    ROUND(AVG(CASE WHEN sold_flag THEN deal_satisfaction END), 2) AS avg_deal_satisfaction
FROM silver.property_transactions
GROUP BY building_id, building_label
ORDER BY building_id;

CREATE OR REPLACE TABLE gold.mart_country_performance AS
SELECT
    country,
    COUNT(*) FILTER (WHERE sold_flag) AS sold_properties,
    SUM(CASE WHEN has_mortgage THEN 1 ELSE 0 END) AS mortgage_sales,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(AVG(CASE WHEN sold_flag THEN price END), 2) AS avg_price,
    ROUND(AVG(CASE WHEN sold_flag THEN area END), 2) AS avg_area,
    ROUND(AVG(CASE WHEN sold_flag THEN deal_satisfaction END), 2) AS avg_deal_satisfaction
FROM silver.property_transactions
WHERE sold_flag
GROUP BY country
ORDER BY sold_properties DESC, country;

CREATE OR REPLACE TABLE gold.mart_state_distribution AS
WITH state_counts AS (
    SELECT
        state,
        COUNT(*) AS sold_properties,
        ROUND(SUM(revenue), 2) AS total_revenue
    FROM silver.property_transactions
    WHERE sold_flag
    GROUP BY state
)
SELECT
    state,
    sold_properties,
    total_revenue,
    ROUND(sold_properties * 1.0 / SUM(sold_properties) OVER (), 4) AS relative_frequency,
    SUM(sold_properties) OVER (ORDER BY sold_properties DESC, state) AS cumulative_frequency,
    ROUND(SUM(sold_properties) OVER (ORDER BY sold_properties DESC, state) * 1.0 / SUM(sold_properties) OVER (), 4) AS cumulative_share
FROM state_counts
ORDER BY sold_properties DESC, state;

CREATE OR REPLACE TABLE gold.mart_age_intervals AS
SELECT
    age_interval,
    COUNT(*) AS sold_properties,
    ROUND(AVG(price), 2) AS avg_price,
    ROUND(AVG(deal_satisfaction), 2) AS avg_deal_satisfaction
FROM silver.property_transactions
WHERE sold_flag AND age_interval IS NOT NULL
GROUP BY age_interval
ORDER BY MIN(age_at_purchase);

CREATE OR REPLACE TABLE gold.mart_price_intervals AS
SELECT
    price_interval,
    COUNT(*) AS property_count,
    SUM(CASE WHEN sold_flag THEN 1 ELSE 0 END) AS sold_properties,
    SUM(CASE WHEN NOT sold_flag THEN 1 ELSE 0 END) AS available_properties,
    ROUND(MIN(price), 2) AS min_price,
    ROUND(MAX(price), 2) AS max_price
FROM silver.property_transactions
WHERE price_interval IS NOT NULL
GROUP BY price_interval
ORDER BY min_price;

CREATE OR REPLACE TABLE gold.mart_monthly_revenue AS
SELECT
    sale_month,
    COUNT(*) AS sold_properties,
    ROUND(SUM(revenue), 2) AS total_revenue
FROM silver.property_transactions
WHERE sold_flag AND sale_month IS NOT NULL
GROUP BY sale_month
ORDER BY sale_month;

CREATE OR REPLACE TABLE gold.mart_yearly_sales_by_building AS
SELECT
    sale_year,
    building_id,
    building_label,
    COUNT(*) AS sold_properties,
    ROUND(SUM(revenue), 2) AS total_revenue
FROM silver.property_transactions
WHERE sold_flag AND sale_year IS NOT NULL
GROUP BY sale_year, building_id, building_label
ORDER BY sale_year, building_id;

CREATE OR REPLACE TABLE gold.mart_correlation_metrics AS
SELECT
    'customer_age_vs_property_price' AS metric,
    COUNT(*) FILTER (WHERE age_at_purchase IS NOT NULL AND price IS NOT NULL) AS observations,
    ROUND(CORR(age_at_purchase, price), 4) AS correlation,
    ROUND(COVAR_SAMP(age_at_purchase, price), 2) AS covariance
FROM silver.property_transactions
WHERE sold_flag;
