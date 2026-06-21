# Thread Walkthrough

## M1 - Repository Initialized And Skill Package Started

- Git was initialized in `C:\Users\Nitro\data-analytics-project\365ds-demo-projects`.
- The repo initially contained project briefs in `project-instructions/` and raw sources in `source-datasets/`.
- Source repos were inspected for reusable context:
  - Maven Fuzzy Factory provided a standardized DuckDB medallion analytics workflow.
  - Baraa warehouse example provided a second DuckDB warehouse and star-schema reference.
  - AICVGen provided general engineering skills and a memory artifact pattern.
- Hidden `.agents` and `.codex` paths were not viable for new child files in this sandbox due ACL Deny entries, so the working skill package was created in `agent-skills/`.

## M2 - External Analytics And Pipeline Skills Adapted

- The requested GitHub skill folders were reviewed:
  - `12-data-analytics`
  - `11-data-pipelines`
- Instead of copying all narrow upstream skills, the useful concepts were condensed into three repo-local skills:
  - `analytics-sql-patterns`
  - `dashboard-storytelling`
  - `data-quality-contracts`
- The adaptation keeps this repo focused on 365DS project briefs, immutable raw datasets, DuckDB-friendly SQL, Streamlit/Tableau-ready outputs, and quality gates.

## M3 - Hidden Skill Paths Repaired

- Normal writes to `.agents/` and `.codex/` failed because those hidden directories carried sandbox-hostile Deny ACL behavior.
- Direct ACL edits and `icacls /remove:d` did not make the normal sandbox write path reliable.
- The durable local fix was to preserve the old hidden roots under `C:\tmp`, then replace `.agents` and `.codex` with junction roots into `agent-hidden-roots/`.
- `.agents/skills` and `.codex/skills` now both point to `agent-skills/`, keeping one canonical visible skill package while making hidden skill paths usable.

## M4 - DuckDB Streamlit Project Pattern Established

- The analytics stack was set to DuckDB plus Streamlit, with `.venv-365ds` as the project environment.
- Real Estate Market Analysis became the first completed project, proving the Bronze/Silver/Gold pattern on CSV sources.
- User Journey Analysis became the second completed project, keeping the required Python journey functions while exposing reusable DuckDB Gold marts and a Streamlit dashboard.
- A deferred mission was recorded: after the remaining projects are complete, standardize relational transformations so Python orchestrates and SQL files define Bronze/Silver/Gold tables wherever practical.

## M5 - Checkout Flow Optimization Added

- Checkout Flow Optimization was implemented as the first SQL-first project in `projects/checkout-flow-optimization/`.
- The MySQL dump is parsed into DuckDB Bronze tables, Silver filters the July 2022 through January 2023 analysis window, and Gold produces monthly checkout, abandonment, error, device, KPI, quiz, and report outputs.
- The Streamlit dashboard reads Gold marts only and translates the Tableau story requirements into three tabs: checkout success, cart abandonment, and errors/devices.
- MySQL CLI remains a fallback validation oracle, but DuckDB is canonical because ingestion and quality checks passed locally.

## M6 - Customer Engagement Analysis Added

- Customer Engagement Analysis was implemented in `projects/customer-engagement-analysis/` as the second SQL-first Tableau-to-Streamlit project.
- The source MySQL dump requires multi-block INSERT parsing for `365_student_learning`; Bronze records insert-block counts so the parser behavior is quality-checked.
- Silver creates subscription windows, country labels from installed Babel data, and the course-required `student_engagement` extract with 81,532 rows.
- Gold produces course performance, monthly engagement, onboarding, country funnel, KPI, quiz, and report marts; the dashboard reads Gold only.

## M7 - Tracking User Engagement Added

- Tracking User Engagement was implemented in `projects/tracking-user-engagement/` as a SQL-first DuckDB project with Python statistical/model outputs.
- Bronze parses the MySQL dump with multi-block INSERT support; Silver creates subscription windows, Q2 watched-minute cohorts, paid/free flags, and certificate-minute extracts.
- Gold keeps relational marts in SQL, then Python creates 99th-percentile filtered datasets, confidence interval statistics, t-test outputs, certificate correlation, linear regression, probability, KPI, quiz, and report tables.
- The Streamlit dashboard reads Gold only and covers Q2 engagement, distribution/outliers, statistical tests, and certificate prediction.

## M8 - Portfolio Learning Hub Added

- The standalone LangChain chatbot idea was upgraded into `apps/learning-hub/`, one cross-project portfolio assistant for all five completed projects.
- The hub uses a YAML project catalog, indexes docs/reports/instructions/code/Gold table summaries, and provides a citation-first local retrieval fallback that works without an API key.
- A safe DuckDB tool reads only approved `gold.*` marts from each project warehouse and rejects writes, lower-layer access, unapproved tables, and multi-statement SQL.
- Docker support was added from v1 via `Dockerfile.learning-hub` and `docker-compose.yml`; local Streamlit and Docker verification both pass when Docker Desktop is running.

