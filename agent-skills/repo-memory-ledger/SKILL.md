---
name: repo-memory-ledger
description: Maintain repo-local agent memory artifacts for data analytics and data engineering work. Use when starting or ending a long thread, importing skills, making durable workflow decisions, completing a milestone, preparing a handoff, or updating docs/agent-memory/current-thread-memory.md.
---

# Repo Memory Ledger

## Overview

Use this skill to keep the repo's durable working context current without copying raw chat history. The memory package is `docs/agent-memory/`.

## Artifacts

- `current-thread-memory.md`: current mission, decisions, repo map, changed files, verification, risks, and next steps.
- `thread-walkthrough.md`: compact milestone narrative.
- `memory-index.json`: artifact routing and freshness metadata.
- `artifact-schema.md`: what belongs in each artifact.

## Workflow

1. Load memory before planning.
- Read `docs/agent-memory/current-thread-memory.md` before substantial work.
- Read `thread-walkthrough.md` when the sequence of prior decisions matters.
- Treat memory as current truth only after checking it against the repo.

2. Update after meaningful milestones.
- Record durable decisions, changed behavior, touched files, commands, test results, and unresolved risks.
- Replace stale entries instead of appending duplicate history.
- Keep entries short enough for future agents to reload quickly.

3. Sync before handoff.
- Update `current-thread-memory.md`.
- Add one compact milestone to `thread-walkthrough.md` when the work materially changes the repo.
- Refresh `memory-index.json` freshness fields.

## Quality Rules

- Store durable engineering context, not transcript logs.
- Separate confirmed decisions from open questions.
- Prefer paths and command results over prose.
- Include exact error text only when future debugging depends on it.
- Keep source-data assumptions visible for analytics work.
