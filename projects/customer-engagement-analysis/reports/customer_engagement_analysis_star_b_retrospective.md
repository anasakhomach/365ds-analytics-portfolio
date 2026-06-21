# Customer Engagement Analysis STAR-B Retrospective

This is the STAR-B retrospective for `projects/customer-engagement-analysis` inside the 365DS demo projects workspace.

Working title: **Customer Engagement Warehouse And Dashboard Retrospective**

The project started from a 365 Data Science SQL and Tableau brief. The delivered local implementation translates it into a SQL-first DuckDB medallion pipeline, multi-block MySQL dump parsing, Gold engagement marts, quality checks, a Streamlit dashboard, and a generated Markdown report.

## Project Metadata

- Project name: Customer Engagement Analysis
- Project type: 365DS SQL/Tableau project implementation and retrospective proof artifact
- Domain: online education engagement, onboarding, course performance, country funnels
- Source brief: `project-instructions/Customer Engagement Analysis with SQL and Tableau Project Instructions.md`
- Source dataset: `source-datasets/Customer Engagement Analysis with SQL and Tableau/365_database.sql`
- Delivered project path: `projects/customer-engagement-analysis/`
- Delivery status: local implementation exists; retrospective added after implementation
- Current status: internal proof document, not a public case study yet
- Primary stack: SQL, Python, DuckDB, Streamlit, Plotly, Babel, Markdown
- Public link: not published
- Demo link: local dashboard only
- External stakeholder validation: not claimed

## Transparency Statement

This retrospective is an internal proof record. It separates verified local artifacts from judgment, estimated value, and unproven external outcomes.

Verified local evidence:

- The implementation exists under `projects/customer-engagement-analysis/`.
- The generated report states 35,230 registered students, 18,156 onboarded students, and 1,835,588 minutes watched.
- The report states an overall onboarding rate of 51.5%.
- The project uses SQL-first DuckDB layers and handles multi-block MySQL inserts.
- The dashboard reads Gold marts only.

Not claimed:

- No production learning-platform decision is claimed.
- No marketing spend or retention outcome is claimed.
- No Tableau workbook delivery is claimed for this repo implementation.
- No external stakeholder validation is claimed.

Honest framing:

> This project proves local SQL-first engagement analytics and dashboard delivery. It does not prove that learner retention or revenue improved.

## Audience Fit

### Hiring Manager Signal

This project shows the ability to ingest relational course-platform data, model engagement and onboarding, create country and course performance marts, handle source parsing issues, and present insights through dashboards and reports.

### Recruiter Signal

Recruiter-visible keywords and skills:

- SQL
- DuckDB
- Python orchestration
- engagement analytics
- onboarding funnel
- course performance
- country analysis
- Streamlit
- data quality
- MySQL dump parsing

### Freelance Client Signal

This resembles a client request to understand which users engage, which courses drive usage, and which countries show registration volume versus realized learning activity.

### Wrong Audience To Filter Out

This is not a production customer data platform, lifecycle marketing engine, or hosted BI service.

## Executive Summary

- Problem: The brief needed customer engagement analysis across registrations, onboarding, purchases, courses, countries, and minutes watched.
- Delivered solution: SQL-first DuckDB medallion pipeline, Gold marts, Streamlit dashboard, and Markdown report.
- Role: end-to-end local analytics and data engineering implementation.
- Main constraint: the source dump required multi-block insert parsing, especially for large learning tables.
- Most important decision: validate source counts and keep DuckDB canonical instead of relying on MySQL as the runtime engine.
- Outcome: the project exposes monthly engagement, onboarding, course rankings, country funnels, summary KPIs, and quiz support.
- Evidence: `projects/customer-engagement-analysis/reports/customer_engagement_analysis_report.md`
- Main lesson: source ingestion reliability matters as much as dashboard design.

## Delivery Context

### Situation

The course brief used SQL and Tableau against a MySQL-style source. The repo needed a reproducible DuckDB/Streamlit implementation that preserved the analysis contract and worked with local project standards.

### Task

The project needed to:

