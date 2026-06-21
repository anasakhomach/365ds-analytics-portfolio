from __future__ import annotations

import argparse
import sys
from pathlib import Path


APP_DIR = Path(__file__).resolve().parents[1]
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from learning_hub.catalog import load_catalog
from learning_hub.cloud_data import build_gold_snapshot, cloud_snapshot_path
from learning_hub.paths import PUBLIC_DATA_DIR, display_path


def build_all_snapshots(output_dir: Path = PUBLIC_DATA_DIR) -> list[dict[str, object]]:
    summaries: list[dict[str, object]] = []
    for project in load_catalog():
        result = build_gold_snapshot(
            project.source_warehouse_path,
            cloud_snapshot_path(project.slug, output_dir),
            project.gold_tables,
        )
        summaries.append(
            {
                "project": project.slug,
                "path": display_path(result.path),
                "tables": len(result.table_rows),
                "rows": sum(result.table_rows.values()),
            }
        )
    return summaries


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Gold-only DuckDB snapshots for Streamlit Cloud.")
    parser.add_argument("--output-dir", type=Path, default=PUBLIC_DATA_DIR)
    args = parser.parse_args()

    for summary in build_all_snapshots(args.output_dir):
        print(
            f"{summary['project']}: {summary['tables']} tables, "
            f"{summary['rows']} rows -> {summary['path']}"
        )


if __name__ == "__main__":
    main()

