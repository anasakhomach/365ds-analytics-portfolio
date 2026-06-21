# Checkout Flow Optimization STAR-B Retrospective

This is the STAR-B retrospective for `projects/checkout-flow-optimization` inside the 365DS demo projects workspace.

Working title: **Checkout Funnel Warehouse And Dashboard Retrospective**

The project started from a 365 Data Science SQL and Tableau brief. The delivered local implementation translates it into a SQL-first DuckDB medallion pipeline, Gold marts, SQL quality checks, a Streamlit dashboard, and a generated Markdown business report.

## Project Metadata

- Project name: Checkout Flow Optimization
- Project type: 365DS SQL/Tableau project implementation and retrospective proof artifact
- Domain: checkout funnel analytics, cart abandonment, payment errors, device split
- Source brief: `project-instructions/Checkout Flow Optimization Analysis with SQL and Tableau Project Instructions.md`
- Source dataset: `source-datasets/Checkout Flow Optimization Analysis With SQL And Tableau/365_checkout_database.sql`
- Delivered project path: `projects/checkout-flow-optimization/`
- Delivery status: local implementation exists; retrospective added after implementation
- Current status: internal proof document, not a public case study yet
- Primary stack: SQL, Python, DuckDB, Streamlit, Plotly, Markdown
- Public link: not published
- Demo link: local dashboard only
- External stakeholder validation: not claimed

## Transparency Statement

This retrospective is an internal proof record. It separates verified local artifacts from judgment, estimated value, and unproven external outcomes.

Verified local evidence:

- The implementation exists under `projects/checkout-flow-optimization/`.
- The raw MySQL dump is the declared source contract.
- The generated report states the analysis window is July 2022 through January 2023.
- The report states 5,001 carts, 4,334 checkout attempts, 1,372 successful attempts, 31.7% success rate, and 13.3% cart abandonment rate.
- The dashboard reads Gold marts only.

Not claimed:

- No checkout conversion lift is claimed.
- No production payment system change is claimed.
- No external stakeholder used this dashboard.
- No Tableau workbook delivery is claimed for this repo implementation.

Honest framing:

> This project proves local SQL-first funnel analytics and dashboard delivery. It does not prove that checkout conversion improved in production.

## Audience Fit

### Hiring Manager Signal

This project shows the ability to ingest a SQL dump, model a funnel, calculate success and abandonment metrics, surface error drivers, and translate a BI brief into a reproducible local dashboard.

### Recruiter Signal

Recruiter-visible keywords and skills:

- SQL
- DuckDB
- Python orchestration
- funnel analytics
- cart abandonment
- checkout errors
- Streamlit
- data quality checks
- dashboarding

### Freelance Client Signal

This resembles a client request to diagnose checkout friction and prioritize fixes around error handling, form validation, and device-specific checkout behavior.

### Wrong Audience To Filter Out

This is not a live payment observability system, experimentation platform, or production checkout optimization campaign.

## Executive Summary

- Problem: The brief needed checkout funnel, abandonment, error, and device analysis from a MySQL-style dump.
- Delivered solution: SQL-first DuckDB Bronze/Silver/Gold pipeline, Gold marts, Streamlit dashboard, and Markdown report.
- Role: end-to-end local analytics and dashboard implementation.
- Main constraint: preserve course logic while translating Tableau deliverables into Streamlit.
- Most important decision: use DuckDB as canonical and keep MySQL CLI only as fallback validation.
- Outcome: the project exposes monthly checkout success, abandonment, error rankings, device split, KPIs, and quiz support.
- Evidence: `projects/checkout-flow-optimization/reports/checkout_flow_optimization_report.md`
- Main lesson: funnel dashboards need transparent formulas, especially when source data creates odd cases like attempts exceeding carts.

## Delivery Context

### Situation

The course project was framed around SQL and Tableau. The repo standard had become DuckDB plus Streamlit, so the task was to preserve the analytical contract while making the deliverable reproducible inside the local analytics workspace.

