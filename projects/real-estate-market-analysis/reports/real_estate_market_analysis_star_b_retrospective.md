# Real Estate Market Analysis STAR-B Retrospective

This is the canonical STAR-B retrospective for `projects/real-estate-market-analysis` inside the 365DS demo projects workspace.

Working title: **Real Estate Analytics Warehouse Retrospective**

The project started from a 365 Data Science Python/Jupyter analytics brief. The delivered local implementation reframes it as a reproducible DuckDB medallion pipeline with Bronze raw CSV loading, Silver cleaning and joining, Gold marts, SQL quality checks, a Streamlit dashboard, and a generated Markdown business report.

## Project Metadata

- Project name: Real Estate Market Analysis
- Project type: 365DS analytics project implementation and retrospective proof artifact
- Domain: real estate transactions, customer profiles, descriptive analytics, dashboarding
- Time period: June 2026 local implementation thread
- Source brief: `project-instructions/Real Estate Market Analysis with Python Project Instructions.md`
- Source datasets: `source-datasets/Real Estate Market Analysis With Python/customers.csv` and `source-datasets/Real Estate Market Analysis With Python/properties.csv`
- Delivered project path: `projects/real-estate-market-analysis/`
- Delivery status: local implementation exists; retrospective restored and expanded after implementation
- Current status: internal proof document, not a public case study yet
- Role: local analytics engineer, data modeler, dashboard builder, report writer
- Team size: solo delivery with AI pair-programming support
- Client, employer, or self-directed: self-directed portfolio project
- Primary stack: Python, pandas, DuckDB, SQL, Streamlit, Plotly, Markdown
- Public link: not published
- Repo link: local repo only
- Demo link: local dashboard only
- Case study link: this file
- Related LinkedIn post: not published yet
- Private evidence location: repo memory and local verification notes under `docs/agent-memory/`

## Audience Fit

### Hiring Manager Signal

This project shows the ability to take a small, notebook-oriented analytics brief and turn it into a reproducible analytics workflow. The strongest signal is not the chart layer by itself. The stronger signal is the raw-to-report path:

- immutable raw source files;
- explicit Bronze/Silver/Gold layers;
- repeatable cleaning and customer/property joins;
- derived fields such as customer age at purchase;
- Gold marts organized around business questions;
- SQL quality checks;
- Streamlit dashboard reading Gold only;
- generated Markdown report;
- transparent proof document that does not overclaim impact.

For a data analyst role, it shows cleaning, interpretation, and visualization. For an analytics engineer role, it shows modeling boundaries, reproducibility, and quality checks. For a BI-adjacent role, it shows a dashboard backed by modeled data rather than hidden transformation logic.

### Recruiter Signal

Recruiter-visible keywords and outcomes:

- Python
- pandas
- DuckDB
- SQL
- Streamlit
- Plotly
- data cleaning
- medallion architecture
- dashboarding
- data quality checks
- real estate analytics
- customer/property joins
- descriptive statistics
- business reporting

Simple outcome: a 365DS Python real estate brief was converted into a repeatable local analytics project with a dashboard and report.

### Freelance Client Signal

This project resembles a small client engagement where the client has CSV exports and wants a trusted dashboard/report:

- property inventory and sales status;
- sold-property revenue;
- average price and area;
- geography distribution;
- buyer age intervals;
- satisfaction by country;
- price intervals and available inventory;
- clear caveats about what the data does and does not prove.

The project proves an ability to deliver value from local files without pretending the output is a production BI platform.

### Wrong Audience To Filter Out

This project should not attract someone expecting:

- production cloud BI;
- predictive property valuation;
- automated market forecasting;
- geospatial property search;
- real-time data ingestion;
- investment-grade market research.

It is a local descriptive analytics project and should be presented that way.

## Transparency Statement

This retrospective is written as an internal proof record. It separates verified local artifacts from judgment, estimated value, private/local context, and lessons learned. It does not claim outcomes that cannot be supported.

Fully verifiable:

