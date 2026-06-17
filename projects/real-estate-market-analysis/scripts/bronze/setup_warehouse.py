from __future__ import annotations

from common import CUSTOMERS_CSV, PROPERTIES_CSV, connect, read_bronze_source, write_dataframe


def setup_bronze() -> dict[str, int]:
    with connect() as con:
        customers = read_bronze_source(CUSTOMERS_CSV)
        properties = read_bronze_source(PROPERTIES_CSV)

        write_dataframe(con, "bronze", "raw_customers", customers)
        write_dataframe(con, "bronze", "raw_properties", properties)

        return {
            "raw_customers": len(customers),
            "raw_properties": len(properties),
        }


if __name__ == "__main__":
    counts = setup_bronze()
    for table, row_count in counts.items():
        print(f"{table}: {row_count} rows")
