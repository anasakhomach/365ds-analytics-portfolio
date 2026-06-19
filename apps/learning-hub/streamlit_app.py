from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from learning_hub.assistant import LearningAssistant, response_table_markdown
from learning_hub.catalog import catalog_summary, describe_gold_tables, get_project, load_catalog
from learning_hub.data_tool import GoldQueryTool, UnsafeQueryError
from learning_hub.indexing import check_index_inputs, load_local_index, load_manifest
from learning_hub.paths import DEFAULT_INDEX_DIR, display_path


st.set_page_config(page_title="365DS Learning Hub", layout="wide")


@st.cache_data(show_spinner=False)
def cached_projects():
    return load_catalog()


@st.cache_data(show_spinner=False)
def cached_summary() -> pd.DataFrame:
    return pd.DataFrame(catalog_summary(cached_projects()))


@st.cache_resource(show_spinner=False)
def cached_index():
    return load_local_index(DEFAULT_INDEX_DIR)


@st.cache_resource(show_spinner=False)
def cached_assistant():
    return LearningAssistant(index=cached_index(), projects=cached_projects())


def project_options(include_all: bool = False) -> dict[str, str]:
    options = {project.title: project.slug for project in cached_projects()}
    if include_all:
        return {"All Projects": ""} | options
    return options


def selected_project(label: str = "Project", include_all: bool = False) -> str | None:
    options = project_options(include_all=include_all)
    choice = st.selectbox(label, list(options.keys()))
    return options[choice] or None


def render_citations(citations) -> None:
    if not citations:
        return
    st.caption("Sources")
    for citation in citations:
        label = f"{citation.project_slug} | {citation.source_type} | {citation.path}"
        if citation.section:
            label += f" | {citation.section}"
        st.caption(f"- {label} ({citation.score:.3f})")


def portfolio_overview() -> None:
    st.title("365DS Portfolio Learning Hub")
    summary = cached_summary()
    kpi_cols = st.columns(4)
    kpi_cols[0].metric("Projects", len(summary))
    kpi_cols[1].metric("Gold Tables", int(summary["gold_tables"].sum()))
    kpi_cols[2].metric("Indexed Documents", int(summary["documents"].sum()))
    kpi_cols[3].metric("Code Files", int(summary["code_files"].sum()))

    st.dataframe(
        summary[["title", "summary", "gold_tables", "documents", "code_files"]],
        use_container_width=True,
        hide_index=True,
    )

    manifest = load_manifest(DEFAULT_INDEX_DIR)
    if manifest:
        st.caption(
            f"Index backend: {manifest.get('backend')} | chunks: {manifest.get('chunk_count')} | created: {manifest.get('created_at')}"
        )
    else:
        check = check_index_inputs()
        st.warning("Search index has not been built yet.")
        st.code(r".\.venv-365ds\Scripts\python.exe apps\learning-hub\scripts\build_index.py")
        st.caption(f"Ready to index {check.document_count} documents into {check.chunk_count} chunks.")


def project_explorer() -> None:
    st.title("Project Explorer")
    slug = selected_project()
    project = get_project(slug, cached_projects())

    st.subheader(project.title)
    st.write(project.summary)

    left, right = st.columns([2, 3])
    with left:
        st.caption("Artifacts")
        st.write(f"README: `{display_path(project.readme_path)}`")
        st.write(f"Dashboard: `{display_path(project.dashboard_path)}`")
        st.write(f"Warehouse: `{display_path(project.warehouse_path)}`")
        st.caption("Starter Questions")
        for question in project.starter_questions:
            st.write(f"- {question}")

    with right:
        table_rows = [
            {
                "table": table.name,
                "rows": table.row_count,
                "columns": ", ".join(table.columns[:8]),
            }
            for table in describe_gold_tables(project)
        ]
        st.dataframe(pd.DataFrame(table_rows), use_container_width=True, hide_index=True)


def ai_learning_helper() -> None:
    st.title("AI Learning Helper")
    slug = selected_project("Scope", include_all=True)

    try:
        assistant = cached_assistant()
    except FileNotFoundError:
        st.error("Build the local search index before using the assistant.")
        st.code(r".\.venv-365ds\Scripts\python.exe apps\learning-hub\scripts\build_index.py")
        return

    if "learning_hub_messages" not in st.session_state:
        st.session_state.learning_hub_messages = []

    for message in st.session_state.learning_hub_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask about the projects, architecture, quiz answers, or Gold marts"):
        st.session_state.learning_hub_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        response = assistant.answer(prompt, project_slug=slug)
        answer = response.answer
        if response.data_result:
            answer += "\n\n" + response_table_markdown(response.data_result)
        with st.chat_message("assistant"):
            st.markdown(answer)
            render_citations(response.citations)
        st.session_state.learning_hub_messages.append({"role": "assistant", "content": answer})


def quiz_data_coach() -> None:
    st.title("Quiz And Data Coach")
    slug = selected_project()
    project = get_project(slug, cached_projects())
    tool = GoldQueryTool(cached_projects())

    if "mart_quiz_answers" in project.gold_tables:
        result = tool.run_gold_query(
            slug,
            """
            SELECT question_number, question, answer_value, support_value, answer_basis
            FROM gold.mart_quiz_answers
            ORDER BY question_number
            """,
            max_rows=100,
        )
        st.dataframe(pd.DataFrame(result.rows, columns=result.columns), use_container_width=True, hide_index=True)
    else:
        st.info("This project does not expose a quiz-answer Gold mart.")

    st.subheader("Approved Gold Query")
    table_name = st.selectbox("Gold Table", project.gold_tables)
    limit = st.slider("Rows", min_value=5, max_value=50, value=10, step=5)
    try:
        preview = tool.preview_table(slug, table_name, limit=limit)
        st.dataframe(pd.DataFrame(preview.rows, columns=preview.columns), use_container_width=True, hide_index=True)
    except UnsafeQueryError as exc:
        st.error(str(exc))


def architecture_lineage() -> None:
    st.title("Architecture And Lineage")
    slug = selected_project("Project For Detail", include_all=True)

    rows = []
    for project in cached_projects():
        if slug and project.slug != slug:
            continue
        rows.append(
            {
                "project": project.title,
                "brief": display_path(project.instruction_path),
                "docs": len(project.docs),
                "reports": len(project.reports),
                "warehouse": display_path(project.warehouse_path),
                "gold_tables": len(project.gold_tables),
            }
        )
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    st.markdown(
        """
The hub treats each course project as an immutable portfolio artifact. It indexes documentation, reports, source instructions, SQL, Python, dashboards, and generated Gold table catalogs. Data questions are served from read-only DuckDB connections restricted to approved `gold.*` marts.
"""
    )


pages = {
    "Portfolio": [
        st.Page(portfolio_overview, title="Overview"),
        st.Page(project_explorer, title="Project Explorer"),
    ],
    "Learning": [
        st.Page(ai_learning_helper, title="AI Helper"),
        st.Page(quiz_data_coach, title="Quiz And Data"),
    ],
    "Architecture": [
        st.Page(architecture_lineage, title="Lineage"),
    ],
}

navigation = st.navigation(pages)
navigation.run()