- The source brief exists under `project-instructions/`.
- Raw real estate source files exist under `source-datasets/Real Estate Market Analysis With Python/`.
- The implementation exists under `projects/real-estate-market-analysis/`.
- The project has scripts, docs, quality checks, a dashboard, and a generated report.
- The generated report states 267 properties, 195 sold, 72 available, $52,539,739 in sold-property revenue, $269,435 average sold price, 3.60/5 average satisfaction, and -0.1745 age-price correlation.

Partially verifiable:

- Local dashboard behavior is supported by code and previous runtime checks, but this retrospective does not include screenshots.
- The workflow is documented, but this file does not rerun the pipeline itself.

Not shared publicly:

- Local machine-specific runtime details beyond repo-relative paths.
- Any private environment details.

Estimated:

- Hiring, recruiter, or freelance usefulness is judgment, not measured market response.

Not my responsibility or not claimed:

- No production deployment is claimed.
- No external stakeholder adopted the dashboard.
- No real estate investment decision was made from this analysis.
- No business impact, user adoption, or revenue improvement is claimed.

Misleading claims to avoid:

- "Built a production real estate BI platform."
- "Improved real estate revenue."
- "Predicted property prices."
- "Validated market strategy."

Honest framing:

> This project proves local analytics engineering and reporting execution on a small real estate dataset. It does not prove production deployment, external stakeholder adoption, market impact, or predictive modeling maturity.

## Executive Summary

- Problem: The original brief required real estate preprocessing, descriptive analysis, visualization, interpretation, and quiz answers from property and customer datasets.
- Delivered solution: A reproducible DuckDB and Streamlit analytics project with Bronze/Silver/Gold layers, SQL quality checks, dashboard, and generated report.
- Your role: End-to-end local analytics engineer and report/dashboard builder.
- Main technical or business constraint: Preserve the Python learning objective while making the work more inspectable than a notebook.
- Most important decision: Use a lightweight medallion workflow and keep the dashboard on Gold marts only.
- Outcome: The project reports sales, revenue, building, geography, age interval, price interval, satisfaction, and correlation findings.
- Evidence: `projects/real-estate-market-analysis/reports/real_estate_market_analysis_report.md`
- Main lesson: A small analytics project becomes stronger proof when the lineage from raw data to trusted output is visible.

## Delivery Context

### Situation

Before this implementation, the source material was a learning-project brief and raw CSV files. The project could have been solved in a notebook, but a notebook would be weaker as portfolio proof because:

- cleaning logic is harder to inspect;
- dashboard logic can become mixed with transformation logic;
- quality checks are often missing;
- rerun behavior is less explicit;
- final charts do not prove how the data was prepared.

The business context is a real estate dataset with property listings/sales and customer information. The analytic need is descriptive: understand sold and available inventory, revenue, building performance, geography, buyer age, satisfaction, and price patterns.

### Task

Primary objective:

- Turn the source CSV files into a reproducible local analytics project that answers the original business and quiz questions.

Secondary objectives:

- Preserve raw files.
- Document data flow.
- Build a dashboard that reads modeled outputs only.
- Generate a report with findings and quiz support.
- Create proof that can be reused for interviews and portfolio material.

Success criteria:

- Pipeline can rebuild the warehouse from raw CSVs.
- Gold marts support dashboard and report questions.
- Dashboard reads `gold.*` marts only.
- Report includes concrete metrics and caveats.
- Claims remain supported by repo artifacts.

Definition of done:

- Project folder contains scripts, docs, tests, dashboard, and report.
- Raw data remains under `source-datasets/`.
- Generated runtime artifacts stay ignored by git.
- Retrospective identifies what the project proves and does not prove.

Non-goals:

- Production cloud deployment.
- Predictive price modeling.
- External market data enrichment.
- Tableau workbook.
- Automated scheduled refresh.

Risks known at the start:

- Overengineering a small dataset.
- Overclaiming weak descriptive findings.
- Hiding cleaning logic inside the dashboard.
- Treating quiz outputs as business impact.

### Scope Boundaries

Included:

