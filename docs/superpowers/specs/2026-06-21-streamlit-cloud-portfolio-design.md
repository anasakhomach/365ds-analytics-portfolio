# Streamlit Cloud Portfolio Deployment Design

## Status

Approved direction, awaiting implementation-plan approval.

## Summary

Deploy the 365DS workspace as one public Streamlit Community Cloud multipage app backed by the complete public GitHub repository. The Learning Hub remains the single entrypoint and becomes the navigation shell for all five analytics dashboards, the AI helper, Quiz/Data Coach, Project Explorer, and architecture/lineage views.

Each LinkedIn post links directly to a stable project pathname under one branded Streamlit subdomain. Visitors can move between dashboards without opening unrelated apps or losing the portfolio context.

## Goals

- Provide one canonical public portfolio URL.
- Give every analytics project a stable deep link for LinkedIn posts.
- Preserve all five standalone dashboard entrypoints for local development.
- Publish the entire repository: source assets, project instructions, Bronze/Silver/Gold code, quality checks, dashboards, reports, retrospectives, and Learning Hub.
- Make each Streamlit project page link back to the complete GitHub project folder and learning artifacts.
- Keep executable data access read-only and restricted to approved Gold marts.
- Start reliably on Community Cloud without rebuilding every analytics pipeline during a cold start.
- Keep live AI optional, provider-agnostic, and safe when the owner key is unavailable.

## Non-Goals

- Six independent Community Cloud deployments for the initial release.
- Production BI, enterprise authentication, or multi-tenant data access.
- Executable Bronze/Silver/raw SQL through the public AI data tool.
- Celery, background workers, or distributed indexing.
- Replacing GitHub as the complete technical proof surface.

## Chosen Architecture

### Public Surfaces

The public GitHub repository is the complete engineering and learning record. It includes:

- project instructions and source datasets;
- complete Bronze/Silver/Gold pipeline code;
- quality checks and documentation;
- standalone Streamlit dashboard entrypoints;
- reports and detailed STAR-B retrospectives;
- Learning Hub, RAG/indexing, AI provider layer, Quiz/Data Coach, and safe data tool;
- deployment scripts and cloud snapshots.

The Streamlit app is the guided interactive surface. It does not replace or hide project code.

### Community Cloud Entrypoint

- Repository: new public GitHub repository for this workspace.
- Branch: the selected stable branch, initially `master` unless renamed before deployment.
- Entrypoint: `apps/learning-hub/streamlit_app.py`.
- Suggested subdomain: `365ds-analytics-portfolio.streamlit.app`, subject to availability.
- Python: 3.13 to match the verified local environment, provided the Community Cloud build passes.

Community Cloud clones the repository and runs from the repository root. All cloud file paths must use forward slashes and be valid from that working directory.

## Navigation Design

Use `st.Page` and `st.navigation`, with the Learning Hub entrypoint acting as the router.

### Portfolio

- Overview: `/`
- Project Explorer: `/projects`

### Analytics Projects

- Real Estate Market Analysis: `/real-estate`
- User Journey Analysis: `/user-journey`
- Checkout Flow Optimization: `/checkout-flow`
- Customer Engagement Analysis: `/customer-engagement`
- Tracking User Engagement: `/tracking-engagement`

### Learning

- AI Learning Helper: `/ai-helper`
- Quiz And Data Coach: `/quiz-data`

### Architecture

- Architecture And Lineage: `/lineage`

Streamlit page pathnames are flat, stable, and explicitly configured through `url_path`. Each LinkedIn post uses its relevant dashboard URL. The root URL is used for the LinkedIn Featured section, resume, and GitHub README badge.

## Dashboard Integration

Register each existing dashboard script as an internal `st.Page` source relative to the Learning Hub entrypoint. Streamlit supports page files in subdirectories or superdirectories relative to the entrypoint.

The current dashboard files remain valid standalone entrypoints for local development. Page-specific calls to `st.set_page_config` may override the app default additively.

Required changes:

