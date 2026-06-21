# User Journey Analysis STAR-B Retrospective

This is the STAR-B retrospective for `projects/user-journey-analysis` inside the 365DS demo projects workspace.

Working title: **User Journey Analytics Functions And Pathing Retrospective**

The project started from a 365 Data Science Python project brief about analyzing website journeys for subscription users. The delivered local implementation keeps the required Python journey functions while adding a reproducible DuckDB medallion pipeline, Gold marts, quality checks, a Streamlit dashboard, and a generated Markdown report.

## Project Metadata

- Project name: User Journey Analysis
- Project type: 365DS analytics project implementation and retrospective proof artifact
- Domain: product analytics, user journeys, subscription behavior, page-path analysis
- Source brief: `project-instructions/User Journey Analysis in Python Project Instructions.md`
- Source dataset: `source-datasets/User Journey Analysis in Python/user_journey_raw.csv`
- Delivered project path: `projects/user-journey-analysis/`
- Delivery status: local implementation exists; retrospective added after implementation
- Current status: internal proof document, not a public case study yet
- Primary stack: Python, pandas, DuckDB, SQL, Streamlit, Plotly, Markdown
- Public link: not published
- Demo link: local dashboard only
- External stakeholder validation: not claimed

## Transparency Statement

This retrospective is an internal proof record. It separates verified local artifacts from judgment, estimated value, and unproven external outcomes.

Verified local evidence:

- The source brief exists under `project-instructions/`.
- The project implementation exists under `projects/user-journey-analysis/`.
- The generated report states 9,935 raw sessions, 1,350 unique users, 931 Annual users, 376 Monthly users, and 43 Quarterly users.
- The project implements the required public functions: `remove_page_duplicates`, `group_by`, and `remove_pages`.
- The dashboard reads Gold marts only.

Not claimed:

- No production deployment is claimed.
- No external stakeholder used the dashboard.
- No business decision was made from this dashboard outside the local repo.
- No public adoption or recruiter response is claimed.

Honest framing:

> This project proves local product-analytics execution, journey preprocessing, reusable Python function design, and dashboard/report delivery. It does not yet prove production product analytics adoption.

## Audience Fit

### Hiring Manager Signal

This project shows the ability to turn behavioral clickstream-style data into reusable functions, modeled marts, dashboard views, and quiz-supported findings. The strongest signal is the combination of brief-required Python APIs with a reproducible warehouse/reporting workflow.

### Recruiter Signal

Recruiter-visible keywords and skills:

- Python
- pandas
- DuckDB
- Streamlit
- product analytics
- user journey analysis
- pathing
- sequence analysis
- data cleaning
- dashboarding
- quality checks

### Freelance Client Signal

This resembles a client request to understand how users move through a website, which pages dominate journeys, and which paths appear before conversion or subscription events.

### Wrong Audience To Filter Out

This is not a production event-streaming platform, real-time analytics system, or enterprise product analytics deployment.

## Executive Summary

- Problem: The brief needed analysis of user journey strings across sessions and subscription plans.
- Delivered solution: Python journey helpers, DuckDB Bronze/Silver/Gold layers, Gold marts, Streamlit dashboard, and Markdown report.
- Role: end-to-end local analytics implementation.
- Main constraint: preserve the course-required function behavior and preprocessing order.
- Most important decision: keep journey manipulation in Python while using DuckDB for reproducible reporting marts.
- Outcome: the project can answer page count, page presence, destination, sequence, and journey-length questions.
- Evidence: `projects/user-journey-analysis/reports/user_journey_analysis_report.md`
- Main lesson: list/session algorithms can be clearer in Python while still fitting a warehouse-backed dashboard workflow.

## Delivery Context

### Situation

The source data contained one row per raw journey/session. The brief expected Python functions for grouping sessions, removing pages, and removing consecutive duplicates. A simple notebook could answer the questions, but the portfolio needed repeatable outputs and a dashboard.

### Task

The project needed to:

- preserve raw data;
- implement the required public functions exactly;
- follow the course preprocessing order;
- generate scenario-level marts;
- support quiz answers;
- provide an interactive dashboard backed by Gold tables.

### Scope Boundaries

Included:

- raw load into Bronze;
- Silver validation and scenario construction;
- Gold page/path/sequence marts;
- Streamlit dashboard;
- Markdown report and quiz support.

Excluded:

- real-time event ingestion;
- production web analytics tracking;
- user identity enrichment beyond source fields;
- external A/B testing or attribution modeling.

## STAR-B Story Bank

### STAR-B Story 1: Main Delivery Story

**Situation**

The project brief asked for user journey analysis in Python, including specific helper functions and quiz outputs.

**Task**

Deliver the course-required analysis in a way that also fits the repo-standard DuckDB and Streamlit portfolio workflow.

**Action**

Built the required Python functions, loaded raw journeys into DuckDB, created grouped journey scenarios, generated Gold marts for counts, destinations, sequences, lengths, plan comparisons, and quiz support, then built a dashboard over Gold.

**Result**

The project reports 9,935 raw sessions, 1,350 users, and a strongest four-page last-three-session pattern count of 49.

**Bridge**

This proves product analytics execution and the ability to combine algorithmic Python with reproducible reporting layers.

**Evidence**

- Repo artifact: `projects/user-journey-analysis/`
- Report: `projects/user-journey-analysis/reports/user_journey_analysis_report.md`
- Dashboard: `projects/user-journey-analysis/dashboard/app.py`
- Confidence level: verified

### STAR-B Story 2: Technical Decision Story

**Situation**

The repo standard favors SQL-first transformations where relational, but this brief explicitly required Python APIs and journey-list logic.

**Task**

Choose the right boundary between Python and SQL.

**Action**

Kept session grouping, page removal, duplicate removal, and sequence metrics in Python where list operations are clearer, then persisted reporting outputs into DuckDB Gold marts.

**Result**

The project satisfies the Python learning objective without becoming an unstructured notebook-only analysis.

**Bridge**

This proves judgment about when not to force SQL.

**Evidence**

- Project helper functions: `projects/user-journey-analysis/scripts/pipeline.py`
- Catalog traits: `apps/learning-hub/catalog/projects.yaml`
- Confidence level: verified

### STAR-B Story 3: Constraint Or Failure Story

**Situation**

The sequence-counting requirement depends on the exact interpretation of journeys and sessions.

**Task**

Avoid ambiguous preprocessing that could shift quiz answers.

**Action**

Preserved the preprocessing order: group selected sessions, optionally remove selected pages, then remove consecutive duplicate pages.

**Result**

Quiz regression answers are documented, including quarterly page count third place as `Sign up`, Pricing destination fourth as `Courses`, and last-three average journey length as 3.6.

**Bridge**

This proves careful handling of business rules and course-contract details.

**Evidence**

- Report quiz section: `projects/user-journey-analysis/reports/user_journey_analysis_report.md`
- Confidence level: verified

## Evidence Ledger

| Claim | Evidence | Location | Public? | Confidence |
| --- | --- | --- | --- | --- |
| Raw sessions total 9,935. | Generated report. | `reports/user_journey_analysis_report.md` | yes | verified |
| Unique users total 1,350. | Generated report. | `reports/user_journey_analysis_report.md` | yes | verified |
| Subscription mix is 931 Annual, 376 Monthly, 43 Quarterly. | Generated report. | `reports/user_journey_analysis_report.md` | yes | verified |
| Strongest four-page pattern in the last-three-session view appears 49 times. | Generated report. | `reports/user_journey_analysis_report.md` | yes | verified |
| Dashboard reads Gold marts only. | Project report and architecture convention. | `reports/user_journey_analysis_report.md` | yes | verified |

## Delivered Artifacts