- CSV ingestion;
- data cleaning and type normalization;
- customer/property joins;
- derived age and interval fields;
- Gold marts;
- SQL quality checks;
- Streamlit dashboard;
- generated Markdown report;
- this retrospective proof record.

Excluded:

- production hosting;
- real estate valuation;
- model training;
- external market validation;
- stakeholder adoption tracking.

What changed during delivery:

- The project was elevated from a Python analysis exercise into the first proof of the repo-standard DuckDB and Streamlit workflow.
- The dashboard became a presentation layer over Gold marts rather than a place for hidden data transformation.

## STAR-B Story Bank

### STAR-B Story 1: Main Delivery Story

**Situation**

A 365DS real estate project brief required cleaning, joining, analyzing, visualizing, and interpreting property and customer data.

**Task**

Preserve the brief's analysis contract while turning the work into a reproducible local analytics project suitable for portfolio review.

**Action**

Built a DuckDB medallion pipeline with Bronze raw CSV loading, Silver cleaning and joining, Gold business-question marts, SQL quality checks, a generated Markdown report, and a Streamlit dashboard that reads Gold marts only.

**Result**

The project produced verified local metrics: 267 properties, 195 sold, 72 available, $52,539,739 in sold-property revenue, $269,435 average sold price, 3.60/5 average satisfaction, and -0.1745 customer age/property price correlation.

**Bridge**

This proves I can turn a learning brief into a repeatable analytics deliverable with data lineage, quality checks, dashboarding, and honest interpretation.

**Evidence**

- Repo artifact: `projects/real-estate-market-analysis/`
- Report: `projects/real-estate-market-analysis/reports/real_estate_market_analysis_report.md`
- Dashboard: `projects/real-estate-market-analysis/dashboard/app.py`
- Data flow doc: `projects/real-estate-market-analysis/docs/data_flow.md`
- Metric: report metrics listed above
- Confidence level: verified

### STAR-B Story 2: Technical Decision Story

**Situation**

The original brief could be solved in pandas or Jupyter, but the repo needed reusable architecture across multiple analytics projects.

**Task**

Choose a structure that was more reproducible than a notebook without becoming unnecessarily heavy for a small dataset.

**Action**

Used Python orchestration and DuckDB layers. Bronze preserves raw CSVs, Silver cleans and joins, Gold creates business marts, and Streamlit reads Gold only.

**Result**

The project became the first working example of the repo's DuckDB/Streamlit medallion pattern over CSV sources.

**Bridge**

This proves judgment about scaling structure to the problem: enough architecture for proof and repeatability, not production machinery for its own sake.

**Evidence**

- Architecture note: `projects/real-estate-market-analysis/docs/data_flow.md`
- Gold SQL: `projects/real-estate-market-analysis/scripts/gold/create_marts.sql`
- Dashboard: `projects/real-estate-market-analysis/dashboard/app.py`
- Confidence level: verified

### STAR-B Story 3: Constraint Or Failure Story

**Situation**

The dataset is small and descriptive. It would be easy to make the project sound more advanced than it is.

**Task**

Make the project useful as proof without overstating business or modeling impact.

**Action**

Framed the outputs as local descriptive analytics. Reported weak age-price correlation plainly. Avoided claims about production deployment, adoption, valuation, or revenue impact.

**Result**

The retrospective remains credible: it shows execution while preserving limitations.

**Bridge**

Next time, I would add screenshots, a dashboard smoke test, and maybe external/public demo packaging before turning it into a public case study.

**Evidence**

- Limitation notes in this retrospective
- Report interpretation: `projects/real-estate-market-analysis/reports/real_estate_market_analysis_report.md`
- Confidence level: verified

### STAR-B Story 4: Collaboration Or Client Story

**Situation**

The repo direction evolved from project completion into portfolio proof. That required making the work understandable to different audiences.

**Task**

Document the work so it can serve hiring managers, recruiters, freelance clients, and future maintainers.

**Action**

Added project docs, generated report output, and this retrospective with audience-specific proof summaries.

**Result**

