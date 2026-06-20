from __future__ import annotations

import importlib.util
from dataclasses import dataclass
from pathlib import Path
from textwrap import shorten
from typing import Any, Sequence, TypedDict

from .catalog import Project, get_project, load_catalog
from .data_tool import GoldQueryTool, QueryResult, UnsafeQueryError
from .indexing import LocalSearchIndex, SearchResult, load_local_index
from .llm_client import LLMClient, Message
from .paths import DEFAULT_INDEX_DIR
from .settings import AIRuntime


VALID_AGENT_BACKENDS = {"custom", "langgraph", "auto"}


class AgentGraphState(TypedDict, total=False):
    question: str
    project_slug: str | None
    history: list[Message]
    response: dict[str, Any]
    data_response: dict[str, Any] | None
    results: list[dict[str, Any]]
    plan: dict[str, Any]


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


@dataclass(frozen=True)
class AssistantPlan:
    fallback_response: AssistantResponse
    messages: tuple[Message, ...] = ()
    llm_route: str = "llm_rag"


class LearningAssistant:
    def __init__(
        self,
        index: LocalSearchIndex | None = None,
        data_tool: GoldQueryTool | None = None,
        projects: list[Project] | None = None,
        index_dir: Path = DEFAULT_INDEX_DIR,
        llm_client: LLMClient | None = None,
        runtime: AIRuntime | None = None,
        agent_backend: str = "custom",
        thread_id: str | None = None,
    ) -> None:
        self.projects = projects or load_catalog()
        self.index = index or load_local_index(index_dir)
        self.data_tool = data_tool or GoldQueryTool(self.projects)
        self.llm_client = llm_client
        self.runtime = runtime
        self.agent_backend = agent_backend if agent_backend in VALID_AGENT_BACKENDS else "custom"
        self.thread_id = thread_id or "learning-hub-session"
        self._langgraph_graph = None

    def answer(
        self,
        question: str,
        project_slug: str | None = None,
        history: Sequence[Message] | None = None,
    ) -> AssistantResponse:
        plan = self.plan_answer(question, project_slug=project_slug, history=history)
        if self.llm_client and plan.messages:
            try:
                answer = self.llm_client.complete(list(plan.messages))
                return AssistantResponse(
                    answer=answer,
                    citations=plan.fallback_response.citations,
                    data_result=plan.fallback_response.data_result,
                    route=plan.llm_route,
                )
            except Exception as exc:
                return self._with_llm_fallback_note(plan.fallback_response, exc)
        return plan.fallback_response

    def stream_answer(
        self,
        question: str,
        project_slug: str | None = None,
        history: Sequence[Message] | None = None,
    ) -> tuple[AssistantResponse, object]:
        plan = self.plan_answer(question, project_slug=project_slug, history=history)
        shell = AssistantResponse(
            answer="",
            citations=plan.fallback_response.citations,
            data_result=plan.fallback_response.data_result,
            route=plan.llm_route if self.llm_client and plan.messages else plan.fallback_response.route,
        )
        if not self.llm_client or not plan.messages:
            return shell, iter([plan.fallback_response.answer])

        def chunks():
            try:
                yield from self.llm_client.stream(list(plan.messages))
            except Exception as exc:
                yield self._with_llm_fallback_note(plan.fallback_response, exc).answer

        return shell, chunks()

    def plan_answer(
        self,
        question: str,
        project_slug: str | None = None,
        history: Sequence[Message] | None = None,
    ) -> AssistantPlan:
        if self._should_use_langgraph_backend():
            try:
                return self._langgraph_plan_answer(question, project_slug=project_slug, history=history)
            except ImportError as exc:
                if self.agent_backend == "langgraph":
                    response = AssistantResponse(
                        answer=(
                            "The LangGraph agent backend was requested, but LangGraph is not installed "
                            f"in this environment. Error type: {type(exc).__name__}."
                        ),
                        citations=(),
                        route="agent_unavailable",
                    )
                    return AssistantPlan(fallback_response=response)

        return self._custom_plan_answer(question, project_slug=project_slug, history=history)

    def _custom_plan_answer(
        self,
        question: str,
        project_slug: str | None = None,
        history: Sequence[Message] | None = None,
    ) -> AssistantPlan:
        question = question.strip()
        if not question:
            response = AssistantResponse(answer="Ask a question about the portfolio projects.", citations=())
            return AssistantPlan(fallback_response=response)

        capability_response = self._try_capability_route(question, project_slug)
        if capability_response:
            return AssistantPlan(fallback_response=capability_response)

        runtime_response = self._try_runtime_route(question)
        if runtime_response:
            return AssistantPlan(fallback_response=runtime_response)

        trait_response = self._try_project_traits_route(question, project_slug)
        if trait_response:
            return AssistantPlan(fallback_response=trait_response)

        data_response = self._try_data_route(question, project_slug)
        search_query = self._search_query(question, history)
        results = self.index.search(search_query, project_slug=project_slug, limit=6)
        return self._plan_from_context(
            question=question,
            project_slug=project_slug,
            history=history,
            data_response=data_response,
            results=results,
        )

    def _plan_from_context(
        self,
        question: str,
        project_slug: str | None,
        history: Sequence[Message] | None,
        data_response: AssistantResponse | None,
        results: list[SearchResult],
    ) -> AssistantPlan:
        if not results and not data_response:
            scope = f" for `{project_slug}`" if project_slug else ""
            response = AssistantResponse(
                answer=f"I don't know from the indexed project sources{scope}. Try asking about a project report, pipeline, Gold mart, or quiz answer.",
                citations=(),
                route="rag_no_context",
            )
            return AssistantPlan(fallback_response=response)

        if data_response and not results:
            return AssistantPlan(
                fallback_response=data_response,
                messages=tuple(self._llm_messages(question, [], data_response, history)),
                llm_route="llm_data",
            )

        answer = self._extractive_answer(question, results)
        citations = tuple(self._citation(result) for result in results[:4])
        fallback = AssistantResponse(
            answer=answer,
            citations=citations,
            data_result=data_response.data_result if data_response else None,
            route=data_response.route if data_response else "rag",
        )
        return AssistantPlan(
            fallback_response=fallback,
            messages=tuple(self._llm_messages(question, results, data_response, history)),
            llm_route="llm_data" if data_response else "llm_rag",
        )

    def _should_use_langgraph_backend(self) -> bool:
        if self.agent_backend == "custom":
            return False
        available = importlib.util.find_spec("langgraph") is not None
        if self.agent_backend == "auto":
            return available
        return True

    def _langgraph_plan_answer(
        self,
        question: str,
        project_slug: str | None,
        history: Sequence[Message] | None,
    ) -> AssistantPlan:
        graph = self._compiled_langgraph()
        state = {
            "question": question,
            "project_slug": project_slug,
            "history": list(history or []),
        }
        result = graph.invoke(
            state,
            {"configurable": {"thread_id": self.thread_id}},
        )
        if result.get("plan"):
            return self._plan_from_payload(result["plan"])
        if result.get("response"):
            return AssistantPlan(fallback_response=self._response_from_payload(result["response"]))
        return self._custom_plan_answer(question, project_slug=project_slug, history=history)

    def _compiled_langgraph(self):
        if self._langgraph_graph is not None:
            return self._langgraph_graph

        from langgraph.checkpoint.memory import InMemorySaver
        from langgraph.graph import END, START, StateGraph

        def classify(state: dict[str, Any]) -> dict[str, Any]:
            question = str(state.get("question", "")).strip()
            project_slug = state.get("project_slug")
            if not question:
                response = AssistantResponse(answer="Ask a question about the portfolio projects.", citations=())
                return {"response": self._response_payload(response)}

            capability_response = self._try_capability_route(question, project_slug)
            if capability_response:
                return {"response": self._response_payload(capability_response)}

            runtime_response = self._try_runtime_route(question)
            if runtime_response:
                return {"response": self._response_payload(runtime_response)}

            trait_response = self._try_project_traits_route(question, project_slug)
            if trait_response:
                return {"response": self._response_payload(trait_response)}
            return {}

        def route_after_classify(state: dict[str, Any]) -> str:
            return END if state.get("response") else "retrieve"

        def retrieve(state: dict[str, Any]) -> dict[str, Any]:
            question = str(state.get("question", "")).strip()
            project_slug = state.get("project_slug")
            history = state.get("history") or []
            data_response = self._try_data_route(question, project_slug)
            search_query = self._search_query(question, history)
            results = self.index.search(search_query, project_slug=project_slug, limit=6)
            return {
                "data_response": self._response_payload(data_response) if data_response else None,
                "results": [self._search_result_payload(result) for result in results],
            }

        def synthesize(state: dict[str, Any]) -> dict[str, Any]:
            question = str(state.get("question", "")).strip()
            project_slug = state.get("project_slug")
            history = state.get("history") or []
            data_response = (
                self._response_from_payload(state["data_response"])
                if state.get("data_response")
                else None
            )
            results = [self._search_result_from_payload(result) for result in state.get("results", [])]
            plan = self._plan_from_context(
                question=question,
                project_slug=project_slug,
                history=history,
                data_response=data_response,
                results=results,
            )
            return {"plan": self._plan_payload(plan)}

        builder = StateGraph(AgentGraphState)
        builder.add_node("classify", classify)
        builder.add_node("retrieve", retrieve)
        builder.add_node("synthesize", synthesize)
        builder.add_edge(START, "classify")
        builder.add_conditional_edges(
            "classify",
            route_after_classify,
            {"retrieve": "retrieve", END: END},
        )
        builder.add_edge("retrieve", "synthesize")
        builder.add_edge("synthesize", END)
        self._langgraph_graph = builder.compile(checkpointer=InMemorySaver())
        return self._langgraph_graph

    def _plan_payload(self, plan: AssistantPlan) -> dict[str, Any]:
        return {
            "fallback_response": self._response_payload(plan.fallback_response),
            "messages": list(plan.messages),
            "llm_route": plan.llm_route,
        }

    def _plan_from_payload(self, payload: dict[str, Any]) -> AssistantPlan:
        return AssistantPlan(
            fallback_response=self._response_from_payload(payload["fallback_response"]),
            messages=tuple(payload.get("messages", [])),
            llm_route=str(payload.get("llm_route", "llm_rag")),
        )

    def _response_payload(self, response: AssistantResponse) -> dict[str, Any]:
        return {
            "answer": response.answer,
            "citations": [
                {
                    "project_slug": citation.project_slug,
                    "source_type": citation.source_type,
                    "path": citation.path,
                    "section": citation.section,
                    "score": citation.score,
                }
                for citation in response.citations
            ],
            "data_result": self._query_result_payload(response.data_result) if response.data_result else None,
            "route": response.route,
        }

    def _response_from_payload(self, payload: dict[str, Any]) -> AssistantResponse:
        return AssistantResponse(
            answer=str(payload.get("answer", "")),
            citations=tuple(
                Citation(
                    project_slug=str(citation.get("project_slug", "")),
                    source_type=str(citation.get("source_type", "")),
                    path=str(citation.get("path", "")),
                    section=str(citation.get("section", "")),
                    score=float(citation.get("score", 0.0)),
                )
                for citation in payload.get("citations", [])
            ),
            data_result=(
                self._query_result_from_payload(payload["data_result"])
                if payload.get("data_result")
                else None
            ),
            route=str(payload.get("route", "rag")),
        )

    def _query_result_payload(self, result: QueryResult) -> dict[str, Any]:
        return {
            "columns": list(result.columns),
            "rows": [[str(value) for value in row] for row in result.rows],
            "row_count": result.row_count,
        }

    def _query_result_from_payload(self, payload: dict[str, Any]) -> QueryResult:
        return QueryResult(
            columns=tuple(str(column) for column in payload.get("columns", [])),
            rows=tuple(tuple(row) for row in payload.get("rows", [])),
            row_count=int(payload.get("row_count", 0)),
        )

    def _search_result_payload(self, result: SearchResult) -> dict[str, Any]:
        return {
            "text": result.text,
            "metadata": dict(result.metadata),
            "score": result.score,
        }

    def _search_result_from_payload(self, payload: dict[str, Any]) -> SearchResult:
        return SearchResult(
            text=str(payload.get("text", "")),
            metadata={str(key): str(value) for key, value in payload.get("metadata", {}).items()},
            score=float(payload.get("score", 0.0)),
        )

    def _try_runtime_route(self, question: str) -> AssistantResponse | None:
        lower = question.lower()
        runtime_phrases = (
            "which model are you",
            "what model are you",
            "what model is this",
            "are you a live model",
            "are you live",
            "local version",
            "local model",
            "live model",
            "api key",
            "key source",
            "which provider",
            "what provider",
            "runtime",
        )
        if not any(phrase in lower for phrase in runtime_phrases):
            return None

        if not self.runtime:
            return AssistantResponse(
                answer=(
                    "I am the 365DS Portfolio Learning Helper. This assistant instance does not "
                    "have runtime metadata attached, so I cannot report the active provider or model."
                ),
                citations=(),
                route="runtime",
            )

        status = "live model synthesis" if self.runtime.live_enabled else "local retrieval fallback"
        key_source = self.runtime.api_key_source or "none"
        answer = (
            "I am the 365DS Portfolio Learning Helper, not one of the project ML models. "
            f"Current runtime: {status}. "
            f"Provider: {self.runtime.provider}. "
            f"Mode: {self.runtime.effective_mode}. "
            f"Chat model: {self.runtime.chat_model}. "
            f"Key source: {key_source}. "
            f"Base URL: {self.runtime.base_url}."
        )
        return AssistantResponse(answer=answer, citations=(), route="runtime")

    def _try_capability_route(self, question: str, project_slug: str | None) -> AssistantResponse | None:
        lower = question.lower().strip()
        help_phrases = (
            "how can you help",
            "how can u help",
            "what can you do",
            "what do you do",
            "what can i ask",
            "help me",
            "help with",
        )
        asks_help = any(phrase in lower for phrase in help_phrases)
        asks_sql_capability = (
            ("can you" in lower or "do you" in lower)
            and any(term in lower for term in ("sql", "query", "queries", "queies"))
            and any(term in lower for term in ("run", "write", "execute", "create", "help"))
        )

        if not asks_help and not asks_sql_capability:
            return None

        if asks_sql_capability:
            answer = (
                "Yes, with guardrails. I can help write SQL for the portfolio projects, explain the existing SQL pipelines, "
                "and answer data questions from approved DuckDB Gold marts. In the app, executable data access is read-only: "
                "single `SELECT` or `WITH` queries against catalog-approved `gold.*` tables for a selected project. "
                "I do not run writes, raw/Bronze/Silver queries, arbitrary database paths, file reads, or destructive SQL. "
                "For live model SQL planning, use the Quiz And Data page with a configured provider or session key; the generated SQL still passes the same Gold-only validator before DuckDB executes it."
            )
        else:
            scope = "the selected project" if project_slug else "all five projects"
            answer = (
                f"I can help you explore {scope} in a few practical ways:\n\n"
                "- Explain the five analytics projects, their business questions, datasets, medallion layers, and dashboards.\n"
                "- Answer quiz-style and report questions with citations from indexed project docs and reports.\n"
                "- Explain architecture choices such as DuckDB, Streamlit, SQL-first pipelines, provider-agnostic AI, and LangGraph.\n"
                "- Query approved Gold marts through the safe DuckDB data tool when a project scope/table is selected.\n"
                "- Help draft or review SQL/Python/Streamlit work for these projects, while keeping raw data and lower warehouse layers protected.\n\n"
                "A good next question is: `Which projects use SQL-first medallion layers?` or choose a project and ask for its quiz answers or KPIs."
            )

        citations = (
            Citation(
                project_slug or "learning-hub",
                "app_contract",
                "apps/learning-hub/docs/architecture.md",
                "Assistant Backends",
                1.0,
            ),
            Citation(
                project_slug or "learning-hub",
                "app_contract",
                "apps/learning-hub/docs/architecture.md",
                "Data Access",
                1.0,
            ),
        )
        return AssistantResponse(answer=answer, citations=citations, route="capabilities")

    def _try_project_traits_route(self, question: str, project_slug: str | None) -> AssistantResponse | None:
        if project_slug:
            return None
        lower = question.lower()
        asks_sql_first = "sql-first" in lower or "sql first" in lower or ("sql" in lower and "medallion" in lower)
        if not asks_sql_first:
            return None

        sql_first = [
            project
            for project in self.projects
            if project.traits.get("workflow") == "sql_first_medallion"
        ]
        other_medallion = [
            project
            for project in self.projects
            if project.traits.get("workflow") != "sql_first_medallion"
            and "medallion" in project.traits.get("workflow", "")
        ]
        lines = [
            "The SQL-first medallion projects are:",
            "",
            *[f"- **{project.title}**" for project in sql_first],
        ]
        if other_medallion:
            lines.extend(
                [
                    "",
                    "Also note: these projects still use DuckDB medallion layers, but they are not SQL-first:",
                    *[f"- **{project.title}**: {self._workflow_label(project.traits.get('workflow', ''))}" for project in other_medallion],
                ]
            )
        lines.append("")
        lines.append("All five projects use DuckDB as the analytics engine and Streamlit for visualization.")
        citations = tuple(
            Citation(
                project.slug,
                "catalog",
                "apps/learning-hub/catalog/projects.yaml",
                "traits",
                1.0,
            )
            for project in (*sql_first, *other_medallion)
        )
        return AssistantResponse(answer="\n".join(lines), citations=citations, route="project_traits")

    def _workflow_label(self, workflow: str) -> str:
        labels = {
            "python_first_medallion": "Python-first medallion",
            "python_functions_medallion": "Python function-heavy medallion",
            "sql_first_medallion": "SQL-first medallion",
        }
        return labels.get(workflow, workflow.replace("_", " "))

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
                "This local fallback is retrieval-grounded. Configure a live provider or enter a session API key for more fluent synthesized answers.",
            ]
        )
        return "\n".join(lines)

    def _llm_messages(
        self,
        question: str,
        results: list[SearchResult],
        data_response: AssistantResponse | None,
        history: Sequence[Message] | None,
    ) -> list[Message]:
        context_lines: list[str] = []
        for index, result in enumerate(results[:6], start=1):
            metadata = result.metadata
            label = (
                f"[S{index}] project={metadata.get('project_slug', '')}; "
                f"type={metadata.get('source_type', '')}; path={metadata.get('path', '')}; "
                f"section={metadata.get('section', '')}"
            )
            context_lines.append(label)
            context_lines.append(shorten(" ".join(result.text.split()), width=1200, placeholder="..."))
            context_lines.append("")

        data_block = ""
        if data_response and data_response.data_result:
            data_block = response_table_markdown(data_response.data_result)

        history_block = self._history_block(history)
        system = (
            "You are the 365DS Portfolio Learning Helper. Answer as a practical tutor for "
            "analytics learners and portfolio reviewers. Cite sources using the provided "
            "source labels or Gold table names. Cite sources; do not invent facts. If the "
            "recent conversation, provided context, and approved data do not answer the question, say: "
            "\"I don't know from the indexed project sources.\""
        )
        user = (
            f"Recent conversation:\n{history_block or 'No previous conversation in this session.'}\n\n"
            f"Question:\n{question}\n\n"
            f"Retrieved context:\n{chr(10).join(context_lines).strip() or 'No retrieved text context.'}\n\n"
            f"Approved Gold data:\n{data_block or 'No Gold data result.'}"
        )
        return [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ]

    def _search_query(self, question: str, history: Sequence[Message] | None) -> str:
        history_block = self._history_block(history, max_turns=4)
        if not history_block:
            return question

        lower = question.lower()
        follow_up_markers = (
            " it ",
            " that ",
            " this ",
            " they ",
            " them ",
            " those ",
            " role ",
            " mean ",
            " also ",
            " about ",
        )
        starts_like_follow_up = lower.startswith(("does ", "do ", "is ", "are ", "and ", "also ", "what about", "how about"))
        if starts_like_follow_up or any(marker in f" {lower} " for marker in follow_up_markers):
            return f"{history_block}\n\nFollow-up question: {question}"
        return question

    def _history_block(self, history: Sequence[Message] | None, max_turns: int = 6) -> str:
        if not history:
            return ""
        turns: list[str] = []
        for message in list(history)[-max_turns:]:
            role = str(message.get("role", "user")).strip() or "user"
            if role not in {"user", "assistant"}:
                continue
            content = str(message.get("content", "")).strip()
            if not content:
                continue
            turns.append(f"{role}: {shorten(' '.join(content.split()), width=500, placeholder='...')}")
        return "\n".join(turns)

    def _with_llm_fallback_note(self, response: AssistantResponse, exc: Exception) -> AssistantResponse:
        note = (
            "\n\nLive model synthesis was configured but unreachable, so this answer used the local grounded fallback. "
            f"Error type: {type(exc).__name__}. Check the AI Runtime provider/base URL or switch to local mode to avoid live calls."
        )
        return AssistantResponse(
            answer=response.answer + note,
            citations=response.citations,
            data_result=response.data_result,
            route=response.route,
        )

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