## M9 - Learning Hub Provider Layer Started

- Batch 1 upgraded the hub from local-only retrieval to an optional provider-agnostic live AI layer.
- Default configuration targets owner gateway mode with LiteLLM, while OpenRouter and custom OpenAI-compatible endpoints use the same adapter contract.
- If no key is configured, the hub stays in local TF-IDF retrieval plus DuckDB Gold mode; visitor BYOK is session-only and masked in UI status.
- The AI Helper page now shows runtime status, starter prompts, clear chat, and streamed assistant responses.

## M10 - Learning Hub Gateway And Planner Added

- Batch 2 added optional Chroma/OpenAI-compatible vector indexing while keeping TF-IDF as the no-key deterministic backend.
- The index manifest now records a source hash, backend, and embedding model so model/source drift can be detected before relying on stale retrieval.
- Docker Compose now has an optional LiteLLM gateway profile using a project-local config file; OpenRouter remains a managed gateway option through env configuration.
- The Quiz/Data Coach can use a live model to propose JSON SQL, but every query still runs through the existing approved Gold-mart validator before DuckDB execution.

## M11 - Provider-Agnostic Hub Upgrade Documented

- Batch 3 documented local, OpenRouter, custom OpenAI-compatible, LiteLLM, BYOK, and Chroma runbooks in the Learning Hub README.
- The architecture note now reflects the actual live AI, vector index, gateway, and Gold SQL planner behavior.
- ADR-001 records the provider-agnostic runtime decision and why BYOK-only, OpenAI-only, and Celery-from-v1 were rejected.
- Docker Compose config, image build, indexer run, container startup, HTTP smoke test, and container-internal pytest all pass with Docker Desktop running.

## M12 - Learning Hub Conversational Agent Upgrade Added

- The assistant now has session-only conversational memory, follow-up-aware retrieval, and runtime self-awareness so questions about the active model/provider do not get confused with project ML models.
- `catalog/projects.yaml` records project traits for workflow, analytics engine, visualization, and AI data access; the assistant uses these traits for deterministic portfolio architecture answers such as SQL-first medallion project lists.
- `LEARNING_HUB_AGENT_BACKEND=custom|langgraph|auto` selects between the default custom backend and an optional LangGraph `StateGraph` backend with session-local thread IDs.
- ADR-002 documents the hybrid backend decision; README, architecture notes, `.env.example`, and Compose expose the new backend selector.
- Local and Docker verification pass with LangGraph installed: 31 hub tests, index checks, Docker rebuild, container tests, HTTP smoke, and explicit container LangGraph route smoke.

## M13 - Learning Hub Capability QA Fix

- User testing showed that assistant self/capability questions like "how can you help me" and "can you run or write sql queries" were still being treated as project RAG questions.
- A deterministic `capabilities` route now answers app-contract and SQL-safety questions before retrieval or live model calls.
- Regression tests cover the two user prompts plus LangGraph parity; local and container test suites now pass with 34 tests.
- Docker was rebuilt and the running service on `http://localhost:8507` was recreated so the browser app serves the fixed assistant.

## M14 - Learning Hub Owner-Key BYOK Runtime Fix

- The Learning Hub now defaults to direct OpenRouter provider mode instead of an optional LiteLLM gateway hostname, so Docker no longer starts with a missing live endpoint by default.
- Groq is a first-class provider preset with `GROQ_API_KEY`, Groq's OpenAI-compatible base URL, and common Groq model IDs.
- The Streamlit AI Runtime panel exposes local/live mode, provider, model/custom model, relevant base URL, key-source status, and session-only BYOK.
- Live-provider failures are classified into rate limit, auth, connection, invalid model, and other categories; local grounded fallback still answers while the UI explains the right next action.
- Local verification passes with 40 Learning Hub tests plus compile and index checks.
- Follow-up testing switched the OpenRouter default to `cohere/north-mini-code:free`, added OpenRouter-vs-Groq key-shape warnings, made simple greetings and typo-ish runtime questions deterministic, and verified the Docker app starts live with the owner key from ignored `.env`.

## M15 - Portfolio STAR-B Retrospectives Added

- A portfolio-level STAR-B retrospective package was added under `docs/retrospectives/`.
- The package treats the whole repo as one delivered portfolio product: five analytics projects, DuckDB medallion pipelines, Streamlit dashboards, reports, quiz support, Learning Hub, AI assistant, provider runtime, safe data tool, LangGraph option, and Docker path.
- `bug-recovery-ledger.md` turns the documented delivery friction into evidence-backed stories, including Windows ACL issues, uv/cache setup friction, multi-INSERT SQL dump parsing, Docker readiness, assistant routing fixes, provider fallback fixes, and dashboard service recovery.
- `evidence-ledger.md` maps claims to repo artifacts and explicitly marks unsupported production/user/adoption claims as not claimed.
- Verification focused on docs quality: diff whitespace checks, secret-pattern scan over the retrospective package, and coverage scans for key architecture and recovery terms.