- assign explicit titles, icons, and `url_path` values;
- update each dashboard's database resolver to prefer its committed cloud snapshot when available;
- retain the existing local `projects/<slug>/warehouse.duckdb` fallback;
- add project-proof links for GitHub folder, README, data flow, report, retrospective, and source brief;
- keep dashboard data queries restricted to Gold marts;
- add consistent navigation/branding through the shared Learning Hub shell.

## Cloud Data Contract

### Public Project Data

The full source datasets and all pipeline code remain public in GitHub. Nothing in the Bronze or Silver implementation is withheld.

### Runtime Snapshots

Community Cloud does not receive ignored local `warehouse.duckdb` files. Building all five warehouses on every cold start would be slower and less reliable. Therefore, create release-generated Gold-only snapshots:

```text
apps/learning-hub/data/
  real-estate-market-analysis.duckdb
  user-journey-analysis.duckdb
  checkout-flow-optimization.duckdb
  customer-engagement-analysis.duckdb
  tracking-user-engagement.duckdb
```

Each snapshot contains the project's `gold` schema and approved marts. A release script rebuilds snapshots from the full local project warehouses and validates table names and row counts before publication.

This is a runtime optimization and execution boundary, not a visibility boundary. Visitors can inspect every source, Bronze, Silver, and Gold implementation in GitHub. Public executable SQL remains Gold-only because Gold is the curated reporting contract.

### Path Resolution

- In Community Cloud or when cloud snapshots exist, dashboards and the Learning Hub data tool use `apps/learning-hub/data/<slug>.duckdb`.
- In local standalone dashboard development, the project uses `projects/<slug>/warehouse.duckdb`.
- The resolver must fail clearly when neither path exists.

## RAG And Assistant Startup

Do not commit the current `.index/local_index.pkl` as-is. Its manifest contains an absolute local path and its source hash becomes stale whenever docs/reports change.

On Community Cloud:

- check index inputs at startup;
- build the local TF-IDF index automatically when missing or stale;
- cache the loaded index with `st.cache_resource`;
- store runtime index files only in the app filesystem/cache;
- keep optional Chroma mode disabled unless explicitly configured.

The source corpus remains the complete public repository content selected by the indexer, including instructions, docs, reports, retrospectives, SQL, Python, dashboards, and Gold table metadata.

## AI Runtime And Secrets

- Configure the owner provider key through Streamlit Community Cloud secrets, never through committed `.env` files.
- Keep direct OpenRouter provider mode as the default live path.
- Keep local TF-IDF fallback available when no owner key exists or the provider is unavailable.
- Keep session-only BYOK enabled as the visitor fallback.
- Display provider, model, backend, mode, and safe key-source metadata without showing key values.
- Preserve provider error classification for rate limits, authentication, connection, invalid model, and generic failures.
- Keep SQL planning subject to the same read-only Gold validator.

## Dependencies And Configuration

Add `apps/learning-hub/requirements.txt` because Community Cloud recognizes dependency files at the repository root or beside the entrypoint.

The cloud requirements should:

- pin Streamlit and core analytics packages to verified compatible ranges;
- include DuckDB, pandas, Plotly, PyYAML, scikit-learn, pytest dependencies needed by runtime code, OpenAI client, and LangGraph if the public backend remains selectable;
- omit local-only Jupyter packages;
- omit optional Chroma/LangChain packages unless the deployed app actually uses them;
- be tested with the selected Community Cloud Python version.

Add one root `.streamlit/config.toml` because multiple apps/pages in a repository share the root configuration. Use it for theme and safe server settings only; never store secrets there.

## LinkedIn Linking Strategy

Use the root portfolio URL for:

- LinkedIn Featured section;
- GitHub README badge;
- resume/portfolio master link;
- general architecture or AI Learning Hub posts.

Use project deep links for project-specific posts:

