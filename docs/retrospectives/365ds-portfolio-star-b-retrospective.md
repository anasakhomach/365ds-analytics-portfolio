# 365DS Portfolio STAR-B Retrospective

This is the master STAR-B retrospective for the `365ds-demo-projects` repo. It treats the whole workspace as one delivered portfolio product: five analytics projects, DuckDB medallion pipelines, Streamlit dashboards, generated reports, quiz support, a cross-project Learning Hub, and an AI assistant with safe data access.

## Project Metadata

- Project name: 365DS Analytics Portfolio And Learning Hub
- Project type: self-directed analytics engineering and applied AI portfolio
- Domain: education analytics, customer behavior, checkout funnels, engagement, real estate, portfolio learning
- Time period: June 2026 local build thread
- Delivery status: local implementation exists; retrospective package added after delivery
- Current status: local/Docker portfolio demo, not a production hosted service
- Role: end-to-end analytics engineer, data engineer, dashboard builder, AI app implementer, documentation owner
- Team size: solo delivery with AI pair-programming support
- Client, employer, or self-directed: self-directed portfolio project
- Public link: not recorded
- Repo link: local repo path
- Demo link: local ports only; Learning Hub at `http://localhost:8507` when running
- Case study link: this retrospective package
- Related LinkedIn post: not published yet
- Private evidence location: repo-local memory under `docs/agent-memory/`

## Audience Fit

### Hiring Manager Signal

This project proves the ability to turn ambiguous course assets into reproducible analytics products, then layer an AI learning assistant on top without weakening data safety. The strongest signal is the combination of data engineering, dashboarding, QA, documentation, and applied AI product recovery.

### Recruiter Signal

Relevant keywords: Python, SQL, DuckDB, Streamlit, data pipelines, medallion architecture, analytics engineering, dashboards, RAG, LangGraph, Docker, provider-agnostic AI, BYOK, data quality, statistical analysis.

### Freelance Client Signal

This project resembles a client engagement where scattered datasets and briefs need to become reusable dashboards, reports, and a guided assistant for stakeholders or learners.

### Wrong Audience To Filter Out

This is not a claim of production-scale SaaS, paid customer adoption, cloud observability, or enterprise governance. It is a local portfolio proof system.

## Transparency Statement

This retrospective is written as a transparent delivery record. It separates verified evidence, personal judgment, estimated value, private/local context, and lessons learned. It does not claim outcomes that cannot be supported.

- Fully verifiable: repo files, project reports, catalog, architecture docs, ADRs, memory milestones, local verification notes.
- Partially verifiable: local runtime behavior and Docker checks documented in memory artifacts.
- Not publicly shared: actual API keys, raw chat transcript details, local machine-specific secrets.
- Estimated: portfolio usefulness for hiring, recruiter, or freelance audiences.
- Not claimed: production usage, external user adoption, revenue impact, client approval, or hosted uptime.

## Executive Summary

- Problem: The repo began as 365DS briefs and source datasets, not a cohesive portfolio product.
- Delivered solution: Five DuckDB/Streamlit analytics projects plus a Dockerized Learning Hub with an AI helper and safe Gold-mart data access.
- Your role: End-to-end builder across data ingestion, modeling, dashboards, reports, AI runtime, Docker, QA, and documentation.
- Main constraint: Course assets, local Windows/Docker tooling, and provider/API behavior needed practical adaptation.
- Most important decision: Standardize on DuckDB, Streamlit, Gold marts, and evidence-backed docs while keeping live AI optional.
- Outcome: A local portfolio workspace that can be explored project-by-project or through the Learning Hub assistant.
- Evidence: Project reports, catalog, architecture docs, ADRs, tests, and memory artifacts.
- Main lesson: Applied AI works best when deterministic product routes, safe data tools, retrieval, and provider fallback are designed together.

## Delivery Context

### Situation

The repo contained 365DS project instructions and raw source datasets. The desired end state evolved from individual analytics tasks into a portfolio system that demonstrates data analytics, data engineering, dashboards, and AI-assisted learning.