The project can now be discussed as a technical implementation, a business analysis, or a portfolio case study seed.

**Bridge**

This proves communication discipline around analytics work, not only code execution.

**Evidence**

- Project docs: `projects/real-estate-market-analysis/docs/`
- Report: `projects/real-estate-market-analysis/reports/real_estate_market_analysis_report.md`
- Confidence level: verified

## Evidence Ledger

| Claim | Evidence | Location | Public? | Confidence | Notes |
| --- | --- | --- | --- | --- | --- |
| The project uses a Bronze/Silver/Gold flow. | Data flow docs and scripts. | `docs/data_flow.md`, `scripts/` | yes | verified | Local DuckDB medallion pattern. |
| Raw source files are preserved. | Source files remain under `source-datasets/`. | `source-datasets/Real Estate Market Analysis With Python/` | yes | verified | Derived files are project-local. |
| Dashboard reads Gold marts only. | Data flow doc and report. | `docs/data_flow.md`, `reports/real_estate_market_analysis_report.md` | yes | verified | Dashboard is presentation layer. |
| Portfolio size is 267 properties. | Generated report. | `reports/real_estate_market_analysis_report.md` | yes | verified | Dataset metric. |
| Sold properties total 195 and available properties total 72. | Generated report. | `reports/real_estate_market_analysis_report.md` | yes | verified | Dataset metric. |
| Sold-property revenue is $52,539,739. | Generated report. | `reports/real_estate_market_analysis_report.md` | yes | verified | Dataset revenue, not business impact. |
| Average sold price is $269,435. | Generated report. | `reports/real_estate_market_analysis_report.md` | yes | verified | Dataset metric. |
| Average sold area is 899.87 sq ft. | Generated report. | `reports/real_estate_market_analysis_report.md` | yes | verified | Dataset metric. |
| Average deal satisfaction is 3.60/5. | Generated report. | `reports/real_estate_market_analysis_report.md` | yes | verified | Descriptive metric. |
| Age-price correlation is -0.1745. | Generated report. | `reports/real_estate_market_analysis_report.md` | yes | verified | Weak relationship; not predictive. |
| No production usage is claimed. | No deployment artifact exists. | n/a | yes | verified | Must remain explicit. |

## Delivered Artifacts

| Artifact | Purpose | Your Contribution | Proof Location | Public? |
| --- | --- | --- | --- | --- |
| Bronze raw loader | Preserve source CSVs in DuckDB | Built local ingestion layer | `scripts/bronze/` | yes |
| Silver cleaning layer | Normalize, type, join, derive fields | Built cleaning/join logic | `scripts/silver/` | yes |
| Gold marts | Expose business-question tables | Built reporting marts | `scripts/gold/create_marts.sql` | yes |
| SQL quality checks | Validate key assumptions | Added project checks | `tests/quality_checks.sql` | yes |
| Streamlit dashboard | Explore metrics interactively | Built dashboard over Gold marts | `dashboard/app.py` | yes |
| Markdown report | Summarize findings and quiz answers | Generated report output | `reports/real_estate_market_analysis_report.md` | yes |
| Data flow docs | Explain rerun contract | Documented flow | `docs/data_flow.md` | yes |
| Retrospective | Turn delivery into proof | Wrote transparent STAR-B record | this file | yes |

## Technical Stack

- Languages: Python, SQL, Markdown
- Frameworks: Streamlit
- Databases: DuckDB
- APIs: none
- Cloud or hosting: none; local only
- Auth: none
- Testing: SQL quality checks, pipeline checks, static compile during delivery
- CI/CD: none
- Monitoring or logging: local command output only
- Data tools: pandas, DuckDB, Plotly
- AI or automation tools: AI pair-programming support in repo workflow, not a runtime dependency for this project
- Other: uv-managed project environment

### Stack Rationale

Python and pandas fit the original project brief. DuckDB adds a local warehouse with clear layers. Streamlit provides a lightweight dashboard without requiring Tableau or a cloud BI service. SQL Gold marts make the dashboard easier to inspect because transformation logic is not hidden inside UI code.

