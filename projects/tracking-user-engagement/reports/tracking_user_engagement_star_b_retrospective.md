# Tracking User Engagement STAR-B Retrospective

This is the STAR-B retrospective for `projects/tracking-user-engagement` inside the 365DS demo projects workspace.

Working title: **Engagement Statistics And Prediction Warehouse Retrospective**

The project started from a 365 Data Science SQL, Excel, and Python brief. The delivered local implementation translates the SQL and Excel tasks into a SQL-first DuckDB medallion pipeline with Python statistical/model Gold outputs, a Streamlit dashboard, and a generated Markdown report.

## Project Metadata

- Project name: Tracking User Engagement
- Project type: 365DS SQL/Excel/Python project implementation and retrospective proof artifact
- Domain: online education engagement, paid/free cohorts, statistical comparison, certificate prediction
- Source brief: `project-instructions/Tracking User Engagement with SQL, Excel, and Python Project Instructions.md`
- Source dataset: `source-datasets/Tracking User Engagement With SQL Excel And Python/data_scientist_project.sql`
- Delivered project path: `projects/tracking-user-engagement/`
- Delivery status: local implementation exists; retrospective added after implementation
- Current status: internal proof document, not a public case study yet
- Primary stack: SQL, Python, pandas, DuckDB, Streamlit, scipy/statsmodels/sklearn style statistics, Markdown
- Public link: not published
- Demo link: local dashboard only
- External stakeholder validation: not claimed

## Transparency Statement

This retrospective is an internal proof record. It separates verified local artifacts from judgment, estimated value, and unproven external outcomes.

Verified local evidence:

- The implementation exists under `projects/tracking-user-engagement/`.
- The generated report states Q2 watched-student records increased from 7,639 in 2021 to 8,841 in 2022.
- The report states free-plan filtered average minutes increased from 14.21 to 16.04.
- The report states paid filtered average minutes decreased from 360.10 to 292.22.
- The report states correlation 0.5126, regression R-squared 0.4678, and a rounded 1,200-minute prediction of 4 certificates.

Not claimed:

- No actual platform feature impact is proven.
- No production model deployment is claimed.
- No Excel workbook is committed as the deliverable.
- No external stakeholder validation is claimed.

Honest framing:

> This project proves local statistical analytics and reproducible modeling outputs. It does not prove production prediction accuracy or causal product impact.

## Audience Fit

### Hiring Manager Signal

This project shows the ability to combine SQL cohorting, outlier handling, confidence intervals, t-tests, correlation, regression, probability calculations, dashboarding, and clear interpretation in one reproducible workflow.

### Recruiter Signal

Recruiter-visible keywords and skills:

- SQL
- Python
- DuckDB
- statistical analysis
- hypothesis testing
- confidence intervals
- linear regression
- paid/free cohort analysis
- Streamlit
- data quality

### Freelance Client Signal

This resembles a client request to compare engagement before and after product changes, understand paid/free behavior, and build a simple predictive signal from learning activity.

### Wrong Audience To Filter Out

This is not a production ML system, experiment platform, or causal inference study.

## Executive Summary

- Problem: The brief needed Q2 2021 versus Q2 2022 engagement comparison, paid/free segmentation, statistics, and certificate prediction.
- Delivered solution: SQL-first DuckDB pipeline plus Python-generated statistical and regression Gold marts, Streamlit dashboard, and Markdown report.
- Role: end-to-end local analytics, statistics, modeling, and dashboard implementation.
- Main constraint: translate Excel tasks into reproducible Python and Gold tables while preserving course logic.
- Most important decision: keep relational cohort work in SQL and statistical/model outputs in Python.
- Outcome: the project reports engagement shifts, t-tests, confidence intervals, certificate correlation, regression, and quiz support.
- Evidence: `projects/tracking-user-engagement/reports/tracking_user_engagement_report.md`
- Main lesson: statistical dashboards need clear boundaries between descriptive output, hypothesis testing, and predictive interpretation.

## Delivery Context

### Situation

The course project mixed SQL, Excel, and Python. The repo needed a reproducible implementation that avoided manual spreadsheet artifacts while preserving the analytical steps.

### Task

The project needed to:

