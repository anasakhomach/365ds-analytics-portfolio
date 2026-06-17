from __future__ import annotations

from pathlib import Path

from common import connect


CHECKS_PATH = Path(__file__).resolve().parents[1] / "tests" / "quality_checks.sql"


def run_quality_checks() -> list[dict[str, object]]:
    with connect(read_only=True) as con:
        checks = con.execute(CHECKS_PATH.read_text(encoding="utf-8")).fetchdf()

    failures = checks[checks["failures"] > 0]
    if not failures.empty:
        raise RuntimeError(f"Quality checks failed: {failures.to_dict('records')}")
    return checks.to_dict("records")


if __name__ == "__main__":
    for check in run_quality_checks():
        print(f"{check['check_name']}: {check['failures']} failures")