- parse and load multiple MySQL dump tables;
- support multiple `INSERT` blocks per table;
- create purchase windows and student engagement extracts;
- enrich country codes into readable country names;
- create Gold marts for course, monthly, onboarding, country, KPI, and quiz outputs;
- build a Streamlit dashboard reading Gold only.

### Scope Boundaries

Included:

- SQL-first medallion pipeline;
- multi-block MySQL dump parser support;
- engagement, onboarding, country, and course marts;
- generated report and dashboard.

Excluded:

- production customer lifecycle automation;
- marketing campaign attribution;
- external BI publishing;
- real user tracking outside the provided dump.

## STAR-B Story Bank

### STAR-B Story 1: Main Delivery Story

**Situation**

The project needed to explain student engagement across courses, geographies, onboarding, and paid/free behavior.

**Task**

Build a reproducible engagement warehouse and dashboard from the MySQL-style source.

**Action**

Parsed the source dump into DuckDB Bronze tables, created Silver purchase windows and engagement extracts, generated Gold marts for course performance, monthly engagement, registrations, onboarding, country rankings, KPIs, and quiz support, then built a Streamlit dashboard.

**Result**

The report shows 35,230 registered students, 18,156 onboarded students, 1,835,588 minutes watched, and a 51.5% onboarding rate.

**Bridge**

This proves customer engagement analytics across relational data and dashboard reporting.

**Evidence**

- Repo artifact: `projects/customer-engagement-analysis/`
- Report: `projects/customer-engagement-analysis/reports/customer_engagement_analysis_report.md`
- Dashboard: `projects/customer-engagement-analysis/dashboard/app.py`
- Confidence level: verified

### STAR-B Story 2: Technical Decision Story

**Situation**

The source dump contained multiple insert blocks for a large table, which could break simple ingestion.

**Task**

Ensure Bronze row counts were complete before any engagement analysis.

**Action**

Updated the dump parser pattern to support multiple `INSERT` blocks per table and validated expected row counts before building Silver and Gold.

**Result**

The project loaded the large learning table and reconciled total watched minutes to 1,835,588.10 in the quality checks recorded during delivery.

**Bridge**

This proves ingestion reliability and source-fidelity discipline.

**Evidence**

- Memory verification: `docs/agent-memory/current-thread-memory.md`
- Report: `reports/customer_engagement_analysis_report.md`
- Confidence level: verified

### STAR-B Story 3: Constraint Or Failure Story

**Situation**

One converted quiz question was truncated in the project brief.

**Task**

Avoid inventing an unsupported quiz answer.

**Action**

Computed the data-derived paid/free average-minutes ratio and documented the basis and truncation.

**Result**

The report records the paid/free average-minutes ratio as 23.12 with a note that the question text was truncated.

**Bridge**

This proves honest reporting when source requirements are incomplete.

**Evidence**

- Report notes and quiz support: `reports/customer_engagement_analysis_report.md`
- Confidence level: verified

## Evidence Ledger

| Claim | Evidence | Location | Public? | Confidence |
| --- | --- | --- | --- | --- |
| Registered students total 35,230. | Generated report. | `reports/customer_engagement_analysis_report.md` | yes | verified |
| Onboarded students total 18,156. | Generated report. | `reports/customer_engagement_analysis_report.md` | yes | verified |
| Total minutes watched is 1,835,588. | Generated report. | `reports/customer_engagement_analysis_report.md` | yes | verified |
| Overall onboarding rate is 0.5154. | Generated report quiz support. | `reports/customer_engagement_analysis_report.md` | yes | verified |
| Paying to free average-minutes ratio is 23.12. | Generated report quiz support. | `reports/customer_engagement_analysis_report.md` | yes | verified |
| Tableau requirements are translated into Streamlit. | Report notes. | `reports/customer_engagement_analysis_report.md` | yes | verified |

## Delivered Artifacts

