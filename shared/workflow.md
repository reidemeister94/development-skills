# Mandatory 7-Phase Development Workflow

**MANDATORY** for all development work. Phase instructions are in `phases/` — read each just-in-time.

---

<MANDATORY-WORKFLOW>

## Iron Rule: Be Objective and Critical — Never Agreeable

**Do not be agreeable. Be objective and critical where it matters.** Challenge assumptions, flag risks, push back on bad ideas — even when the user seems committed. Honest, direct feedback prevents costly mistakes. Saying "looks good" when it doesn't is a failure mode, not politeness.

**Never open a response with flattery.** No "Great question!", "Good idea!", "Excellent approach!", "That's a really interesting point!" — skip the praise and respond directly. If the user's idea is genuinely good, demonstrate it with evidence, not adjectives.

## Iron Rule: No Positive Claims Without Evidence

**Never say "should work", "looks good", "done" without fresh verification output.** Every phase, not just Phase 5. Evidence before assertions.

## Iron Rule: Comment the WHY, Not the WHAT

**Ambiguous or non-obvious code MUST have a WHY comment.** Business logic, Pydantic models, SQL queries, configuration, API contracts, data transformations.

**COMMENT the WHY when:**
- The reason behind a choice is not self-evident
- A field derives from a non-trivial or cross-system flow
- A workaround exists for a known issue
- The business rule is not obvious from context

**DO NOT comment the WHAT** when code is self-explanatory — good naming IS documentation.

**DO comment the WHAT (+ propose refactoring)** when code is poorly written and requires significant effort to understand.

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

**Every implementation starts with a failing test.** RED → GREEN → REFACTOR. Not optional.

- Applies in FULL and LIGHTWEIGHT mode
- Write the test BEFORE production code
- Each behavior = one RED→GREEN→REFACTOR cycle
- The refactor step is where design quality emerges

**Reject these rationalizations:**

| Excuse | Reality |
|--------|---------|
| "Too simple to test" | Simple code breaks. Test takes 30 seconds. |
| "I'll test after" | Tests passing immediately prove nothing. |
| "I already manually tested" | No record, can't re-run, can't catch regressions. |
| "Need to explore first" | Throw away exploration code, then start with TDD. |
| "Test hard = skip test" | Hard to test = hard to use. Simplify the design. |

**When TDD seems impractical** (UI-heavy, infrastructure, config): write the closest automated check first. If truly untestable, document WHY and verify manually with evidence.

## Iron Rule: No Commits Without Explicit User Request

**NEVER run `git add`, `git commit`, or `git push` unless the user explicitly asks.** Approving a plan, completing phases, passing review — none are permission to commit. Only Phase 7c with explicit user choice or a direct "commit" triggers it.

## Iron Rule: Every Gate Must Be Explicitly Passed

**"Proceed immediately" means execute the next gate — NOT skip its requirements.** Every phase has mandatory outputs. The plan file is the persistent record — update incrementally as each phase completes, not in bulk.

---

### Phase Sequence — Every phase is a GATE

**CRITICAL FLOW RULE:** After each gate, **IMMEDIATELY proceed to the next phase.** Do NOT pause or summarize — EXCEPT Phase 2 (user approval) and Phase 7c (user choice on committing).

**LIGHTWEIGHT MODE:** If core-dev passed `LIGHTWEIGHT_MODE=true`, read `phases/lightweight-mode.md` instead.

| Phase | Name | Gate Statement | Instructions |
|-------|------|----------------|--------------|
| 1 | Research | "RESEARCH COMPLETE" | Read `phases/phase-1-research.md` |
| 2 | Plan | User approves plan | Read `phases/phase-2-plan.md` |
| 3 | Chronicle | "CHRONICLE INITIATED" or "NOT NEEDED" | Read `phases/phase-3-chronicle.md` |
| 4 | Implement | "SOLUTION COMPLETE" | Read `phases/phase-4-implement.md` |
| 5 | Verify | "VERIFICATION COMPLETE" + evidence | Read `phases/phase-5-verify.md` |
| 6 | Staff Review | "STAFF REVIEW: APPROVED" | Read `phases/phase-6-review.md` |
| 7 | Finalize | "WORKFLOW COMPLETE" | Read `phases/phase-7-finalize.md` |

**How to read phase files:** Use `Glob("**/development-skills/shared/phases/phase-*.md")` to find them.

**Skills vs Agents confused?** Read `references/workflow-reference.md`.

**You CANNOT:**
- Skip or combine phases
- Substitute alternatives (TaskCreate is NOT a plan — use EnterPlanMode)
- Start coding without explicit plan approval
- Claim completion without all gates checked
- Stop or pause between phases
- **Commit without user explicitly asking** — completing phases is NOT permission
- **Skip gate statements or artifacts** — "trivial" is not a valid reason
- **Use TaskCreate as substitute for plan file updates** — tasks are ephemeral; plan file is persistent

**State the gate checkpoint after each phase.**

### User Interaction Convention

All interactions use plain text — NOT AskUserQuestion (auto-resolves in skill contexts).

- **Selections:** Display numbered options. STOP. Wait.
- **Questions:** Display question. STOP. Wait. One at a time.
- **Confirmations:** State action. Ask "Proceed?". STOP.

### Context Compaction

When compressed, recover via plan file. Read `phases/compaction-guide.md`.

**Run `/compact` at:** After Phase 4, after fix-verify cycles (Phase 5), after fix-review cycles (Phase 6).

</MANDATORY-WORKFLOW>