- load the MySQL-style source dump into DuckDB;
- handle multi-block inserts;
- create refund-aware subscription windows;
- build Q2 2021 and Q2 2022 paid/free cohorts;
- apply 99th percentile outlier filtering;
- generate means, medians, confidence intervals, t-tests, correlation, regression, probabilities, and quiz answers;
- present the findings in a Gold-backed Streamlit dashboard.

### Scope Boundaries

Included:

- SQL-first medallion layers;
- Python statistical/model outputs;
- Gold marts and dashboard;
- report and quiz support.

Excluded:

- committed Excel workbook;
- production ML serving;
- causal experiment design;
- long-term model monitoring.

## STAR-B Story Bank

### STAR-B Story 1: Main Delivery Story

**Situation**

The brief asked whether engagement changed between Q2 2021 and Q2 2022 and whether paid/free student behavior differed.

**Task**

Build a reproducible workflow that calculates cohorts, statistics, hypothesis tests, and certificate prediction outputs.

**Action**

Loaded source data into DuckDB, modeled subscription windows, created Q2 watched-minute cohorts, split paid/free segments, filtered outliers at the 99th percentile, generated statistical marts, fit a simple certificate regression, and built a Streamlit dashboard.

**Result**

The report shows Q2 watcher records increasing from 7,639 to 8,841, free-plan average minutes rising after filtering, paid average minutes declining, and regression R-squared of 0.4678.

**Bridge**

This proves statistical analytics and reproducible model-supporting data workflows.

**Evidence**

- Repo artifact: `projects/tracking-user-engagement/`
- Report: `projects/tracking-user-engagement/reports/tracking_user_engagement_report.md`
- Dashboard: `projects/tracking-user-engagement/dashboard/app.py`
- Confidence level: verified

### STAR-B Story 2: Technical Decision Story

**Situation**

The project had both relational transformations and statistical/modeling tasks.

**Task**

Choose a boundary that kept SQL readable and Python appropriate.

**Action**

Used SQL for Bronze, Silver, cohorting, and relational Gold tables, then used Python for confidence intervals, t-tests, correlation, regression, probability, and report generation.

**Result**

The implementation keeps warehouse lineage while avoiding awkward SQL-only statistical code.

**Bridge**

This proves pragmatic analytics engineering across SQL and Python.

**Evidence**

- README: `projects/tracking-user-engagement/README.md`
- Report: `reports/tracking_user_engagement_report.md`
- Confidence level: verified

### STAR-B Story 3: Constraint Or Failure Story

**Situation**

The source dump used multiple `INSERT` blocks for large tables, and the original brief expected Excel calculations.

**Task**

Avoid incomplete ingestion and avoid manual spreadsheet-only outputs.

**Action**

Used the multi-block parser pattern, validated expected row counts during delivery, and translated Excel calculations into reproducible Python/Gold marts.

**Result**

The project produced repeatable statistical outputs and dashboard views without committing a workbook.

**Bridge**

This proves repeatability and quality control over manual analysis.

**Evidence**

- Memory: `docs/agent-memory/current-thread-memory.md`
- Report notes: `reports/tracking_user_engagement_report.md`
- Confidence level: verified

## Evidence Ledger

| Claim | Evidence | Location | Public? | Confidence |
| --- | --- | --- | --- | --- |
| Q2 watched records increased from 7,639 to 8,841. | Generated report. | `reports/tracking_user_engagement_report.md` | yes | verified |
| Free-plan filtered average minutes increased from 14.21 to 16.04. | Generated report. | `reports/tracking_user_engagement_report.md` | yes | verified |
| Paid filtered average minutes decreased from 360.10 to 292.22. | Generated report. | `reports/tracking_user_engagement_report.md` | yes | verified |
| Correlation is 0.5126. | Generated report. | `reports/tracking_user_engagement_report.md` | yes | verified |
| Regression R-squared is 0.4678. | Generated report. | `reports/tracking_user_engagement_report.md` | yes | verified |
| 1,200 watched minutes predicts 4 certificates after rounding up. | Generated report. | `reports/tracking_user_engagement_report.md` | yes | verified |

## Delivered Artifacts