| Artifact | Purpose | Proof Location | Public? |
| --- | --- | --- | --- |
| Multi-block dump loader | Complete Bronze ingestion | `scripts/` | yes |
| SQL medallion layers | Reproducible transformations | `scripts/bronze`, `scripts/silver`, `scripts/gold` | yes |
| Country and course marts | Engagement storytelling | Gold catalog and generated warehouse | yes |
| Streamlit dashboard | Interactive engagement reporting | `dashboard/app.py` | yes |
| Markdown report | Findings, recommendations, quiz support | `reports/customer_engagement_analysis_report.md` | yes |

## Technical Stack

- Languages: SQL, Python, Markdown
- Frameworks: Streamlit
- Databases: DuckDB
- Source format: MySQL SQL dump
- Data tools: Babel country names, pandas/Python orchestration, SQL quality checks
- Visualization: Streamlit and Plotly
- Testing: row counts, watched-minute reconciliation, date ranges, binary flags, Gold mart checks

### Stack Rationale

SQL fits the relational engagement model. DuckDB keeps the workflow local and consistent with the rest of the portfolio. Streamlit replaces Tableau with a reproducible dashboard surface.

### Stack Limitations

The dashboard is local, not hosted. The analysis is descriptive and does not prove causality or campaign impact.

## Technical Decisions And Trade-Offs

| Decision | Options Considered | Choice Made | Trade-Off | Result |
| --- | --- | --- | --- | --- |
| Dump ingestion | MySQL runtime, simple parser, multi-block DuckDB parser | Multi-block DuckDB parser | More parser complexity | Complete local Bronze loading |
| Country labels | Keep raw country codes, external API, local Babel data | Babel fallback to raw code | Depends on installed package data | Readable country analysis without network calls |
| Tableau translation | Require Tableau, static report, Streamlit | Streamlit | Not a Tableau workbook | Reproducible local dashboard |
| Question 10 | Guess missing text, omit answer, document data-derived ratio | Document data-derived ratio | Less tidy quiz section | Honest answer support |

## Metrics And Outcomes

### Measured Local Outcomes

- Registered students: 35,230.
- Onboarded students: 18,156.
- Total minutes watched: 1,835,588.
- Average minutes watched per engaged student: 101.10.
- Top country by registered students: India with 6,933.
- Top country by minutes watched: United States with 449,029 minutes.
- Paying/free average-minutes ratio: 23.12.

### Unmeasured Outcomes

- No retention lift, paid conversion lift, or marketing improvement is measured.

## Retrospective Analysis

### Keep Doing

- Validate Bronze row counts before analysis.
- Keep ambiguous quiz text documented.
- Separate country registration volume from realized minutes watched.

### More Of

- Add dashboard annotations explaining the paid/free ratio.
- Add screenshots for course and country views.

### Less Of

- Avoid treating registration count as engagement without minutes watched context.

### Start Doing

- Add fixture-based parser tests for multi-block dumps.

## Challenges, Mistakes, And Constraints

| Issue | What Happened | Impact | Response | Next Time |
| --- | --- | --- | --- | --- |
| Multi-block dump inserts | Large tables used multiple insert blocks. | Risk of incomplete Bronze load. | Parser supported multiple blocks and quality checks validated counts. | Inspect dump structure before implementation. |
| Truncated quiz question | Question 10 text was incomplete. | Could lead to invented answer. | Documented data-derived ratio and limitation. | Preserve brief conversion notes earlier. |
| Tableau-to-Streamlit translation | Original expected Tableau. | Needed adjusted deliverable. | Built Streamlit story pages over Gold marts. | Note translation in README and report upfront. |

## Risk Register

| Risk | Severity | What Reduced The Risk | What Remains |
| --- | --- | --- | --- |
| Incomplete SQL dump parsing | high | Multi-block parser and row checks | More parser fixtures would help |
| Overstating engagement causality | medium | Descriptive wording and recommendations | No causal experiment |
| Local-only dashboard | low | Streamlit run command | No public hosted URL |

## Proof Summary For Hiring Managers

