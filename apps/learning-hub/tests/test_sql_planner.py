from __future__ import annotations

import sys
from pathlib import Path

import pytest

APP_DIR = Path(__file__).resolve().parents[1]
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from learning_hub.data_tool import UnsafeQueryError
from learning_hub.sql_planner import plan_and_run_gold_query


class FakePlannerLLM:
    def __init__(self, response: str) -> None:
        self.response = response
        self.messages: list[dict[str, str]] = []

    def complete(self, messages: list[dict[str, str]]) -> str:
        self.messages = messages
        return self.response

    def stream(self, messages: list[dict[str, str]]):
        yield self.complete(messages)


def test_sql_planner_runs_safe_gold_query() -> None:
    llm = FakePlannerLLM(
        '{"sql": "SELECT r_squared FROM gold.mart_regression", "explanation": "Read the model fit."}'
    )

    planned = plan_and_run_gold_query(
        project_slug="tracking-user-engagement",
        question="What is the regression R-squared?",
        llm_client=llm,
    )

    assert planned.sql == "SELECT r_squared FROM gold.mart_regression"
    assert planned.result.row_count == 1
    assert planned.result.columns == ("r_squared",)
    assert "approved Gold marts" in llm.messages[0]["content"]


def test_sql_planner_rejects_unsafe_llm_sql() -> None:
    llm = FakePlannerLLM(
        '{"sql": "DROP TABLE gold.mart_regression", "explanation": "Bad idea."}'
    )

    with pytest.raises(UnsafeQueryError):
        plan_and_run_gold_query(
            project_slug="tracking-user-engagement",
            question="Delete the regression mart.",
            llm_client=llm,
        )