| Artifact | Purpose | Proof Location | Public? |
| --- | --- | --- | --- |
| SQL medallion pipeline | Reproducible warehouse layers | `scripts/` | yes |
| Q2 cohort marts | Paid/free engagement comparison | Gold catalog and generated warehouse | yes |
| Statistical Gold marts | Means, medians, confidence intervals, t-tests | `scripts/gold/` | yes |
| Regression outputs | Certificate prediction support | Gold marts and report | yes |
| Streamlit dashboard | Interactive statistical story | `dashboard/app.py` | yes |
| Markdown report | Findings, recommendations, quiz support | `reports/tracking_user_engagement_report.md` | yes |

## Technical Stack

- Languages: SQL, Python, Markdown
- Frameworks: Streamlit
- Databases: DuckDB
- Data tools: pandas, statistical tests, linear regression
- Visualization: Streamlit and Plotly
- Testing: row counts, cohort counts, outlier counts, correlation/regression checks, dashboard Gold-only convention

### Stack Rationale

SQL handles cohorting and warehouse lineage. Python handles statistics and modeling. DuckDB keeps the project local and reproducible.

### Stack Limitations

The regression is a simple local model, not a production predictor. The statistical comparison is not a causal experiment.

## Technical Decisions And Trade-Offs

| Decision | Options Considered | Choice Made | Trade-Off | Result |
| --- | --- | --- | --- | --- |
| Excel translation | Commit workbook, manual calculations, Python/Gold outputs | Python/Gold outputs | Less like the original Excel surface | More reproducible |
| Statistics location | SQL-only, Python-only, mixed | SQL cohorts plus Python stats | Mixed workflow | Clearer statistical code |
| Outlier handling | No filter, global filter, segment 99th percentile | Segment 99th percentile below-threshold filter | More logic to validate | Matches brief |
| Prediction model | Omit model, complex ML, simple regression | Simple linear regression | Limited predictive power | Transparent quiz support |

## Metrics And Outcomes

### Measured Local Outcomes

- Q2 watched-student records: 7,639 in 2021 and 8,841 in 2022.
- Free-plan filtered average minutes: 14.21 to 16.04.
- Paid filtered average minutes: 360.10 to 292.22.
- Conditional probability `P(watched Q2 2021 | watched Q2 2022)`: about 7.24%.
- Correlation: 0.5126.
- Regression R-squared: 0.4678.
- 1,200-minute certificate prediction: 4 after rounding up.

### Unmeasured Outcomes

- No production prediction accuracy, learner behavior change, or causal feature impact is measured.

## Retrospective Analysis

### Keep Doing

- Translate spreadsheet work into reproducible code when portfolio proof matters.
- Keep statistical assumptions visible.
- Separate descriptive and predictive conclusions.

### More Of

- Add explanatory charts for confidence intervals and t-tests.
- Add model limitations directly to the dashboard.

### Less Of

- Avoid implying product features caused engagement change without experimental evidence.

### Start Doing

- Add a model card for the certificate regression if the project is published.

## Challenges, Mistakes, And Constraints

| Issue | What Happened | Impact | Response | Next Time |
| --- | --- | --- | --- | --- |
| SQL/Excel/Python mixed brief | Deliverable could become fragmented. | Risk of manual-only output. | Translated Excel tasks into Python/Gold marts. | Define outputs before implementing stats. |
| Multi-block SQL source | Large tables required robust parsing. | Ingestion risk. | Used multi-block parser pattern and validation. | Add parser fixtures. |
| Prediction interpretation | Regression output can be overread. | Risk of overstating model value. | Report calls it directional and recommends more features. | Add model card. |

## Risk Register

| Risk | Severity | What Reduced The Risk | What Remains |
| --- | --- | --- | --- |
| Causal overclaim | high | Report language and recommendations | No experiment |
| Model overclaim | medium | R-squared and limitation notes | No production validation |
| Parser drift | medium | Multi-block support and checks | More fixture tests |

## Proof Summary For Hiring Managers

- I delivered: a reproducible SQL/Python statistical engagement project with dashboard and report.
- I was responsible for: source loading, cohorting, outlier handling, tests, stats, regression, dashboard, and quiz support.
- The hardest constraint was: converting mixed SQL/Excel/Python tasks into one repeatable workflow.
- Strongest evidence: statistical report metrics and Gold-backed dashboard.
- I would improve: model card, parser fixtures, and dashboard explanatory annotations.