## M16 - Per-Project STAR-B Retrospectives Added

- Each analytics project now has its own STAR-B retrospective under `projects/*/reports/`.
- New retrospectives were added for User Journey Analysis, Checkout Flow Optimization, Customer Engagement Analysis, and Tracking User Engagement.
- Each report follows the same proof pattern: metadata, transparency statement, audience fit, STAR-B stories, evidence ledger, delivered artifacts, stack/trade-offs, metrics, challenges, risks, proof summaries, resume bullets, LinkedIn angle, follow-ups, and final judgment.
- Verification confirmed five project-level retrospective files, no secret-pattern matches, no non-ASCII characters, and clean `git diff --check`.

## M17 - Project Retrospectives Expanded To Raw Proof Depth

- User feedback rejected the compressed Real Estate rewrite because the original detailed style was stronger.
- Real Estate was recreated as a fuller raw STAR-B proof document rather than a compact summary.
- User Journey, Checkout Flow Optimization, Customer Engagement Analysis, and Tracking User Engagement were expanded with detailed proof addenda and raw template completion notes.
- The project-level reports now preserve more hiring/recruiter/freelance material: delivery contracts, deeper evidence ledgers, trade-offs, timelines, interview answers, public-version notes, claim-safety checks, and one-page summaries.
- Future public case studies should be shortened from these raw proof reports instead of replacing them.

## M18 - Streamlit Community Cloud Portfolio Design Approved

- The deployment shape is one public multipage Streamlit app, not six independent apps.
- `apps/learning-hub/streamlit_app.py` remains the entrypoint and gains internal pages for all five dashboards with stable deep links for LinkedIn posts.
- The complete GitHub repository will be public, including source datasets, instructions, Bronze/Silver/Gold code, dashboards, reports, retrospectives, and the Learning Hub.
- Release-generated Gold-only DuckDB snapshots are a cloud runtime optimization and safe execution boundary; they do not hide the source or lower-layer implementation.
- The TF-IDF index will be built automatically when missing or stale instead of committing the current machine-specific pickle.
- The approved design is recorded at `docs/superpowers/specs/2026-06-21-streamlit-cloud-portfolio-design.md`; implementation planning is the next step.

## M19 - Streamlit Cloud Portfolio Release Implemented

- The Learning Hub now registers all five analytics dashboards through `st.navigation` with stable flat paths for LinkedIn and portfolio links.
- Each dashboard prefers its full local warehouse and falls back to a release-generated Gold-only snapshot when the ignored local warehouse is unavailable in Community Cloud.
- The app builds its local TF-IDF index when missing or stale, so deployment does not rely on a machine-specific committed pickle.
- Root Streamlit configuration, an app-local runtime requirements file, GitHub source links, a portfolio README, and a Community Cloud runbook complete the deployment package.
- Verification passed with 56 hub tests, explicit compilation, a 104-document/465-chunk index check, a Gold-only schema audit of all five snapshots, and HTTP 200 responses for the root and eight deep links.

## M20 - Community Cloud Cache Collision Diagnosed

- The public app launched at `https://365ds-analytics-portfolio-apps.streamlit.app/`, but four project pages failed after Real Estate was visited.
- Exported Cloud logs showed project-specific KPI `KeyError`s even though local and cloud snapshot schemas matched.
- A five-dashboard Streamlit AppTest sequence reproduced the exact order-dependent failure locally and isolated the cause: identical cached query functions keyed on SQL but not warehouse path.
- All five dashboards now pass the resolved DuckDB path as an explicit cached argument, preventing cross-project DataFrame reuse while preserving read-only Gold access.
- The regression test moved from four failing project pages to one passing five-page sequence.

## M21 - Community Cloud Release Recovered And Groq Enabled

- Cache-isolation commit `d6ce2b1` reached `master` and triggered the Community Cloud rebuild.
- Public route probes returned HTTP 200, and the user confirmed User Journey, Checkout Flow, Customer Engagement, and Tracking Engagement all render again.
- The live AI runtime was switched from the no-key fallback/OpenRouter test path to Groq through Streamlit's encrypted Secrets panel.
- Production runtime metadata now reports provider `groq`, model `llama-3.3-70b-versatile`, and live synthesis enabled; TF-IDF remains the no-key fallback.
- The Groq key posted in chat must be rotated and replaced in Streamlit Secrets before the app is treated as production-ready.