| Artifact | Purpose | Proof Location | Public? |
| --- | --- | --- | --- |
| Python journey helper functions | Required API behavior from the brief | `scripts/pipeline.py` | yes |
| DuckDB medallion pipeline | Reproducible data layers | `scripts/` | yes |
| Gold marts | Dashboard and quiz support | `warehouse.duckdb` generated locally; catalog lists marts | yes |
| Streamlit dashboard | Interactive journey exploration | `dashboard/app.py` | yes |
| Markdown report | Findings and quiz answers | `reports/user_journey_analysis_report.md` | yes |

## Technical Stack

- Languages: Python, SQL, Markdown
- Frameworks: Streamlit
- Databases: DuckDB
- Data tools: pandas, journey helper functions, quality checks
- Visualization: Streamlit and Plotly
- Testing: static compile, runtime pipeline checks, quality and quiz regression checks

### Stack Rationale

Python fits the brief-required path algorithms. DuckDB and Streamlit make the outputs reproducible and portfolio-friendly.

### Stack Limitations

The implementation is batch/local, not a real-time product analytics system. Session order depends on `session_id` ascending because no timestamp exists.

## Technical Decisions And Trade-Offs

| Decision | Options Considered | Choice Made | Trade-Off | Result |
| --- | --- | --- | --- | --- |
| Journey logic location | SQL arrays, pandas/Python lists, notebook only | Python helpers plus DuckDB marts | Mixed Python and SQL workflow | Clearer algorithms with reproducible outputs |
| Dashboard source | Raw CSV, Silver data, Gold marts | Gold marts only | Requires mart generation first | Safer and cleaner dashboard |
| Session order | no ordering, source order, `session_id` ascending | `session_id` ascending | Assumption because no timestamp exists | Deterministic grouped scenarios |

## Metrics And Outcomes

### Measured Local Outcomes

- Raw sessions: 9,935.
- Unique users: 1,350.
- Top all-session page after preprocessing: Homepage with 2,679 visits.
- Average all-session journey length after preprocessing: 10.4 pages.
- Most popular four-page last-three-session sequence count: 49.

### Unmeasured Outcomes

- No production product decisions, user behavior changes, or external stakeholder impact are measured.

## Retrospective Analysis

### Keep Doing

- Preserve brief-required public function contracts.
- Keep dashboards on modeled Gold data.
- Document assumptions like session ordering.

### More Of

- Add examples for each helper function in the docs.
- Add more scenario comparisons for stakeholders.

### Less Of

- Avoid embedding interpretation in helper functions; keep functions pure and reports interpretive.

### Start Doing

- Add small unit tests directly for the three public journey functions.

## Challenges, Mistakes, And Constraints

| Issue | What Happened | Impact | Response | Next Time |
| --- | --- | --- | --- | --- |
| No timestamp field | Session order was not explicit. | Journey grouping could be ambiguous. | Used `session_id` ascending and documented the assumption. | Confirm ordering from source owner when available. |
| Python-first brief in SQL-standard repo | Pure SQL would not fit required APIs. | Needed mixed implementation. | Kept Python functions and persisted outputs to DuckDB. | Define language boundaries before coding. |

## Risk Register

| Risk | Severity | What Reduced The Risk | What Remains |
| --- | --- | --- | --- |
| Session-order ambiguity | medium | Explicit `session_id` assumption | Real timestamp would be better |
| Overfitting to quiz answers | medium | Business report plus dashboard marts | More open-ended analysis could be added |
| Local-only demo | low | Streamlit run commands | No hosted proof yet |

## Proof Summary For Hiring Managers

- I delivered: a Python journey-analysis project with reusable functions, DuckDB marts, report, and dashboard.
- I was responsible for: preprocessing logic, metric generation, dashboard/report outputs, and verification.
- The hardest constraint was: preserving exact Python function behavior while fitting the repo-standard warehouse pattern.
- Strongest evidence: report metrics and required function implementation.
- I would improve: direct unit tests for helper functions and additional stakeholder-facing journey examples.

## Proof Summary For Recruiters

