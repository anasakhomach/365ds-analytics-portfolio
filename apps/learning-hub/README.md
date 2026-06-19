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

The hub is provider-agnostic. It defaults to owner gateway mode, but falls back to local TF-IDF retrieval plus the DuckDB Gold tool when no key is configured.

Copy `.env.example` to `.env`, then choose one mode.

### Assistant Backend

```powershell
LEARNING_HUB_AGENT_BACKEND=custom
```

- `custom`: default, lightweight assistant pipeline with session memory, runtime self-awareness, RAG, and safe Gold data routing.
- `langgraph`: explicit LangGraph `StateGraph` backend using session-local thread IDs and the same provider/data-tool contracts.
- `auto`: use LangGraph when the dependency is installed; otherwise fall back to `custom`.

The backend choice does not change data safety: DuckDB access remains read-only and restricted to approved Gold marts.

### Local Fallback

```powershell
LEARNING_HUB_AI_MODE=local
LEARNING_HUB_EMBEDDING_BACKEND=local_tfidf
```

No key is required. Answers are extractive and citation-first.

### OpenRouter

```powershell
LEARNING_HUB_AI_MODE=gateway
LEARNING_HUB_PROVIDER=openrouter
LEARNING_HUB_CHAT_MODEL=~openai/gpt-latest
OPENROUTER_API_KEY=...
```

### Custom OpenAI-Compatible Endpoint

```powershell
LEARNING_HUB_AI_MODE=provider
LEARNING_HUB_PROVIDER=openai_compatible
LEARNING_HUB_BASE_URL=https://api.openai.com/v1
LEARNING_HUB_CHAT_MODEL=gpt-4o-mini
OPENAI_API_KEY=...
```

### LiteLLM Gateway

```powershell
OPENAI_API_KEY=...
LITELLM_API_KEY=anything
LEARNING_HUB_PROVIDER=litellm
LEARNING_HUB_BASE_URL=http://litellm:4000/v1
LEARNING_HUB_CHAT_MODEL=365ds-chat
docker compose --profile gateway up learning-hub litellm
```

The LiteLLM profile uses `apps/learning-hub/config/litellm_config.yaml` and exposes the gateway on port `4000`.

### BYOK

If `LEARNING_HUB_ENABLE_BYOK=true`, visitors can enter a session API key in the Streamlit sidebar. The key is held only in `st.session_state`, masked in status labels, and never written to disk.

### Optional Chroma Index

```powershell
.\.venv-365ds\Scripts\python.exe apps\learning-hub\scripts\build_index.py --backend chroma_openai_compatible
```

Chroma indexing requires a configured embedding key. The default `local_tfidf` backend remains the deterministic offline path.

## Safety

- The data tool connects to project warehouses in DuckDB read-only mode.
- Queries are restricted to approved `gold.*` marts listed in `catalog/projects.yaml`.
- Writes, lower-layer access, arbitrary file paths, and destructive SQL are blocked.
- LLM-generated SQL is treated as untrusted and must pass the same Gold-only validator before execution.
- Generated `.index/`, `.chroma/`, caches, and logs are ignored by git.