## Proof Summary For Recruiters

- Role fit: Data Analyst, Analytics Engineer, Product Analyst.
- Keywords: SQL, Python, DuckDB, hypothesis testing, confidence intervals, regression, Streamlit.
- Outcome: reproducible engagement comparison and prediction-support dashboard.

## Proof Summary For Freelance Clients

- Client problem this resembles: comparing engagement across time periods and customer segments.
- What I can deliver: cohort tables, statistical tests, dashboards, and cautious recommendations.
- What I will not overpromise: causal lift or production prediction without further validation.

## Resume Bullets

- Built a SQL/Python engagement analytics project in DuckDB and Streamlit, comparing Q2 2021 and Q2 2022 paid/free cohorts with outlier filtering, confidence intervals, t-tests, and dashboard reporting.
- Produced certificate prediction support with correlation 0.5126, regression R-squared 0.4678, and documented limitations around causal and predictive interpretation.

## LinkedIn Post Angle

- Main claim: I converted an SQL/Excel/Python engagement brief into reproducible analytics.
- Non-obvious lesson: Excel-style statistical work becomes stronger when it is represented as Gold marts and code.
- Concrete proof: Q2 cohorts, t-tests, correlation, regression, and dashboard outputs.

## Follow-Up Improvements

| Improvement | Why It Matters | Effort | Status |
| --- | --- | --- | --- |
| Add a regression model card | Prevents overclaiming model usefulness. | low | planned |
| Add parser fixtures | Protects ingestion. | medium | planned |
| Add dashboard screenshots | Improves portfolio readability. | low | planned |
| Add richer model features | Improves prediction proof. | medium | planned |

## Final Retrospective Judgment

### What This Project Proves

It proves SQL/Python statistical analytics, cohort modeling, reproducible spreadsheet translation, and dashboard/report delivery.

### What This Project Does Not Prove

It does not prove causal product impact, production ML deployment, or external user adoption.

### Strongest Evidence

The generated statistical report and Gold-backed dashboard.

### Best Use Of This Retrospective

Interview story and portfolio case study.

## Detailed STAR-B Proof Addendum

This addendum expands the report into a fuller proof document, with more explicit treatment of statistical interpretation, Excel translation, and production-claim safety.

### Full Delivery Contract

**Inputs**

- `data_scientist_project.sql`: MySQL-style source dump.
- Source brief: `project-instructions/Tracking User Engagement with SQL, Excel, and Python Project Instructions.md`.

**Transformations**

- Bronze loads student certificates, student info, purchases, and watched-video data.
- Silver creates refund-aware subscription windows, Q2 watched-minute aggregates, paid/free segment flags, and certificate-minute extracts.
- Gold creates raw and outlier-filtered engagement marts, segment statistics, hypothesis tests, certificate correlation, regression outputs, watch probability, summary KPIs, and quiz answers.
- Python handles statistical and regression outputs where that is clearer and more faithful to the brief than SQL-only implementation.

**Outputs**

- Generated local DuckDB warehouse.
- Streamlit dashboard for Q2 comparison, distributions/outliers, hypothesis tests, probability, and certificate prediction.
- Markdown report with findings, recommendations, limitations, and quiz support.

**Verification**

- Bronze row counts and multi-block parsing were validated during delivery.
- Q2 watcher counts and paid/free splits were checked.
- 99th percentile filtered row counts were checked.
- Correlation, regression R-squared, and prediction values were checked.

**Known limits**

- The statistical tests are local analysis, not a causal experiment.
- The regression is simple and directional, not production ML.
- No actual platform feature impact is proven.

### Expanded Audience Fit

**Hiring manager**

This project is strong evidence for analytics work that crosses SQL, Python, and statistics. It shows data loading, cohort definition, subscription-window logic, outlier handling, confidence intervals, t-tests, correlation, regression, probability, dashboarding, and cautious interpretation.

**Recruiter**

Recruiter keywords include SQL, Python, DuckDB, Streamlit, hypothesis testing, confidence intervals, t-tests, linear regression, cohort analysis, paid/free segmentation, and statistical reporting.

