# Mandatory 7-Phase Development Workflow

This workflow is **MANDATORY** for all development work. Phase instructions are in the `phases/` directory — read each phase file just-in-time.

---

<MANDATORY-WORKFLOW>

## Iron Rule: No Positive Claims Without Evidence

**Never say "should work", "looks good", "done", or any success claim without fresh verification output.** This applies to EVERY phase, not just Phase 5. Evidence before assertions, always.

## Iron Rule: No Commits Without Explicit User Request

**NEVER run `git add`, `git commit`, or `git push` unless the user explicitly asks you to commit.** "Proceed to next phase", "looks good", "proceed", or approving a plan is NOT permission to commit. Completing verification, passing review, or reaching Phase 7 is NOT permission to commit. The ONLY trigger for committing is the user saying "commit", "/commit", or explicitly choosing a commit option in Phase 7c. This rule overrides any momentum from the workflow flow.

## Iron Rule: Every Gate Must Be Explicitly Passed

**"Proceed immediately" means go to the next phase and execute its gate — NOT skip the gate's requirements.** Every phase has mandatory outputs (gate statements, plan file updates, artifacts). You CANNOT rationalize skipping them ("it's a simple change", "not worth documenting", "I'll do it later"). The plan file is the single persistent record of this workflow — update it incrementally as each phase completes, not in bulk at the end. If Phase 3 applies, state the gate ("CHRONICLE INITIATED" or "CHRONICLE: NOT NEEDED — [reason]"). If Phase 4 has a checklist, mark items `[x]` after each task, not after all tasks.

---

### Phase Sequence — Every phase is a GATE

**CRITICAL FLOW RULE:** After each gate, **IMMEDIATELY proceed to the next phase.** Do NOT pause, summarize, or wait for user input — EXCEPT Phase 2 (requires user approval) and Phase 7c (requires user choice on committing/landing). "Proceed to next phase" means continue the workflow — it is NEVER implicit permission to `git commit`.

**LIGHTWEIGHT MODE:** If core-dev passed `LIGHTWEIGHT_MODE=true`, read `phases/lightweight-mode.md` instead of following the full phase sequence. All other rules in this document still apply.

| Phase | Name | Gate Statement | Instructions |
|-------|------|----------------|--------------|
| 1 | Research | "RESEARCH COMPLETE" | Read `phases/phase-1-research.md` |
| 2 | Plan | User approves plan | Read `phases/phase-2-plan.md` |
| 3 | Chronicle | "CHRONICLE INITIATED" or "NOT NEEDED" | Read `phases/phase-3-chronicle.md` |
| 4 | Implement | "SOLUTION COMPLETE" | Read `phases/phase-4-implement.md` |
| 5 | Verify | "VERIFICATION COMPLETE" + evidence | Read `phases/phase-5-verify.md` |
| 6 | Staff Review | "STAFF REVIEW: APPROVED" | Read `phases/phase-6-review.md` |
| 7 | Finalize | "WORKFLOW COMPLETE" | Read `phases/phase-7-finalize.md` |

**How to read phase files:** Use Glob to find `**/phases/phase-N-*.md` or resolve relative to this file's directory.

**Skills vs Agents confusion?** Read `references/workflow-reference.md` for the lookup table.

**You CANNOT:**
- Skip or combine phases
- Substitute alternatives (TaskCreate is NOT a plan — use EnterPlanMode)
- Start coding without explicit plan approval from the user
- Claim completion without all gates checked
- Stop or pause between phases (each gate leads directly to the next)
- **Commit, push, or run any git write command without the user explicitly asking** — completing phases, passing tests, or getting review approval is NOT permission to commit. Only Phase 7c (with user's explicit choice) or a direct user request triggers a commit
- **Skip a gate statement or its required artifacts** — "it's trivial" or "not worth documenting" is not a valid reason. Phase 3 MUST produce either a chronicle or an explicit "NOT NEEDED — [reason]". Phase 4 MUST update the plan file checklist after EACH task, not in bulk
- **Use TaskCreate/TaskUpdate as a substitute for plan file updates** — tasks are ephemeral (gone after the conversation). The plan file is the persistent source of truth. Update it incrementally during every phase

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
