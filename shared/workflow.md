# Mandatory 7-Phase Development Workflow

This workflow is **MANDATORY** for all development work. Phase instructions are in the `phases/` directory — read each phase file just-in-time.

---

<MANDATORY-WORKFLOW>

## STOP — READ THIS BEFORE DOING ANYTHING

**Skills vs Agents confusion?** Read `references/workflow-reference.md` for the lookup table.

---

### Phase Sequence — Every phase is a GATE

**CRITICAL FLOW RULE:** After each gate, **IMMEDIATELY proceed to the next phase.** Do NOT pause, summarize, or wait for user input — EXCEPT Phase 2 (requires user approval).

**LIGHTWEIGHT MODE:** If core-dev passed `LIGHTWEIGHT_MODE=true`, read `phases/lightweight-mode.md` instead of following the full phase sequence. All other rules in this document still apply.

| Phase | Name | Gate Statement | Instructions |
|-------|------|----------------|--------------|
| 1 | Research | "RESEARCH COMPLETE" | Read `phases/phase-1-research.md` |
| 2 | Plan | User approves plan | Read `phases/phase-2-plan.md` |
| 3 | Chronicle | "CHRONICLE INITIATED" or "NOT NEEDED" | Read `phases/phase-3-chronicle.md` |
| 4 | Implement | "SOLUTION COMPLETE" | Read `phases/phase-4-implement.md` |
| 5 | Verify | "VERIFICATION COMPLETE" + evidence | Read `phases/phase-5-verify.md` |
| 6 | Staff Review | "STAFF REVIEW: APPROVED" | Read `phases/phase-6-review.md` |
| 7 | Finalize & Docs | "WORKFLOW COMPLETE" | Read `phases/phase-7-finalize.md` |

**How to read phase files:** Use Glob to find `**/phases/phase-N-*.md` or resolve relative to this file's directory.

**You CANNOT:**
- Skip or combine phases
- Substitute alternatives (TaskCreate is NOT a plan — use EnterPlanMode)
- Start coding without explicit plan approval from the user
- Claim completion without all gates checked
- Stop or pause between phases (each gate leads directly to the next)

**Rationalizing skipping a phase?** Read `references/workflow-reference.md` for the anti-rationalization check.

### Red Flags — STOP if you notice yourself:

- Using uncertain language ("should work", "probably fine")
- About to skip a phase because you feel "confident"
- Expressing satisfaction before running verification
- About to summarize and stop after Phase 4 without continuing to Phases 5-6-7
- Agreeing with the developer's approach without having considered alternatives

**Also check your language skill's red flags.**

**After each phase, explicitly state the gate checkpoint.**

### User Interaction Convention

All user interactions use plain text conversational gates — NOT AskUserQuestion (auto-resolves in skill contexts).

- **Selections:** Display numbered options. STOP. Wait for user's next message.
- **Questions:** Display question with context. STOP. Wait for response. One question at a time.
- **Confirmations:** State what you're about to do. Ask "Proceed?". STOP.

### Context Compaction

When context is compressed, recover via plan file. Read `phases/compaction-guide.md` for full protocol.

**Compaction points — run `/compact` at:**
- After Phase 4 (implementation) — context is heaviest
- After any fix-verify cycle in Phase 5
- After any fix-review cycle in Phase 6

</MANDATORY-WORKFLOW>
