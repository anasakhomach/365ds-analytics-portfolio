# 365DS Portfolio Evidence Ledger

This ledger supports the STAR-B retrospective package. It maps portfolio claims to repo artifacts so the public story can stay useful without inventing impact.

## Claim Safety Rules

- Verified means the claim is supported by files, reports, tests, or memory artifacts in this repo.
- Estimated means the claim is judgment based on the local build, not an externally measured outcome.
- Not claimed means the repo does not currently prove the outcome.
- No API keys, raw chat transcripts, client names, production usage, revenue impact, or user adoption are included here.

## Evidence Table

| Claim | Evidence | Location | Public? | Confidence | Notes |
| --- | --- | --- | --- | --- | --- |
| The repo implements five 365DS analytics projects. | Project folders and catalog entries exist for Real Estate, User Journey, Checkout Flow, Customer Engagement, and Tracking User Engagement. | `projects/`, `apps/learning-hub/catalog/projects.yaml` | yes | verified | The catalog records titles, paths, dashboards, warehouses, Gold tables, and starter questions. |
| Raw source files are treated as immutable inputs. | Repo instructions and memory state this as a durable decision. Project reports repeat raw-source preservation. | `AGENTS.md`, `docs/agent-memory/current-thread-memory.md`, project reports | yes | verified | This is a workflow standard, not an external compliance claim. |
| DuckDB is the canonical local analytics engine. | Every project catalog entry lists DuckDB; reports state dashboards read `gold.*` marts. | `apps/learning-hub/catalog/projects.yaml`, project reports | yes | verified | MySQL is only a fallback/validation source for SQL dumps. |
| Streamlit replaced Tableau/Excel deliverables in this portfolio implementation. | Reports note Tableau/Excel translation into Streamlit or reproducible Gold outputs. | `projects/customer-engagement-analysis/reports/customer_engagement_analysis_report.md`, `projects/tracking-user-engagement/reports/tracking_user_engagement_report.md` | yes | verified | The course briefs remain source requirements. |
| Three projects use SQL-first medallion layers. | Catalog traits mark Checkout, Customer Engagement, and Tracking User Engagement as `sql_first_medallion`. | `apps/learning-hub/catalog/projects.yaml` | yes | verified | Real Estate and User Journey remain Python-first/Python-function projects where that fits the brief. |
| Dashboards read Gold marts only. | Project reports and hub catalog document approved Gold marts. | project reports, `apps/learning-hub/catalog/projects.yaml` | yes | verified | Runtime dashboard behavior is code-backed but not exhaustively restated here. |
| Real Estate project produced local business metrics. | Report lists 267 properties, 195 sold, 72 available, and total sold revenue. | `projects/real-estate-market-analysis/reports/real_estate_market_analysis_report.md` | yes | verified | Local project metric, not market impact. |
| User Journey project implemented required journey analysis and quiz support. | Report lists 9,935 raw sessions, 1,350 users, page metrics, and quiz answers. | `projects/user-journey-analysis/reports/user_journey_analysis_report.md` | yes | verified | Session ordering assumption is documented. |
| Checkout Flow project modeled checkout success, abandonment, and errors. | Report lists July 2022 through January 2023 window, checkout attempts, success rate, abandonment rate, and errors. | `projects/checkout-flow-optimization/reports/checkout_flow_optimization_report.md` | yes | verified | Some converted quiz options diverge from data-derived answers. |
| Customer Engagement project modeled registrations, onboarding, minutes watched, country, and course performance. | Report lists 35,230 registered students, 18,156 onboarded, and 1,835,588 minutes watched. | `projects/customer-engagement-analysis/reports/customer_engagement_analysis_report.md` | yes | verified | Question 10 was truncated in the converted brief and is documented as such. |
| Tracking User Engagement project reproduced statistical and prediction outputs. | Report lists Q2 cohorts, t-tests, correlation, R-squared, and 1,200-minute certificate prediction. | `projects/tracking-user-engagement/reports/tracking_user_engagement_report.md` | yes | verified | Excel tasks were translated into reproducible Python/Gold outputs. |
| Learning Hub provides a cross-project assistant and safe data tool. | Architecture doc describes RAG index, provider runtime, safe DuckDB access, and multipage Streamlit app. | `apps/learning-hub/docs/architecture.md` | yes | verified | Live AI is optional; local fallback remains supported. |
| The data tool restricts execution to approved Gold marts. | Architecture doc and catalog describe read-only DuckDB and approved Gold tables. | `apps/learning-hub/docs/architecture.md`, `apps/learning-hub/catalog/projects.yaml` | yes | verified | The validator is still the enforcement point; LLM-generated SQL is untrusted. |
| Provider-agnostic AI runtime is a documented architecture decision. | ADR-001 records provider-agnostic runtime, local fallback, owner-key path, BYOK, and rejected alternatives. | `docs/decisions/ADR-001-provider-agnostic-learning-hub-ai.md` | yes | verified | Do not publish actual key values. |
| Hybrid custom and LangGraph assistant backend is a documented decision. | ADR-002 records custom, LangGraph, and auto backend behavior. | `docs/decisions/ADR-002-hybrid-learning-hub-agent-backend.md` | yes | verified | LangGraph is optional and reuses the same safety contracts. |
| Docker path has been verified locally. | Memory records Docker build, indexer, HTTP smoke, and container tests when Docker Desktop was running. | `docs/agent-memory/current-thread-memory.md`, `docs/agent-memory/thread-walkthrough.md` | yes | verified | This is local Docker verification, not hosted production deployment. |
| Bugs and recovery actions were documented during delivery. | Memory artifacts record ACL, uv/cache, Docker, assistant routing, provider fallback, and dashboard runtime recovery milestones. | `docs/agent-memory/current-thread-memory.md`, `docs/agent-memory/thread-walkthrough.md` | yes | verified | The retrospective references curated memory, not raw transcript logs. |
| The project proves external user adoption or business impact. | No analytics, testimonials, public deployment, or client approval exist in repo evidence. | n/a | no | not claimed | Public wording must avoid adoption, revenue, or production claims. |

## Strongest Proof Links

- Project catalog: `apps/learning-hub/catalog/projects.yaml`
- Learning Hub architecture: `apps/learning-hub/docs/architecture.md`
- Provider runtime ADR: `docs/decisions/ADR-001-provider-agnostic-learning-hub-ai.md`
- Hybrid agent ADR: `docs/decisions/ADR-002-hybrid-learning-hub-agent-backend.md`
- Delivery memory: `docs/agent-memory/current-thread-memory.md`
- Milestone walkthrough: `docs/agent-memory/thread-walkthrough.md`
- Project reports under `projects/*/reports/`