### Stack Limitations

The stack is local and batch-oriented. It does not provide role-based access, scheduled refresh, hosted dashboards, or production observability. DuckDB is excellent for local analytics, but a production multi-user BI environment would need additional deployment and governance work.

## Technical Decisions And Trade-Offs

| Decision | Options Considered | Choice Made | Why | Trade-Off | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| Notebook-only vs pipeline | Jupyter only, pandas scripts, DuckDB medallion | DuckDB medallion with Python orchestration | Better portfolio proof and rerun behavior | More structure than a notebook | Clear raw-to-Gold lineage | `docs/data_flow.md` |
| Dashboard source | Raw CSV, Silver table, Gold marts | Gold marts only | Keeps UI separate from transformation logic | Requires marts before dashboard | Cleaner dashboard contract | `dashboard/app.py` |
| Correlation interpretation | Ignore, overstate, or report plainly | Report weak negative correlation plainly | Avoids false predictive claim | Less dramatic story | More credible analysis | generated report |
| Scope | Add ML, deploy cloud, stay descriptive | Stay descriptive/local | Fits data size and brief | Less advanced surface | Honest project proof | this file |

## Delivery Timeline

| Phase | Dates | What Happened | Key Decision | Evidence |
| --- | --- | --- | --- | --- |
| Discovery | June 2026 | Read source brief and raw CSV contract. | Preserve raw files. | source brief, `source-datasets/` |
| Architecture | June 2026 | Established DuckDB/Streamlit pattern. | Use Bronze/Silver/Gold. | `docs/data_flow.md` |
| Build | June 2026 | Created raw load, cleaning, joins, and Gold marts. | Derive age and business intervals in modeled layers. | `scripts/` |
| Test | June 2026 | Ran quality checks and generated report. | Tie report to Gold outputs. | `tests/`, report |
| Delivery | June 2026 | Built Streamlit dashboard and project docs. | Dashboard reads Gold only. | `dashboard/app.py` |
| Follow-up | June 2026 | Wrote project-level retrospective. | Keep proof honest and detailed. | this file |

## Metrics And Outcomes

### Measured Outcomes

- Metric: property portfolio size
  - Before: raw CSVs only
  - After: 267 modeled properties
  - Source: generated report
  - Confidence level: verified

- Metric: sold-property revenue
  - Before: raw property records
  - After: $52,539,739
  - Source: generated report
  - Confidence level: verified

- Metric: age-price relationship
  - Before: unreported relationship
  - After: -0.1745 correlation
  - Source: generated report
  - Confidence level: verified

### Qualitative Outcomes

- Stakeholder feedback: not collected.
- User feedback: not collected.
- Recruiter or interviewer relevance: estimated; the project gives concrete proof of Python/DuckDB/Streamlit delivery.
- Client relevance: estimated; resembles a CSV-to-dashboard engagement.
- Confidence level: estimated.

### Unmeasured Outcomes

What probably improved:

- Inspectability of the original analysis.
- Reproducibility of the cleaning and report.
- Ease of explaining the project in interviews.

Honest phrasing:

- "The project makes the analysis easier to inspect and rerun locally."
- Do not say "the dashboard improved business decisions" without evidence.

## Retrospective Analysis

### Keep Doing

- Preserve raw source files.
- Separate cleaning, modeling, dashboarding, and reporting.
- Keep dashboard reads on Gold marts.
- Use generated reports as proof anchors.
- Write limitations directly into the retrospective.

### More Of

- More visual proof: screenshots, short demo clips, and dashboard walkthroughs.
- More automated checks around date parsing and join completeness.
- More explicit dashboard annotations for caveats.

### Less Of

- Less compression when writing proof docs. The detailed raw version is more useful for future public and interview material.
- Less temptation to make small descriptive projects sound like predictive systems.

### Stop Doing

- Stop treating "finished dashboard" as enough proof by itself.
- Stop rewriting detailed retrospectives into shorter versions when the detailed raw artifact is more valuable.

### Start Doing