### Task

The project needed to:

- parse and load a MySQL dump into DuckDB;
- preserve raw Bronze data;
- filter the analysis window in Silver;
- create Gold funnel, error, device, KPI, and quiz marts;
- build a dashboard that reads Gold only;
- generate a report with current state, hypothesis, recommendations, and quiz calculations.

### Scope Boundaries

Included:

- MySQL dump ingestion;
- SQL-first medallion layers;
- checkout success and abandonment metrics;
- error rankings and device analysis;
- Streamlit dashboard and report.

Excluded:

- production payment processing changes;
- A/B testing;
- actual revenue recovery measurement;
- Tableau workbook delivery.

## STAR-B Story Bank

### STAR-B Story 1: Main Delivery Story

**Situation**

The source data described checkout actions and carts, but the deliverable needed a funnel story a stakeholder could act on.

**Task**

Build a reproducible local checkout funnel analysis that surfaces success rate, abandonment, and error drivers.

**Action**

Loaded the MySQL dump into DuckDB Bronze tables, typed and filtered the analysis window in Silver, created Gold marts for checkout steps, monthly success, cart abandonment, errors, devices, KPIs, and quiz support, then built a Streamlit dashboard.

**Result**

The report shows 4,334 checkout attempts, 1,372 successful attempts, a 31.7% success rate, and the most common error as `number field is required`.

**Bridge**

This proves practical funnel analytics and dashboard storytelling.

**Evidence**

- Repo artifact: `projects/checkout-flow-optimization/`
- Report: `projects/checkout-flow-optimization/reports/checkout_flow_optimization_report.md`
- Dashboard: `projects/checkout-flow-optimization/dashboard/app.py`
- Confidence level: verified

### STAR-B Story 2: Technical Decision Story

**Situation**

The brief expected SQL and Tableau, while the repo standard favored DuckDB and Streamlit.

**Task**

Keep the SQL-first learning objective while avoiding a separate BI dependency.

**Action**

Used SQL files for Bronze/Silver/Gold transformations and Python only to orchestrate the pipeline and report/dashboard generation.

**Result**

The implementation became a SQL-first project that still runs in the same local stack as the rest of the portfolio.

**Bridge**

This proves tool translation without losing the analytical contract.

**Evidence**

- README: `projects/checkout-flow-optimization/README.md`
- Catalog traits: `apps/learning-hub/catalog/projects.yaml`
- Confidence level: verified

### STAR-B Story 3: Constraint Or Failure Story

**Situation**

The report notes that November 2022 has more checkout attempts than carts under the course formula.

**Task**

Avoid hiding or clamping an odd result that affects abandonment interpretation.

**Action**

Kept the formula visible and documented the issue in the report rather than forcing a cleaner-looking metric.

**Result**

The report remains transparent about how the metric was calculated.

**Bridge**

This proves responsible analytics communication when source logic produces unintuitive results.

**Evidence**

- Report current state: `projects/checkout-flow-optimization/reports/checkout_flow_optimization_report.md`
- Confidence level: verified

## Evidence Ledger

| Claim | Evidence | Location | Public? | Confidence |
| --- | --- | --- | --- | --- |
| Analysis window is July 2022 through January 2023. | Generated report and README contract. | `README.md`, `reports/checkout_flow_optimization_report.md` | yes | verified |
| Total carts are 5,001. | Generated report. | `reports/checkout_flow_optimization_report.md` | yes | verified |
| Checkout attempts are 4,334. | Generated report. | `reports/checkout_flow_optimization_report.md` | yes | verified |
| Successful attempts are 1,372. | Generated report. | `reports/checkout_flow_optimization_report.md` | yes | verified |
| Overall success rate is 31.7%. | Generated report. | `reports/checkout_flow_optimization_report.md` | yes | verified |
| Most common checkout error is `number field is required`. | Generated report. | `reports/checkout_flow_optimization_report.md` | yes | verified |

## Delivered Artifacts

