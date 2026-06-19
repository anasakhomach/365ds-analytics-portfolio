CREATE SCHEMA IF NOT EXISTS bronze;

CREATE OR REPLACE TABLE bronze.student_certificates (
    certificate_id INTEGER,
    student_id INTEGER,
    date_issued DATE
);

CREATE OR REPLACE TABLE bronze.student_info (
    student_id INTEGER,
    date_registered DATE
);

CREATE OR REPLACE TABLE bronze.student_purchases (
    purchase_id INTEGER,
    student_id INTEGER,
    plan_id INTEGER,
    date_purchased DATE,
    date_refunded DATE
);

CREATE OR REPLACE TABLE bronze.student_video_watched (
    student_id INTEGER,
    course_id INTEGER,
    seconds_watched INTEGER,
    date_watched DATE
);

CREATE OR REPLACE TABLE bronze.load_metadata (
    source_table VARCHAR,
    insert_blocks INTEGER,
    row_count INTEGER
);
