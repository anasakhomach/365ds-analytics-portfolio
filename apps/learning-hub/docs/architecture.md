# Learning Hub Architecture

## Purpose

The hub turns the five completed analytics projects into one portfolio learning layer. Visitors can inspect project artifacts, ask grounded questions, view citations, and query modeled Gold marts without modifying project data.

## Runtime Shape

- Streamlit runs one multipage app from `apps/learning-hub/streamlit_app.py`.
- `catalog/projects.yaml` is the source of truth for project paths, reports, dashboards, warehouses, approved Gold tables, and starter questions.
- The local indexer builds a TF-IDF search index under `.index/` for offline demos and tests.
- OpenAI/Chroma dependencies are listed in `requirements-learning-hub.txt` for a fuller RAG backend, but the v1 app does not require network calls.
- Docker Compose runs the hub and an `indexer` one-shot service with persistent volumes for `.index/` and `.chroma/`.

## Data Access

The hub does not restructure existing projects. It reads the generated `warehouse.duckdb` files and only exposes tables listed in the catalog. The query tool opens DuckDB in read-only mode and rejects writes, raw/Bronze/Silver access, unapproved tables, and multiple statements.

## Why Celery Is Deferred

Indexing is a one-shot command and chat requests run synchronously in Streamlit. Celery would add a broker, workers, and platform complexity before the workload requires it. If indexing becomes slow or the hub becomes multi-user, add a worker service later behind the same catalog and index contracts.
