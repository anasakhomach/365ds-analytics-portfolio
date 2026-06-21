from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path

import duckdb

from .paths import PUBLIC_DATA_DIR


SAFE_IDENTIFIER = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


@dataclass(frozen=True)
class SnapshotBuildResult:
    path: Path
    table_rows: dict[str, int]


def cloud_snapshot_path(slug: str, snapshot_dir: Path = PUBLIC_DATA_DIR) -> Path:
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
        raise ValueError(f"Invalid project slug: {slug}")
    return (snapshot_dir / f"{slug}.duckdb").resolve()


def resolve_warehouse_path(
    slug: str,
    local_warehouse: Path,
    snapshot_dir: Path = PUBLIC_DATA_DIR,
) -> Path:
    snapshot = cloud_snapshot_path(slug, snapshot_dir)
    if snapshot.exists():
        return snapshot
    return local_warehouse.resolve()


def build_gold_snapshot(
    source_warehouse: Path,
    destination: Path,
    approved_tables: tuple[str, ...],
) -> SnapshotBuildResult:
    source = source_warehouse.resolve()
    target = destination.resolve()
    if not source.exists():
        raise FileNotFoundError(f"Missing source warehouse: {source}")
    if not approved_tables:
        raise ValueError("At least one approved Gold table is required")
    for table_name in approved_tables:
        if not SAFE_IDENTIFIER.fullmatch(table_name):
            raise ValueError(f"Unsafe Gold table identifier: {table_name}")

    with duckdb.connect(str(source), read_only=True) as con:
        existing = {
            row[0]
            for row in con.execute(
                """
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'gold'
                """
            ).fetchall()
        }
    missing = sorted(set(approved_tables) - existing)
    if missing:
        raise ValueError(f"Source warehouse is missing approved Gold tables: {', '.join(missing)}")

    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_name(f".{target.name}.tmp")
    temporary.unlink(missing_ok=True)
    source_sql = str(source).replace("'", "''")
    table_rows: dict[str, int] = {}
    try:
        with duckdb.connect(str(temporary)) as con:
            con.execute(f"ATTACH '{source_sql}' AS source_warehouse (READ_ONLY)")
            con.execute("CREATE SCHEMA gold")
            for table_name in approved_tables:
                quoted = f'"{table_name}"'
                con.execute(
                    f"CREATE TABLE gold.{quoted} AS "
                    f"SELECT * FROM source_warehouse.gold.{quoted}"
                )
                table_rows[table_name] = int(
                    con.execute(f"SELECT COUNT(*) FROM gold.{quoted}").fetchone()[0]
                )
            con.execute("DETACH source_warehouse")
        os.replace(temporary, target)
    finally:
        temporary.unlink(missing_ok=True)

    return SnapshotBuildResult(path=target, table_rows=table_rows)

