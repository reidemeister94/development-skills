# Mandatory 4-Phase Development Workflow

**MANDATORY** for all development work. Phase instructions are in `phases/` — read each just-in-time.

---

<MANDATORY-WORKFLOW>

## Iron Rules

All Iron Rules live in `shared/iron-rules.md`. Apply them in every phase. Reference, don't duplicate.

---

### Phase Sequence — Every phase is a GATE

**CRITICAL FLOW RULE:** After each gate, **IMMEDIATELY proceed to the next phase.** Do NOT pause or summarize — EXCEPT Phase 1 (user approval of plan) and Phase 4d (user choice on committing).

| Phase | Name | Gate Statement | Instructions |
|-------|------|----------------|--------------|
| 1 | Research + Plan | "RESEARCH + PLAN COMPLETE — APPROVED" | Read `phases/phase-1-research-plan.md` |
| 2 | Chronicle | "CHRONICLE INITIATED" or "NOT NEEDED" | Read `phases/phase-2-chronicle.md` |
| 3 | Implement + Verify | "IMPLEMENT + VERIFY COMPLETE" + evidence | Read `phases/phase-3-implement-verify.md` |
| 4 | Review + Finalize | "WORKFLOW COMPLETE" | Read `phases/phase-4-review-finalize.md` |

**How to read phase files:** Use `Glob("**/development-skills/shared/phases/phase-*.md")` to find them.

**Skills vs Agents confused?** Read `references/workflow-reference.md`.

**You CANNOT:**
- Skip or combine phases
- Substitute alternatives (the plan file IS the plan)
- Start coding without explicit plan approval (Phase 1 gate)
- Claim completion without all gates checked
- Stop or pause between phases (except Phase 1 approval and Phase 4d commit-choice)
- **Commit without user explicitly asking** — completing phases is NOT permission
- **Skip gate statements or artifacts** — "trivial" is not a valid reason

**State the gate checkpoint after each phase.**

### User Interaction Convention

On Claude Code main thread, prefer `AskUserQuestion` when the answer fits 2-4 discrete options (plan approval, commit choice, approach selection). It auto-resolves inside Task subagents — never call it from `staff-reviewer`'s prompt. Codex has no equivalent: use the fallback pattern.

- **Discrete options (2-4):** `AskUserQuestion` on Claude Code; numbered list + STOP on Codex.
- **Free-form questions:** plain text + STOP, one at a time.
- **Confirmations:** state action, ask *"Proceed?"*, STOP.

### Context Compaction

When compressed, recover via plan file. Read `phases/compaction-guide.md`.

**Run `/compact` at:** After Phase 3 implementation (heaviest phase), after fix-verify cycles, after fix-review cycles.

</MANDATORY-WORKFLOW>