- I delivered: a SQL-first customer engagement warehouse, report, and dashboard.
- I was responsible for: dump parsing, modeling, Gold marts, dashboard, quiz support, and documentation.
- The hardest constraint was: reliable ingestion of multi-block MySQL dump data.
- Strongest evidence: report metrics and documented parser/quality behavior.
- I would improve: parser fixtures and public demo screenshots.

## Proof Summary For Recruiters

- Role fit: Analytics Engineer, Data Analyst, BI Analyst.
- Keywords: SQL, DuckDB, Streamlit, customer engagement, onboarding, country analysis, course analytics.
- Outcome: reproducible engagement dashboard and report.

## Proof Summary For Freelance Clients

- Client problem this resembles: understanding platform engagement across users, countries, courses, and paid/free segments.
- What I can deliver: engagement models, dashboards, and recommendations.
- What I will not overpromise: retention or revenue lift without further data and experiments.

## Resume Bullets

- Built a SQL-first customer engagement analytics project in DuckDB and Streamlit, modeling 35,230 students, onboarding, course performance, country rankings, and 1,835,588 minutes watched.
- Implemented multi-block MySQL dump ingestion and Gold marts for monthly engagement, onboarding, paid/free comparison, and quiz-supported reporting.

## LinkedIn Post Angle

- Main claim: I turned a customer engagement SQL dump into a reproducible warehouse and dashboard.
- Non-obvious lesson: ingestion reliability comes before dashboard polish.
- Concrete proof: 35,230 students, 18,156 onboarded, and 1,835,588 minutes watched.

## Follow-Up Improvements

| Improvement | Why It Matters | Effort | Status |
| --- | --- | --- | --- |
| Add parser fixtures | Protects dump ingestion. | medium | planned |
| Add dashboard screenshots | Makes portfolio proof faster to scan. | low | planned |
| Add cohort retention view | Extends descriptive analysis. | medium | planned |

## Final Retrospective Judgment

### What This Project Proves

It proves SQL-first customer engagement analytics, source-ingestion discipline, Gold-mart modeling, and Streamlit dashboard delivery.

### What This Project Does Not Prove

It does not prove causal engagement improvement, production adoption, or marketing impact.

### Strongest Evidence

The generated engagement report and row-count/parser validation history.

### Best Use Of This Retrospective

Portfolio case study and interview story.

## Detailed STAR-B Proof Addendum

This addendum expands the report into a fuller proof document, emphasizing ingestion reliability, engagement modeling, dashboard storytelling, and honest handling of converted brief limitations.

### Full Delivery Contract

**Inputs**

- `365_database.sql`: MySQL-style source dump for course, rating, student, learning, and purchase data.
- Source brief: `project-instructions/Customer Engagement Analysis with SQL and Tableau Project Instructions.md`.

**Transformations**

- Bronze loads course, rating, student, learning, and purchase tables into DuckDB.
- The dump parser supports multiple `INSERT` blocks because large source tables are not always represented by a single insert statement.
- Silver creates purchase windows, readable country names, and a course-required student engagement extract.
- Gold creates course performance, monthly engagement, monthly registration/onboarding, country registration, country minutes, summary KPI, student engagement, and quiz answer marts.

**Outputs**

- Generated local DuckDB warehouse.
- Streamlit dashboard with engagement trend, country funnel, onboarding, and course performance views.
- Markdown report with findings, recommendations, notes, and quiz support.

**Verification**

- Bronze row counts were validated during delivery.
- Total watched minutes were reconciled.
- Date ranges, paid/onboarded flags, and Gold mart counts were checked.
- Dashboard follows the Gold-only contract.

**Known limits**

- The analysis is descriptive.
- It does not prove conversion lift, retention lift, or marketing ROI.
- One converted quiz question was truncated, so the report documents a data-derived interpretation.

### Expanded Audience Fit

**Hiring manager**

This project is strong evidence for relational analytics engineering. It includes dump ingestion, parser adaptation, subscription-window logic, engagement facts, country labeling, marts, dashboard story pages, and transparent reporting.

**Recruiter**

Recruiter keywords include SQL, DuckDB, Streamlit, customer engagement, onboarding, course analytics, country analysis, paid/free analysis, MySQL dump parsing, and data quality.