- Create both raw and public versions: detailed internal proof first, shorter public case study later.
- Add screenshots as evidence before publishing.
- Add a small smoke check for each dashboard.

## Challenges, Mistakes, And Constraints

### Real Constraints

- Time: built as part of a larger multi-project portfolio thread.
- Budget: local/free tooling only.
- Access: no external stakeholder validation.
- Data: small CSV dataset; no external market enrichment.
- Stakeholder availability: none; self-directed project.
- Technical debt: local dashboard and report only; no hosted deployment.
- Knowledge gaps: no need for advanced real estate modeling because the brief was descriptive.
- Tooling: local DuckDB/Streamlit stack.

### Mistakes Or Weak Spots

| Issue | What Happened | Impact | What I Did | What I Would Do Next Time |
| --- | --- | --- | --- | --- |
| The project can be overstructured for its size. | A medallion pattern adds files and concepts. | Could feel heavier than a notebook. | Kept the scope local and focused. | Use the same structure only when it improves proof and rerun behavior. |
| The age-price correlation is weak. | The metric exists but is not decision-grade. | Could be overread. | Reported it plainly as weak. | Add richer features before any predictive framing. |
| No screenshots yet. | The report proves metrics but not visual polish. | Weaker public portfolio proof. | Listed screenshots as follow-up. | Capture dashboard screenshots as part of delivery. |

### Blameless System Notes

The original learning brief was not designed as a production analytics spec. Turning it into portfolio proof required adding structure that the brief did not ask for: project docs, quality checks, Gold marts, and retrospective proof. That overhead is justified for portfolio and interview purposes, but would be unnecessary for a one-off classroom notebook.

## Risk Register

| Risk | Severity | What Reduced The Risk | What Remains | Evidence |
| --- | --- | --- | --- | --- |
| Overstating market insight | medium | Transparent descriptive wording | No external market validation | report, this file |
| Weak visual proof | medium | Dashboard code exists | Screenshots/video missing | `dashboard/app.py` |
| Local-only delivery | low | Run commands and docs exist | No hosted demo | README |
| Predictive overclaim | medium | No predictive claim is made | Could be misread if public copy is too short | this file |

## Proof Summary For Hiring Managers

- I delivered: a Python/DuckDB real estate analytics project with medallion layers, Gold marts, checks, report, and dashboard.
- I was responsible for: raw ingestion, cleaning, customer/property joins, derived fields, mart design, dashboarding, reporting, and retrospective proof.
- The hardest constraint was: making a small learning project reproducible without overengineering it.
- The strongest evidence is: generated report metrics, data flow docs, Gold mart SQL, quality checks, and dashboard code.
- This maps to these job responsibilities: data cleaning, analytics engineering, dashboarding, stakeholder reporting, and data quality.
- I would improve: screenshots, dashboard smoke tests, and richer geography/modeling only if more data supports it.

## Proof Summary For Recruiters

- Role fit: Data Analyst, Analytics Engineer, BI Analyst.
- Keywords: Python, pandas, SQL, DuckDB, Streamlit, Plotly, dashboards, data cleaning, medallion architecture.
- Project type: self-directed analytics portfolio project.
- Tools: Python, pandas, DuckDB, SQL, Streamlit.
- Outcome: local reproducible dashboard and report over real estate transaction/customer data.
- Seniority signal: honest trade-offs, quality checks, and separation of dashboard from transformation logic.
- Proof link: `projects/real-estate-market-analysis/`.

## Proof Summary For Freelance Clients

- Client problem this resembles: "I have property/customer CSVs and need clean metrics, a dashboard, and a report."
- What I can deliver: cleaned data, joined datasets, KPI marts, dashboard views, and written findings.
- How I manage ambiguity: separate verified metrics from interpretation and avoid unsupported claims.
- How I communicate progress: docs, report, dashboard, and evidence ledger.
- What proof I can show: local project files and report metrics.
- What I will not overpromise: valuation, investment decisions, or production BI without more scope.

## Interview Answer Bank

### Tell Me About A Project You Delivered