| Artifact | Purpose | Proof Location | Public? |
| --- | --- | --- | --- |
| MySQL dump parser/load step | Preserve source tables in Bronze | `scripts/` | yes |
| SQL medallion layers | Reproducible transformations | `scripts/bronze`, `scripts/silver`, `scripts/gold` | yes |
| Gold funnel marts | Dashboard-ready checkout metrics | Catalog and generated warehouse | yes |
| Streamlit dashboard | Interactive checkout story | `dashboard/app.py` | yes |
| Markdown report | Business findings and quiz support | `reports/checkout_flow_optimization_report.md` | yes |

## Technical Stack

- Languages: SQL, Python, Markdown
- Frameworks: Streamlit
- Databases: DuckDB
- Source format: MySQL SQL dump
- Visualization: Streamlit and Plotly
- Testing: static compile, runtime pipeline, row counts, analysis-window checks, dashboard Gold-only convention

### Stack Rationale

DuckDB allowed the SQL-first analysis to run locally without requiring a MySQL server as the canonical engine. Streamlit translated the Tableau story into a reproducible app.

### Stack Limitations

The implementation does not prove production checkout behavior or actual conversion lift. MySQL CLI remains a fallback validation path, not the main engine.

## Technical Decisions And Trade-Offs

| Decision | Options Considered | Choice Made | Trade-Off | Result |
| --- | --- | --- | --- | --- |
| Engine | MySQL, Postgres, DuckDB | DuckDB | Needed dump parsing | Shared local warehouse workflow |
| Visualization | Tableau, static report, Streamlit | Streamlit | Not a Tableau workbook | Local interactive dashboard |
| Abandonment formula | Clamp odd values, hide them, keep formula visible | Keep formula visible | Some results look unintuitive | More transparent analysis |
| Python role | Transform in Python, orchestrate SQL, notebook | Python orchestrates SQL | More files than notebook | Clear lineage |

## Metrics And Outcomes

### Measured Local Outcomes

- Total carts: 5,001.
- Total checkout attempts: 4,334.
- Successful attempts: 1,372.
- Overall checkout success rate: 31.7%.
- Course-formula abandonment rate: 13.3%.
- Highest success-rate month: August 2022 at 47.1%.
- Highest abandonment-rate month: October 2022 at 37.5%.

### Unmeasured Outcomes

- No production checkout improvement, revenue recovery, or customer behavior change is measured.

## Retrospective Analysis

### Keep Doing

- Keep SQL transformations explicit.
- Document formula edge cases.
- Separate Bronze preservation from Silver/Gold analysis windows.

### More Of

- Add screenshots of the funnel dashboard.
- Add query examples for each Gold mart.

### Less Of

- Avoid assuming converted quiz options always match data-derived answers.

### Start Doing

- Add a small dashboard smoke check to confirm the Streamlit app boots.

## Challenges, Mistakes, And Constraints

| Issue | What Happened | Impact | Response | Next Time |
| --- | --- | --- | --- | --- |
| Course formula produced odd monthly abandonment behavior | Some attempts exceeded carts. | Could confuse readers. | Documented the formula and did not clamp values. | Add a formula caveat directly in dashboard UI. |
| Tableau brief in Streamlit repo | Original expected Tableau deliverable. | Needed translation. | Preserved business story in Streamlit. | Document translation upfront. |
| MySQL dump source | Dump parsing can diverge from MySQL behavior. | Ingestion risk. | DuckDB is canonical; MySQL CLI noted as fallback. | Add parser regression fixtures for future dumps. |

## Risk Register

| Risk | Severity | What Reduced The Risk | What Remains |
| --- | --- | --- | --- |
| Formula misunderstanding | medium | Report notes and visible quiz support | Dashboard caveat could be stronger |
| Dump parsing drift | medium | Row count and date checks | More parser fixtures would help |
| Local-only dashboard | low | Streamlit run command | No hosted demo yet |

## Proof Summary For Hiring Managers

