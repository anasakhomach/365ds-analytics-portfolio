from __future__ import annotations

import ast
import re
from pathlib import Path

import duckdb
import pandas as pd
from babel import Locale


PROJECT_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = PROJECT_DIR.parents[1]
RAW_DIR = REPO_ROOT / "source-datasets" / "Customer Engagement Analysis With SQL And Tableau"
DB_PATH = PROJECT_DIR / "warehouse.duckdb"
REPORT_DIR = PROJECT_DIR / "reports"

CUSTOMER_ENGAGEMENT_DUMP = RAW_DIR / "365_database.sql"


def connect(read_only: bool = False) -> duckdb.DuckDBPyConnection:
    return duckdb.connect(str(DB_PATH), read_only=read_only)


def ensure_project_dirs() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)


def read_sql(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def script_path(*parts: str) -> Path:
    return Path(__file__).resolve().parent.joinpath(*parts)


def _extract_insert_blocks(dump_text: str, table_name: str) -> list[str]:
    pattern = rf"INSERT INTO `{re.escape(table_name)}` VALUES (.*?);"
    blocks = re.findall(pattern, dump_text, flags=re.DOTALL)
    if not blocks:
        raise ValueError(f"Could not find INSERT blocks for {table_name}")
    return blocks


def parse_mysql_insert_table(table_name: str, columns: list[str]) -> tuple[pd.DataFrame, int]:
    if not CUSTOMER_ENGAGEMENT_DUMP.exists():
        raise FileNotFoundError(f"Missing source dump: {CUSTOMER_ENGAGEMENT_DUMP}")

    dump_text = CUSTOMER_ENGAGEMENT_DUMP.read_text(encoding="utf-8")
    rows: list[tuple[object, ...]] = []
    blocks = _extract_insert_blocks(dump_text, table_name)
    for block in blocks:
        rows.extend(ast.literal_eval(f"[{block.replace('NULL', 'None')}]"))
    return pd.DataFrame(rows, columns=columns), len(blocks)


def build_country_lookup(country_codes: pd.Series) -> pd.DataFrame:
    territories = Locale.parse("en").territories
    codes = sorted(str(code) for code in country_codes.dropna().unique())
    return pd.DataFrame(
        {
            "student_country": codes,
            "country_name": [territories.get(code, code) for code in codes],
        }
    )
