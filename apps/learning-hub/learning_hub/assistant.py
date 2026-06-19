from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from textwrap import shorten

from .catalog import Project, get_project, load_catalog
from .data_tool import GoldQueryTool, QueryResult, UnsafeQueryError
from .indexing import LocalSearchIndex, SearchResult, load_local_index
from .paths import DEFAULT_INDEX_DIR


@dataclass(frozen=True)
class Citation:
    project_slug: str
    source_type: str
    path: str
    section: str
    score: float


@dataclass(frozen=True)
class AssistantResponse:
    answer: str
    citations: tuple[Citation, ...]
    data_result: QueryResult | None = None
    route: str = "rag"


class LearningAssistant:
    def __init__(
        self,
        index: LocalSearchIndex | None = None,
        data_tool: GoldQueryTool | None = None,
        projects: list[Project] | None = None,
        index_dir: Path = DEFAULT_INDEX_DIR,
    ) -> None:
        self.projects = projects or load_catalog()
        self.index = index or load_local_index(index_dir)
        self.data_tool = data_tool or GoldQueryTool(self.projects)

    def answer(self, question: str, project_slug: str | None = None) -> AssistantResponse:
        question = question.strip()
        if not question:
            return AssistantResponse(answer="Ask a question about the portfolio projects.", citations=())

        data_response = self._try_data_route(question, project_slug)
        if data_response:
            return data_response

        results = self.index.search(question, project_slug=project_slug, limit=6)
        if not results:
            scope = f" for `{project_slug}`" if project_slug else ""
            return AssistantResponse(
                answer=f"I don't know from the indexed project sources{scope}. Try asking about a project report, pipeline, Gold mart, or quiz answer.",
                citations=(),
                route="rag_no_context",
            )

        answer = self._extractive_answer(question, results)
        citations = tuple(self._citation(result) for result in results[:4])
        return AssistantResponse(answer=answer, citations=citations, route="rag")

    def _try_data_route(self, question: str, project_slug: str | None) -> AssistantResponse | None:
        if not project_slug:
            return None
        project = get_project(project_slug, self.projects)
        lower = question.lower()

        try:
            if "quiz" in lower and "mart_quiz_answers" in project.gold_tables:
                result = self.data_tool.run_gold_query(
                    project_slug,
                    """
                    SELECT question_number, question, answer_value, support_value
                    FROM gold.mart_quiz_answers
                    ORDER BY question_number
                    """,
                    max_rows=50,
                )
                return AssistantResponse(
                    answer=f"Here are the quiz-supporting answers available for {project.title}.",
                    citations=(
                        Citation(project_slug, "gold_table", "warehouse.duckdb", "mart_quiz_answers", 1.0),
                    ),
                    data_result=result,
                    route="data",
                )

            if "summary" in lower or "kpi" in lower or "metric" in lower:
                if "mart_summary_kpis" in project.gold_tables:
                    result = self.data_tool.preview_table(project_slug, "mart_summary_kpis", limit=10)
                    return AssistantResponse(
                        answer=f"These are the Gold summary KPIs for {project.title}.",
                        citations=(
                            Citation(project_slug, "gold_table", "warehouse.duckdb", "mart_summary_kpis", 1.0),
                        ),
                        data_result=result,
                        route="data",
                    )

            if project_slug == "tracking-user-engagement" and (
                "r-squared" in lower
                or "r squared" in lower
                or "1200" in lower
                or "certificate prediction" in lower
            ):
                result = self.data_tool.run_gold_query(
                    project_slug,
                    """
                    SELECT
                        r_squared,
                        prediction_minutes,
                        predicted_certificates_rounded_up,
                        slope,
                        intercept
                    FROM gold.mart_regression
                    """,
                    max_rows=5,
                )
                return AssistantResponse(
                    answer="The certificate prediction model output is stored in the Gold regression mart.",
                    citations=(
                        Citation(project_slug, "gold_table", "warehouse.duckdb", "mart_regression", 1.0),
                    ),
                    data_result=result,
                    route="data",
                )
        except (UnsafeQueryError, KeyError):
            return None

        return None

    def _extractive_answer(self, question: str, results: list[SearchResult]) -> str:
        lines = [
            "From the indexed project sources:",
            "",
        ]
        for result in results[:4]:
            title = result.metadata.get("project_title", result.metadata.get("project_slug", "Project"))
            path = result.metadata.get("path", "")
            snippet = shorten(" ".join(result.text.split()), width=340, placeholder="...")
            lines.append(f"- **{title}** (`{path}`): {snippet}")

        lines.extend(
            [
                "",
                "This local fallback is retrieval-grounded. Configure `OPENAI_API_KEY` and install the hub AI dependencies to generate more fluent synthesized answers.",
            ]
        )
        return "\n".join(lines)

    def _citation(self, result: SearchResult) -> Citation:
        metadata = result.metadata
        return Citation(
            project_slug=metadata.get("project_slug", ""),
            source_type=metadata.get("source_type", ""),
            path=metadata.get("path", ""),
            section=metadata.get("section", ""),
            score=result.score,
        )


def response_table_markdown(result: QueryResult) -> str:
    if not result.columns:
        return ""
    header = "| " + " | ".join(result.columns) + " |"
    separator = "| " + " | ".join("---" for _ in result.columns) + " |"
    rows = [
        "| " + " | ".join(str(value) for value in row) + " |"
        for row in result.rows
    ]
    return "\n".join([header, separator, *rows])
