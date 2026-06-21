# Streamlit Community Cloud Deployment

## Deployment Shape

Deploy one multipage app from the public GitHub repository. Do not deploy the five dashboards as separate Community Cloud apps. The shared navigation provides one portfolio URL, stable project deep links, one dependency environment, and one secrets surface.

## GitHub

- Owner: `anasakhomach`
- Repository: `365ds-analytics-portfolio`
- Visibility: public
- Branch: `master`
- Entrypoint: `apps/learning-hub/streamlit_app.py`

The complete repository is public. Cloud runtime reads compact Gold-only snapshots from `apps/learning-hub/data/`; source datasets and all Bronze/Silver/Gold implementation files remain available as portfolio evidence.

Rebuild snapshots before a release:

```powershell
.\.venv-365ds\Scripts\python.exe apps\learning-hub\scripts\build_cloud_snapshots.py
```

## Community Cloud

1. Open `https://share.streamlit.io/user/anasakhomach`.
2. Select **Create app** and choose the GitHub repository.
3. Set branch `master` and file `apps/learning-hub/streamlit_app.py`.
4. Use the deployed subdomain `365ds-analytics-portfolio-apps`.
5. Choose Python 3.13 in advanced settings.
6. Add secrets using the template below, with a fresh owner key.

```toml
LEARNING_HUB_AI_MODE = "provider"
LEARNING_HUB_PROVIDER = "openrouter"
LEARNING_HUB_CHAT_MODEL = "cohere/north-mini-code:free"
LEARNING_HUB_AGENT_BACKEND = "custom"
LEARNING_HUB_EMBEDDING_BACKEND = "local_tfidf"
LEARNING_HUB_ENABLE_BYOK = "true"
LEARNING_HUB_REPOSITORY_URL = "https://github.com/anasakhomach/365ds-analytics-portfolio"
OPENROUTER_API_KEY = "replace-with-a-fresh-key"
```

Never commit the secrets block or paste the real key into repository files.

## Stable Links

The live root is `https://365ds-analytics-portfolio-apps.streamlit.app/`. Use these paths in project-specific posts:

- `/real-estate`
- `/user-journey`
- `/checkout-flow`
- `/customer-engagement`
- `/tracking-engagement`

Use `/ai-helper`, `/quiz-data`, and `/lineage` for posts about the portfolio assistant, guarded SQL coach, and architecture.

## Verification

Open every route in a private browser window. Confirm each dashboard loads KPIs and charts, the sidebar can return to the overview, the GitHub link opens the public source, local retrieval answers without a key, and live synthesis reports the configured provider without exposing its key.