I delivered a Real Estate Market Analysis project from a 365DS Python brief. I converted raw customer and property CSVs into a local DuckDB warehouse with Bronze, Silver, and Gold layers, then built a Streamlit dashboard and generated a Markdown report with metrics and quiz answers.

### Tell Me About A Technical Trade-Off

The trade-off was notebook simplicity versus portfolio-grade reproducibility. A notebook would be faster, but less inspectable. A full production stack would be too heavy. DuckDB and Streamlit gave me a middle path.

### Tell Me About A Time Something Went Wrong

The main risk was not a runtime bug but a proof risk: overstating descriptive metrics. For example, the age-price correlation is weak. I documented it plainly and avoided treating it as predictive.

### Tell Me About A Time You Worked With Ambiguity

The brief asked for analysis and visualization, but not a specific engineering structure. I defined the structure: raw files stay immutable, Silver cleans and joins, Gold answers business questions, and Streamlit reads Gold only.

### Tell Me About A Measurable Result

The project reports 267 properties, 195 sold, 72 available, $52,539,739 in sold-property revenue, $269,435 average sold price, 3.60/5 satisfaction, and -0.1745 age-price correlation.

## Public Version Notes

### Safe To Share

- Project purpose.
- Stack.
- Report metrics.
- Dashboard screenshots.
- Repo-relative paths.
- Limitations.

### Must Redact

- Local machine-specific paths if publishing outside the repo.
- Any private environment details.

### Needs Permission

- Any claim involving external reviewers, hiring outcomes, client feedback, or stakeholder adoption.

### Can Be Generalized

- "365DS project" can become "education project brief."
- "Local dashboard" can become "Streamlit dashboard demo."

## Resume Bullets

- Built a Python, DuckDB, and Streamlit real estate analytics project over 267 properties, producing cleaned customer/property joins, Gold marts, quality checks, dashboard views, and a report with revenue, geography, age, price, and satisfaction insights.
- Converted a notebook-style analytics brief into a reproducible medallion pipeline with raw preservation, SQL Gold marts, and dashboard-ready outputs.

## LinkedIn Post Angle

- Main claim: I turned a small real estate analytics brief into a reproducible local data product.
- Non-obvious lesson: portfolio proof is stronger when it shows the raw-to-report path, not only the final chart.
- Concrete proof: 267 properties, 195 sold, $52,539,739 in sold-property revenue, and Gold-backed dashboard marts.
- Mistake or trade-off: More structure than a notebook, but less complexity than production BI.
- Audience: data analysts, analytics engineers, portfolio reviewers.
- Hook options:
  1. "A chart is not a portfolio project. The raw-to-report path is."
  2. "I rebuilt a small real estate notebook brief as a DuckDB analytics workflow."
  3. "The most honest metric in this project is the weak one."

## Follow-Up Improvements

| Improvement | Why It Matters | Effort | Owner | Status |
| --- | --- | --- | --- | --- |
| Add dashboard screenshots | Makes the proof faster to scan. | low | self | planned |
| Add short demo video | Helps reviewers understand the flow without running it. | medium | self | planned |
| Add dashboard smoke check | Protects local demo reliability. | low | self | planned |
| Add geography/map view | Real estate analysis benefits from spatial context. | medium | self | planned |
| Add richer predictive model only with more data | Avoids overclaiming from a small dataset. | high | self | deferred |

## Claim Safety Checklist

- Every metric has a source in the generated report.
- Every stack detail appears in project files.
- Responsibility is framed as self-directed local implementation.
- No production deployment is implied.
- No external stakeholder adoption is implied.
- No revenue improvement is implied.
- The weak correlation is not framed as predictive.
- The public version should keep limitations visible.

## Final Retrospective Judgment

### What This Project Proves

- I can interpret an analytics brief and preserve its business questions.
- I can build a local medallion-style DuckDB analytics workflow.
- I can clean and join raw CSV data into analysis-ready tables.
- I can model Gold marts around business questions.
- I can add lightweight quality checks.
- I can create a Streamlit dashboard from modeled data.
- I can generate a written report from warehouse output.
- I can write transparent proof documentation without overclaiming.

