# Analytics Projects And Dashboards Retrospective

This appendix covers the five analytics projects as a portfolio system. It focuses on the data engineering pattern, dashboarding decisions, quiz support, and how course briefs were translated into reproducible local artifacts.

## Portfolio Pattern

The repo standard became:

- preserve raw source files under `source-datasets/`;
- use DuckDB as the local analytics warehouse;
- model Bronze, Silver, and Gold layers per project;
- use Python orchestration and SQL transformations where the work is relational;
- use Python where the brief requires functions, pandas, statistics, or clearer list/session logic;
- expose dashboard-ready `gold.*` marts to Streamlit;
- keep dashboards free of hidden transformation logic;
- generate Markdown reports with findings, recommendations, and quiz support.

## Project Coverage

| Project | Workflow | Dashboard Story | Report Evidence |
| --- | --- | --- | --- |
| Real Estate Market Analysis | Python-first medallion project over CSV sources. | Market KPIs, building/state/country/age/price views, revenue and satisfaction interpretation. | 267 properties, 195 sold, 72 available, and $52,539,739 sold-property revenue. |
| User Journey Analysis | Python journey functions plus DuckDB marts. | User paths, page counts, page presence, destinations, sequences, and scenario filters. | 9,935 raw sessions, 1,350 users, and strongest four-page last-three-session pattern count of 49. |
| Checkout Flow Optimization | SQL-first DuckDB pipeline over MySQL dump. | Checkout success, cart abandonment, error rankings, and device split. | 4,334 attempts, 1,372 successes, 31.7% success rate, and 13.3% abandonment rate. |
| Customer Engagement Analysis | SQL-first DuckDB pipeline over MySQL dump with multi-insert parsing. | Engagement trends, country funnels, onboarding, and course performance. | 35,230 registered students, 18,156 onboarded, and 1,835,588 minutes watched. |
| Tracking User Engagement | SQL-first DuckDB pipeline plus Python statistical/model Gold marts. | Q2 paid/free comparison, outliers, confidence intervals, t-tests, probability, and certificate prediction. | Q2 watcher counts, t-tests, 0.5126 correlation, 0.4678 R-squared, and 4-certificate prediction for 1,200 minutes. |

## Dashboard Decisions

### Streamlit Instead Of Tableau Or Excel

Some 365DS briefs ask for Tableau or Excel. The portfolio implementation translated those deliverables into Streamlit dashboards and reproducible Gold-backed outputs. This keeps the learning objective visible while showing a modern local analytics stack.

### Gold-Only Dashboard Reads

Dashboards are intended to read Gold marts only. This decision makes each dashboard a presentation layer, not a transformation engine. It also allows the Learning Hub and Quiz/Data Coach to query the same modeled outputs safely.

### Quiz Support As A First-Class Artifact

The projects do not only answer business questions. They also preserve quiz-supporting answers in reports and Gold marts. This makes the repo useful for learning, walkthroughs, and verification.

## Technical Trade-Offs

| Decision | Options Considered | Choice Made | Trade-Off | Result |
| --- | --- | --- | --- | --- |
| DuckDB as canonical engine | MySQL/Postgres per dump, flat files only, DuckDB | DuckDB | Requires dump parsing for MySQL-style assets. | One local analytics engine across all projects. |
| Streamlit dashboard layer | Tableau, notebooks, static Markdown, Streamlit | Streamlit | Less polished than a production BI tool out of the box. | Interactive local dashboards that run with the Python stack. |
| SQL-first where relational | pandas-only, SQL-only, mixed | SQL files for relational layers, Python orchestration | More files per project. | Clearer lineage and reusable warehouse pattern. |
| Python where brief requires it | Force everything into SQL, keep notebooks | Python functions/statistics where appropriate | Mixed implementation style. | Better match to course requirements and problem shape. |
| Gold-only dashboard/tool access | Query any layer, query raw files, restrict to Gold | Restrict to Gold | Requires modeled marts before dashboarding. | Safer demos and cleaner architecture. |

## Bugs And Recovery

- Multi-INSERT SQL dumps forced a parser upgrade for larger course assets.
- Some converted quiz questions did not match data-derived options; reports document those divergences instead of forcing a false match.
- Excel/statistical work was converted into reproducible Python and Gold marts for Tracking User Engagement.
- Multi-dashboard local testing required an explicit port map and service smoke checks.

## Evidence

- Catalog: `apps/learning-hub/catalog/projects.yaml`
- Reports: `projects/*/reports/*_report.md`
- Project docs: `projects/*/docs/data_flow.md`
- Dashboards: `projects/*/dashboard/app.py`
- Memory: `docs/agent-memory/current-thread-memory.md`

## What This Proves

- Ability to turn course briefs into reproducible analytics products.
- Practical data engineering judgment around raw preservation, typed cleaning, marts, and quality checks.
- Dashboard storytelling that separates business interpretation from transformation code.
- Honest handling of data conversion issues and ambiguous quiz prompts.

## What This Does Not Prove

- Production BI adoption.
- External stakeholder usage.
- Automated cloud deployment.
- Revenue or operational business impact.

## Follow-Up Improvements

| Improvement | Why It Matters | Effort | Status |
| --- | --- | --- | --- |
| Add screenshots for each dashboard | Helps recruiters and visitors understand the work quickly. | medium | planned |
| Add a portfolio landing README linking all ports | Makes local demo navigation easier. | low | planned |
| Add dashboard smoke scripts | Reduces repeated manual port checks. | medium | planned |
| Standardize SQL-first refactor for earlier relational pieces | Aligns all projects with the deferred warehouse mission. | medium | deferred |
| Add demo video | Makes the portfolio more shareable. | medium | planned |

