# Learning Hub AI Retrospective

This appendix covers the cross-project Learning Hub: the Streamlit portfolio app, RAG/indexing layer, AI helper, Quiz/Data Coach, provider-agnostic runtime, BYOK behavior, safe DuckDB tool, LangGraph backend, and Docker path.

## Project Metadata

- Project name: 365DS Portfolio Learning Hub
- Project type: cross-project Streamlit app and applied AI portfolio layer
- Domain: data analytics education, portfolio explanation, RAG, safe data access
- Source projects: five completed 365DS analytics projects under `projects/`
- Primary app path: `apps/learning-hub/`
- Current status: local/Docker portfolio demo
- Public impact: not claimed

## Situation

The repo had five analytics projects, each with its own pipeline, report, and dashboard. That showed analytics execution, but it did not give a visitor one guided surface for understanding the whole portfolio, asking questions, inspecting quiz support, or querying approved project data.

## Task

Build a Learning Hub that could:

- explain the five projects and architecture;
- answer questions with citations from indexed repo artifacts;
- support quiz-style data questions;
- query approved DuckDB Gold marts only;
- work without an API key;
- support live AI through provider-agnostic configuration;
- allow session-only BYOK;
- run locally and in Docker.

## Delivered Solution

The hub is one Streamlit multipage app with:

- project catalog from `apps/learning-hub/catalog/projects.yaml`;
- local TF-IDF indexing for no-key fallback;
- optional vector indexing path;
- OpenAI-compatible live synthesis through selectable providers;
- session-only BYOK;
- deterministic runtime/capability routes;
- safe DuckDB Gold data tool;
- LLM-assisted SQL planning that still passes validation;
- optional LangGraph backend;
- Dockerfile and Compose services for app and indexer.

## Assistant Architecture

The assistant uses a layered approach:

1. deterministic routes for greetings, capabilities, runtime/model questions, and project traits;
2. retrieval over indexed docs/reports/instructions/code;
3. optional safe DuckDB Gold queries for data questions;
4. optional live model synthesis when a provider key is available;
5. local grounded fallback when no key or provider failure exists.

This is intentionally not a pure chatbot. It is a learning helper with guardrails and project-specific tools.

## Quiz And Data Coach

The Quiz/Data Coach is designed for data questions, not arbitrary database access. It can help inspect approved Gold marts, explain quiz-supporting values, and propose SQL for modeled outputs. The important rule is that generated SQL remains untrusted: it must be a read-only single query against catalog-approved `gold.*` tables.

## Provider Runtime

The runtime supports:

- local no-key fallback;
- direct OpenAI-compatible providers;
- OpenRouter-style managed provider mode;
- Groq-style direct provider mode;
- optional LiteLLM gateway mode;
- session-only BYOK;
- provider/model picker in the UI;
- rate-limit/auth/connection/model/generic error classification.

The default demo path was corrected away from an optional gateway endpoint so the app can start live when an owner key is configured, while still falling back locally when no key exists.

## LangGraph Backend

The custom assistant remains the stable default. LangGraph was added as an optional orchestration backend, controlled by runtime configuration. It reuses the same retrieval, provider, BYOK, and DuckDB safety contracts. It does not replace the safe SQL validator.

## Bug And Recovery Stories

### Capability Routing

Early assistant tests showed that "how can you help me" and SQL capability questions returned irrelevant retrieved snippets. The fix was deterministic capability routing before retrieval. This turned the assistant from a search wrapper into a product-aware helper.

### Runtime Self-Awareness

Questions like "what model are you" were initially confused with project ML-model references. The fix was runtime/self-awareness routing from safe app metadata.

### Live Provider Fallback

The app could appear to be in live mode while answering with local fallback. The fix added visible runtime status, provider/model selection, owner-key default behavior, session BYOK, error categories, and clearer fallback messaging.

### Gateway Default

The initial gateway-oriented setup could point Docker at a LiteLLM hostname that was not running. The fix made direct provider mode the default and kept LiteLLM as an explicit profile.

## Evidence

- Architecture: `apps/learning-hub/docs/architecture.md`
- Provider ADR: `docs/decisions/ADR-001-provider-agnostic-learning-hub-ai.md`
- Hybrid agent ADR: `docs/decisions/ADR-002-hybrid-learning-hub-agent-backend.md`
- Catalog: `apps/learning-hub/catalog/projects.yaml`
- Tests: `apps/learning-hub/tests/`
- Memory: `docs/agent-memory/current-thread-memory.md`

## What This Proves

- Applied AI architecture beyond a standalone chatbot.
- Practical RAG implementation with citations and local fallback.
- Provider/model-agnostic runtime design.
- Safe data-tool boundaries around approved analytics marts.
- Ability to debug assistant UX with deterministic routes and regression tests.
- Containerization and local demo operations.

## What This Does Not Prove

- Hosted production scaling.
- Multi-user concurrency under load.
- Long-term conversation persistence.
- Enterprise auth, billing, or audit logging.
- Public visitor adoption.

## Follow-Up Improvements

| Improvement | Why It Matters | Effort | Status |
| --- | --- | --- | --- |
| Add screenshots and short demo clips | Makes AI behavior easier to prove publicly. | medium | planned |
| Add dashboard and hub smoke command | Reduces manual port checks. | medium | planned |
| Add hosted deployment recipe | Moves from local Docker proof to public demo readiness. | high | planned |
| Add observability for provider fallbacks | Makes runtime reliability easier to monitor. | medium | planned |
| Add more curated starter questions | Improves first-time visitor experience. | low | planned |

