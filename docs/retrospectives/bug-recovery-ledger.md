# Bug And Recovery Ledger

This ledger turns delivery friction into transparent engineering evidence. It is sourced from `docs/agent-memory/current-thread-memory.md` and `docs/agent-memory/thread-walkthrough.md`, then cross-checked against repo artifacts where possible.

## Incident Summary

| Incident | Impact | Response | Verification | Lesson |
| --- | --- | --- | --- | --- |
| Hidden `.agents/` and `.codex/` ACL issue | Hidden skill paths were unusable for normal child-file writes. | Kept `agent-skills/` as the canonical visible package and used junctions so hidden skill paths resolve to the same package. | Memory milestones M1 and M3 record the failure and durable fix. | Prefer a visible canonical source when hidden/local tooling paths become fragile. |
| Sandbox and uv cache friction | Environment setup hit ACL/socket limits around caches and package installs. | Used a workspace-local `.uv-cache/` and verified `.venv-365ds` once dependencies became available. | Memory records venv creation, cache decision, static compile, and project runtime checks. | Put local build caches inside the repo workspace when user-level paths are unreliable. |
| MySQL dump parsing complexity | Some SQL dumps used multiple `INSERT` blocks; a naive parser would silently miss rows. | Implemented multi-block parsing and quality checks for affected projects. | Customer Engagement and Tracking User Engagement memory milestones record row-count validation and multi-block support. | Data ingestion should validate row counts and parser assumptions, especially for converted course assets. |
| Tableau and Excel deliverable translation | Course briefs expected Tableau or Excel, while the portfolio stack standardized on Streamlit and reproducible local outputs. | Preserved the analytical intent while implementing Streamlit dashboards and Gold-backed Python/statistical outputs. | Project reports document Tableau/Excel translation and Gold-only dashboard reads. | A portfolio implementation can modernize the surface if the analytical contract remains visible and reproducible. |
| Docker Desktop Linux engine unavailable at first | Learning Hub Docker verification could not complete until Docker Desktop was running. | Kept local tests passing, then reran Docker build, indexer, app startup, HTTP smoke, and container tests after Docker was available. | Memory records the initial block and later successful Docker verification. | Separate local correctness from container readiness and re-run container checks when the engine is available. |
| Assistant self/model questions routed to project RAG | Questions like "what model are you" were answered as if they referred to project ML models. | Added deterministic runtime/self-awareness routing and session memory. | Memory records Batch 1, focused assistant tests, and later live behavior verification. | Assistant UX needs explicit capability and identity routes; RAG alone is not enough. |
| Capability questions produced weak retrieval answers | Questions like "how can you help me" and "can you run SQL" returned document snippets instead of app-contract answers. | Added deterministic capability routing before retrieval or live synthesis. | Memory records the capability QA fix and regression tests. | Core product capabilities should be answered from app contracts, not semantic search. |
| Provider fallback started local when live mode was expected | The app could fall back to local retrieval despite a user expecting live model synthesis. | Added provider/model picker, owner-key default, BYOK fallback, provider error classification, and clearer runtime status. | Memory records owner-key/BYOK runtime fix and 40 to 45 passing hub tests across iterations. | Provider state must be visible, actionable, and testable; silent fallback damages trust. |
| Default LiteLLM endpoint was unreachable in normal Docker runs | Docker default could point at an optional gateway hostname that was not running. | Changed default demo path to direct OpenRouter provider mode and left LiteLLM behind an explicit gateway profile. | ADR-001 and memory record the decision and Docker verification. | Optional infrastructure should not be the default dependency for a portfolio demo. |
| Some local dashboards were not reachable during multi-app testing | Several dashboard ports were not serving while others worked. | Restarted and verified the intended local port map: 8501, 8502, 8503, 8504, 8505, and 8507; 8506 remains intentionally unused. | User-facing runtime verification was summarized after the fix. | A multi-dashboard portfolio needs an explicit service map and smoke checks, not assumptions. |

## STAR-B Recovery Stories

### Story 1: Tooling And ACL Recovery

**Situation:** The repo needed durable agent skills and memory, but hidden `.agents/` and `.codex/` directories were blocked by Windows ACL behavior.

**Task:** Preserve a reusable local skill package without breaking global skills or depending on fragile hidden copies.

**Action:** The canonical package stayed in `agent-skills/`; hidden paths were repaired through junctions and documented in memory and repo instructions.

**Result:** The repo gained local analytics/data engineering skills while keeping a single visible edit target.

**Bridge:** This proves operational problem solving around local developer tooling, not just analytics code writing.

### Story 2: Data Ingestion Recovery

**Situation:** Later SQL projects used MySQL dumps with multiple `INSERT` blocks, which could produce incomplete Bronze loads if parsed naively.

**Task:** Keep DuckDB canonical while respecting source row counts.

**Action:** The parser was updated to support multi-block inserts and quality checks validated expected counts.

**Result:** Customer Engagement and Tracking User Engagement could be loaded reproducibly into DuckDB Bronze/Silver/Gold layers.

**Bridge:** This proves data engineering discipline around source fidelity and ingestion validation.

### Story 3: Assistant Product Recovery

**Situation:** The first assistant behavior was technically grounded but disappointing: it answered capability and runtime questions with irrelevant RAG snippets.

**Task:** Make the Learning Hub assistant behave like a product helper instead of a search box.

**Action:** Deterministic routes were added for greetings, capabilities, model/provider identity, SQL guardrails, project traits, and provider state.

**Result:** The assistant can now explain how it helps, what runtime it uses, and what SQL it can safely execute before falling back to retrieval or live synthesis.

**Bridge:** This proves applied AI judgment: retrieval, tools, memory, provider routing, and deterministic product behavior all matter.

### Story 4: Deployment Readiness Recovery

**Situation:** Docker verification was initially blocked by Docker Desktop readiness, and later the default live-AI endpoint could point at an optional gateway.

**Task:** Make the app runnable for a portfolio visitor without fragile local assumptions.

**Action:** The Docker path was verified after Docker Desktop started, and the default AI path was changed to direct provider mode while LiteLLM remained optional.

**Result:** The Learning Hub can run locally and in Docker with a clear fallback story for no-key, owner-key, and BYOK paths.

**Bridge:** This proves demo reliability thinking: good portfolio apps need operational paths, not just code artifacts.

## Remaining Risks

- The retrospective can cite local verification, but it should not claim hosted production reliability.
- Local app screenshots and demo videos would make the proof stronger.
- Secrets must remain out of retrospectives even when discussing owner-key or BYOK behavior.
- The existing Real Estate STAR-B draft is useful supporting evidence but should not be treated as the only project-level retrospective.

