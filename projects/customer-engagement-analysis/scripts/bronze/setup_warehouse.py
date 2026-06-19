from __future__ import annotations

import pandas as pd

from common import connect, parse_mysql_insert_table, read_sql, script_path


SOURCES = {
    "course_info": ("365_course_info", ["course_id", "course_title"]),
    "course_ratings": ("365_course_ratings", ["course_id", "student_id", "course_rating", "date_rated"]),
    "student_info": ("365_student_info", ["student_id", "student_country", "date_registered"]),
    "student_learning": ("365_student_learning", ["student_id", "course_id", "minutes_watched", "date_watched"]),
    "student_purchases": ("365_student_purchases", ["purchase_id", "student_id", "purchase_type", "date_purchased"]),
}


def setup_bronze() -> dict[str, int]:
    parsed: dict[str, pd.DataFrame] = {}
    metadata: list[dict[str, int | str]] = []
    for target_table, (source_table, columns) in SOURCES.items():
        frame, insert_blocks = parse_mysql_insert_table(source_table, columns)
        parsed[target_table] = frame
        metadata.append(
            {
                "source_table": target_table,
                "insert_blocks": insert_blocks,
                "row_count": len(frame),
            }
        )

    with connect() as con:
        con.execute(read_sql(script_path("bronze", "ddl_bronze.sql")))
        for table_name, frame in parsed.items():
            con.register(f"tmp_{table_name}", frame)
        con.register("tmp_load_metadata", pd.DataFrame(metadata))
        try:
            con.execute(read_sql(script_path("bronze", "load_from_views.sql")))
        finally:
            for table_name in parsed:
                con.unregister(f"tmp_{table_name}")
            con.unregister("tmp_load_metadata")

        return {
            table_name: con.execute(f"SELECT COUNT(*) FROM bronze.{table_name}").fetchone()[0]
            for table_name in [*SOURCES.keys(), "load_metadata"]
        }


if __name__ == "__main__":
    for table, row_count in setup_bronze().items():
        print(f"{table}: {row_count}")