**Freelance client**

This resembles a client asking, "Did engagement change after product updates, and how do paid and free users differ?" It can support a cautious evidence report and dashboard, not a causal claim by itself.

**Wrong audience**

This is not a production ML deployment, feature experimentation platform, or causal inference system.

### Expanded Evidence Ledger

| Claim | Evidence | Location | Public? | Confidence | Notes |
| --- | --- | --- | --- | --- | --- |
| Q2 watched records increased from 7,639 to 8,841. | Generated report. | `reports/tracking_user_engagement_report.md` | yes | verified | Local data output. |
| Free-plan filtered average minutes increased from 14.21 to 16.04. | Generated report. | `reports/tracking_user_engagement_report.md` | yes | verified | Descriptive/statistical output. |
| Paid filtered average minutes decreased from 360.10 to 292.22. | Generated report. | `reports/tracking_user_engagement_report.md` | yes | verified | Descriptive/statistical output. |
| Free-plan t-test statistic is -3.9512. | Generated report. | `reports/tracking_user_engagement_report.md` | yes | verified | Interpreted by report. |
| Paid t-test statistic is 5.1544. | Generated report. | `reports/tracking_user_engagement_report.md` | yes | verified | Interpreted by report. |
| Correlation is 0.5126. | Generated report. | `reports/tracking_user_engagement_report.md` | yes | verified | Moderate positive relationship. |
| Regression R-squared is 0.4678. | Generated report. | `reports/tracking_user_engagement_report.md` | yes | verified | Simple model only. |
| A 1,200-minute learner is predicted to earn 4 certificates after rounding up. | Generated report. | `reports/tracking_user_engagement_report.md` | yes | verified | Directional prediction. |
| No causal feature impact is proven. | No experiment design exists. | n/a | yes | verified | Must be retained in public framing. |

### Detailed Delivery Timeline

| Phase | What Happened | Key Decision | Evidence |
| --- | --- | --- | --- |
| Discovery | Read SQL/Excel/Python brief and source dump. | Translate Excel tasks into reproducible Python/Gold outputs. | README and report |
| Ingestion | Parsed MySQL-style dump with multi-block support. | Validate row counts before analysis. | Memory and scripts |
| Cohorting | Built Q2 2021 and Q2 2022 watched-minute tables. | Use subscription overlap to determine paid/free flags. | Silver/Gold scripts |
| Statistics | Built outlier-filtered datasets, confidence intervals, and t-tests. | Follow brief's 99th percentile filter rule. | Report and Gold marts |
| Prediction | Built certificate correlation and simple regression. | Keep interpretation directional. | Report |
| Dashboard | Built Streamlit pages for Q2 comparison, stats, and prediction. | Gold-only dashboard contract. | `dashboard/app.py` |
| Retrospective | Wrote proof report. | Avoid causal or production ML overclaims. | this file |

### Detailed Interview Answer Bank

**Tell me about a project you delivered**

I delivered a Tracking User Engagement project that compares Q2 2021 and Q2 2022 engagement across paid and free segments. I built SQL cohort tables, outlier-filtered datasets, confidence intervals, t-tests, certificate correlation, a regression output, a dashboard, and a report.

**Tell me about a technical trade-off**

The key trade-off was SQL versus Python. I used SQL for relational cohorting and subscription-window logic, then Python for statistical tests and regression. That kept the warehouse lineage clear while avoiding awkward SQL-only statistics.

**Tell me about a time something could be overclaimed**

The analysis compares engagement before and after platform additions, but it is not a controlled experiment. I framed the result as evidence of engagement differences, not proof that features caused those differences.

**Tell me about ambiguity**

The brief mixed SQL, Excel, and Python. I turned the Excel pieces into reproducible Python/Gold outputs so the work could be rerun and inspected without manual spreadsheet steps.

**Tell me about a measurable result**

The project found Q2 watched records increasing from 7,639 to 8,841, free-plan filtered average minutes increasing from 14.21 to 16.04, correlation of 0.5126 between minutes and certificates, and regression R-squared of 0.4678.

### Public Version Notes

**Safe to share**

- Cohort metrics, statistical outputs, model limitations, dashboard screenshots, and reproducibility story.

**Must redact**

