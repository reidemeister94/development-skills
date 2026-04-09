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
- For adoption/integration tasks: what in the current stack already covers each proposed feature? Is this gap-driven or feature-driven?

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

**Adoption/integration exception:** If the task involves evaluating external projects, recommending features to adopt, or integrating patterns from other codebases — ALWAYS invoke brainstorming. The analysis agent MUST evaluate each candidate through this framework:

1. **Overlap audit** — List every existing mechanism that covers the same need. If overlap > 50%, reject.
2. **Value assessment** — What real problem does this solve? How often does it occur? What is the cost of NOT having it? If you can't name a concrete, recurring pain point, reject.
3. **Fit analysis** — Does it integrate naturally into the existing architecture, or does it require compromises, new dependencies, or new patterns? If it forces the project to bend around it, reject or redesign.
4. **Maintenance cost** — What is the ongoing cost of keeping this? Will it break when upstream changes? Does it add surface area that must be tested and documented? Value must clearly exceed maintenance burden.
5. **Implementation form** — If it survives 1-4, HOW should it be integrated? Minimal change to an existing file beats a new skill. A new convention beats a new hook. Configuration beats code.

Present the filtered shortlist with this analysis to the user BEFORE any implementation.

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
| "Project X has it, we should too" | Feature-driven, not gap-driven. What in OUR stack already covers this? |
| "User confirmed, so my analysis was correct" | User confirmed trust, not validation. Overlap audit still required. |
| "I found 4 good features to add" | Did you check 4 times what already exists? More recommendations ≠ better analysis. |

**Red flags:**
- About to say "Development workflow activated" before finishing this guard
- Classifying a multi-module change as "direct instruction"
- Feeling "confident" without considering alternatives
- Reading code before completing this guard
- Building a recommendation list without checking what already exists for each item
- Implementing multiple features in one pass without user validation of each
- Criticizing an external project for pattern X and then importing pattern X

**Default: invoke brainstorming.** Near-zero cost. Building the wrong thing is high cost.

**Return to core-dev SKILL.md Step 3.**
