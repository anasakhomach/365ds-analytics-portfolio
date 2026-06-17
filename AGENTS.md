# Repository Agent Instructions

## Local Skill Package

- Repo-local agent skills live in `agent-skills/`.
- Treat each `agent-skills/<skill-name>/SKILL.md` as a Codex-style skill.
- Hidden `.agents` and `.codex` are local junction roots that point into `agent-hidden-roots/`.
- `.agents/skills` and `.codex/skills` are junctions to `agent-skills/`, so all three skill paths resolve to the same local package.
- Do not edit hidden skill copies separately; edit `agent-skills/` and let the junctions reflect the same files.
- Do not treat ordinary application folders named `skills/` as agent skills unless they are intentionally documented here.

## Workflow

1. Read the relevant project instruction file under `project-instructions/`.
2. Inventory the matching raw files under `source-datasets/`.
3. Define the deliverable contract before editing: inputs, outputs, toolchain, assumptions, and verification.
4. Preserve raw source files. Put derived work in a project-specific output folder.
5. Run focused verification for touched code, SQL, notebooks, dashboards, or generated artifacts.
6. Update `docs/agent-memory/current-thread-memory.md` after meaningful milestones or before handoff.

## Useful Local Skills

- `agent-skills/data-analytics-case-study`: 365DS-style analytics projects from briefs and datasets.
- `agent-skills/analytics-sql-patterns`: reusable SQL patterns for metrics, funnels, cohorts, retention, date windows, joins, and validation.
- `agent-skills/dashboard-storytelling`: dashboard/report layout, chart selection, KPI presentation, and data story structure.
- `agent-skills/duckdb-medallion-pipeline`: DuckDB Bronze/Silver/Gold pipeline and Streamlit dashboard work.
- `agent-skills/data-quality-contracts`: schemas, quality gates, metadata, lineage, and pipeline reliability checks.
- `agent-skills/repo-memory-ledger`: Durable repo-local memory updates.
- Imported general skills from AICVGen cover planning, debugging, testing, review, documentation, git workflow, context setup, source-grounding, and incremental implementation.
