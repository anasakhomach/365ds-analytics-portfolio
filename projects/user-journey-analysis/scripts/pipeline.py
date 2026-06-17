from __future__ import annotations

import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from bronze.setup_warehouse import setup_bronze
from gold.build_gold import build_gold
from run_quality_checks import run_quality_checks
from silver.build_silver import build_silver


def _print_counts(stage: str, counts: dict[str, int]) -> None:
    print(f"\n{stage}")
    for name, row_count in counts.items():
        print(f"  {name}: {row_count}")


def run_pipeline() -> None:
    print("Starting User Journey DuckDB pipeline...")
    _print_counts("Bronze", setup_bronze())
    _print_counts("Silver", build_silver())
    _print_counts("Gold", build_gold())

    checks = run_quality_checks()
    print("\nQuality checks")
    for check in checks:
        print(f"  {check['check_name']}: {check['failures']} failures")
    print("\nPipeline complete.")


if __name__ == "__main__":
    run_pipeline()
