from __future__ import annotations

from common import PROJECT_DIR, connect, read_sql


QUALITY_SQL = PROJECT_DIR / "tests" / "quality_checks.sql"
DASHBOARD_APP = PROJECT_DIR / "dashboard" / "app.py"
DISALLOWED_DASHBOARD_PATTERNS = ("bronze.", "silver.", "source-datasets", "source_datasets")


def _dashboard_gold_only_failures() -> int:
    if not DASHBOARD_APP.exists():
        return 1
    app_text = DASHBOARD_APP.read_text(encoding="utf-8").lower()
    return sum(1 for pattern in DISALLOWED_DASHBOARD_PATTERNS if pattern in app_text)


def run_quality_checks() -> list[dict[str, int | str]]:
    with connect(read_only=True) as con:
        rows = con.execute(read_sql(QUALITY_SQL)).fetchall()
    checks = [{"check_name": row[0], "failures": row[1]} for row in rows]
    checks.append(
        {
            "check_name": "dashboard_gold_only_contract",
            "failures": _dashboard_gold_only_failures(),
        }
    )
    return checks


if __name__ == "__main__":
    for result in run_quality_checks():
        print(f"{result['check_name']}: {result['failures']}")
