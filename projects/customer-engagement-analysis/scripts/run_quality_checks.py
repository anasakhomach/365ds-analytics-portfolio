from __future__ import annotations

from common import PROJECT_DIR, connect, read_sql


QUALITY_SQL = PROJECT_DIR / "tests" / "quality_checks.sql"


def run_quality_checks() -> list[dict[str, int | str]]:
    with connect(read_only=True) as con:
        rows = con.execute(read_sql(QUALITY_SQL)).fetchall()
    return [{"check_name": row[0], "failures": row[1]} for row in rows]


if __name__ == "__main__":
    for result in run_quality_checks():
        print(f"{result['check_name']}: {result['failures']}")