Pain points included:

- multiple project formats: CSV, SQL dump, Tableau, Excel-style tasks, and Python briefs;
- need to preserve raw sources while creating reusable outputs;
- local Windows ACL and environment issues;
- Docker readiness;
- weak early assistant behavior that needed product-level routing;
- provider configuration that needed to be live by default without storing secrets in tracked files.

### Task

The project needed to:

- implement the analytics projects reproducibly;
- keep raw inputs immutable;
- use DuckDB/Streamlit as the repo-standard stack;
- expose Gold marts and reports for each project;
- build a cross-project Learning Hub;
- make the assistant useful for architecture, quizzes, and safe data questions;
- document the delivery honestly enough to support interviews and portfolio review.

### Scope Boundaries

Included:

- five analytics projects;
- medallion pipelines;
- dashboards and reports;
- project catalog;
- Learning Hub;
- AI assistant;
- quiz/data helper;
- Docker support;
- documentation and memory.

Excluded:

- production hosting;
- public user analytics;
- committed API secrets;
- Tableau workbook delivery;
- persistent visitor chat storage;
- Celery or multi-worker async infrastructure.

## STAR-B Story Bank

### STAR-B Story 1: Main Delivery Story

**Situation**

The workspace started as course briefs and source datasets. It needed to become a portfolio proof system rather than a pile of disconnected exercises.

**Task**

Deliver reproducible analytics projects and a cross-project app that lets a visitor understand the architecture, findings, dashboards, quiz answers, and data safely.

**Action**

Implemented DuckDB Bronze/Silver/Gold projects, generated business reports, built Streamlit dashboards, created a YAML project catalog, added a Learning Hub, indexed project artifacts, added safe Gold-only DuckDB access, and documented decisions through ADRs and memory.

**Result**

The repo now contains five completed analytics projects and a Learning Hub that can explain and query them locally or through optional live AI.

**Bridge**

This proves end-to-end analytics engineering plus applied AI product thinking.

**Evidence**

- Repo artifact: `projects/`, `apps/learning-hub/`
- Architecture note: `apps/learning-hub/docs/architecture.md`
- Reports: `projects/*/reports/*_report.md`
- Confidence level: verified

### STAR-B Story 2: Technical Decision Story

**Situation**

The briefs used different tool expectations, including Python, SQL, Tableau, Excel, and LangChain. A portfolio needed one coherent stack.

**Task**

Choose a standard that preserved the course intent while making the outputs reproducible and demo-friendly.

**Action**

Standardized on DuckDB for local analytics, Streamlit for dashboards, Gold marts for dashboard/data-tool access, Python orchestration, and SQL transformations where relational.

**Result**

The five projects share a consistent workflow while still respecting Python-specific and statistics-specific requirements.

**Bridge**

This proves stack judgment and translation from learning assets into professional delivery artifacts.

**Evidence**

- Catalog traits: `apps/learning-hub/catalog/projects.yaml`
- Architecture docs: `apps/learning-hub/docs/architecture.md`
- Confidence level: verified

### STAR-B Story 3: Constraint Or Failure Story

**Situation**

Several issues appeared during delivery: hidden-folder ACL failures, environment setup friction, Docker readiness, multi-INSERT SQL dumps, weak assistant routing, and provider fallback confusion.

**Task**

Keep the repo moving without hiding the friction or breaking existing local/global skills.

**Action**

Used `agent-skills/` as the canonical visible package, added junctions for hidden skill paths, used workspace-local caches, validated SQL ingestion, kept Docker checks separate from local checks, added deterministic assistant routes, and changed the default live AI path away from an optional gateway.

**Result**

The repo now records both the fixes and the verification trail in memory and docs.

**Bridge**

This proves debugging discipline and honest recovery under local tooling constraints.

**Evidence**

- Bug ledger: `docs/retrospectives/bug-recovery-ledger.md`
- Memory: `docs/agent-memory/current-thread-memory.md`
- Confidence level: verified

### STAR-B Story 4: Collaboration Or Client Story

