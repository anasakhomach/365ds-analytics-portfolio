# ADR-002: Use Hybrid Custom And LangGraph Learning Hub Agent Backends

## Status
Accepted

## Date
2026-06-19

## Context
The Learning Hub assistant needs to answer portfolio, architecture, quiz, and approved Gold-mart data questions. The first live-AI test showed that the assistant needed better conversational memory and runtime self-awareness before a larger agent framework would add value.

Key requirements:
- Keep no-key local demos working.
- Preserve the existing provider-agnostic runtime and session-only BYOK behavior.
- Keep DuckDB access constrained to approved `gold.*` marts.
- Showcase AI engineering proficiency with a real graph-based agent path.
- Avoid a big-bang rewrite of the working Streamlit hub.

## Decision
Use a hybrid backend strategy controlled by `LEARNING_HUB_AGENT_BACKEND`:
- `custom`: default stable assistant path.
- `langgraph`: explicit LangGraph `StateGraph` path.
- `auto`: prefer LangGraph when installed, otherwise use `custom`.

The custom backend now has session history, follow-up retrieval, runtime/self-awareness routing, catalog-trait routing, RAG, live-model synthesis, and safe Gold data access.

The LangGraph backend reuses the same contracts but organizes orchestration as graph nodes: classify, retrieve, and synthesize. It uses LangGraph in-memory checkpointing with a Streamlit session thread id so visitor chat state is session-scoped and not persisted to disk.

LangGraph does not replace the SQL safety layer. All data questions still execute through the existing read-only DuckDB Gold validator.

## Alternatives Considered

### Replace The Custom Assistant Immediately
- Pros: one backend.
- Cons: higher regression risk and harder debugging.
- Rejected because the custom path is useful as a deterministic fallback and test oracle.

### Stay Custom Only
- Pros: simplest runtime and fewer dependencies.
- Cons: weaker AI-engineering portfolio signal and less explicit orchestration.
- Rejected because the user wants to showcase applied AI architecture.

### Persist Conversation Memory To Disk
- Pros: conversations survive browser reloads.
- Cons: privacy and key/session trust concerns for a portfolio demo.
- Rejected for now. Session-only memory is enough.

## Consequences
- Local/no-key demos remain stable on the custom backend.
- LangGraph can be demonstrated by setting `LEARNING_HUB_AGENT_BACKEND=langgraph`.
- Tests cover both custom behavior and LangGraph parity for structured and Gold-data routes.
- Future agent nodes can be added without changing Streamlit UI contracts.

## Sources
- LangGraph short-term memory and thread IDs: https://docs.langchain.com/oss/python/langgraph/add-memory
- LangGraph agentic RAG graph pattern: https://docs.langchain.com/oss/python/langgraph/agentic-rag