- I delivered: SQL-first checkout funnel analysis with DuckDB, Streamlit, and Gold marts.
- I was responsible for: dump ingestion, transformations, metrics, dashboard, report, and quiz support.
- The hardest constraint was: translating a Tableau/MySQL brief into a local DuckDB/Streamlit workflow.
- Strongest evidence: report metrics and transparent formula caveats.
- I would improve: dashboard screenshots and automated Streamlit smoke tests.

## Proof Summary For Recruiters

- Role fit: Data Analyst, Analytics Engineer, BI Analyst.
- Keywords: SQL, checkout funnel, cart abandonment, DuckDB, Streamlit, data quality.
- Outcome: local reproducible checkout flow dashboard and report.

## Proof Summary For Freelance Clients

- Client problem this resembles: diagnosing checkout drop-off and payment-form errors.
- What I can deliver: funnel metrics, error rankings, dashboard, and recommendations.
- What I will not overpromise: conversion lift without experiments or production rollout.

## Resume Bullets

- Built a SQL-first checkout funnel analytics project in DuckDB and Streamlit, modeling 4,334 checkout attempts, 1,372 successes, monthly success, abandonment, errors, and device splits.
- Translated a SQL/Tableau checkout brief into reproducible Gold marts and a dashboard while documenting formula edge cases and quiz-supporting calculations.

## LinkedIn Post Angle

- Main claim: I turned a checkout SQL dump into a reproducible funnel dashboard.
- Non-obvious lesson: transparent formulas matter more than clean-looking metrics.
- Concrete proof: 31.7% success rate, 13.3% abandonment rate, and top error `number field is required`.

## Follow-Up Improvements

| Improvement | Why It Matters | Effort | Status |
| --- | --- | --- | --- |
| Add dashboard screenshots | Faster portfolio review. | low | planned |
| Add formula caveat to dashboard | Reduces stakeholder confusion. | low | planned |
| Add parser fixtures | Protects future SQL dump ingestion. | medium | planned |

## Final Retrospective Judgment

### What This Project Proves

It proves SQL-first funnel analytics, local warehouse modeling, dashboard delivery, and transparent communication of metric caveats.

### What This Project Does Not Prove

It does not prove production checkout optimization, payment system changes, or conversion lift.

### Strongest Evidence

The generated business report and Gold-backed dashboard.

### Best Use Of This Retrospective

Portfolio case study and interview story.

## Detailed STAR-B Proof Addendum

This addendum expands the report into a fuller proof document for hiring, interview, recruiter, freelance, and public-case-study use.

### Full Delivery Contract

**Inputs**

- `365_checkout_database.sql`: MySQL-style dump containing checkout actions and carts.
- Source brief: `project-instructions/Checkout Flow Optimization Analysis with SQL and Tableau Project Instructions.md`.

**Transformations**

- Bronze loads `checkout_actions` and `checkout_carts` into DuckDB.
- Silver types dates and filters the July 2022 through January 2023 analysis window.
- Gold creates daily checkout steps, monthly checkout success, monthly abandonment, checkout errors, device distribution, KPIs, and quiz answer marts.

**Outputs**

- Generated local `warehouse.duckdb`.
- Streamlit dashboard for checkout success, cart abandonment, checkout errors, and device split.
- Markdown business report with hypothesis, recommendations, and quiz support.

**Verification**

- Raw row counts were validated during project delivery.
- Date ranges and Gold monthly coverage were checked.
- Dashboard follows the Gold-only contract.
- MySQL CLI remains a fallback validation oracle, but DuckDB is canonical.

**Known limits**

- No production checkout system was changed.
- No A/B test or conversion lift is measured.
- The abandonment formula follows the course prompt and can produce unintuitive monthly cases.

### Expanded Audience Fit

**Hiring manager**

This project is strong evidence for analytics engineering and business analysis because it starts with raw operational-style checkout data and ends with a stakeholder story: success rate, abandonment, error drivers, and recommendations. It also shows the maturity to document formula caveats instead of hiding them.

