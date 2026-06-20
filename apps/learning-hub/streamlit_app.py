from __future__ import annotations

from pathlib import Path
from uuid import uuid4

import pandas as pd
import streamlit as st

from learning_hub.assistant import LearningAssistant, response_table_markdown
from learning_hub.catalog import catalog_summary, describe_gold_tables, get_project, load_catalog
from learning_hub.data_tool import GoldQueryTool, UnsafeQueryError
from learning_hub.indexing import check_index_inputs, load_manifest, load_search_index
from learning_hub.llm_client import classify_provider_error, create_llm_client
from learning_hub.paths import DEFAULT_INDEX_DIR, display_path
from learning_hub.provider_catalog import get_provider_preset, key_provider_warning, model_options, provider_labels
from learning_hub.settings import load_ai_settings, resolve_ai_runtime
from learning_hub.sql_planner import plan_and_run_gold_query


st.set_page_config(page_title="365DS Learning Hub", layout="wide")


@st.cache_data(show_spinner=False)
def cached_projects():
    return load_catalog()


@st.cache_data(show_spinner=False)
def cached_summary() -> pd.DataFrame:
    return pd.DataFrame(catalog_summary(cached_projects()))


@st.cache_resource(show_spinner=False)
def cached_index():
    return load_search_index(DEFAULT_INDEX_DIR, settings=load_ai_settings())


@st.cache_resource(show_spinner=False)
def cached_assistant():
    return LearningAssistant(index=cached_index(), projects=cached_projects())