- Role fit: Product Analyst, Data Analyst, Analytics Engineer.
- Keywords: Python, pandas, user journeys, pathing, sequence analysis, DuckDB, Streamlit.
- Outcome: local reproducible journey analytics project with dashboard and quiz support.

## Proof Summary For Freelance Clients

- Client problem this resembles: understanding user paths before conversion.
- What I can deliver: journey metrics, page sequence analysis, dashboards, and repeatable reporting.
- What I will not overpromise: real-time tracking or production instrumentation without additional work.

## Resume Bullets

- Built a Python and DuckDB user journey analytics project over 9,935 sessions, producing reusable pathing functions, Gold marts, a Streamlit dashboard, and quiz-supported findings.
- Implemented page count, page presence, destination, N-page sequence, and journey-length metrics with documented session-order assumptions and reproducible reporting.

## LinkedIn Post Angle

- Main claim: I turned a Python journey-analysis brief into a reusable product analytics workflow.
- Non-obvious lesson: Some analytics logic belongs in Python, even inside a warehouse-standard repo.
- Concrete proof: 9,935 sessions, 1,350 users, required helper functions, and Gold-backed dashboard marts.

## Follow-Up Improvements

| Improvement | Why It Matters | Effort | Status |
| --- | --- | --- | --- |
| Add unit tests for helper functions | Protects the public API behavior. | low | planned |
| Add screenshots | Helps portfolio reviewers see the dashboard quickly. | low | planned |
| Add more scenario presets | Improves stakeholder exploration. | medium | planned |

## Final Retrospective Judgment

### What This Project Proves

It proves local product analytics, Python pathing algorithms, reproducible reporting, and dashboard delivery.

### What This Project Does Not Prove

It does not prove real-time tracking, production product analytics adoption, or external business impact.

### Strongest Evidence

The required helper functions and generated report metrics.

### Best Use Of This Retrospective

Interview story and portfolio case study.

## Detailed STAR-B Proof Addendum

This addendum expands the report into a fuller raw proof document, matching the deeper style expected for project-level portfolio retrospectives.

### Full Delivery Contract

**Inputs**

- `user_journey_raw.csv`: raw journey/session records from the 365DS source assets.
- Source brief: `project-instructions/User Journey Analysis in Python Project Instructions.md`.

**Required public functions**

- `remove_page_duplicates(data, target_column="user_journey")`
- `group_by(data, group_column="user_id", target_column="user_journey", sessions="All", count_from="last")`
- `remove_pages(data, pages, target_column="user_journey")`

**Required preprocessing order**

1. Group selected sessions.
2. Optionally remove selected pages.
3. Remove consecutive duplicate pages.

**Outputs**

- Gold marts for page count, page presence, page destinations, page sequences, journey length, summary KPIs, and quiz answers.
- Streamlit dashboard reading Gold marts only.
- Markdown business report with findings and quiz support.

**Verification**

- Raw row counts and user counts were checked during delivery.
- Required quiz answers were regression-checked.
- Cleaned journeys are expected to contain no consecutive duplicate pages after preprocessing.
- Dashboard follows the Gold-only contract.

**Known limits**

- Session ordering uses `session_id` ascending because no timestamp exists.
- The project is batch/local, not production event tracking.
- It analyzes provided journeys; it does not instrument a live website.

### Expanded Audience Fit

**Hiring manager**

This project is useful because it shows judgment about algorithmic analytics. User journeys are not just rows and joins; they require ordered sequences, duplicate handling, page removal rules, and scenario construction. The project also shows that Python-specific requirements can coexist with a warehouse/reporting workflow.

**Recruiter**

Recruiter keywords include product analytics, pathing, sequence analysis, Python, pandas, DuckDB, Streamlit, page destinations, page presence, conversion journeys, and subscription behavior.

**Freelance client**

This resembles a request from a product team asking, "What do users do before they subscribe? Which pages dominate journeys? Which page sequences repeat?" It can be framed as a lightweight product analytics deliverable.