**Recruiter**

Recruiter keywords include SQL, funnel analytics, checkout optimization, cart abandonment, DuckDB, Streamlit, BI dashboarding, data quality, and payment-error analysis.

**Freelance client**

This resembles a client project where checkout data is available, but leadership needs a concise diagnosis: where users fail, which errors dominate, and what fixes should be prioritized.

**Wrong audience**

This should not attract anyone expecting payment gateway engineering, fraud detection, live observability, or experimentation infrastructure.

### Expanded Evidence Ledger

| Claim | Evidence | Location | Public? | Confidence | Notes |
| --- | --- | --- | --- | --- | --- |
| Analysis window is July 2022 through January 2023. | README and report. | `README.md`, `reports/checkout_flow_optimization_report.md` | yes | verified | Silver/Gold window. |
| Total carts are 5,001. | Generated report. | `reports/checkout_flow_optimization_report.md` | yes | verified | Analysis-window metric. |
| Checkout attempts are 4,334. | Generated report. | `reports/checkout_flow_optimization_report.md` | yes | verified | Analysis-window metric. |
| Successful checkout attempts are 1,372. | Generated report. | `reports/checkout_flow_optimization_report.md` | yes | verified | Analysis-window metric. |
| Overall checkout success rate is 31.7%. | Generated report. | `reports/checkout_flow_optimization_report.md` | yes | verified | Descriptive, not improvement claim. |
| Course-formula abandonment rate is 13.3%. | Generated report. | `reports/checkout_flow_optimization_report.md` | yes | verified | Formula caveats documented. |
| Top error is `number field is required`. | Generated report. | `reports/checkout_flow_optimization_report.md` | yes | verified | Error count: 1,220 attempts. |
| No checkout lift is proven. | No experiment or production rollout exists. | n/a | yes | verified | Must remain clear. |

### Detailed Delivery Timeline

| Phase | What Happened | Key Decision | Evidence |
| --- | --- | --- | --- |
| Discovery | Read SQL/Tableau brief and dump contract. | Translate Tableau story to Streamlit. | Source brief and README |
| Ingestion | Parsed MySQL dump into DuckDB Bronze. | Keep DuckDB canonical; reserve MySQL as fallback. | `scripts/` |
| Modeling | Built Silver typed analysis window and Gold funnel marts. | Keep source rows outside the window in Bronze only. | Gold SQL and report |
| Dashboard | Created Streamlit story pages for success, abandonment, and errors/devices. | Dashboard reads Gold only. | `dashboard/app.py` |
| Reporting | Wrote current state, hypothesis, recommendations, and quiz support. | Document formula edge cases. | `reports/checkout_flow_optimization_report.md` |
| Retrospective | Wrote proof report for portfolio/interview use. | Do not claim conversion lift. | this file |

### Detailed Interview Answer Bank

**Tell me about a project you delivered**

I delivered a checkout funnel analysis project from a SQL/Tableau brief. I parsed the MySQL-style data into DuckDB, modeled checkout attempts, successes, cart abandonment, errors, and device splits, then built a Streamlit dashboard and generated a business report.

**Tell me about a technical trade-off**

The trade-off was whether to use MySQL as the main engine because the dump was MySQL-style. I chose DuckDB as canonical to keep the repo consistent, with MySQL CLI available only as a fallback validation path.

**Tell me about a time something was tricky**

The course formula created a case where checkout attempts could exceed carts for a month. Instead of clamping the metric or hiding it, I documented the formula behavior and kept the analysis transparent.

**Tell me about ambiguity**

The brief expected Tableau, but the repo standard was Streamlit. I preserved the business story and SQL logic while translating the visualization layer into Streamlit.

**Tell me about a measurable result**

The local analysis found 4,334 checkout attempts, 1,372 successes, 31.7% overall checkout success, 13.3% course-formula abandonment, and `number field is required` as the most common error.

