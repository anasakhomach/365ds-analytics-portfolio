# Agent Memory Artifact Schema

## current-thread-memory.md

Use for current operational truth:

- workstream and objective
- how to use the artifacts
- durable decisions
- repository map
- imported skills or workflow contracts
- source repos consulted
- known risks and constraints
- verification history
- next steps
- recent delta

## thread-walkthrough.md

Use for milestone narrative:

- why the work started
- what changed at each milestone
- what each milestone unlocked
- major constraints discovered

Keep this lighter than `current-thread-memory.md`.

## memory-index.json

Use for routing and freshness:

- primary artifact path
- walkthrough path
- schema path
- repo focus
- last updated date
- notable constraints

## Update Rules

- Store durable repo context, not raw conversation.
- Replace stale truth instead of adding duplicate sections.
- Record paths, commands, tests, and risks when they affect future work.
- Refresh the index when memory artifacts are updated.