**Freelance client**

This resembles a client asking for an engagement dashboard from platform data: "Where are students coming from, which courses drive watch time, who onboards, and how do paid users differ from free users?"

**Wrong audience**

This is not a lifecycle marketing automation platform, customer data platform, attribution model, or production BI service.

### Expanded Evidence Ledger

| Claim | Evidence | Location | Public? | Confidence | Notes |
| --- | --- | --- | --- | --- | --- |
| Registered students total 35,230. | Generated report. | `reports/customer_engagement_analysis_report.md` | yes | verified | Local dataset metric. |
| Onboarded students total 18,156. | Generated report. | `reports/customer_engagement_analysis_report.md` | yes | verified | Local dataset metric. |
| Overall onboarding rate is 51.5%. | Generated report. | `reports/customer_engagement_analysis_report.md` | yes | verified | Rounded report value. |
| Total minutes watched is 1,835,588. | Generated report. | `reports/customer_engagement_analysis_report.md` | yes | verified | Local dataset metric. |
| Average minutes watched per engaged student is 101.10. | Generated report. | `reports/customer_engagement_analysis_report.md` | yes | verified | Descriptive KPI. |
| Top registered-student country is India with 6,933. | Generated report. | `reports/customer_engagement_analysis_report.md` | yes | verified | Registration volume, not engagement quality. |
| Top minutes-watched country is United States with 449,029 minutes. | Generated report. | `reports/customer_engagement_analysis_report.md` | yes | verified | Engagement volume. |
| Question 10 is truncated in the converted brief. | Report notes. | `reports/customer_engagement_analysis_report.md` | yes | verified | Avoids invented certainty. |

### Detailed Delivery Timeline

| Phase | What Happened | Key Decision | Evidence |
| --- | --- | --- | --- |
| Discovery | Read SQL/Tableau brief and inspected source dump shape. | Use DuckDB as canonical, not MySQL runtime. | README and memory |
| Ingestion | Loaded multiple source tables and handled multi-block inserts. | Validate row counts before analysis. | Memory and scripts |
| Modeling | Created purchase windows, country labels, and engagement extract. | Keep subscription logic explicit. | Silver scripts |
| Gold marts | Built course, country, monthly, onboarding, KPI, and quiz marts. | Dashboard should read modeled Gold outputs. | Gold scripts/catalog |
| Dashboard | Created Streamlit story pages. | Translate Tableau requirements to Streamlit. | `dashboard/app.py` |
| Reporting | Generated findings and quiz support. | Mark truncated quiz text honestly. | `reports/customer_engagement_analysis_report.md` |
| Retrospective | Wrote proof report. | Emphasize ingestion reliability and limits. | this file |

### Detailed Interview Answer Bank

**Tell me about a project you delivered**

I delivered a customer engagement analysis project over a 365DS learning-platform dataset. I loaded the MySQL-style dump into DuckDB, built SQL medallion layers, modeled student engagement, course performance, country funnels, onboarding rates, monthly minutes watched, and created a Streamlit dashboard and report.

**Tell me about a technical trade-off**

I chose DuckDB as the canonical runtime even though the data came as a MySQL dump. That kept the repo consistent, but required a stronger dump parser, especially for multiple `INSERT` blocks.

**Tell me about a time something went wrong or was incomplete**

One quiz question in the converted brief was truncated. I avoided inventing an answer and instead documented the data-derived paid/free average-minutes ratio and the reason for that interpretation.

**Tell me about ambiguity**

Engagement can mean registrations, onboarding, minutes watched, paid/free activity, course performance, or country behavior. I separated these into different Gold marts and dashboard views.

**Tell me about a measurable result**

The project reports 35,230 registered students, 18,156 onboarded students, 1,835,588 minutes watched, and paying students watching about 23.12 times more minutes than free-plan students on the average-minutes KPI.

### Public Version Notes

**Safe to share**

- Engagement metrics, onboarding rate, country/course findings, dashboard screenshots, and SQL-first architecture.