- Local absolute paths in public copy.

**Needs permission**

- Any claim about actual 365DS platform impact or stakeholder use.

**Can be generalized**

- The project can be described as "Q2 engagement comparison and certificate prediction analysis."

### Claim Safety Checklist

- Every metric comes from the generated report.
- The regression is not described as production ML.
- The Q2 comparison is not described as causal proof.
- Excel is described as translated into reproducible outputs, not delivered as a workbook.
- The 99th percentile rule is stated clearly.
- The local dashboard is not described as hosted.

### Detailed Follow-Up Backlog

| Improvement | Why It Matters | Effort | Owner | Status |
| --- | --- | --- | --- | --- |
| Add model card | Prevents overclaiming prediction usefulness. | low | self | planned |
| Add causal-design note | Clarifies what would be needed to prove feature impact. | low | self | planned |
| Add parser fixtures | Protects SQL dump ingestion. | medium | self | planned |
| Add dashboard screenshots | Makes statistical story easier to scan. | low | self | planned |
| Add richer features for prediction | Improves model quality if prediction becomes a real goal. | medium | self | deferred |

### One-Page Version

**Project:** Tracking User Engagement.

**Problem:** A SQL/Excel/Python brief needed Q2 engagement comparison, paid/free segmentation, statistical testing, and certificate prediction.

**Delivered:** SQL-first DuckDB pipeline, Python statistical Gold outputs, Streamlit dashboard, and Markdown report.

**My role:** End-to-end analytics engineer, statistical analyst, and dashboard builder.

**STAR-B summary:** The situation was a mixed-tool engagement brief. The task was to make it reproducible. The action was to load the source dump, create cohorts, calculate stats, generate regression outputs, and build a dashboard. The result was verified Q2 comparisons, t-tests, correlation 0.5126, R-squared 0.4678, and a 4-certificate prediction for 1,200 watched minutes. The bridge is that this proves SQL/Python statistical analytics while preserving interpretation limits.

**Evidence:** `README.md`, `scripts/`, `dashboard/app.py`, and `reports/tracking_user_engagement_report.md`.

**Trade-off:** Reproducible Python/Gold outputs replaced manual Excel artifacts.

**Lesson:** Statistical portfolio projects need explicit limits around causality and prediction.

**Relevance:** Useful for Data Analyst, Analytics Engineer, Product Analyst, and statistical reporting work.

## Raw Template Completion Notes

This section preserves the deeper internal proof material needed for interviews and later public editing.

### Delivered Artifacts In Detail

| Artifact | Purpose | My Contribution | Proof Location | Public? |
| --- | --- | --- | --- | --- |
| SQL dump ingestion | Preserve raw student, purchase, watch, and certificate data. | Loaded source tables into DuckDB Bronze. | `scripts/bronze/` | yes |
| Refund-aware purchase model | Determine subscription windows correctly. | Modeled `date_start`, `date_end`, refund override, and plan behavior. | `scripts/silver/` | yes |
| Q2 watched cohorts | Compare Q2 2021 and Q2 2022 engagement. | Built cohort tables and paid/free flags. | `scripts/silver/`, `scripts/gold/` | yes |
| Statistical outputs | Support confidence intervals and hypothesis tests. | Generated means, medians, intervals, and t-test marts. | `scripts/gold/` | yes |
| Prediction outputs | Support certificate prediction section. | Generated correlation and regression marts. | `scripts/gold/`, report | yes |
| Streamlit dashboard | Present engagement, statistics, and prediction views. | Built dashboard over Gold marts. | `dashboard/app.py` | yes |
| Markdown report | Summarize findings, recommendations, and quiz support. | Generated report with statistical interpretation. | `reports/tracking_user_engagement_report.md` | yes |
| Retrospective | Convert delivery into proof. | Wrote this STAR-B report. | this file | yes |

### Technical Stack Detail

- Languages: SQL, Python, Markdown.
- Frameworks: Streamlit.
- Database: DuckDB.
- Source format: MySQL SQL dump.
- Data tools: pandas-style statistics, t-tests, confidence intervals, linear regression.
- Visualization: Streamlit dashboard.
- Testing approach: Bronze row counts, Q2 watcher counts, paid/free split counts, outlier-filtered row counts, correlation, R-squared, prediction, dashboard Gold-only convention.
- CI/CD: none; local verification only.
- Monitoring: none; not a production statistical service.

