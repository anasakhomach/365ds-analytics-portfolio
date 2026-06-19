CREATE SCHEMA IF NOT EXISTS bronze;

CREATE OR REPLACE TABLE bronze.course_info (
    course_id INTEGER,
    course_title VARCHAR
);

CREATE OR REPLACE TABLE bronze.course_ratings (
    course_id INTEGER,
    student_id INTEGER,
    course_rating INTEGER,
    date_rated DATE
);

CREATE OR REPLACE TABLE bronze.student_info (
    student_id INTEGER,
    student_country VARCHAR,
    date_registered DATE
);

CREATE OR REPLACE TABLE bronze.student_learning (
    student_id INTEGER,
    course_id INTEGER,
    minutes_watched DOUBLE,
    date_watched DATE
);

CREATE OR REPLACE TABLE bronze.student_purchases (
    purchase_id INTEGER,
    student_id INTEGER,
    purchase_type VARCHAR,
    date_purchased DATE
);

CREATE OR REPLACE TABLE bronze.load_metadata (
    source_table VARCHAR,
    insert_blocks INTEGER,
    row_count INTEGER
);