### What This Project Does Not Prove

- It does not prove production deployment.
- It does not prove stakeholder adoption.
- It does not prove hiring-market response.
- It does not prove freelance conversion.
- It does not prove automated refresh or cloud operations.
- It does not prove predictive valuation skill.

### Strongest Evidence

- `project-instructions/Real Estate Market Analysis with Python Project Instructions.md`
- `projects/real-estate-market-analysis/docs/data_flow.md`
- `projects/real-estate-market-analysis/scripts/pipeline.py`
- `projects/real-estate-market-analysis/scripts/silver/build_silver.py`
- `projects/real-estate-market-analysis/scripts/gold/create_marts.sql`
- `projects/real-estate-market-analysis/tests/quality_checks.sql`
- `projects/real-estate-market-analysis/dashboard/app.py`
- `projects/real-estate-market-analysis/reports/real_estate_market_analysis_report.md`

### Weakest Evidence

- No saved dashboard screenshot.
- No external user feedback.
- No public portfolio page yet.
- No deployment proof.
- No measured hiring or freelance outcome.

### Best Use Of This Retrospective

Primary use:

- internal proof and interview preparation

Secondary uses:

- portfolio case study seed
- LinkedIn post seed
- recruiter proof note
- freelance proposal proof for CSV-to-dashboard work

## One-Page Version

### Project

Real Estate Market Analysis: a 365DS Python/Jupyter analytics brief rebuilt as a local DuckDB and Streamlit analytics project.

### Problem

The original project asked for preprocessing, descriptive statistics, analysis, visualization, interpretation, and quiz answers from real estate property and customer datasets.

A notebook could answer the questions once, but it would be weaker as long-term proof because the cleaning, marts, dashboard, checks, and report would be harder to inspect separately.

### Delivered

- Bronze raw CSV loading
- Silver cleaned customer/property transaction table
- Gold business-question marts
- SQL quality checks
- generated Markdown report
- Streamlit dashboard reading Gold marts only
- project docs for data flow and naming
- this STAR-B retrospective

### My Role

Builder and analyst for the local implementation and retrospective proof record.

### STAR-B Summary

**Situation:** A 365DS real estate brief required Python analysis of property transactions and customer profiles.

**Task:** Preserve the analysis contract while making the work more reproducible and easier to inspect.

**Action:** Built a DuckDB Bronze/Silver/Gold pipeline, added SQL quality checks, generated a Markdown report, and created a Streamlit dashboard that reads Gold marts only.

**Result:** The local project produced verified report findings: 267 properties, 195 sold, 72 available, $52,539,739 revenue, $269,435 average sold price, 3.60/5 satisfaction, and -0.1745 age-price correlation.

**Bridge:** This proves analytics engineering discipline on a small project. It does not yet prove external adoption, production deployment, or business impact.

### Evidence

- source brief: `project-instructions/Real Estate Market Analysis with Python Project Instructions.md`
- project docs: `projects/real-estate-market-analysis/docs/data_flow.md`
- pipeline: `projects/real-estate-market-analysis/scripts/pipeline.py`
- marts: `projects/real-estate-market-analysis/scripts/gold/create_marts.sql`
- checks: `projects/real-estate-market-analysis/tests/quality_checks.sql`
- dashboard: `projects/real-estate-market-analysis/dashboard/app.py`
- report: `projects/real-estate-market-analysis/reports/real_estate_market_analysis_report.md`

### Trade-Off

The solution is more structured than the original notebook-oriented brief. That adds overhead, but it makes the work easier to rerun, test, inspect, and explain.

### Lesson

A portfolio analytics project is stronger when the proof is not just a chart. The proof is the path from raw data to trusted output.

### Relevance

For hiring managers, this shows reproducible analytics delivery. For recruiters, it turns Python, SQL, DuckDB, and Streamlit into a concrete project receipt. For freelance clients, it shows how raw CSVs can become a local dashboard and report without pretending the result is already a production BI platform.

