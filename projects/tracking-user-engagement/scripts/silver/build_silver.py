from __future__ import annotations

import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parents[1]
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from common import connect, read_sql, script_path


SILVER_TABLES = (
    "student_certificates",
    "student_info",
    "student_purchases",
    "student_video_watched",
    "purchases_info",
    "q2_minutes_watched",
    "q2_paid_flags",
    "q2_engagement_segments",
    "certificates_minutes",
)


def build_silver() -> dict[str, int]:
    with connect() as con:
        con.execute(read_sql(script_path("silver", "build_silver.sql")))
        return {
            table: con.execute(f"SELECT COUNT(*) FROM silver.{table}").fetchone()[0]
            for table in SILVER_TABLES
        }


if __name__ == "__main__":
    for table, row_count in build_silver().items():
        print(f"{table}: {row_count}")
