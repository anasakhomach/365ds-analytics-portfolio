CREATE SCHEMA IF NOT EXISTS silver;

CREATE OR REPLACE TABLE silver.checkout_actions AS
SELECT
    user_id,
    action_date,
    action_name,
    error_message,
    lower(device) AS device,
    action_name LIKE '%checkout%' AS is_checkout_action,
    action_name LIKE '%checkout%' AND action_name LIKE '%.success' AS is_successful_checkout,
    action_name LIKE '%checkout%' AND action_name LIKE '%.fail' AS is_failed_checkout,
    nullif(regexp_extract(action_name, 'checkout_([^_]+)_completepayment', 1), '') AS checkout_product
FROM bronze.checkout_actions
WHERE action_date BETWEEN DATE '2022-07-01' AND DATE '2023-01-31';

CREATE OR REPLACE TABLE silver.checkout_carts AS
SELECT
    user_id,
    action_date
FROM bronze.checkout_carts
WHERE action_date BETWEEN DATE '2022-07-01' AND DATE '2023-01-31';

CREATE OR REPLACE TABLE silver.checkout_attempts AS
SELECT
    user_id,
    action_date,
    action_name,
    error_message,
    device,
    checkout_product,
    is_successful_checkout,
    is_failed_checkout
FROM silver.checkout_actions
WHERE is_checkout_action;

CREATE OR REPLACE TABLE silver.successful_checkout_attempts AS
SELECT *
FROM silver.checkout_attempts
WHERE is_successful_checkout;

CREATE OR REPLACE TABLE silver.checkout_errors AS
SELECT
    user_id,
    action_date,
    action_name,
    error_message,
    device,
    checkout_product
FROM silver.checkout_attempts
WHERE error_message IS NOT NULL;
