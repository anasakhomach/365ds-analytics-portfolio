# Current Thread Memory

## Workstream

- Repository: `C:\Users\Nitro\data-analytics-project\365ds-demo-projects`
- Focus: set up durable agent skills and memory for 365 Data Science analytics projects, with reusable data engineering patterns from neighboring DuckDB warehouse repos.
- Current objective: preserve enough repo-local context that future agents can continue analytics or data engineering work without rediscovering the source repos.

## How To Use This Artifact

- Read this file before planning substantial work in this repo.
- Use `thread-walkthrough.md` only when the milestone sequence matters.
- Update this file after meaningful repo changes, verification runs, or durable workflow decisions.
- Keep entries curated and concise; do not paste raw transcript history.

## Durable Decisions

- Raw files under `source-datasets/` are immutable inputs.
- Project briefs under `project-instructions/` define the analysis contract for each 365DS project.
- Local skill package lives under `agent-skills/`.
- `.agents` and `.codex` are repo-local junction roots into `agent-hidden-roots/`.
- `.agents/skills` and `.codex/skills` are junctions to `agent-skills/`, so the hidden skill paths and the visible source package resolve to the same files.
- `.gitignore` excludes `.agents/`, `.codex/`, and `agent-hidden-roots/` because these are local junction/support paths.
- Neighboring repos establish the preferred local warehouse pattern: DuckDB plus Bronze/Silver/Gold layers, Python orchestration, SQL quality checks, and Streamlit dashboards.
- Current repo standard: use DuckDB as the canonical local analytics engine and Streamlit for dashboards. Tableau project briefs remain source requirements, but repo deliverables should use Streamlit unless the user explicitly asks for Tableau.
- Project venv target is `.venv-365ds`, created with the latest local Python that `uv` resolves for Python 3.13. On 2026-06-17 this resolved to CPython 3.13.7.
- `uv` must use the workspace-local cache `.uv-cache/` in this sandbox because the user-level uv cache and `C:\tmp` both hit ACL issues.
- AICVGen memory artifacts were used as the workflow model only; product-specific CV-generator decisions were not imported into this repo.

## Repository Map

- `project-instructions/`: user-facing project briefs.
- `source-datasets/`: raw SQL, CSV, Tableau workbook, PDF, and notebook/source assets.
- `agent-skills/`: repo-local agent skill package.
- `docs/agent-memory/`: durable memory package for future handoffs.
- `requirements-analytics.txt`: common Python/Jupyter analytics environment for pandas, plotting, stats, and ML.
- `requirements-langchain.txt`: pinned LangChain/OpenAI/Chroma environment for the chatbot project.
- `projects/real-estate-market-analysis/`: first implemented 365DS project, with DuckDB Bronze/Silver/Gold scripts, SQL quality checks, docs, and a Streamlit dashboard reading Gold marts only.
- `projects/user-journey-analysis/`: second implemented 365DS project, with required journey helper functions, DuckDB Bronze/Silver/Gold scripts, SQL quality checks, docs, report, and a Streamlit dashboard reading Gold marts only.
- `projects/checkout-flow-optimization/`: third implemented 365DS project, with SQL-first DuckDB Bronze/Silver/Gold layers, MySQL dump ingestion, SQL quality checks, generated business report, and a Streamlit dashboard reading Gold marts only.
- `projects/customer-engagement-analysis/`: fourth implemented 365DS project, with SQL-first DuckDB Bronze/Silver/Gold layers, multi-insert MySQL dump parsing, SQL quality checks, generated business report, and a Streamlit dashboard reading Gold marts only.
- `projects/tracking-user-engagement/`: fifth implemented 365DS project, with SQL-first DuckDB Bronze/Silver/Gold layers, multi-insert MySQL dump parsing, Python-generated statistical/model Gold marts, generated business report, and a Streamlit dashboard reading Gold marts only.

## Imported Skills

Custom skills:
- `data-analytics-case-study`
- `analytics-sql-patterns`
- `dashboard-storytelling`
- `duckdb-medallion-pipeline`
- `data-quality-contracts`
- `repo-memory-ledger`

Imported from `C:\Users\Nitro\aicvgen\.tmp\agent-skills\skills`:
- `using-agent-skills`
- `context-engineering`
- `planning-and-task-breakdown`
- `incremental-implementation`
- `test-driven-development`
- `debugging-and-error-recovery`
- `code-review-and-quality`
- `documentation-and-adrs`
- `git-workflow-and-versioning`
- `source-driven-development`

## Source Repos Consulted

- `C:\Users\Nitro\data-analytics-project\maven-fuzzy-factory`: standardized DuckDB analytics pipeline with `warehouse.duckdb`, Bronze/Silver/Gold scripts, SQL quality checks, and Streamlit dashboard.
- `C:\Users\Nitro\data-analytics-project\baraa-warehouse-example`: modern DuckDB warehouse example with ERP/CRM CSV sources, medallion layers, star schema, docs, SQL tests, and Streamlit dashboard.
- `C:\Users\Nitro\aicvgen`: source of general engineering skills and the memory artifact pattern under `mvp/docs/agent-memory/`.
- `https://github.com/jeremylongshore/claude-code-plugins-plus-skills/tree/main/skills/12-data-analytics`: upstream source list for analytics skill ideas such as funnels, cohorts, KPIs, SQL helpers, dashboards, reports, and visualization.
- `https://github.com/jeremylongshore/claude-code-plugins-plus-skills/tree/main/skills/11-data-pipelines`: upstream source list for pipeline skill ideas such as data quality, schema validation, metadata, lineage, file conversion, and SQL transforms.

