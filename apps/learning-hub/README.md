# 365DS Portfolio Learning Hub

The Learning Hub is a cross-project Streamlit app for exploring the five completed 365DS analytics projects. It indexes project docs, reports, instructions, SQL, Python code, quality checks, and Gold table catalogs, then provides a citation-first AI helper and a safe read-only DuckDB data tool.

## Local Run

```powershell
.\.venv-365ds\Scripts\python.exe apps\learning-hub\scripts\build_index.py --check
.\.venv-365ds\Scripts\python.exe apps\learning-hub\scripts\build_index.py
.\.venv-365ds\Scripts\streamlit.exe run apps\learning-hub\streamlit_app.py --server.port 8507
```

Open `http://localhost:8507`.

## Docker Run

```powershell
docker compose config
docker compose build learning-hub
docker compose run --rm indexer
docker compose up learning-hub
```

The Compose app exposes the hub at `http://localhost:8507`.

## AI Configuration

The local TF-IDF backend works without an API key and is used for tests/offline demos. To enable OpenAI-backed answer generation in a later enhancement, copy `.env.example` to `.env` and set `OPENAI_API_KEY`.

## Safety

- The data tool connects to project warehouses in DuckDB read-only mode.
- Queries are restricted to approved `gold.*` marts listed in `catalog/projects.yaml`.
- Writes, lower-layer access, arbitrary file paths, and destructive SQL are blocked.
- Generated `.index/`, `.chroma/`, caches, and logs are ignored by git.
