# Phase 3: IMPLEMENT + VERIFY — GATE

Cannot start without a user-approved plan; no approval → Phase 1. Implementation in the main thread, verification inline via `Bash`. Apply [Iron Rules](../iron-rules.md) throughout — TDD (7), surgical (4), fresh-evidence (8), root-cause (9), spirit beats letter.

## Step 1 — Plan file before any source file
WORKFLOW STATE → `Current Phase: 3`; add `## Task Checklist`, one `- [ ]` per task.

**Pre-flight plan scan (before Task 1):** one adversarial pass over the approved plan for internal contradictions — task-vs-task, task-vs-**Global Constraints**, a HOW-lock a task defeats, conflicts that only surface at implementation. A conflict → STOP, return to Phase 1, fix, re-approve (do not code around it). Record the one-line result under `## Pre-Flight Plan Review`.

## Implementation discipline
- **Vertical slices:** one behavior → minimal code → verify → next. Never all tests first then all code (horizontal slicing breeds brittle tests for an imagined shape). A task needing >100 lines before feedback → split it.
- **Anti-poisoning:** re-read source before each task (Glob/Grep paths, confirm signatures). Never trust memory of file contents across tasks.
- **Module moves:** Grep every import + mock/patch path before moving; after moving, update every caller + mock. Not done until linter is clean and tests show zero `ImportError`.
- **Checkpoints (5+ tasks):** every 3 done, mark `[x]` with affected files; near context limit, flush progress to disk.

## Step 2 — Per task
Read source fresh → if unclear STOP and ask (never guess) → run TDD cycle(s) → record in plan: `- [x] Task N — files: path:lines`.

## Step 3 — Verify (inline Bash, no subagent)
Run the locked verification procedure (the plan's Verification strategy, per [`../definition-of-done.md`](../definition-of-done.md)) plus the language skill's verification commands from project root. Long output → temp file, read excerpts. Append the full trail to the plan's `## Verification Results`; keep only pass/fail + failing excerpts in chat. Don't write useless unit tests that bring zero value: instead, analyze with critical thinking what are the use cases and edge cases and write the tests that actually verify the behaviors.

Tiers: **A** (has tests) — run all commands, add tests for new code first, 70-80% coverage. **B** (legacy, no tests) — run inline, but confirm with the user before any command that mutates state (DB/network/filesystem beyond the working tree).

Honesty: report `Tests: PASS (N/M)` / `COULD NOT RUN — reason` / `FAIL (N/M)` distinctly. Never "all checks pass" when tests did not execute. Always attempt the test command, not just the linter.

## Step 4 — Fix-verify
Fail → read the trail. Code bug: fix, re-run, stay here. Plan wrong: back to Phase 1. Environmental: document, ask. **Regression guard:** net regression → stop and reassess; two consecutive regressions → Phase 1.

## Step 5 — Log
After all tasks pass, append `## Implementation Log` (per task: approach / discoveries / decisions — omit empty). Fold discoveries into the chronicle. WORKFLOW STATE → `Current Phase: 4`.

**Gate:** state **"IMPLEMENT + VERIFY COMPLETE"** with evidence. → Read `phase-4-review-finalize.md`.
