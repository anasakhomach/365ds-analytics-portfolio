# ADR-001: Use Provider-Agnostic AI Runtime For Learning Hub

## Status
Accepted

## Date
2026-06-19

## Context
The Learning Hub is a portfolio surface for five analytics projects. It needs to demonstrate AI proficiency without making the demo unusable when no API key is present, and without locking the app to one model vendor.

Key requirements:
- Work offline for reviewers who only want to inspect the project.
- Support owner-configured live AI for hosted demos.
- Let local visitors bring a temporary key without saving it.
- Keep data access constrained to approved DuckDB Gold marts.
- Allow OpenRouter, LiteLLM, OpenAI, or another OpenAI-compatible gateway.

## Decision
Use a provider-agnostic runtime with four effective modes:
- Local fallback with TF-IDF retrieval and DuckDB Gold data access.
- Direct OpenAI-compatible provider calls.
- Managed gateway mode through OpenRouter.
- Self-hosted gateway mode through LiteLLM.

The app resolves keys in this order:
- session BYOK key when enabled,
- `LEARNING_HUB_API_KEY`,
- provider-specific alias such as `OPENROUTER_API_KEY` or `LITELLM_API_KEY`.

The LiteLLM path does not treat an upstream `OPENAI_API_KEY` as the gateway bearer key. That key belongs to the proxy's upstream provider config, not to the hub client.

## Alternatives Considered

### OpenAI Only
- Pros: simplest integration and docs.
- Cons: weaker portfolio story, vendor lock-in, no gateway controls.
- Rejected because the user explicitly wants provider/model agnosticism.

### BYOK Only
- Pros: avoids owner demo cost.
- Cons: poor visitor experience and trust friction.
- Rejected as the default, but kept as an optional session-only path.

### Celery Worker From V1
- Pros: background indexing and request isolation.
- Cons: broker/service complexity before workload requires it.
- Rejected for now. Streamlit synchronous requests and one-shot indexing are enough.

## Consequences
- No-key demos remain functional through local retrieval.
- Hosted demos can use a limited owner gateway key.
- LiteLLM can later add budgets, virtual keys, logging, and routing without changing hub code.
- Changing embedding backend/model requires rebuilding the vector index because embeddings are model-specific.
- All LLM-generated SQL remains untrusted and must pass the Gold-only validator before execution.
