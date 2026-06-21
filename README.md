# 365DS Analytics Portfolio

Five analytics case studies and one AI learning experience, delivered as a single Streamlit portfolio. The repository keeps the complete project evidence public: source briefs and datasets, Bronze/Silver/Gold pipelines, quality checks, reports, dashboards, and the provider-agnostic Learning Hub.

## Portfolio App

The public app uses stable pages so each LinkedIn post can link directly to the relevant project while visitors can still move through the complete portfolio from one sidebar.

| Experience | Public path |
| --- | --- |
| Portfolio overview | `/` |
| Real Estate Market Analysis | `/real-estate` |
| User Journey Analysis | `/user-journey` |
| Checkout Flow Optimization | `/checkout-flow` |
| Customer Engagement Analysis | `/customer-engagement` |
| Tracking User Engagement | `/tracking-engagement` |
| AI Learning Helper | `/ai-helper` |
| Quiz And Data Coach | `/quiz-data` |
| Architecture And Lineage | `/lineage` |

The Streamlit Community Cloud entrypoint is `apps/learning-hub/streamlit_app.py`.

## Architecture

- DuckDB implements reproducible Bronze, Silver, and Gold analytics layers.
- Python orchestrates pipelines and handles project-specific algorithms and statistical work.
- Streamlit and Plotly present Gold-only dashboards.
- The Learning Hub indexes project evidence for citation-grounded retrieval.
- The AI assistant supports local TF-IDF fallback, direct OpenRouter/Groq providers, optional LiteLLM, session-only BYOK, and LangGraph orchestration.
- The safe data coach executes read-only queries against catalog-approved `gold.*` marts only.

## Local Run

```powershell
uv venv .venv-365ds --python 3.13
uv pip install --python .\.venv-365ds\Scripts\python.exe -r requirements-learning-hub.txt
.\.venv-365ds\Scripts\streamlit.exe run apps\learning-hub\streamlit_app.py --server.port 8507
```

The app builds its local TF-IDF index on first use. Full local warehouses are preferred; committed Gold-only snapshots provide the Streamlit Cloud runtime data boundary.

See [the deployment runbook](docs/deployment/streamlit-community-cloud.md) and [Learning Hub documentation](apps/learning-hub/README.md) for details.