**Situation**

The project direction changed several times: from setup, to analytics projects, to SQL-first standardization, to Learning Hub, to provider-agnostic AI, to retrospective proof.

**Task**

Adapt the implementation without losing the architecture, safety boundaries, or previous work.

**Action**

Documented durable decisions in memory, used ADRs for major AI architecture choices, and kept project folders intact while adding the hub as a separate app.

**Result**

The repo supports multiple audiences: learner, reviewer, hiring manager, recruiter, and future maintainer.

**Bridge**

This proves ambiguity management and iterative delivery.

**Evidence**

- ADRs: `docs/decisions/`
- Memory walkthrough: `docs/agent-memory/thread-walkthrough.md`
- Confidence level: verified

## Delivered Artifacts

| Artifact | Purpose | Contribution | Proof Location | Public? |
| --- | --- | --- | --- | --- |
| Five analytics projects | Reproducible course implementations | Built pipelines, reports, dashboards, checks | `projects/` | yes |
| DuckDB warehouses and Gold marts | Local analytics engine and modeled outputs | Standardized medallion layers | `projects/*/scripts/`, catalog | yes |
| Streamlit dashboards | Interactive local reporting | Built dashboard surfaces over Gold marts | `projects/*/dashboard/app.py` | yes |
| Learning Hub | Cross-project portfolio app | Built catalog, index, assistant, data coach, Docker path | `apps/learning-hub/` | yes |
| AI runtime and assistant | RAG/live/local learning helper | Added provider modes, BYOK, deterministic routes, LangGraph option | `apps/learning-hub/`, ADRs | yes |
| Documentation and memory | Future handoff and proof | Maintained ADRs, memory, retrospectives | `docs/` | yes |

## Technical Stack

- Languages: Python, SQL, Markdown
- Frameworks: Streamlit, optional LangGraph
- Databases: DuckDB
- APIs: OpenAI-compatible provider interface
- Cloud or hosting: local Docker only; no production hosting claimed
- Testing: pytest, py_compile, smoke checks recorded in memory
- Data tools: pandas, DuckDB, SQL quality checks, project reports
- AI or automation tools: local TF-IDF retrieval, optional vector indexing, live model synthesis, safe SQL planner
- Other: Docker Compose, uv, repo-local skills and memory artifacts

### Stack Rationale

DuckDB and Streamlit made the repo easy to run locally while keeping analytics logic reproducible. Provider-agnostic AI let the hub demonstrate applied AI without forcing one vendor or requiring a key for no-key demos.

### Stack Limitations

Streamlit is convenient but not a full production frontend framework. Docker local verification is not hosted production proof. Live AI behavior depends on provider availability, rate limits, and model compatibility.

## Technical Decisions And Trade-Offs

| Decision | Choice Made | Trade-Off | Result | Evidence |
| --- | --- | --- | --- | --- |
| Local warehouse engine | DuckDB | Needed dump parsing for MySQL-style sources. | Consistent local analytics layer. | Catalog and reports |
| Dashboard surface | Streamlit | Less BI-native than Tableau. | Runnable local dashboards. | Project dashboards |
| Assistant runtime | Provider-agnostic with local fallback | More configuration surface. | No-key and live demos both possible. | ADR-001 |
| Assistant backend | Custom default, optional LangGraph | Two paths to maintain. | Stable fallback plus AI orchestration proof. | ADR-002 |
| Data access | Gold-only DuckDB tool | Requires curated marts. | Safer portfolio data queries. | Hub architecture |
| Async work | No Celery in v1 | Indexing and chat are synchronous. | Lower ops burden for local demo. | Hub architecture |

## Delivery Timeline