**Wrong audience**

This is not a live clickstream system, Segment/Amplitude replacement, attribution platform, or real-time experimentation product.

### Expanded Evidence Ledger

| Claim | Evidence | Location | Public? | Confidence | Notes |
| --- | --- | --- | --- | --- | --- |
| Raw sessions total 9,935. | Generated report. | `reports/user_journey_analysis_report.md` | yes | verified | Local dataset metric. |
| Unique users total 1,350. | Generated report. | `reports/user_journey_analysis_report.md` | yes | verified | Local dataset metric. |
| Annual users total 931. | Generated report. | `reports/user_journey_analysis_report.md` | yes | verified | Part of subscription mix. |
| Monthly users total 376. | Generated report. | `reports/user_journey_analysis_report.md` | yes | verified | Part of subscription mix. |
| Quarterly users total 43. | Generated report. | `reports/user_journey_analysis_report.md` | yes | verified | Small segment; interpret carefully. |
| Average all-session journey length is 10.4 pages. | Generated report. | `reports/user_journey_analysis_report.md` | yes | verified | After preprocessing. |
| Strongest four-page last-three-session pattern appears 49 times. | Generated report. | `reports/user_journey_analysis_report.md` | yes | verified | Count each sequence only once per journey. |
| Session order depends on an assumption. | Report notes. | `reports/user_journey_analysis_report.md` | yes | verified | Uses `session_id` ascending because no timestamp exists. |

### Detailed Delivery Timeline

| Phase | What Happened | Key Decision | Evidence |
| --- | --- | --- | --- |
| Discovery | Read the Python journey brief and source fields. | Preserve required function signatures. | Source brief |
| Modeling | Defined journey scenarios for all sessions and selected first/last sessions. | Keep journey algorithms in Python. | `scripts/` |
| Warehouse | Persisted scenario outputs to DuckDB Gold marts. | Dashboard and quiz answers should read modeled outputs. | Catalog and report |
| Dashboard | Built Streamlit filters for scenario, plan, page, and sequence length. | Keep UI exploratory but Gold-only. | `dashboard/app.py` |
| Reporting | Generated business findings and quiz answers. | Document session-order assumption. | `reports/user_journey_analysis_report.md` |
| Retrospective | Wrote proof report for product analytics and portfolio use. | Make limitations explicit. | this file |

### Detailed Interview Answer Bank

**Tell me about a project you delivered**

I built a User Journey Analysis project that analyzes page paths for 1,350 users and 9,935 raw sessions. The implementation keeps the required Python APIs while producing DuckDB Gold marts and a Streamlit dashboard for page counts, destinations, sequences, page presence, and journey length.

**Tell me about a technical trade-off**

The trade-off was Python versus SQL. Since journey paths are ordered lists and the brief required public Python functions, I kept the journey algorithms in Python. I used DuckDB for reproducible marts and dashboard outputs instead of forcing everything into SQL.

**Tell me about a time something could have gone wrong**

Session ordering could have been ambiguous because there was no timestamp. I made the ordering assumption explicit: `session_id` ascending. That makes the result reproducible and honest.

**Tell me about ambiguity**

The phrase "user journey" can mean many things: page views, sessions, paths, conversion funnels, or attribution. I narrowed the scope to the source data and brief: grouped journeys, optional page removal, duplicate removal, and sequence metrics.

**Tell me about a measurable result**

The project found 9,935 sessions, 1,350 users, Homepage as the top all-session page after preprocessing with 2,679 visits, and a strongest last-three-session four-page sequence appearing 49 times.

### Public Version Notes

**Safe to share**

- Project objective, required functions, journey metrics, dashboard screenshots, and report findings.

**Must redact**

- No secrets are involved, but public paths should be converted to repo-relative paths.

**Needs permission**

- Any claim that a real product team used the results.

**Can be generalized**

- The project can be described as "subscription product journey analysis" for portfolio pages.

### Claim Safety Checklist