### Public Version Notes

**Safe to share**

- Funnel metrics, dashboard screenshots, SQL-first architecture, formula caveat, and recommendations.

**Must redact**

- No secrets are involved, but local absolute paths should become repo-relative paths.

**Needs permission**

- Any claim about production checkout, revenue recovery, or stakeholder adoption.

**Can be generalized**

- The project can be described as "checkout funnel optimization analysis from event/cart tables."

### Claim Safety Checklist

- Every metric comes from the generated report.
- No conversion lift is claimed.
- No payment system change is claimed.
- Formula caveats are visible.
- Tableau is described as translated to Streamlit, not delivered as Tableau.
- MySQL is described as source/fallback, not the canonical runtime.

### Detailed Follow-Up Backlog

| Improvement | Why It Matters | Effort | Owner | Status |
| --- | --- | --- | --- | --- |
| Add formula caveat to dashboard UI | Prevents stakeholder confusion. | low | self | planned |
| Add dashboard screenshots | Improves public proof. | low | self | planned |
| Add parser fixtures | Protects future dump ingestion. | medium | self | planned |
| Add opportunity-sizing sensitivity table | Makes recommendations more business-ready. | medium | self | planned |
| Add experiment design section | Shows how to validate checkout fixes. | medium | self | planned |

### One-Page Version

**Project:** Checkout Flow Optimization.

**Problem:** A SQL/Tableau brief required checkout success, abandonment, error, and device analysis from a MySQL-style dump.

**Delivered:** A SQL-first DuckDB pipeline, Gold funnel marts, Streamlit dashboard, and business report.

**My role:** End-to-end analytics engineer and dashboard builder.

**STAR-B summary:** The situation was checkout data with conversion friction. The task was to make a reproducible funnel analysis. The action was to parse the dump, model Bronze/Silver/Gold tables, create marts, and build a dashboard. The result was 4,334 attempts, 1,372 successes, 31.7% success rate, and a ranked error story. The bridge is that this proves funnel analytics and transparent metric communication.

**Evidence:** `README.md`, `scripts/`, `dashboard/app.py`, and `reports/checkout_flow_optimization_report.md`.

**Trade-off:** Streamlit replaced Tableau for local reproducibility.

**Lesson:** Funnel metrics must show formula assumptions, not just polished KPIs.

**Relevance:** Useful for BI Analyst, Analytics Engineer, Data Analyst, and ecommerce/funnel analytics work.

## Raw Template Completion Notes

This section is intentionally detailed so the report can later be shortened into a public case study, recruiter proof note, or interview answer set.

### Delivered Artifacts In Detail

| Artifact | Purpose | My Contribution | Proof Location | Public? |
| --- | --- | --- | --- | --- |
| MySQL dump ingestion | Preserve checkout source tables locally. | Parsed dump into DuckDB Bronze tables. | `scripts/bronze/` | yes |
| Silver analysis window | Type and filter checkout data for the course period. | Modeled July 2022 through January 2023 analysis rows. | `scripts/silver/` | yes |
| Gold funnel marts | Support success, abandonment, and error analysis. | Built dashboard-ready marts and quiz outputs. | `scripts/gold/` | yes |
| Streamlit dashboard | Present checkout story interactively. | Built pages for monthly success, abandonment, and errors/devices. | `dashboard/app.py` | yes |
| Markdown report | Capture current state, hypothesis, recommendations, and quiz support. | Generated report with caveats. | `reports/checkout_flow_optimization_report.md` | yes |
| Retrospective | Convert project into proof. | Wrote transparent STAR-B record. | this file | yes |

### Technical Stack Detail

- Languages: SQL, Python, Markdown.
- Frameworks: Streamlit.
- Database: DuckDB.
- Source format: MySQL SQL dump.
- Visualization: Streamlit and Plotly-style local dashboarding.
- Testing approach: raw count checks, date range checks, device checks, Gold coverage checks, static compile and pipeline run during delivery.
- CI/CD: none; local verification only.
- Monitoring: none; not a production checkout system.