| Phase | What Happened | Key Decision | Evidence |
| --- | --- | --- | --- |
| Setup | Git initialized, skills and memory established. | Use repo-local `agent-skills/` and memory artifacts. | Memory M1-M3 |
| Stack baseline | DuckDB/Streamlit standard chosen. | Raw sources immutable; Gold marts power dashboards. | Memory M4 |
| Analytics build | Five projects implemented. | SQL-first where relational, Python where required. | Memory M5-M7 |
| Learning Hub v1 | Catalog, indexer, assistant fallback, safe data tool, Docker added. | Hub is additive and does not restructure projects. | Memory M8 |
| Provider upgrade | Live AI, BYOK, Chroma option, SQL planner, docs added. | Provider-agnostic runtime. | Memory M9-M11, ADR-001 |
| Agent upgrade | Memory, runtime awareness, project traits, LangGraph added. | Hybrid custom/LangGraph backend. | Memory M12, ADR-002 |
| QA recovery | Capability routing, provider fallback, live-start, dashboard services fixed. | Deterministic routes and direct provider default. | Memory M13-M14, bug ledger |
| Retrospective | Portfolio proof package created. | Bugs and recovery are part of the story. | `docs/retrospectives/` |

## Metrics And Outcomes

### Measured Local Outcomes

- Five analytics projects completed under `projects/`.
- Learning Hub catalog covers all five projects.
- Project reports include reproducibility notes and quiz support.
- Memory records passing local and Docker verification for the Learning Hub during the build thread.

### Qualitative Outcomes

- The repo now reads as an integrated portfolio rather than isolated exercises.
- The assistant can explain the architecture, capabilities, and runtime more clearly after QA fixes.
- The bug/recovery trail creates credible interview material.

### Unmeasured Outcomes

- Recruiter response, hiring manager feedback, freelance client conversion, public visitor usage, and business impact are not measured.

## Retrospective Analysis

### Keep Doing

- Preserve raw data and make transformations reproducible.
- Keep dashboards on Gold marts only.
- Record architectural decisions and memory milestones.
- Treat assistant failures as product bugs, not just model limitations.

### More Of

- Earlier smoke tests for all dashboard ports.
- Earlier deterministic assistant routes for capabilities and runtime questions.
- Earlier screenshots and demo artifacts.

### Less Of

- Depending on optional infrastructure as a default path.
- Letting RAG answer product-contract questions that should be deterministic.

### Stop Doing

- Treating no-key local fallback as enough when the user expects live model behavior.
- Assuming converted course assets are structurally simple.

### Start Doing

- Add public-demo runbooks and screenshots earlier.
- Maintain a small dashboard smoke script.
- Capture provider fallback behavior as screenshots or logs for future proof.

## Challenges, Mistakes, And Constraints

### Real Constraints

- Time: many project surfaces were built in one long thread.
- Budget: free/local AI provider paths shaped the live demo strategy.
- Access: local Docker and Windows ACL behavior affected verification.
- Data: source assets included CSVs, SQL dumps, converted instructions, Tableau/Excel expectations.
- Tooling: provider models, local caches, and sandbox behavior affected setup.

### Mistakes Or Weak Spots

| Issue | What Happened | Impact | What I Did | What I Would Do Next Time |
| --- | --- | --- | --- | --- |
| Assistant capability routing was too retrieval-heavy. | Simple product questions returned source snippets. | User trust dropped. | Added deterministic capability/runtime routes. | Define assistant contract routes before RAG. |
| Default gateway assumption was fragile. | LiteLLM could be selected without its service running. | Live mode fell back unexpectedly. | Made direct provider mode default and gateway explicit. | Keep optional services opt-in from the start. |
| Multi-dashboard runtime was not smoke-tested early enough. | Several ports were not reachable during user testing. | Demo reliability suffered. | Recovered and documented explicit port map. | Add smoke scripts as soon as multiple apps exist. |
| SQL dump parsing needed stronger assumptions. | Multi-block inserts could have been missed. | Risked incomplete Bronze data. | Added parser support and row-count checks. | Inspect dump structure before parser design. |

## Risk Register