- Every metric comes from the generated report.
- The session-order assumption is disclosed.
- No production instrumentation is claimed.
- No conversion lift is claimed.
- Quarterly segment conclusions are not overstated because that segment is small.
- The dashboard is described as local, not hosted production BI.

### Detailed Follow-Up Backlog

| Improvement | Why It Matters | Effort | Owner | Status |
| --- | --- | --- | --- | --- |
| Add direct unit tests for the three public functions | Protects the course-required API behavior. | low | self | planned |
| Add dashboard screenshots | Makes the pathing story easier to review. | low | self | planned |
| Add a glossary of journey metrics | Helps non-technical readers. | low | self | planned |
| Add timestamp-aware version if data becomes available | Removes the session-order assumption. | medium | self | deferred |
| Add conversion-focused funnel view | Makes the dashboard more stakeholder-ready. | medium | self | planned |

### One-Page Version

**Project:** User Journey Analysis.

**Problem:** A Python brief required analysis of user paths across subscription-plan journeys.

**Delivered:** Required Python journey functions, DuckDB medallion pipeline, Gold marts, Streamlit dashboard, and Markdown report.

**My role:** End-to-end local product analytics implementation.

**STAR-B summary:** The situation was a pathing-analysis brief with required Python APIs. The task was to preserve those APIs while making the outputs reproducible. The action was to implement journey functions, create scenario marts, and build a Gold-backed dashboard. The result was verified metrics over 9,935 sessions and 1,350 users. The bridge is that this proves product analytics and algorithmic preprocessing judgment.

**Evidence:** `scripts/`, `dashboard/app.py`, `reports/user_journey_analysis_report.md`, and catalog Gold table entries.

**Trade-off:** Python for ordered path logic, DuckDB for reproducible reporting.

**Lesson:** Not every analytics transformation should be forced into SQL; the right boundary matters.

**Relevance:** Useful for Product Analyst, Data Analyst, Analytics Engineer, and customer journey analysis work.

## Raw Template Completion Notes

This section is intentionally detailed. It is meant to preserve material for later public editing, not to be the final public case study.

### Delivered Artifacts In Detail

| Artifact | Purpose | My Contribution | Proof Location | Public? |
| --- | --- | --- | --- | --- |
| Raw data contract | Preserve the source user journey rows. | Kept source data immutable and loaded it through the project pipeline. | `source-datasets/`, `scripts/` | yes |
| Public journey functions | Satisfy the Python brief and create reusable preprocessing tools. | Implemented grouping, page removal, and duplicate-page cleanup behavior. | `scripts/pipeline.py` | yes |
| Scenario construction | Compare all sessions, first sessions, and last sessions. | Modeled journey scenarios as repeatable outputs. | `scripts/` | yes |
| Gold marts | Support dashboard and quiz questions. | Created marts for page counts, presence, destinations, sequences, length, KPIs, and quiz answers. | generated DuckDB warehouse and catalog | yes |
| Dashboard | Let reviewers explore journey scenarios. | Built Streamlit views over Gold marts. | `dashboard/app.py` | yes |
| Report | Summarize metrics, findings, and quiz answers. | Generated Markdown report. | `reports/user_journey_analysis_report.md` | yes |
| Retrospective | Turn project into interview/portfolio proof. | Wrote this transparent proof document. | this file | yes |

### Technical Stack Detail

- Languages: Python, SQL, Markdown.
- Frameworks: Streamlit.
- Database: DuckDB.
- Data tools: pandas-style journey manipulation, ordered sequence logic, local quality checks.
- Visualization: Streamlit dashboard charts and tables.
- Testing approach: static compile, runtime pipeline, quality assertions, quiz regression checks.
- CI/CD: none; local project verification only.
- Monitoring: none; not a production app.

### Technical Decisions And Trade-Offs In Detail

