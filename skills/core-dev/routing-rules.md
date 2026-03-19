# Brainstorming Guard — Routing Rules

**DEFAULT: invoke brainstorming.** You must actively PROVE this task does not need brainstorming before proceeding without it.

---

## Step 0: Request Sense Check + First-Principles Challenge

Before evaluating scope and approach, evaluate WHETHER the request itself is sound.

**Sense check:**
- Does the request contain contradictions or assumptions that may not hold?
- Is the developer solving a symptom instead of the root cause?
- Is the developer's reasoning flawed or based on a misunderstanding?
- Is critical context missing that the developer may not realize they need?

**First-principles challenge:**
- Strip away the proposed solution: what is the actual problem? What outcome does the developer need?
- Is the developer anchored on a specific approach? Would they reach the same solution if they started from scratch?
- What is the simplest path to the desired outcome? Does the request introduce unnecessary complexity?
- What happens if we do nothing? If the cost of inaction is low, the request might not be worth the complexity.

**If issues found:** STOP. State concretely what doesn't add up. Ask the developer to clarify or reconsider. Do NOT proceed with a request that has fundamental problems.

**If sound:** Continue to Step 1.

---

## Step 1: Answer these 4 questions

1. **Scope:** Will this change affect more than 3 files?
2. **Reversibility:** Can this be fully undone in under 1 hour?
3. **Approaches:** Is there only ONE obvious way to implement this?
4. **Motivation:** Does the request state WHY this change is needed?

---

## Step 2: Route based on answers

**Invoke brainstorming (via Skill tool `development-skills:brainstorming`) if ANY of these are true:**

**CRITICAL:** Brainstorming runs in a forked context with NO conversation history. Pass the user's complete request as the `args` parameter.

- Q1 = YES (large scope)
- Q2 = NO (hard to reverse)
- Q3 = NO (multiple valid approaches exist)
- Q4 = NO and the WHY matters for choosing the right approach
- The request asks "should we...", "what approach...", or "how should we handle..." (decision question)
- Technology selection, design pattern choice, or migration strategy question
- The request asks to analyze, investigate, or evaluate code changes, diffs, or errors

**Bug fix exception:** If the task is primarily a bug fix (error/stack trace, "fix this bug", "debug this"), invoke `development-skills:debugging` instead -- UNLESS the bug involves architectural decisions or multiple valid fix approaches. Pass the full error context as args.

**User bypass:** If the user explicitly says "skip brainstorming", "just code it", or "I already know the approach", respect it -- proceed to language detection directly. Note: "I want it done fast" or "hurry" is NOT a bypass -- urgency does not override the guard.

**Proceed without brainstorming ONLY if ALL of:**
- Scope is small (1-3 files)
- Fully reversible in under 1 hour
- ONE obvious approach, no meaningful alternatives
- WHY doesn't affect the implementation choice

---

## Step 3: Anti-rationalization check

| Your thought | Reality |
|---|---|
| "This is a direct technical instruction" | Check scope and reversibility, not grammar. "Separate the database connectors" is architectural. |
| "The user said exactly what to do" | Knowing WHAT does not mean only one HOW. Multiple approaches = invoke brainstorming. |
| "I can figure it out during research" | Research explores the codebase. Brainstorming explores the approach. Different purposes. |
| "It's straightforward" | If it touches settings, lifespan, DI, and repositories, it is not straightforward. |
| "I already have a good approach in mind" | Your first approach is not necessarily the best. Brainstorming runs in a fork -- costs nothing. |
| "This is just analysis/investigation" | Analysis of code changes, diffs, and approaches IS a development task. Route to brainstorming. |

**Red flags** -- if you notice yourself:
- About to say "Development workflow activated" before finishing this guard
- Classifying a multi-module change as "direct technical instruction"
- Feeling "confident" about the approach without having considered alternatives
- Running git diff, reading code files, or doing any analysis before completing this guard

**Default: invoke brainstorming.** The cost is near-zero (isolated subagent). The cost of building the wrong thing is high.

**Return to core-dev SKILL.md Step 3 after completing this guard.**
