from __future__ import annotations

import sys
from pathlib import Path

import pytest

APP_DIR = Path(__file__).resolve().parents[1]
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from learning_hub.data_tool import GoldQueryTool, UnsafeQueryError


def test_gold_query_allows_approved_gold_marts() -> None:
    tool = GoldQueryTool()
    result = tool.run_gold_query(
        "tracking-user-engagement",
        "SELECT * FROM gold.mart_regression",
    )
    assert result.row_count == 1
    assert "r_squared" in result.columns


def test_gold_query_rejects_lower_layers() -> None:
    tool = GoldQueryTool()
    with pytest.raises(UnsafeQueryError):
        tool.run_gold_query(
            "tracking-user-engagement",
            "SELECT * FROM silver.q2_minutes_watched",
        )


def test_gold_query_rejects_destructive_sql() -> None:
    tool = GoldQueryTool()
    with pytest.raises(UnsafeQueryError):
        tool.run_gold_query(
            "tracking-user-engagement",
            "DROP TABLE gold.mart_regression",
        )


def test_gold_query_rejects_unapproved_gold_table() -> None:
    tool = GoldQueryTool()
    with pytest.raises(UnsafeQueryError):
        tool.run_gold_query(
            "tracking-user-engagement",
            "SELECT * FROM gold.not_a_real_mart",
        )