- Real Estate post -> `/real-estate`
- User Journey post -> `/user-journey`
- Checkout post -> `/checkout-flow`
- Customer Engagement post -> `/customer-engagement`
- Tracking Engagement/statistics post -> `/tracking-engagement`
- AI/RAG post -> `/ai-helper`
- Data safety/SQL coach post -> `/quiz-data`

Each project page must include a visible `View project on GitHub` link and links to the report and retrospective.

## Alternatives Considered

### Six Separate Apps

Benefits:

- independent app identity and resource allocation;
- direct project-specific subdomains;
- failures remain isolated.

Costs:

- six deployments and cold starts;
- repeated secret/configuration management;
- fragmented visitor navigation;
- harder to keep branding and links synchronized.

Decision: reject for initial launch.

### Hybrid Hub Plus Standalone Apps

Benefits:

- one portfolio hub plus independent flagship projects.

Costs:

- duplicates deployment work before usage data justifies it.

Decision: defer. Revisit only if a project becomes resource-heavy or earns enough traffic to deserve an independent identity.

## Failure Handling

- Missing cloud snapshot: show a clear deployment-data error with project slug and expected path.
- Missing/stale index: rebuild automatically and show progress status.
- Missing owner key: run local retrieval and keep data pages available.
- Provider failure: classify the error and offer local fallback/BYOK guidance.
- Unsafe SQL: reject before DuckDB execution and explain the Gold-only contract.
- Invalid deep link: Streamlit redirects to the default page; keep all published pathnames stable after launch.
- Resource pressure: lazy page execution, query caching, and Gold-only snapshots reduce memory/startup work. Split a project into a standalone deployment only if measurements justify it.

## Test And Acceptance Plan

### Static And Unit Tests

- Existing Learning Hub tests remain green.
- Add tests for cloud/local warehouse path resolution.
- Add tests for snapshot allowlists and Gold-only schemas.
- Add navigation metadata tests for unique stable pathnames.
- Verify no secrets appear in tracked files or Streamlit config.

### Snapshot Validation

- Rebuild all five local pipelines.
- Generate five Gold-only snapshots.
- Verify approved Gold tables and row counts against source warehouses.
- Verify snapshot files contain no Bronze or Silver schemas.

### Local Cloud-Parity Run

- Run from repository root with the Learning Hub entrypoint.
- Temporarily force cloud snapshot resolution.
- Open every page and deep link.
- Verify all dashboards render from snapshots.
- Verify Project Explorer, AI Helper, Quiz/Data Coach, and Lineage.

### Community Cloud Acceptance

- Build succeeds with the pinned requirements and selected Python version.
- Root URL loads from a cold start.
- Every published deep link loads directly.
- Mobile and desktop layouts do not overlap.
- GitHub/report/retrospective links work.
- AI works with owner key, local fallback, and session BYOK.
- Safe SQL accepts approved Gold queries and rejects writes/lower-layer access.
- No API key value appears in logs, UI, or repository.

## Rollout

1. Commit and clean the current workspace changes.
2. Create the public GitHub repository and add the remote.
3. Push the complete project history/artifacts intended for publication.
4. Implement navigation, snapshot generation, path resolution, cloud index startup, requirements, and config.
5. Run local tests and cloud-parity smoke checks.
6. Deploy one Community Cloud app from `apps/learning-hub/streamlit_app.py`.
7. Configure Streamlit secrets and custom subdomain.
8. Verify all deep links before publishing the first LinkedIn post.
9. Keep the root URL stable; avoid renaming pathnames after posts are published.

## Official Sources

- Community Cloud deployment fields and app URL: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy
- Community Cloud repository/file organization: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/file-organization
- Community Cloud dependencies: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies
- Community Cloud status and limitations: https://docs.streamlit.io/deploy/streamlit-community-cloud/status
- Preferred multipage navigation: https://docs.streamlit.io/develop/concepts/multipage-apps/page-and-navigation
- `st.Page` and stable `url_path`: https://docs.streamlit.io/develop/api-reference/navigation/st.page
- `st.page_link`: https://docs.streamlit.io/develop/api-reference/widgets/st.page_link

