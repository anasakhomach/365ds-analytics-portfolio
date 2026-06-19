from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parents[1]
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from common import connect, parse_mysql_insert_table, read_sql, script_path


SOURCES = {
    "student_certificates": (
        "student_certificates",
        ["certificate_id", "student_id", "date_issued"],
    ),
    "student_info": (
        "student_info",
        ["student_id", "date_registered"],
    ),
    "student_purchases": (
        "student_purchases",
        ["purchase_id", "student_id", "plan_id", "date_purchased", "date_refunded"],
    ),
    "student_video_watched": (
        "student_video_watched",
        ["student_id", "course_id", "seconds_watched", "date_watched"],
    ),
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
