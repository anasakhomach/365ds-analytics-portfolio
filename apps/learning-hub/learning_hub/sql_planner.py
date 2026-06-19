from __future__ import annotations

import json
import re
from dataclasses import dataclass

from .data_tool import GoldQueryTool, QueryResult
from .llm_client import LLMClient, Message


@dataclass(frozen=True)
class PlannedGoldQuery:
    sql: str
    explanation: str
    result: QueryResult


def plan_and_run_gold_query(
    project_slug: str,
    question: str,
    llm_client: LLMClient,
    data_tool: GoldQueryTool | None = None,
    max_rows: int = 50,
) -> PlannedGoldQuery:
    tool = data_tool or GoldQueryTool()
    tables = tool.list_gold_tables(project_slug)
    messages = _planner_messages(project_slug, question, tables)
    payload = _parse_json_object(llm_client.complete(messages))
    sql = str(payload.get("sql", "")).strip()
    explanation = str(payload.get("explanation", "")).strip()
    result = tool.run_gold_query(project_slug, sql, max_rows=max_rows)
    return PlannedGoldQuery(sql=sql, explanation=explanation, result=result)


def _planner_messages(project_slug: str, question: str, tables: list[dict[str, object]]) -> list[Message]:
    table_lines = []
    for table in tables:
        columns = ", ".join(str(column) for column in table["columns"])
        table_lines.append(f"- gold.{table['name']} ({table['row_count']} rows): {columns}")

    system = (
        "You write read-only DuckDB SQL for approved Gold marts only. Return one JSON object "
        "with keys sql and explanation. The sql must be a single SELECT or WITH query. Do not "
        "use raw, bronze, silver, file functions, writes, PRAGMA, COPY, ATTACH, or multiple statements."
    )
    user = (
        f"Project slug: {project_slug}\n"
        f"Question: {question}\n\n"
        "Available approved Gold marts:\n"
        f"{chr(10).join(table_lines)}"
    )
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


def _parse_json_object(text: str) -> dict[str, object]:
    cleaned = text.strip()
    fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", cleaned, flags=re.DOTALL)
    if fenced:
        cleaned = fenced.group(1)
    try:
        payload = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise ValueError("LLM SQL planner must return a JSON object") from exc
    if not isinstance(payload, dict):
        raise ValueError("LLM SQL planner must return a JSON object")
    return payload
