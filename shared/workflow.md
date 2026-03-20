# Mandatory 7-Phase Development Workflow

This workflow is **MANDATORY** for all development work. Phase instructions are in the `phases/` directory — read each phase file just-in-time.

---

<MANDATORY-WORKFLOW>

## Iron Rule: No Positive Claims Without Evidence

**Never say "should work", "looks good", "done", or any success claim without fresh verification output.** This applies to EVERY phase, not just Phase 5. Evidence before assertions, always.

## Iron Rule: Comment the WHY, Not the WHAT

**Every piece of code that is ambiguous, non-obvious, or derives from intricate logic MUST have a comment explaining WHY it exists — not what it does.** This applies everywhere: business logic, Pydantic models (field types, defaults, validators), SQL queries, configuration, API contracts, data transformations.

**COMMENT the WHY when:**
- The reason behind a choice is not self-evident (why this type? why this default? why this order?)
- A field or parameter derives from a non-trivial, cryptic, or cross-system flow
- A workaround exists for a known issue or external constraint
- The business rule driving the code is not obvious from context
- A Pydantic model field has a type or constraint that only makes sense knowing the upstream data source

**DO NOT comment the WHAT when:**
- The code is clean and self-explanatory — good naming IS the documentation
- The comment would just restate what the code already says clearly

**DO comment the WHAT (+ propose refactoring) when:**
- The code is poorly written and understanding it requires significant mental effort
- In this case: (1) add a comment explaining what it does, (2) propose a refactoring to make it clearer. The comment is a band-aid — the refactoring is the cure.

**Examples:**
```python
# WHY comment (good) — explains the non-obvious reason
price: Decimal  # Legacy DB returns price as 5-decimal fixed-point; Decimal preserves precision across currency conversions

# WHAT comment on bad code (acceptable + refactor proposal)
# Filters active users who haven't logged in for 90 days and aren't system accounts
result = [u for u in db_users if u[3] == 1 and (now - u[7]).days > 90 and u[2] not in sys_ids]
# TODO: Refactor — use named fields (User model) instead of tuple indexing

# Unnecessary WHAT comment (remove this)
# Loop through users  <-- adds nothing, the code is clear
for user in users:
```

## Iron Rule: Red/Green TDD Is the Starting Point

**Every implementation starts with a failing test.** Red/Green TDD is not optional, not a nice-to-have — it is the foundational discipline that governs ALL coding work in this workflow.

**The cycle: RED (failing test) → GREEN (minimal pass) → REFACTOR (improve design, tests stay green).**

- This applies in FULL mode (the implementer enforces it) AND in LIGHTWEIGHT mode (you enforce it yourself)
- A test that doesn't fail first proves nothing — it might pass for the wrong reason
- Write the test BEFORE the production code, always
- Each behavior = one RED→GREEN→REFACTOR cycle
- The refactor step is where design quality emerges — never skip it

**Common rationalizations — recognize and reject them:**

| Excuse | Reality |
|--------|---------|
| "Too simple to test" | Simple code breaks. Test takes 30 seconds. |
| "I'll test after" | Tests passing immediately prove nothing — they might test the wrong thing. |
| "I already manually tested" | Ad-hoc ≠ systematic. No record, can't re-run, can't catch regressions. |
| "Need to explore first" | Fine. Throw away exploration code, then start fresh with TDD. |
| "Test hard = skip test" | Hard to test = hard to use. Listen to the test — simplify the design. |

**Red flags — STOP and restart with TDD if any of these happen:**
- You wrote production code before a test
- A test passes immediately without failing first
- You're rationalizing "just this once"

**When TDD seems impractical** (UI-heavy code, infrastructure scripts, config changes): write the closest possible automated check first. If truly untestable, document WHY in the implementation log and verify manually with evidence.

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
