INSERT INTO bronze.checkout_actions
SELECT
    CAST(user_id AS INTEGER) AS user_id,
    CAST(action_date AS DATE) AS action_date,
    CAST(action_name AS VARCHAR) AS action_name,
    CAST(error_message AS VARCHAR) AS error_message,
    CAST(device AS VARCHAR) AS device
FROM tmp_checkout_actions;

INSERT INTO bronze.checkout_carts
SELECT
    CAST(user_id AS INTEGER) AS user_id,
    CAST(action_date AS DATE) AS action_date
FROM tmp_checkout_carts;
