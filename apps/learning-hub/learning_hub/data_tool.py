from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

import duckdb

from .catalog import Project, describe_gold_tables, get_project, load_catalog


FORBIDDEN_SQL = re.compile(
    r"\b("
    r"insert|update|delete|drop|create|alter|truncate|attach|detach|copy|export|import|"
    r"install|load|pragma|set|call|read_csv|read_parquet|write_csv"
    r")\b",
    re.IGNORECASE,
)
TABLE_REF = re.compile(r"\b(?:from|join)\s+([a-zA-Z_][\w.]*|\"[^\"]+\"(?:\.\"[^\"]+\")?)", re.IGNORECASE)


class UnsafeQueryError(ValueError):
    pass


@dataclass(frozen=True)
class QueryResult:
    columns: tuple[str, ...]
    rows: tuple[tuple[Any, ...], ...]
    row_count: int


class GoldQueryTool:
    def __init__(self, projects: list[Project] | None = None) -> None:
        self.projects = projects or load_catalog()

    def list_gold_tables(self, project_slug: str) -> list[dict[str, object]]:
        project = get_project(project_slug, self.projects)
        return [
            {
                "name": table.name,
                "row_count": table.row_count,
                "columns": list(table.columns),
            }
            for table in describe_gold_tables(project)
        ]

    def preview_table(self, project_slug: str, table_name: str, limit: int = 10) -> QueryResult:
        self._ensure_allowed_table(project_slug, table_name)
        return self.run_gold_query(
            project_slug,
            f'SELECT * FROM gold."{table_name}"',
            max_rows=limit,
        )

    def run_gold_query(self, project_slug: str, sql: str, max_rows: int = 100) -> QueryResult:
        project = get_project(project_slug, self.projects)
        cleaned = self._validate_sql(project, sql)
        limited_sql = f"SELECT * FROM ({cleaned}) AS safe_query LIMIT {int(max_rows)}"
        with duckdb.connect(str(project.warehouse_path), read_only=True) as con:
            result = con.execute(limited_sql)
            rows = tuple(tuple(row) for row in result.fetchall())
            columns = tuple(col[0] for col in result.description or ())
        return QueryResult(columns=columns, rows=rows, row_count=len(rows))

    def _ensure_allowed_table(self, project_slug: str, table_name: str) -> None:
        project = get_project(project_slug, self.projects)
        if table_name not in project.gold_tables:
            raise UnsafeQueryError(f"Table is not an approved Gold mart: {table_name}")

    def _validate_sql(self, project: Project, sql: str) -> str:
        cleaned = sql.strip().rstrip(";").strip()
        if not cleaned:
            raise UnsafeQueryError("Query is empty")
        if ";" in cleaned:
            raise UnsafeQueryError("Multiple SQL statements are not allowed")
        if not re.match(r"^(select|with)\b", cleaned, flags=re.IGNORECASE):
            raise UnsafeQueryError("Only SELECT/WITH read queries are allowed")
        if FORBIDDEN_SQL.search(cleaned):
            raise UnsafeQueryError("Query contains a forbidden operation")

        refs = TABLE_REF.findall(cleaned)
        if not refs:
            raise UnsafeQueryError("Query must reference at least one approved Gold table")

        allowed = set(project.gold_tables)
        for ref in refs:
            normalized = ref.replace('"', "")
            parts = normalized.split(".")
            if len(parts) == 1:
                table = parts[0]
            elif len(parts) == 2 and parts[0].lower() == "gold":
                table = parts[1]
            else:
                raise UnsafeQueryError(f"Only Gold schema tables are allowed: {ref}")
            if table not in allowed:
                raise UnsafeQueryError(f"Table is not an approved Gold mart: {table}")
        return cleaned
