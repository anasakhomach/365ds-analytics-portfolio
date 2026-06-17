from __future__ import annotations

import ast
import re
from pathlib import Path

import duckdb
import pandas as pd


PROJECT_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = PROJECT_DIR.parents[1]
RAW_DIR = REPO_ROOT / "source-datasets" / "Checkout Flow Optimization Analysis With SQL And Tableau"
DB_PATH = PROJECT_DIR / "warehouse.duckdb"
REPORT_DIR = PROJECT_DIR / "reports"

CHECKOUT_DUMP = RAW_DIR / "365_checkout_database.sql"
ANALYSIS_START = "2022-07-01"
ANALYSIS_END = "2023-01-31"


def connect(read_only: bool = False) -> duckdb.DuckDBPyConnection:
    return duckdb.connect(str(DB_PATH), read_only=read_only)


def ensure_project_dirs() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)


def read_sql(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def script_path(*parts: str) -> Path:
    return Path(__file__).resolve().parent.joinpath(*parts)


def _extract_insert_block(dump_text: str, table_name: str) -> str:
    pattern = rf"INSERT INTO `{re.escape(table_name)}` VALUES (.*?);"
    match = re.search(pattern, dump_text, flags=re.DOTALL)
    if not match:
        raise ValueError(f"Could not find INSERT block for {table_name}")
    return match.group(1)


def parse_mysql_insert_table(table_name: str, columns: list[str]) -> pd.DataFrame:
    if not CHECKOUT_DUMP.exists():
        raise FileNotFoundError(f"Missing source dump: {CHECKOUT_DUMP}")

    dump_text = CHECKOUT_DUMP.read_text(encoding="utf-8")
    values = _extract_insert_block(dump_text, table_name).replace("NULL", "None")
    rows = ast.literal_eval(f"[{values}]")
    return pd.DataFrame(rows, columns=columns)
