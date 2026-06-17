from __future__ import annotations

import re
from pathlib import Path

import duckdb
import pandas as pd


PROJECT_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = PROJECT_DIR.parents[1]
RAW_DIR = REPO_ROOT / "source-datasets" / "Real Estate Market Analysis With Python"
DB_PATH = PROJECT_DIR / "warehouse.duckdb"
REPORT_DIR = PROJECT_DIR / "reports"

CUSTOMERS_CSV = RAW_DIR / "customers.csv"
PROPERTIES_CSV = RAW_DIR / "properties.csv"


def connect(read_only: bool = False) -> duckdb.DuckDBPyConnection:
    return duckdb.connect(str(DB_PATH), read_only=read_only)


def ensure_project_dirs() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)


def normalize_column(name: object) -> str:
    value = str(name).replace("\ufeff", "").strip().lower()
    value = re.sub(r"[^0-9a-zA-Z]+", "_", value)
    value = re.sub(r"_+", "_", value).strip("_")
    if value == "property":
        return "property_number"
    return value


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


def read_bronze_source(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Missing source file: {path}")
    return pd.read_csv(path, encoding="utf-8-sig", dtype="string")
