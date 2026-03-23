# Lightweight Mode

For genuinely small tasks, the full 7-phase workflow is overkill. Lightweight mode collapses phases while preserving quality.

**Criteria (ALL must be true — determined by core-dev guard):**
- Scope: 3 files or fewer
- Single obvious approach (no meaningful alternatives)
- Fully reversible
- Brainstorming was NOT invoked

**Intellectual Integrity still applies.** Lightweight mode reduces ceremony, not critical thinking. If the developer's request has flaws, stop and say so — even for small tasks.

**Lightweight Phase Sequence:**

| Phase | Lightweight Behavior |
|-------|---------------------|
| 1. Research | Inline — read patterns file (Quick Reference section), quick codebase check. No subagent. |
| 2. Plan | Inline plan summary to user. No EnterPlanMode. User confirms with "ok"/"proceed". No plan file to disk. |
| 3. Chronicle | SKIP — not needed for small reversible changes. |
| 4. Implement | Implement directly in main context. No implementer subagent. |
| 5. Verify | Run tests/build/lint inline. No test-verifier subagent. |
| 6. Staff Review | Quick self-review: verify no regressions against quality checklist. No subagent. |
| 7. Finalize | State "WORKFLOW COMPLETE". No chronicle to finalize. |

**Exit to full mode:** If at any point during lightweight execution you discover the task is larger than expected (more files, unexpected complexity, multiple approaches), STOP and announce: "Switching to full 7-phase workflow." Then start from Phase 1 of the standard workflow.

**Gate statements still required:** State "RESEARCH COMPLETE", user confirms plan, "SOLUTION COMPLETE", "VERIFICATION COMPLETE", "WORKFLOW COMPLETE".
