from __future__ import annotations

from pathlib import Path

import duckdb
import pandas as pd


PROJECT_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = PROJECT_DIR.parents[1]
RAW_DIR = REPO_ROOT / "source-datasets" / "User Journey Analysis In Python"
DB_PATH = PROJECT_DIR / "warehouse.duckdb"
REPORT_DIR = PROJECT_DIR / "reports"

USER_JOURNEY_CSV = RAW_DIR / "user_journey_raw.csv"


def connect(read_only: bool = False) -> duckdb.DuckDBPyConnection:
    return duckdb.connect(str(DB_PATH), read_only=read_only)


def ensure_project_dirs() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)


def write_dataframe(
    con: duckdb.DuckDBPyConnection,
    schema: str,
    table: str,
    df: pd.DataFrame,
) -> None:
    con.execute(f"CREATE SCHEMA IF NOT EXISTS {schema}")
    view_name = f"tmp_{schema}_{table}"
    con.register(view_name, df)
    try:
        con.execute(f"CREATE OR REPLACE TABLE {schema}.{table} AS SELECT * FROM {view_name}")
    finally:
        con.unregister(view_name)


def read_bronze_source() -> pd.DataFrame:
    if not USER_JOURNEY_CSV.exists():
        raise FileNotFoundError(f"Missing source file: {USER_JOURNEY_CSV}")
    return pd.read_csv(USER_JOURNEY_CSV, encoding="utf-8-sig")
