# Learning Hub Architecture

## Purpose

The hub turns the five completed analytics projects into one portfolio learning layer. Visitors can inspect project artifacts, ask grounded questions, view citations, and query modeled Gold marts without modifying project data.

## Runtime Shape

- Streamlit runs one multipage app from `apps/learning-hub/streamlit_app.py`.
- `catalog/projects.yaml` is the source of truth for project paths, reports, dashboards, warehouses, approved Gold tables, and starter questions.
- The default indexer builds a TF-IDF search index under `.index/` for offline demos and tests.
- The optional Chroma backend uses OpenAI-compatible embeddings and records backend, embedding model, and source hash metadata in `manifest.json`.
- Live answers use an OpenAI-compatible client pointed at OpenAI, OpenRouter, LiteLLM, or another compatible gateway.
- The assistant backend is selected by `LEARNING_HUB_AGENT_BACKEND`. `custom` is the default stable path; `langgraph` runs an explicit `StateGraph`; `auto` prefers LangGraph when installed and otherwise uses the custom path.
- Docker Compose runs the hub and an `indexer` one-shot service. The optional `gateway` profile adds a LiteLLM proxy service using `apps/learning-hub/config/litellm_config.yaml`.

## AI Modes

- `local`: no key required; retrieval-grounded fallback and DuckDB Gold tool only.
- `provider`: direct OpenAI-compatible endpoint configured by `LEARNING_HUB_BASE_URL`.
- `gateway`: default owner-key mode for LiteLLM or OpenRouter.
- BYOK: optional visitor key stored only in Streamlit session state.

## Assistant Backends

The custom backend is a small deterministic pipeline: classify runtime/self questions, route catalog-trait questions, optionally query approved Gold marts, retrieve indexed context, and synthesize with the configured live model when available.

The LangGraph backend preserves the same public assistant interface but moves orchestration into a `StateGraph` with classify, retrieve, and synthesize nodes. It uses an in-memory checkpointer plus a Streamlit session thread id, so conversational state is session-scoped and not written to disk.

Both backends share the same provider runtime, BYOK behavior, local TF-IDF or Chroma retrieval, and DuckDB Gold validator.

## Data Access

The hub does not restructure existing projects. It reads the generated `warehouse.duckdb` files and only exposes tables listed in the catalog. The query tool opens DuckDB in read-only mode and rejects writes, raw/Bronze/Silver access, unapproved tables, file reads, and multiple statements.

The LLM SQL planner is advisory only. It must return JSON with a single SQL string, and that SQL still goes through the same Gold-only validator before DuckDB execution.

## Why Celery Is Deferred

Indexing is a one-shot command and chat requests run synchronously in Streamlit. Celery would add a broker, workers, and platform complexity before the workload requires it. If indexing becomes slow or the hub becomes multi-user, add a worker service later behind the same catalog and index contracts.
