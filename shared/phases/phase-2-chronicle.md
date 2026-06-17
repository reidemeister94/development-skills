# Phase 2: CHRONICLE — GATE

A chronicle records WHY a change happened, all the motivations behind it and the verbatim user input — what Git diffs and plan docs cannot capture. When in doubt, create it.

**Needed when ANY apply:** new feature/endpoint · architectural change or new pattern · bug fix needing investigation · breaking/API change · multi-file refactor with design decisions · non-obvious business logic · significant research/discovery.

**Not needed when ALL apply:** trivial fix · no new pattern/decision · self-evident from the diff · no business context to preserve.

## If needed

1. Next number: `ls docs/chronicles/*.md 2>/dev/null | sort | tail -1`, increment (start 0001).
2. Name `docs/chronicles/NNNN__YYYY-MM-DD__brief-description.md`; instantiate `../templates/chronicle-template.md`.
3. **Fidelity (graduated):** critical input — requirements, constraints, explicit decisions, course corrections, the answer that locked a design choice — kept in the user's **exact words**, never condensed. Everything else summarized losslessly (remove noise, never signal).

Lifecycle: Phase 3 updates Discoveries + design decisions; Phase 4 aligns with final code, fills "After", sets Completed (AGENTS.md updates happen via align-docs in 4c, not here).

WORKFLOW STATE → `Chronicle: docs/chronicles/...`, `Current Phase: 3`.

**Gate:** state **"CHRONICLE INITIATED — [filename]"**.

## If NOT needed

WORKFLOW STATE → `Chronicle: NOT NEEDED — [reason]`, `Current Phase: 3`. **Gate:** state **"CHRONICLE: NOT NEEDED — [reason]"**.

→ Read `phase-3-implement-verify.md`.
