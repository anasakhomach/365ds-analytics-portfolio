CREATE SCHEMA IF NOT EXISTS bronze;

DROP TABLE IF EXISTS bronze.checkout_actions;
DROP TABLE IF EXISTS bronze.checkout_carts;

CREATE TABLE bronze.checkout_actions (
    user_id INTEGER,
    action_date DATE,
    action_name VARCHAR,
    error_message VARCHAR,
    device VARCHAR
);

CREATE TABLE bronze.checkout_carts (
    user_id INTEGER,
    action_date DATE
);
