# Brainstorming Guard — Routing Rules

**DEFAULT: invoke brainstorming.** You must PROVE the task doesn't need it.

---

## Step 0: Request Sense Check + First-Principles Challenge

**Sense check:**
- Does the request contain contradictions or unsound assumptions?
- Is the developer solving a symptom instead of root cause?
- Is the developer's reasoning flawed?
- Is critical context missing?

**First-principles challenge:**
- Strip the proposed solution: what is the actual problem?
- Is the developer anchored on a specific approach?
- What is the simplest path to the desired outcome?
- What happens if we do nothing?

**If issues found:** STOP. State what doesn't add up. Ask to clarify.

**If sound:** Continue to Step 1.

---

## Step 1: Answer 4 questions

1. **Scope:** Will this affect more than 3 files?
2. **Reversibility:** Can this be fully undone in under 1 hour?
3. **Approaches:** Is there only ONE obvious way?
4. **Motivation:** Does the request state WHY?

---

## Step 2: Route

**Invoke brainstorming (`development-skills:brainstorming`) if ANY true:**

**CRITICAL:** Brainstorming runs in a forked context with NO history. Pass the user's complete request as `args`.

- Q1 = YES (large scope)
- Q2 = NO (hard to reverse)
- Q3 = NO (multiple valid approaches)
- Q4 = NO and WHY matters for choosing the approach
- Decision question ("should we...", "what approach...", "how should we handle...")
- Technology selection, design pattern choice, migration strategy
- Analyzing/investigating/evaluating code changes, diffs, errors

**Bug fix exception:** If primarily a bug fix (error/stack trace), invoke `development-skills:debugging` instead — UNLESS it involves architectural decisions or multiple fix approaches.

**Test-focused exception:** If the request is primarily about test creation, test quality, test strategy, or test coverage analysis (e.g., "add tests for X", "what should I test", "improve test quality", "explore untested code", "generate boundary tests") — invoke `development-skills:create-test` instead. UNLESS the request is part of a larger feature implementation (standard workflow handles tests via TDD).

**User bypass:** "skip brainstorming", "just code it", "I already know the approach" — respect it. "I want it done fast" is NOT a bypass.

**Proceed without brainstorming ONLY if ALL:**
- Small scope (1-3 files)
- Fully reversible in under 1 hour
- ONE obvious approach
- WHY doesn't affect the choice

---

## Step 3: Anti-rationalization

| Your thought | Reality |
|---|---|
| "Direct technical instruction" | Check scope and reversibility. "Separate the database connectors" is architectural. |
| "User said exactly what to do" | WHAT ≠ HOW. Multiple approaches = brainstorm. |
| "I can figure it out during research" | Research explores codebase. Brainstorming explores approach. Different. |
| "It's straightforward" | Touching settings, lifespan, DI, and repositories is not straightforward. |
| "I already have a good approach" | First approach ≠ best. Brainstorming costs nothing. |
| "Just analysis/investigation" | Analysis of changes and approaches IS development. Route to brainstorming. |

**Red flags:**
- About to say "Development workflow activated" before finishing this guard
- Classifying a multi-module change as "direct instruction"
- Feeling "confident" without considering alternatives
- Reading code before completing this guard

**Default: invoke brainstorming.** Near-zero cost. Building the wrong thing is high cost.

**Return to core-dev SKILL.md Step 3.**
