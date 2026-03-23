---
name: debugging
description: "Use when fixing bugs, investigating errors, debugging failures, or diagnosing unexpected behavior."
user-invocable: true
allowed-tools: Glob, Grep, Read, Bash, Task, Skill, EnterPlanMode, Edit, Write
---

# Systematic Debugging

**Announce:** "I'm using the debugging skill. Following the systematic root-cause methodology."

## THE IRON LAW

**NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST.**

Random fixes waste time and create new bugs. Systematic debugging fixes correctly on the first attempt 95% of the time.

---

## Phase 0: ESTABLISH BASELINE

**Run the existing test suite first.** Record pass/fail counts. Tests that already fail are NOT your regressions — note them and move on. This gives you: a baseline to compare against, a map of project health, and forces discovery of how to run tests.

## Phase 1: ROOT CAUSE INVESTIGATION

1. **Read error messages completely** — every line, every stack frame
2. **Reproduce consistently** — exact steps, every time
3. **Check recent changes** — `git diff`, `git log`, new dependencies, config changes
4. **Trace data flow backward** — from error to source through the call stack
5. **Gather evidence at boundaries** — log at each component boundary in multi-service systems

## Phase 2: PATTERN ANALYSIS

1. **Find working examples** — similar code in this codebase that works
2. **Compare completely** — diff against the reference implementation
3. **Identify ALL differences** — however small
4. **Understand dependencies** — what assumptions does the working code make?

## Phase 3: HYPOTHESIS & TEST

1. **Form ONE specific hypothesis:** "I think X is root cause because Y"
2. **Test minimally** — change one variable at a time
3. **Verify** — does the evidence support the hypothesis?
4. **If wrong:** Form a new hypothesis based on what you learned. Do NOT guess-and-check.

## Phase 4: IMPLEMENT FIX

1. **Write failing test** that reproduces the bug
2. **Implement single fix** addressing the root cause
3. **Run all tests** — verify fix works AND nothing else broke
4. **If 3+ fix attempts failed:** STOP. Question the architecture, not symptoms.

---

## Red Flags — STOP and return to Phase 1:

- "Quick fix for now, investigate later"
- "Just try changing X and see"
- "Skip the test, I'll manually verify"
- "It's probably X, let me fix that"
- "One more fix attempt" (after 2+ already failed)
- Each fix reveals a new problem in a different place

## Anti-Rationalization

| Your thought | Reality |
|---|---|
| "I know what's wrong, I'll just fix it" | If you knew, you wouldn't be debugging. Investigate first. |
| "This is a simple bug" | Simple bugs have simple root causes. Find it first, then fix. |
| "The fix is obvious from the error message" | Error messages describe symptoms, not causes. Trace the data flow. |
| "I'll add more logging and try again" | Logging is Step 5 of Phase 1. Do Steps 1-4 first. |

## Integration with Development Workflow

This skill enhances Phase 1 (Research) for debugging tasks. After root cause is found:
- Continue to Phase 2 (Plan) — plan the fix
- Follow remaining phases normally (Chronicle, Implement, Verify, Staff Review, Finalize)

When invoked standalone (`/debugging`): after investigation, announce root cause and proposed fix, then ask user if they want to proceed with the development workflow.

**Language-specific context:** If a language skill is active (python-dev, java-dev, etc.), also read its `patterns.md` during Phase 1. Team-specific patterns (Pydantic conventions, async idioms, framework configurations) provide crucial context for understanding why code behaves unexpectedly.
