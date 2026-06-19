from __future__ import annotations

from common import build_country_lookup, connect, read_sql, script_path


SILVER_TABLES = (
    "course_info",
    "course_ratings",
    "student_info",
    "student_learning",
    "student_purchases",
    "purchases_info",
    "student_engagement",
)


def build_silver() -> dict[str, int]:
    with connect() as con:
        country_codes = con.execute("SELECT DISTINCT student_country FROM bronze.student_info").fetchdf()["student_country"]
        con.register("tmp_country_lookup", build_country_lookup(country_codes))
        try:
            con.execute(read_sql(script_path("silver", "build_silver.sql")))
        finally:
            con.unregister("tmp_country_lookup")

        return {
            table: con.execute(f"SELECT COUNT(*) FROM silver.{table}").fetchone()[0]
            for table in SILVER_TABLES
        }


if __name__ == "__main__":
    for table, row_count in build_silver().items():
        print(f"{table}: {row_count}")