### Technical Decisions And Trade-Offs In Detail

| Decision | Options Considered | Choice Made | Why | Trade-Off | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| Canonical engine | MySQL, Postgres, DuckDB | DuckDB | Consistent local portfolio stack. | Required dump parsing. | Reproducible local warehouse. | README |
| Visualization layer | Tableau, notebook charts, Streamlit | Streamlit | Repo standard and easy local demo. | Not a Tableau workbook. | Interactive dashboard without external BI dependency. | `dashboard/app.py` |
| Formula caveat | Hide odd values, clamp values, document formula | Document formula | Honest reporting. | Less polished-looking metric story. | More credible analysis. | report |
| Python role | Transform in Python, orchestrate SQL | Python orchestrates SQL | SQL-first project should keep transformations relational. | More project files. | Clear lineage. | scripts |

### Metrics And Outcomes In Detail

Measured local outcomes:

- Analysis window: July 2022 through January 2023.
- Total carts: 5,001.
- Checkout attempts: 4,334.
- Successful attempts: 1,372.
- Overall checkout success rate: 31.7%.
- Course-formula cart abandonment rate: 13.3%.
- Highest success-rate month: August 2022 at 47.1%.
- Highest abandonment-rate month: October 2022 at 37.5%.
- Most common checkout error: `number field is required` with 1,220 attempts.

Qualitative outcomes:

- The project creates a clear checkout friction story.
- The recommendations are tied to observed payment-form errors.
- The report highlights formula caveats instead of hiding them.

Unmeasured outcomes:

- No checkout fix was deployed.
- No A/B test was run.
- No revenue recovery was measured.

Honest phrasing:

- "This analysis identifies checkout friction in the provided data."
- Do not say "this improved checkout conversion."

### Challenges, Mistakes, And Constraints In Detail

Real constraints:

- The source was a MySQL-style dump, not native DuckDB files.
- The brief expected Tableau but this repo uses Streamlit.
- The course abandonment formula has edge cases.
- The project is local and descriptive.

Blameless system notes:

- Funnel data often exposes instrumentation or formula surprises. The right response is to document the assumptions, not force all metrics to look intuitive.

Mistakes or weak spots:

| Issue | What Happened | Impact | What I Did | What I Would Do Next Time |
| --- | --- | --- | --- | --- |
| Formula oddity | Some monthly attempts can exceed carts. | Abandonment can confuse readers. | Kept the formula visible and documented caveat. | Put caveat directly in dashboard. |
| No screenshots | Dashboard exists but visual proof is not captured. | Portfolio review is slower. | Added follow-up. | Capture screenshots during delivery. |
| No experiment plan in dashboard | Recommendations are descriptive. | Cannot prove lift. | Avoided conversion claims. | Add A/B test design as public case-study addendum. |

### Strong Public Case Study Shape

1. Open with the checkout friction problem.
2. Show the data model: carts and checkout actions.
3. Show monthly success and abandonment trends.
4. Show top errors and device split.
5. Explain recommendations.
6. Close with what would be needed to prove improvement: experiment, tracking, and post-change comparison.

### Additional Interview Prompts

**How did you handle Tableau requirements?**

I translated the Tableau story into Streamlit while keeping the SQL-first transformations. The analytical contract stayed intact even though the visualization technology changed.

**How would you productionize it?**

I would connect the pipeline to scheduled checkout event exports, add data contracts for event schemas, deploy the dashboard, and add experiment tracking for checkout form changes.

**What would you test next?**

I would add parser fixtures for the SQL dump and smoke tests for the dashboard, then validate the abandonment formula against a stakeholder-approved definition.

### Claim Safety Checklist Addendum

- Do not claim conversion lift.
- Do not claim payment-form changes were deployed.
- Do not hide the abandonment formula caveat.
- Do not describe MySQL as the runtime engine.
- Do not imply Tableau was delivered in this repo implementation.