| Risk | Severity | What Reduced The Risk | What Remains | Evidence |
| --- | --- | --- | --- | --- |
| Secrets in public docs | high | Retrospectives avoid key values and use a secret scan. | Local ignored `.env` still requires care. | Verification plan |
| Unsupported impact claims | high | Evidence ledger marks not-claimed outcomes. | Public case study must preserve those limits. | Evidence ledger |
| Provider rate limits | medium | Local fallback and BYOK behavior exist. | Hosted demo would need budgets/monitoring. | ADR-001 |
| Dashboard runtime drift | medium | Explicit port map and Docker/local checks. | Automated smoke script is still future work. | Bug ledger |
| RAG quality drift | medium | Deterministic routes and project traits. | More curated questions and evals would help. | Learning Hub retrospective |

## Proof Summary For Hiring Managers

- I delivered: five analytics projects plus an AI Learning Hub.
- I was responsible for: ingestion, modeling, dashboards, reports, AI runtime, safe data access, Docker, and docs.
- The hardest constraint was: adapting mixed course assets and local tooling into a coherent portfolio system.
- The strongest evidence is: project reports, catalog, ADRs, memory, and bug-recovery ledger.
- This maps to: analytics engineering, BI/dashboarding, data quality, applied AI, product debugging, and documentation.
- I would improve: screenshots, hosted deployment, dashboard smoke automation, and public demo polish.

## Proof Summary For Recruiters

- Role fit: Data Analyst, Analytics Engineer, Data Engineer, Applied AI Engineer.
- Keywords: Python, SQL, DuckDB, Streamlit, RAG, LangGraph, Docker, dashboards, data quality.
- Project type: portfolio-grade analytics and AI assistant workspace.
- Tools: Python, DuckDB, Streamlit, Docker, provider-agnostic AI.
- Outcome: local evidence-backed portfolio product.
- Seniority signal: debugging, trade-off documentation, and safe AI/data-tool boundaries.

## Proof Summary For Freelance Clients

- Client problem this resembles: turn messy source assets into dashboards, reports, and a guided AI helper.
- What I can deliver: reproducible local analytics workflows and stakeholder-facing dashboards.
- How I manage ambiguity: document decisions, preserve source data, and verify claims.
- How I communicate progress: reports, ADRs, memory, and recovery ledgers.
- What proof I can show: repo artifacts and local demos.
- What I will not overpromise: production scale or external impact without evidence.

## Interview Answer Bank

### Tell Me About A Project You Delivered

I built a 365DS analytics portfolio with five DuckDB/Streamlit projects and a Learning Hub that can explain the projects, cite sources, and safely query Gold marts.

### Tell Me About A Technical Trade-Off

I chose DuckDB and Streamlit over separate BI/database tools for each brief because the portfolio needed one reproducible local stack. The trade-off is that it is not production BI, but it is easier to verify and demo.

### Tell Me About A Time Something Went Wrong

The assistant initially answered "what model are you" by retrieving project ML-model content. I fixed it by routing runtime and capability questions deterministically before RAG.

### Tell Me About A Time You Worked With Ambiguity

The briefs mixed Python, SQL, Tableau, Excel, and chatbot work. I turned them into one architecture: Python orchestrates, SQL handles relational layers, dashboards read Gold, and the Learning Hub indexes everything.

### Tell Me About A Measurable Result

The repo contains local project metrics such as 35,230 Customer Engagement students, 1,835,588 minutes watched, and a Tracking User Engagement regression R-squared of 0.4678. These are project data outputs, not external business outcomes.

## Public Version Notes

### Safe To Share

- Stack choices, architecture, reports, local metrics, screenshots, and bug recovery stories.

### Must Redact

- API keys, raw transcript details, local secrets, and machine-specific private paths where unnecessary.

### Needs Permission

- Any claim involving employers, clients, users, or external feedback.

### Can Be Generalized

- Local path details can be rewritten as repo-relative paths for public case studies.

## Resume Bullets

- Delivered a five-project analytics portfolio using Python, SQL, DuckDB, and Streamlit, with reproducible medallion pipelines, Gold marts, dashboards, and quiz-supporting reports.
- Built a provider-agnostic AI Learning Hub with local RAG fallback, optional live model synthesis, session-only BYOK, LangGraph backend option, and safe read-only DuckDB Gold-mart access.
- Recovered delivery blockers across Windows ACLs, SQL dump parsing, Docker readiness, assistant routing, and provider fallback behavior, documenting verification and decisions through ADRs and repo memory.