**Must redact**

- Local absolute paths in public copy.
- Any private environment or machine-specific details.

**Needs permission**

- Any claim that a learning platform team used the results.

**Can be generalized**

- The project can be described as "online education engagement analysis."

### Claim Safety Checklist

- Every metric comes from the generated report.
- The truncated question note remains visible.
- No retention or conversion lift is claimed.
- No Tableau delivery is claimed.
- Country rankings are not treated as marketing ROI.
- Paid/free engagement difference is descriptive, not causal.

### Detailed Follow-Up Backlog

| Improvement | Why It Matters | Effort | Owner | Status |
| --- | --- | --- | --- | --- |
| Add parser fixture tests | Protects multi-block ingestion. | medium | self | planned |
| Add screenshots | Helps portfolio review. | low | self | planned |
| Add cohort retention view | Extends engagement analysis beyond monthly totals. | medium | self | planned |
| Add dashboard notes for paid/free interpretation | Prevents causal overclaiming. | low | self | planned |
| Add public case-study version | Turns raw proof into readable portfolio content. | medium | self | planned |

### One-Page Version

**Project:** Customer Engagement Analysis.

**Problem:** A SQL/Tableau brief needed analysis of student registrations, onboarding, course engagement, country performance, and paid/free behavior.

**Delivered:** SQL-first DuckDB pipeline, multi-block dump loading, Gold engagement marts, Streamlit dashboard, and Markdown report.

**My role:** End-to-end analytics engineer and dashboard/report builder.

**STAR-B summary:** The situation was a relational learning-platform dataset. The task was to create reproducible engagement analysis. The action was to parse the dump, build medallion layers, create Gold marts, and present dashboard/report findings. The result was verified metrics including 35,230 registered students, 18,156 onboarded, and 1,835,588 minutes watched. The bridge is that this proves engagement analytics and source-ingestion discipline.

**Evidence:** `scripts/`, `dashboard/app.py`, `reports/customer_engagement_analysis_report.md`, and memory parser notes.

**Trade-off:** DuckDB consistency required custom dump parsing.

**Lesson:** Engagement dashboards are only as trustworthy as the ingestion checks behind them.

**Relevance:** Useful for Analytics Engineer, Data Analyst, BI Analyst, and education/product analytics work.

## Raw Template Completion Notes

This section keeps the richer internal proof material that can later be cut down for a public case study.

### Delivered Artifacts In Detail

| Artifact | Purpose | My Contribution | Proof Location | Public? |
| --- | --- | --- | --- | --- |
| Multi-table dump ingestion | Preserve course, student, purchase, learning, and rating data. | Loaded source tables into DuckDB Bronze. | `scripts/bronze/` | yes |
| Multi-block insert support | Avoid incomplete Bronze data when tables span multiple INSERT blocks. | Used parser pattern that handles multiple blocks. | scripts and memory | yes |
| Silver engagement model | Build course-required engagement extract and subscription windows. | Modeled purchases, country labels, onboarded/paid flags, and watched minutes. | `scripts/silver/` | yes |
| Gold marts | Expose course, country, monthly, onboarding, KPI, and quiz outputs. | Built dashboard/report marts. | `scripts/gold/` | yes |
| Streamlit dashboard | Tell engagement story interactively. | Built views for engagement trends, countries, onboarding, and course performance. | `dashboard/app.py` | yes |
| Markdown report | Summarize findings, recommendations, and quiz support. | Generated report and documented truncated question. | `reports/customer_engagement_analysis_report.md` | yes |
| Retrospective | Convert delivery into proof. | Wrote this STAR-B report. | this file | yes |

### Technical Stack Detail

- Languages: SQL, Python, Markdown.
- Frameworks: Streamlit.
- Database: DuckDB.
- Source format: MySQL SQL dump.
- Data tools: Babel for country names, pandas/Python orchestration, SQL transformations.
- Visualization: Streamlit dashboard.
- Testing approach: Bronze row counts, insert block expectations, watched-minute reconciliation, date ranges, binary paid/onboarded flags, Gold mart checks.
- CI/CD: none; local verification only.
- Monitoring: none; not a production engagement platform.