## Known Risks And Constraints

- Imported AICVGen skills may contain Claude/OpenCode-flavored wording. Treat them as useful workflow references, not binding product policy.
- Jeremy Longshore upstream skills were adapted as consolidated repo-local skills instead of copied one-for-one because the upstream folders are broad and generic while this repo needs compact 365DS/DuckDB workflows.
- Generated project warehouses, caches, and Streamlit runtime outputs are ignored and should not be committed.
- Some sources require external tools or format-specific handling, such as Tableau `.twbx`, PDF sketches, and notebooks.
- The visible `agent-skills/` directory remains the canonical edit target; hidden paths are local junction aliases.
- Tracking User Engagement translates Excel tasks into reproducible Python/Gold outputs; no committed workbook is required unless the user explicitly asks for one.

## Verification History

- 2026-06-17: Confirmed repo had no Git metadata, then initialized Git with `git init`.
- 2026-06-17: Inventoried current repo, Maven Fuzzy Factory, Baraa warehouse example, and AICVGen skill/memory artifacts.
- 2026-06-17: Attempted `.agents/skills` and `.codex/skills` scaffolding; child writes failed with Windows access denied after initial hidden-folder creation.
- 2026-06-17: Validated all `agent-skills/*/SKILL.md` files with `quick_validate.py`.
- 2026-06-17: Parsed `docs/agent-memory/memory-index.json` with `python -m json.tool`.
- 2026-06-17: Confirmed `agent-skills`, `AGENTS.md`, and `docs/agent-memory` contain no non-ASCII characters.
- 2026-06-17: Reviewed upstream GitHub skill directories for `12-data-analytics` and `11-data-pipelines`; adapted relevant ideas into consolidated local skills.
- 2026-06-17: Replaced problematic `.agents` and `.codex` hidden roots with local junctions to writable support directories; `.agents/skills` and `.codex/skills` now point to `agent-skills/`.
- 2026-06-17: Added setup files `requirements-analytics.txt` and `requirements-langchain.txt`; updated `.gitignore` for `.env`, extra venvs, and local Chroma/vector-store artifacts.
- 2026-06-17: Created baseline commit `fedc359` (`chore: establish 365ds analytics workspace`) and stack commit `0390c9f` (`chore: use duckdb streamlit analytics stack`).
- 2026-06-17: Created `.venv-365ds` with CPython 3.13.7 using `.uv-cache/`; normal `uv pip install` failed on sandboxed PyPI socket access, escalated install was rejected by the approval system usage limit, and offline cache had no pandas.
- 2026-06-17: Added `projects/real-estate-market-analysis/` pipeline code and Streamlit dashboard; static `py_compile` check passed for all new Python files.
- 2026-06-17: Real Estate dependencies became available in `.venv-365ds`; pipeline and quality checks passed, and the project was committed as `e1a1a8b` (`feat: add real estate duckdb streamlit project`), followed by quiz answer documentation commit `2f0adbf`.
- 2026-06-17: Added `projects/user-journey-analysis/` with required Python journey functions, DuckDB Bronze/Silver/Gold pipeline, SQL quality checks, report, and Streamlit dashboard; static compile, runtime pipeline, and quiz regression checks passed.
- 2026-06-17: Added `projects/checkout-flow-optimization/` with SQL-first DuckDB medallion layers, MySQL dump parser, checkout marts, report, and Streamlit dashboard; static compile, runtime pipeline, and SQL quality checks passed.
- 2026-06-19: Added `projects/customer-engagement-analysis/` with SQL-first DuckDB medallion layers, multi-block MySQL dump parsing, engagement marts, report, and Streamlit dashboard; static compile, runtime pipeline, and SQL quality checks passed.
- 2026-06-19: Added `projects/tracking-user-engagement/` with SQL-first DuckDB medallion layers, multi-block MySQL dump parsing, Q2 paid/free cohorts, 99th-percentile outlier filtering, t-tests, certificate correlation, linear regression, probability marts, report, and Streamlit dashboard; static compile, runtime pipeline, and quality checks passed.

- 2026-06-17: Added projects/real-estate-market-analysis/reports/real_estate_market_analysis_star_b_retrospective.md as an internal STAR-B proof report for the Real Estate project; no pipeline rerun or source data changes were performed.

## Next Steps

- Review the Tracking User Engagement Streamlit dashboard and generated report.
- Plan the remaining LangChain chatbot project last; it needs a separate environment and an OpenAI API key, unlike the completed analytics projects.

## Deferred Missions

- After completing the remaining 365DS projects, standardize existing project pipelines toward the preferred warehouse pattern: Python orchestrates; SQL files define Bronze/Silver/Gold tables where transformations are relational; Python remains for project-required APIs, pandas-specific learning objectives, or list/session algorithms that are clearer outside SQL.

## Recent Delta

- 2026-06-19: Added repo-local agent skill package and starter memory artifacts; expanded it with adapted analytics SQL, dashboard storytelling, and data quality contract skills from the requested GitHub sources; fixed hidden `.agents`/`.codex` usability via junctions; added starter Python requirements files for analytics and LangChain work; committed the baseline and DuckDB/Streamlit stack; completed Real Estate, User Journey, Checkout Flow Optimization, Customer Engagement, and Tracking User Engagement as DuckDB/Streamlit projects.