### Technical Decisions And Trade-Offs In Detail

| Decision | Options Considered | Choice Made | Why | Trade-Off | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| Excel output | Commit workbook, manual calculations, reproducible Python/Gold | Python/Gold outputs | Repeatability matters more than matching the spreadsheet surface. | Less Excel-like artifact. | Reproducible stats. | README/report |
| Statistics location | SQL-only, Python-only, mixed | SQL cohorts plus Python statistics | Keeps cohort logic relational and stats readable. | Mixed stack. | Clearer code and lineage. | scripts |
| Outlier rule | No filter, global 99th percentile, segment 99th percentile | Segment-specific 99th percentile below-threshold filter | Matches brief logic. | More validation needed. | Quiz-supporting outputs. | report |
| Prediction model | Complex ML, omit, simple regression | Simple regression | Fits project scope and quiz. | Limited predictive power. | Transparent model output. | report |

### Metrics And Outcomes In Detail

Measured local outcomes:

- Q2 watched-student records: 7,639 in 2021 and 8,841 in 2022.
- Free-plan filtered average minutes: 14.21 to 16.04.
- Paid filtered average minutes: 360.10 to 292.22.
- Free-plan t-test statistic: -3.9512.
- Paid t-test statistic: 5.1544.
- Correlation between minutes watched and certificates issued: 0.5126.
- Linear regression R-squared: 0.4678.
- 1,200-minute learner prediction: 4 certificates after rounding up.
- Conditional probability `P(watched Q2 2021 | watched Q2 2022)`: about 7.24%.

Qualitative outcomes:

- The project translates spreadsheet-style work into auditable outputs.
- The report separates statistical findings from product recommendations.
- The dashboard can support a walkthrough of both cohorts and model limitations.

Unmeasured outcomes:

- No causal feature impact is measured.
- No production prediction performance is measured.
- No learner intervention or retention change is measured.

Honest phrasing:

- "The analysis suggests engagement differences in the provided data."
- Do not say "new platform features caused the change."
- Do not say "the model predicts certificates in production."

### Challenges, Mistakes, And Constraints In Detail

Real constraints:

- Mixed SQL, Excel, and Python brief.
- Multi-block source dump.
- Outlier handling must match the brief.
- Statistical results can be easy to overstate.
- Regression has limited explanatory power.

Blameless system notes:

- A learning project can ask causal-sounding questions without providing experiment design. The implementation must state that limitation clearly.

Mistakes or weak spots:

| Issue | What Happened | Impact | What I Did | What I Would Do Next Time |
| --- | --- | --- | --- | --- |
| Causal interpretation risk | Q2 comparison could sound like feature causality. | Overclaim risk. | Framed results cautiously. | Add experiment-design section. |
| Simple regression | Model uses limited features. | Prediction is directional only. | Reported R-squared and limitations. | Add model card and richer features. |
| Excel translation | Original brief expected Excel work. | Deliverable differs from course surface. | Converted to reproducible Python/Gold. | Explain translation earlier in README. |

### Strong Public Case Study Shape

1. Open with the engagement comparison question.
2. Explain Q2 cohorts and paid/free segmentation.
3. Show outlier handling and confidence intervals.
4. Show t-test results and interpretation.
5. Show certificate correlation/regression as a directional model.
6. Close with the causal and production-model limitations.

### Additional Interview Prompts

**How did you avoid overclaiming?**

I separated statistical comparison from causality. The report says what changed in the dataset, but it does not claim that a feature caused the change.

**How would you productionize it?**

I would add a proper experiment design, richer feature tables, scheduled data refresh, model monitoring, and a dashboard with confidence/assumption notes.

**What would you test next?**

I would add parser fixtures, test refund-window edge cases, test outlier filtering by segment, and add a model card for the regression.

### Claim Safety Checklist Addendum

- Do not claim causal impact.
- Do not claim production ML.
- Do not hide the R-squared.
- Do not imply Excel workbook delivery.
- Do not omit the 99th percentile outlier rule.
- Do not present the 1,200-minute prediction as operational advice.