## LinkedIn Post Angle

- Main claim: I turned five course projects into one reproducible analytics and AI portfolio workspace.
- Non-obvious lesson: The hard part was not only dashboards; it was making the assistant trustworthy and the evidence honest.
- Concrete proof: five project reports, a Learning Hub, ADRs, and bug-recovery ledger.
- Mistake or trade-off: RAG alone answered product questions poorly until deterministic routes were added.
- Audience: analytics/data engineering hiring managers, applied AI builders, portfolio reviewers.
- Hook options:
  1. "I stopped treating my analytics projects like isolated exercises."
  2. "The best part of this portfolio is the bug ledger."
  3. "A RAG chatbot was not enough, so I built a learning helper with guardrails."

## Follow-Up Improvements

| Improvement | Why It Matters | Effort | Owner | Status |
| --- | --- | --- | --- | --- |
| Add demo video | Makes the portfolio easy to review asynchronously. | medium | self | planned |
| Add screenshots | Gives recruiters fast visual proof. | low | self | planned |
| Add dashboard smoke script | Prevents local port drift. | medium | self | planned |
| Add hosted deployment recipe | Moves from local proof to public demo. | high | self | planned |
| Capture visitor feedback | Turns estimated portfolio value into measured evidence. | medium | self | planned |

## Claim Safety Checklist

- Every metric in this retrospective points to a project report or memory artifact.
- Stack details are based on repo files and ADRs.
- Responsibility claims are scoped to this self-directed local repo.
- No client, employer, user, revenue, or production claim is made.
- Estimated portfolio value is labeled as judgment.
- Known limitations are included instead of hidden.
- API key values are not included.

## Final Retrospective Judgment

### What This Project Proves

It proves local analytics engineering, dashboard delivery, applied AI integration, safe data-tool design, Docker demo setup, and transparent debugging.

### What This Project Does Not Prove

It does not prove production scale, public adoption, enterprise security, or business impact outside the local project data.

### Strongest Evidence

The strongest evidence is the combination of project reports, Learning Hub architecture docs, ADRs, catalog, tests, and memory-recorded recovery history.

### Weakest Evidence

The weakest evidence is public-facing adoption: screenshots, hosted deployment, visitor feedback, and public links are not yet captured.

### Best Use Of This Retrospective

Portfolio case study and interview story.

## One-Page Version

### Project

365DS Analytics Portfolio And Learning Hub

### Problem

Course briefs and datasets needed to become a cohesive, reproducible portfolio that showed analytics, dashboards, and applied AI.

### Delivered

Five DuckDB/Streamlit analytics projects, generated reports, quiz support, and a Learning Hub with citation-grounded assistant and safe Gold-mart data access.

### My Role

End-to-end builder across data engineering, analytics, dashboarding, AI runtime, Docker, QA, and documentation.

### STAR-B Summary

**Situation:** The repo started as separate 365DS briefs and source assets.

**Task:** Convert them into a coherent portfolio product.

**Action:** Built medallion pipelines, dashboards, reports, a catalog, AI Learning Hub, provider runtime, safe data tool, Docker path, ADRs, and recovery docs.

**Result:** The workspace can be explored through individual dashboards or one cross-project learning assistant.

**Bridge:** The project demonstrates practical analytics engineering and applied AI judgment.

### Evidence

`projects/`, `apps/learning-hub/`, `docs/decisions/`, `docs/agent-memory/`, and `docs/retrospectives/`.

### Trade-Off

The repo optimizes for local reproducibility and portfolio proof, not production hosting.

### Lesson

A strong AI portfolio project needs deterministic app behavior, safe tools, retrieval, provider fallbacks, and honest evidence.

### Relevance

Relevant to analytics engineer, data analyst, data engineer, and applied AI engineer roles.

