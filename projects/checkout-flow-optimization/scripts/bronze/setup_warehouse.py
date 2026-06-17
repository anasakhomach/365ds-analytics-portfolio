from __future__ import annotations

from common import connect, parse_mysql_insert_table, read_sql, script_path


def setup_bronze() -> dict[str, int]:
    actions = parse_mysql_insert_table(
        "checkout_actions",
        ["user_id", "action_date", "action_name", "error_message", "device"],
    )
    carts = parse_mysql_insert_table("checkout_carts", ["user_id", "action_date"])

    with connect() as con:
        con.execute(read_sql(script_path("bronze", "ddl_bronze.sql")))
        con.register("tmp_checkout_actions", actions)
        con.register("tmp_checkout_carts", carts)
        try:
            con.execute(read_sql(script_path("bronze", "load_from_views.sql")))
        finally:
            con.unregister("tmp_checkout_actions")
            con.unregister("tmp_checkout_carts")

        return {
            "checkout_actions": con.execute("SELECT COUNT(*) FROM bronze.checkout_actions").fetchone()[0],
            "checkout_carts": con.execute("SELECT COUNT(*) FROM bronze.checkout_carts").fetchone()[0],
        }


if __name__ == "__main__":
    for table, row_count in setup_bronze().items():
        print(f"{table}: {row_count}")
