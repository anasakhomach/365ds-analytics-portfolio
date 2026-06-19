INSERT INTO bronze.student_certificates
SELECT
    certificate_id::INTEGER,
    student_id::INTEGER,
    date_issued::DATE
FROM tmp_student_certificates;

INSERT INTO bronze.student_info
SELECT
    student_id::INTEGER,
    date_registered::DATE
FROM tmp_student_info;

INSERT INTO bronze.student_purchases
SELECT
    purchase_id::INTEGER,
    student_id::INTEGER,
    plan_id::INTEGER,
    date_purchased::DATE,
    date_refunded::DATE
FROM tmp_student_purchases;

INSERT INTO bronze.student_video_watched
SELECT
    student_id::INTEGER,
    course_id::INTEGER,
    seconds_watched::INTEGER,
    date_watched::DATE
FROM tmp_student_video_watched;

INSERT INTO bronze.load_metadata
SELECT
    source_table::VARCHAR,
    insert_blocks::INTEGER,
    row_count::INTEGER
FROM tmp_load_metadata;
