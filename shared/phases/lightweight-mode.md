# Lightweight Mode

For genuinely small tasks, the full 7-phase workflow is overkill. Lightweight mode collapses phases while preserving quality.

**Criteria (ALL must be true — determined by core-dev guard):**
- Scope: 3 files or fewer
- Single obvious approach (no meaningful alternatives)
- Fully reversible
- Brainstorming was NOT invoked

**Intellectual Integrity still applies.** Lightweight mode reduces ceremony, not critical thinking. If the developer's request has flaws, stop and say so — even for small tasks.

**TDD still applies.** Even in lightweight mode, write the failing test FIRST, then the production code. RED→GREEN→REFACTOR is not ceremony — it's the foundation. The only exception: changes that are genuinely untestable (config-only, docs-only).

**Lightweight Phase Sequence:**

| Phase | Lightweight Behavior |
|-------|---------------------|
| 1. Research | Inline — read patterns file (Quick Reference section), quick codebase check. No subagent. |
| 2. Plan | Inline plan summary to user. No EnterPlanMode. User confirms with "ok"/"proceed". No plan file to disk. |
| 3. Chronicle | SKIP — not needed for small reversible changes. |
| 4. Implement | Implement directly in main context. No implementer subagent. TDD: write failing test first, then production code. Comment the WHY on ambiguous code. |
| 5. Verify | Run tests/build/lint inline. No test-verifier subagent. |
| 6. Staff Review | Structured self-review (checklist below). No subagent. |
| 7. Finalize | Ask user if they want to commit. State "WORKFLOW COMPLETE". No chronicle to finalize. |

**Lightweight Self-Review Checklist (Phase 6):**

You wrote this code — your judgment is biased. Answer each question with explicit evidence, not "looks fine."

| # | Question | Answer required |
|---|----------|----------------|
| 1 | Does the diff match ONLY what was requested? | List every changed file. Flag anything not in scope. |
| 2 | Can any function be simpler? | For each function >20 lines, state why it can't be shorter. |
| 3 | Are there edge cases not covered by tests? | Name at least one edge case you considered and how it's handled. |
| 4 | Did you introduce any assumptions not in the original request? | List them or state "None — all behavior derives from requirements." |
| 5 | Would you approve this diff if someone else wrote it? | If hesitant, fix it before proceeding. |

If ANY answer reveals an issue, fix it before claiming "VERIFICATION COMPLETE."

**Exit to full mode:** If at any point during lightweight execution you discover the task is larger than expected (more files, unexpected complexity, multiple approaches), STOP and announce: "Switching to full 7-phase workflow." Then start from Phase 1 of the standard workflow.

**Gate statements still required:** State "RESEARCH COMPLETE", user confirms plan, "SOLUTION COMPLETE", "VERIFICATION COMPLETE", "WORKFLOW COMPLETE".