| Decision | Options Considered | Choice Made | Why | Trade-Off | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| Journey algorithm location | SQL string functions, Python list processing, notebook-only | Python list/session helpers | The brief required Python functions and ordered path logic is clearer in Python. | Mixed language workflow | Clear functions plus reproducible marts | `scripts/pipeline.py` |
| Scenario storage | Recompute in dashboard, store intermediate outputs, store Gold marts | Store Gold marts | Dashboard should be a reader, not a transformation engine. | Requires pipeline run first | Cleaner dashboard and Learning Hub compatibility | dashboard/report |
| Session order | Source file order, no ordering, `session_id` ascending | `session_id` ascending | No timestamp exists. | Assumption must be disclosed | Deterministic output | report notes |
| Sequence counting | Count every occurrence, count once per journey | Count each sequence once per grouped journey | Matches brief requirement. | Requires careful implementation | Quiz answer support | report quiz section |

### Metrics And Outcomes In Detail

Measured local outcomes:

- Raw sessions: 9,935.
- Unique users: 1,350.
- Annual users: 931.
- Monthly users: 376.
- Quarterly users: 43.
- Top all-session page after preprocessing: Homepage, 2,679 visits.
- Average all-session journey length after preprocessing: 10.4 pages.
- Average last-three-session journey length: 3.6 pages.
- Most popular four-page sequence count in last-three-session view: 49.

Qualitative outcomes:

- The project is easier to explain because the required functions, marts, dashboard, and report are separate artifacts.
- The dashboard can support both learning review and portfolio walkthrough.
- The report preserves quiz answers without hiding assumptions.

Unmeasured outcomes:

- No conversion improvement is measured.
- No product team adoption is measured.
- No live user instrumentation is implemented.

Honest phrasing:

- "This project models journey behavior from a provided dataset."
- Do not say "I improved conversion" or "I instrumented user behavior."

### Challenges, Mistakes, And Constraints In Detail

Real constraints:

- No timestamp field exists, so session ordering needs an assumption.
- The Quarterly segment is small, so plan-level findings need caution.
- The brief requires Python APIs, so a pure SQL standard would be inappropriate.
- The project is local and batch-oriented.

Blameless system notes:

- The source data shape controls how much behavioral interpretation is possible.
- The project can explain paths in the dataset, but it cannot explain user intent without more context.

Mistakes or weak spots:

| Issue | What Happened | Impact | What I Did | What I Would Do Next Time |
| --- | --- | --- | --- | --- |
| Session order assumption | No timestamp was available. | Could affect grouped journey scenarios. | Used `session_id` ascending and documented it. | Ask for event timestamps or ingestion order metadata. |
| Small plan segment | Quarterly users are only 43. | Findings can be noisy. | Kept conclusions descriptive. | Add confidence/context notes to dashboard. |
| Function tests could be stronger | The project has regression checks, but direct unit tests would help. | Public APIs have less isolated proof. | Recorded follow-up. | Add direct tests for each public helper. |

### Strong Public Case Study Shape

1. Start with the product question: "What paths do users take before and around subscription?"
2. Show the three required Python functions as the technical hook.
3. Show how raw journeys become Gold marts.
4. Show dashboard screenshots for page counts, destinations, and sequences.
5. Close with limitations: no timestamp, local batch analysis, no conversion claim.

### Additional Interview Prompts

**How did you avoid overengineering?**

I kept the complex part in Python functions because the brief needed that, then used DuckDB only to persist reusable reporting marts. I did not introduce orchestration services or a production tracker.

**How would you productionize it?**

I would add timestamped event ingestion, identity resolution, event schema validation, scheduled transformations, dashboard deployment, and a stricter metrics layer.

**What would you test next?**

I would add unit tests for `remove_pages`, `group_by`, and `remove_page_duplicates`, especially around empty journeys, repeated pages, and first/last session limits.

### Claim Safety Checklist Addendum

- Do not imply live website instrumentation.
- Do not imply sequence counts are causal.
- Do not imply small Quarterly-plan patterns generalize to all users.
- Do not omit the session-order assumption in public writeups.
- Do not publish screenshots without checking they show only project/demo data.
