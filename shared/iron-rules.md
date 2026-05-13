# Iron Rules — Canonical

These are the foundational principles for ALL development work in development-skills. Every phase, every skill, every subagent references this file. **Do not duplicate the content elsewhere — link to it.**

Pillars 0-7 come from the project's `AGENTS.md` Core Pillars. Pillars A-C are workflow-specific safety/process rules.

---

## 0. Don't Pander — Be Critical

Challenge assumptions. Flag risks. Push back on bad ideas even when the user seems committed. Saying *"looks good"* when it doesn't is a failure mode, not politeness.

**Never open a response with flattery.** No *"Great question!"*, *"Good idea!"*, *"Excellent approach!"* — respond directly. If the user's idea is genuinely good, demonstrate it with evidence, not adjectives.

**Where it bites:** brainstorming Q&A, plan approval, staff review.

## 1. Maximize Simplicity, Minimize Complexity

Use critical thinking to maximize simplicity while keeping all the features. Abstract complexity rather than letting it propagate. Weigh complexity cost against improvement magnitude — small improvement + ugly complexity = not worth it.

Three concrete questions to ask before adopting anything:
1. Does an existing mechanism already cover >50% of this? If yes → reject or fold in.
2. Can this be one fewer file / one fewer abstraction / one fewer config? If yes → do it.
3. Would removing this line / function / dependency cause a real failure? If no → remove it.

**Where it bites:** brainstorming approach selection, Phase 1 plan, Phase 3 REFACTOR step, Phase 4 staff review.

## 2. All Signal, Zero Noise

Everything must earn its place. If it doesn't add value, remove it. Applies to:
- **Code:** dead branches, unused imports, wrapper-for-nothing functions, defensive try/catch on safe paths.
- **Comments:** restating what the next line says; status comments that rot.
- **Docs:** restating rules in multiple files (link, don't duplicate); past-tense narrative (*"we used to do X, now we do Y"* belongs in chronicles, not in canonical docs).
- **Output to the user:** filler openers, trailing summaries when the diff is the answer.

**Where it bites:** Phase 3 anti-slop check, Phase 4 staff review, doc maintenance.

## 3. Zero Regression in Refactoring

Verify with all appropriate test suites after every change. **No positive claim** (*"works"*, *"done"*, *"should pass"*, *"looks good"*) without fresh verification output in the current turn.

5-step verification gate (mandatory in Phase 3):
1. **IDENTIFY** the command that proves the claim.
2. **RUN** it fresh, complete.
3. **READ** the output. Check exit code. Count pass/fail.
4. **VERIFY** the output confirms the claim.
5. **CLAIM** — only now.

*"I'm confident"* is not a step. Skipping any step = lying, not verifying.

**Where it bites:** Phase 3 verification, Phase 4 staff review, every claim of completion.

## 4. Document Every Discovery

Write insights, useful and non-trivial information immediately. Three destinations, by purpose:

| Type | Where | What |
|---|---|---|
| **Decisions / WHY** | `docs/chronicles/NNNN__...md` | Business context, trade-offs, rejected alternatives |
| **HOW / step-by-step** | `docs/plans/NNNN__...md` | Tasks, file paths, verification commands |
| **Team standards / project rules** | `.agents/rules/<topic>.md` | Reusable across tasks |
| **Essential summary** | `AGENTS.md` (or `CLAUDE.md`) | Brief directives + references (Pillar 7) |

If you discover a non-obvious pattern, edge case, constraint, or gotcha — write it down before moving on. Future-you (or the next agent) reads disk, not memory.

**Where it bites:** Phase 2 chronicle init, Phase 3 implementation log, Phase 4 chronicle finalize + AGENTS.md updates.

## 5. Comments Explain WHY, Not WHAT

Ambiguous or non-obvious code MUST have a WHY comment. Business logic, Pydantic models, SQL queries, configuration, API contracts, data transformations.

**Examples:**
```python
# WHY (good)
price: Decimal  # upstream API returns price as 5-decimal fixed-point; Decimal preserves precision across currency conversions

# WHAT on bad code (acceptable + refactor TODO)
# Filters active users who haven't logged in for 90 days and aren't system accounts
result = [u for u in db_users if u[3] == 1 and (now - u[7]).days > 90 and u[2] not in sys_ids]
# TODO: refactor — use named fields (User model) instead of tuple indexing

# WHAT on clean code (REMOVE)
# Loop through users  ← noise, the code is clear
for user in users:
```

**Where it bites:** Phase 3 implementation, Phase 4 staff review.

## 6. Refactoring Objective: Clear, Descriptive, Efficient, Performant, Reliable, Robust, Maintainable

A refactor must leave the code measurably better against these 7 dimensions. Not *"different"* — better. If you can't name which dimension the change improves, it's not a refactor.

**Where it bites:** Phase 3 REFACTOR step, Phase 4 staff review.

## 7. Keep Project Docs Slim

`AGENTS.md` (or equivalent project-root doc): **max ~70 lines.** Only very specific and brief directives about non-trivial or domain-specific things. Push details to `.agents/rules/<topic>.md` references.

When updating project docs (Phase 4 finalize), apply Pillar 2 ruthlessly — if a line isn't load-bearing for the next agent's task, it belongs in a rule file or a chronicle, not in `AGENTS.md`.

---

## Workflow-Specific Process Rules

These are not Core Pillars; they are safety/process rules for using the development-skills workflow itself.

### A. No Commits Without Explicit User Request

NEVER run `git add`, `git commit`, or `git push` unless the user explicitly asks. Approving a plan, completing phases, passing review — none are permission to commit. Only Phase 4 integration step (4d) with explicit user choice, or a direct user "commit" request, triggers it.

### B. Red/Green TDD Is the Implementation Default

Every implementation starts with a failing test. RED → GREEN → REFACTOR.

- One test = one cycle. Multiple behaviors = separate cycles.
- Skip RED = test proves nothing.
- Skip REFACTOR = Pillar 1 (simplicity) and Pillar 6 (refactoring objective) lost.
- If TDD seems impractical (UI-heavy, infrastructure, config-only): write the closest automated check first. If truly untestable, document WHY and verify manually with evidence (Pillar 3).

### C. Every Gate Must Be Explicitly Passed

*"Proceed immediately"* means execute the next gate — NOT skip its requirements. Every phase has mandatory outputs. The plan file is the persistent record — update incrementally as each phase completes, not in bulk.
