from __future__ import annotations

import sys
from pathlib import Path

import duckdb
import pytest

APP_DIR = Path(__file__).resolve().parents[1]
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from learning_hub.cloud_data import build_gold_snapshot, resolve_warehouse_path


def test_cloud_snapshot_overrides_local_warehouse(tmp_path: Path) -> None:
    local_warehouse = tmp_path / "project" / "warehouse.duckdb"
    local_warehouse.parent.mkdir()
    local_warehouse.touch()
    snapshot_dir = tmp_path / "cloud"
    snapshot_dir.mkdir()
    snapshot = snapshot_dir / "demo-project.duckdb"
    snapshot.touch()

    resolved = resolve_warehouse_path(
        "demo-project",
        local_warehouse,
        snapshot_dir=snapshot_dir,
    )

    assert resolved == snapshot.resolve()


def test_local_warehouse_is_fallback_when_snapshot_is_missing(tmp_path: Path) -> None:
    local_warehouse = tmp_path / "project" / "warehouse.duckdb"
    local_warehouse.parent.mkdir()
    local_warehouse.touch()

    resolved = resolve_warehouse_path(
        "demo-project",
        local_warehouse,
        snapshot_dir=tmp_path / "cloud",
    )

    assert resolved == local_warehouse.resolve()


def test_gold_snapshot_contains_only_approved_gold_tables(tmp_path: Path) -> None:
    source = tmp_path / "source.duckdb"
    destination = tmp_path / "snapshot.duckdb"
    with duckdb.connect(str(source)) as con:
        con.execute("CREATE SCHEMA bronze")
        con.execute("CREATE SCHEMA silver")
        con.execute("CREATE SCHEMA gold")
        con.execute("CREATE TABLE bronze.raw_data AS SELECT 1 AS value")
        con.execute("CREATE TABLE silver.cleaned_data AS SELECT 2 AS value")
        con.execute("CREATE TABLE gold.mart_keep AS SELECT * FROM range(3) AS rows(value)")
        con.execute("CREATE TABLE gold.mart_skip AS SELECT 99 AS value")

    result = build_gold_snapshot(source, destination, ("mart_keep",))

    assert result.table_rows == {"mart_keep": 3}
    with duckdb.connect(str(destination), read_only=True) as con:
        tables = con.execute(
            """
            SELECT table_schema, table_name
            FROM information_schema.tables
            WHERE table_schema NOT IN ('information_schema', 'pg_catalog')
            ORDER BY table_schema, table_name
            """
        ).fetchall()
        rows = con.execute("SELECT COUNT(*) FROM gold.mart_keep").fetchone()[0]
    assert tables == [("gold", "mart_keep")]
    assert rows == 3


def test_gold_snapshot_rejects_missing_approved_table(tmp_path: Path) -> None:
    source = tmp_path / "source.duckdb"
    with duckdb.connect(str(source)) as con:
        con.execute("CREATE SCHEMA gold")
        con.execute("CREATE TABLE gold.mart_exists AS SELECT 1 AS value")

    with pytest.raises(ValueError, match="missing approved Gold tables"):
        build_gold_snapshot(source, tmp_path / "snapshot.duckdb", ("mart_missing",))