def runtime_controls():
    env_settings = load_ai_settings()
    byok_key = None

    with st.sidebar:
        st.subheader("AI Runtime")
        mode_label = st.selectbox(
            "Mode",
            ["Live provider", "Local fallback"],
            index=1 if env_settings.mode == "local" else 0,
            help="Local fallback uses the indexed sources and DuckDB tool without live model calls.",
        )

        labels = provider_labels()
        provider_keys = list(labels)
        provider = st.selectbox(
            "Provider",
            provider_keys,
            index=provider_keys.index(env_settings.provider) if env_settings.provider in provider_keys else 0,
            format_func=lambda key: labels[key],
            disabled=mode_label == "Local fallback",
        )
        preset = get_provider_preset(provider)

        options = list(model_options(provider))
        custom_option = "Custom model..."
        initial_model = env_settings.chat_model if env_settings.provider == provider else preset.default_model
        selected_model = initial_model if initial_model in options else custom_option
        model_choice = st.selectbox(
            "Model",
            [*options, custom_option],
            index=[*options, custom_option].index(selected_model),
            disabled=mode_label == "Local fallback",
        )
        if model_choice == custom_option:
            chat_model = st.text_input(
                "Custom model ID",
                value=initial_model if initial_model not in options else preset.default_model,
                disabled=mode_label == "Local fallback",
            ).strip()
        else:
            chat_model = model_choice

        base_url = preset.base_url
        if preset.allow_custom_base_url or provider == "litellm":
            base_url = st.text_input(
                "Base URL",
                value=env_settings.base_url if env_settings.provider == provider else preset.base_url,
                disabled=mode_label == "Local fallback",
            ).strip()
        else:
            st.caption(f"Endpoint: `{base_url}`")

        if env_settings.enable_byok:
            byok_key = st.text_input(
                "Session API key",
                type="password",
                help="Optional fallback. Kept only in this Streamlit session and never written to disk.",
            )
        live_mode = "local" if mode_label == "Local fallback" else preset.default_mode
        settings = load_ai_settings(
            overrides={
                "LEARNING_HUB_AI_MODE": live_mode,
                "LEARNING_HUB_PROVIDER": provider,
                "LEARNING_HUB_BASE_URL": base_url,
                "LEARNING_HUB_CHAT_MODEL": chat_model,
            }
        )
        runtime = resolve_ai_runtime(settings, session_api_key=byok_key)
        warning = key_provider_warning(provider, runtime.api_key)
        if warning:
            st.warning(warning)
        st.caption(runtime.safe_label())
        if runtime.live_enabled:
            st.success("Live model synthesis enabled.")
        else:
            st.info(runtime.reason)
        if provider == "litellm" and runtime.live_enabled:
            st.caption("LiteLLM requires the Compose gateway profile or another reachable gateway at the configured base URL.")
    return runtime


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
    runtime = runtime_controls()

    if "learning_hub_messages" not in st.session_state:
        st.session_state.learning_hub_messages = []
    if "learning_hub_thread_id" not in st.session_state:
        st.session_state.learning_hub_thread_id = f"learning-hub-{uuid4().hex}"

    try:
        llm_client = create_llm_client(runtime)
        assistant = LearningAssistant(
            index=cached_index(),
            projects=cached_projects(),
            llm_client=llm_client,
            runtime=runtime,
            agent_backend=runtime.settings.agent_backend,
            thread_id=st.session_state.get("learning_hub_thread_id"),
        )
    except FileNotFoundError:
        st.error("Build the local search index before using the assistant.")
        st.code(r".\.venv-365ds\Scripts\python.exe apps\learning-hub\scripts\build_index.py")
        return

    for message in st.session_state.learning_hub_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if not st.session_state.learning_hub_messages:
        st.chat_message("assistant").markdown(
            "Hi, I can explain the five analytics projects, trace the architecture, help with quiz-style questions, and query approved Gold marts."
        )
        starter_questions = [
            "Which projects use SQL-first medallion layers?",
            "How does the safe DuckDB data tool work?",
            "What quiz answers are available for Tracking User Engagement?",
        ]
        cols = st.columns(len(starter_questions))
        for col, question in zip(cols, starter_questions, strict=True):
            if col.button(question):
                st.session_state.learning_hub_pending_prompt = question

    if st.button("Clear chat", type="secondary"):
        st.session_state.learning_hub_messages = []
        st.session_state.learning_hub_thread_id = f"learning-hub-{uuid4().hex}"
        st.session_state.pop("learning_hub_pending_prompt", None)
        st.rerun()

    prompt = st.session_state.pop("learning_hub_pending_prompt", None)
    prompt = prompt or st.chat_input("Ask about the projects, architecture, quiz answers, or Gold marts")
    if prompt:
        history = list(st.session_state.learning_hub_messages)
        st.session_state.learning_hub_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        response_shell, chunks = assistant.stream_answer(prompt, project_slug=slug, history=history)
        with st.chat_message("assistant"):
            answer = st.write_stream(chunks)
            if response_shell.data_result:
                table_markdown = response_table_markdown(response_shell.data_result)
                st.markdown(table_markdown)
                answer += "\n\n" + table_markdown
            render_citations(response_shell.citations)
            if response_shell.provider_error:
                st.warning(f"{response_shell.provider_error.message} {response_shell.provider_error.action}")
        st.session_state.learning_hub_messages.append({"role": "assistant", "content": answer})


def quiz_data_coach() -> None:
    st.title("Quiz And Data Coach")
    slug = selected_project()
    project = get_project(slug, cached_projects())
    tool = GoldQueryTool(cached_projects())
    runtime = runtime_controls()

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

    st.subheader("Ask Approved Gold Data")
    question = st.text_input("Data question", placeholder="Example: What is the regression R-squared?")
    if st.button("Plan and run Gold query"):
        if not runtime.live_enabled:
            st.warning("Live model synthesis is not configured. Add an owner key or session key to use the SQL planner.")
        else:
            try:
                llm_client = create_llm_client(runtime)
                if llm_client is None:
                    raise RuntimeError("Live model client is unavailable.")
                planned = plan_and_run_gold_query(slug, question, llm_client=llm_client)
                st.code(planned.sql, language="sql")
                if planned.explanation:
                    st.caption(planned.explanation)
                st.dataframe(
                    pd.DataFrame(planned.result.rows, columns=planned.result.columns),
                    use_container_width=True,
                    hide_index=True,
                )
            except (UnsafeQueryError, ValueError, RuntimeError) as exc:
                st.error(str(exc))
            except Exception as exc:
                provider_error = classify_provider_error(exc)
                st.error(f"{provider_error.message} {provider_error.action}")


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
