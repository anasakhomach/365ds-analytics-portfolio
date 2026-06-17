from __future__ import annotations

from common import connect, read_sql, script_path


SILVER_TABLES = (
    "checkout_actions",
    "checkout_carts",
    "checkout_attempts",
    "successful_checkout_attempts",
    "checkout_errors",
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
