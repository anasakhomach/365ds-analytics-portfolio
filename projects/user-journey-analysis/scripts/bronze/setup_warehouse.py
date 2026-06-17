from __future__ import annotations

from common import connect, read_bronze_source, write_dataframe


def setup_bronze() -> dict[str, int]:
    with connect() as con:
        journeys = read_bronze_source()
        write_dataframe(con, "bronze", "raw_user_journeys", journeys)
        return {"raw_user_journeys": len(journeys)}


if __name__ == "__main__":
    counts = setup_bronze()
    for table, row_count in counts.items():
        print(f"{table}: {row_count} rows")