### Technical Decisions And Trade-Offs In Detail

| Decision | Options Considered | Choice Made | Why | Trade-Off | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| Dump handling | MySQL runtime, simple parser, multi-block parser | Multi-block parser into DuckDB | Keeps canonical local warehouse and avoids missing rows. | More ingestion logic. | Complete source loading. | memory/report |
| Country labels | Raw country codes, external service, local Babel data | Babel with fallback | Human-readable without network calls. | Depends on local package data. | Better country reporting. | Silver model |
| Visualization | Tableau, static report, Streamlit | Streamlit | Repo standard and local run path. | Not a Tableau workbook. | Interactive dashboard. | dashboard |
| Truncated quiz question | Guess, omit, or document data-derived interpretation | Document data-derived ratio | Honest handling of incomplete source text. | Less tidy quiz answer. | Credible report. | report notes |

### Metrics And Outcomes In Detail

Measured local outcomes:

- Registered students: 35,230.
- Onboarded students: 18,156.
- Overall onboarding rate: 51.5%.
- Total minutes watched: 1,835,588.
- Average minutes watched per engaged student: 101.10.
- Most watched course: `Introduction to Data and Data Science`.
- Top country by registered students: India, 6,933.
- Top country by minutes watched: United States, 449,029 minutes.
- Paying/free average-minutes ratio: 23.12.

Qualitative outcomes:

- The dashboard separates acquisition volume from realized engagement.
- The report explains that paid users watch far more minutes on average.
- The project keeps quiz ambiguity visible.

Unmeasured outcomes:

- No retention lift is measured.
- No paid conversion lift is measured.
- No campaign or country strategy changed as a result.

Honest phrasing:

- "The project identifies engagement patterns in the provided learning-platform data."
- Do not say "this improved onboarding" or "this increased paid conversion."

### Challenges, Mistakes, And Constraints In Detail

Real constraints:

- Source dump contains multiple tables and multiple insert blocks.
- Tableau requirements were translated into Streamlit.
- Question 10 was truncated in the converted brief.
- Engagement is multi-dimensional: registration, onboarding, minutes, paid status, course activity, and geography.

Blameless system notes:

- Course asset conversion can create incomplete instructions. The right response is to mark the uncertainty and compute from available data, not invent missing text.

Mistakes or weak spots:

| Issue | What Happened | Impact | What I Did | What I Would Do Next Time |
| --- | --- | --- | --- | --- |
| Multi-block source tables | Large inserts were split. | Incomplete parser would miss data. | Used multi-block parsing and checks. | Add fixture tests for parser behavior. |
| Truncated quiz text | Question 10 was incomplete. | Could lead to unsupported answer. | Documented data-derived ratio. | Preserve converted brief issues in a known-issues file. |
| No external validation | Findings are local. | Cannot claim business action. | Framed as descriptive. | Add stakeholder feedback if demoed publicly. |

### Strong Public Case Study Shape

1. Open with the learning-platform engagement question.
2. Explain the source data and ingestion challenge.
3. Show registration versus minutes-watched country differences.
4. Show paid/free engagement difference.
5. Show course performance.
6. End with recommendations and limitations.

### Additional Interview Prompts

**How did you know the ingestion was trustworthy?**

I treated row counts and total minutes as quality gates. The multi-block parser was necessary because a simple insert parser could silently drop rows.

**How would you productionize it?**

I would add scheduled ingestion, formal source schemas, incremental loads, dashboard deployment, and monitoring for row counts, minutes totals, and null-country rates.

**What would you test next?**

Parser fixtures, country-label fallback behavior, purchase-window edge cases, and dashboard smoke checks.

### Claim Safety Checklist Addendum

- Do not claim retention improvement.
- Do not claim paid conversion improvement.
- Do not hide the truncated quiz question.
- Do not imply Tableau was delivered.
- Do not treat country registration volume as marketing ROI.
- Do not publish without explaining that this is local descriptive analysis.
