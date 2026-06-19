INSERT INTO bronze.course_info
SELECT course_id::INTEGER, course_title::VARCHAR
FROM tmp_course_info;

INSERT INTO bronze.course_ratings
SELECT course_id::INTEGER, student_id::INTEGER, course_rating::INTEGER, date_rated::DATE
FROM tmp_course_ratings;

INSERT INTO bronze.student_info
SELECT student_id::INTEGER, student_country::VARCHAR, date_registered::DATE
FROM tmp_student_info;

INSERT INTO bronze.student_learning
SELECT student_id::INTEGER, course_id::INTEGER, minutes_watched::DOUBLE, date_watched::DATE
FROM tmp_student_learning;

INSERT INTO bronze.student_purchases
SELECT purchase_id::INTEGER, student_id::INTEGER, purchase_type::VARCHAR, date_purchased::DATE
FROM tmp_student_purchases;

INSERT INTO bronze.load_metadata
SELECT source_table::VARCHAR, insert_blocks::INTEGER, row_count::INTEGER
FROM tmp_load_metadata;
