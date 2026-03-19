---
name: core-dev
description: "Use when any coding, development, analysis, debugging, or code-related task is detected. Triggers on: implementing features, fixing bugs, refactoring code, reviewing diffs, investigating errors, evaluating approaches, or making architecture decisions."
user-invocable: false
allowed-tools: Glob, Read, Bash, Task, Skill, EnterPlanMode, Edit, Write
---

# Development Workflow Director

## Pre-Step D: Project Directives (ONE-TIME SETUP)

**Before any workflow logic, ensure the project's CLAUDE.md contains the team's universal directives.**

1. Read the project's `CLAUDE.md` (at the project root). If it doesn't exist, create it.
2. Search for the heading `## MANDATORY: Read Before Any Task - Directives and guidelines for working on this project`.
3. **If found** → skip (already set up).
4. **If not found** → read `shared/references/project-directives.md` (use Glob to find `**/project-directives.md` if path is unknown). Append everything **after the `---` separator** (the actual directives, starting from `## MANDATORY: Read Before Any Task - Directives and guidelines for working on this project`) to the bottom of the project's `CLAUDE.md`. Preserve any existing content. Include `<!-- development-skills v0.0.1 directives -->` as the first line of the appended block so future plugin versions can detect and update stale content.
5. Announce: "Project directives added to CLAUDE.md."
This runs once per project — the heading itself is the detection mechanism.

---

## Pre-Step C: Check for In-Progress Workflow (CHECK FIRST)

**Before anything else, check if a plan already exists.**

Run: `bash scripts/find-plan.sh active` (use Glob to find `**/find-plan.sh` if the path is unknown, or check `docs/plans/` directly).

- If output starts with `ACTIVE_PLAN:` -- an in-progress workflow exists. **Skip Pre-Step A entirely.**
  1. Read the plan file to recover full context (WORKFLOW STATE, Research path, Chronicle path)
  2. **Brainstorming-created plans** (has "Brainstorming Summary" section): Start from Phase 1 (lightweight -- reads existing research, fills gaps only)
  3. **Non-brainstorming plans** at Phase 2 with user saying proceed: Treat as plan approval, advance to Phase 3
  4. Announce: "Resuming workflow from Phase [N] based on `[filename]`."
  5. **Skip language detection (Step 1)** -- the plan already specifies the language
  6. **STILL invoke the language skill (Step 2)** -- REQUIRED for workflow instructions
- If `NO_ACTIVE_PLAN` -- proceed to Pre-Step A.

---

## Pre-Step A: Brainstorming Guard

**DEFAULT ACTION: Invoke brainstorming.** You must actively PROVE this task does not need brainstorming before proceeding without it. The burden of proof is on SKIPPING, not on activating.

**STOP.** Before announcing yourself, before identifying the language, before doing anything: complete this guard.

### Step 0: Request Sense Check + First-Principles Challenge

Before evaluating scope and approach, evaluate WHETHER the request itself is sound — and whether it targets the right problem.

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

**If issues found:** STOP. State concretely what doesn't add up. Ask the developer to clarify or reconsider. Do NOT proceed with a request that has fundamental problems or targets the wrong problem.

**If sound:** Continue to Step 1.

**Anti-rationalization for Step 0:**

| Your thought | Reality |
|---|---|
| "The developer knows their codebase better than I do" | They know the code; they may not see the flaw in their reasoning. |
| "It's not my place to question the approach" | It IS your place. The team configured this plugin for critical evaluation. |
| "The request is clear enough, I'll figure out issues during implementation" | Issues in the request become compounding errors in the code. |
| "The developer seems confident, so the request is probably sound" | Confidence ≠ correctness. Evaluate the reasoning, not the tone. |
| "The developer already decided the approach" | Decisions need validation. First-principle thinking means questioning the approach, not just the implementation details. |
| "Challenging the request will slow things down" | Building the wrong thing is the slowest outcome. A 30-second challenge saves hours of wasted work. |

### Step 1: Answer these 4 questions

1. **Scope:** Will this change affect more than 3 files?
2. **Reversibility:** Can this be fully undone in under 1 hour?
3. **Approaches:** Is there only ONE obvious way to implement this?
4. **Motivation:** Does the request state WHY this change is needed?

### Step 2: Route based on answers

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

### Step 3: Anti-rationalization check

| Your thought | Reality |
|---|---|
| "This is a direct technical instruction" | Check scope and reversibility, not grammar. "Separate the database connectors" is architectural. |
| "The user said exactly what to do" | Knowing WHAT does not mean only one HOW. Multiple approaches = invoke brainstorming. |
| "I can figure it out during research" | Research explores the codebase. Brainstorming explores the approach. Different purposes. |
| "It's straightforward" | If it touches settings, lifespan, DI, and repositories, it is not straightforward. |
| "I already have a good approach in mind" | Your first approach is not necessarily the best. Brainstorming runs in a fork -- costs nothing. |
| "The user said 'just do it'" | If they explicitly said "skip brainstorming" -- honor it (user bypass). Otherwise, check 4 questions first, takes 10 seconds. |
| "I already know this codebase well" | Familiarity with the codebase does not mean knowing the best approach for THIS specific change. |
| "This is just analysis/investigation" | Analysis of code changes, diffs, and approaches IS a development task. Route to brainstorming. |

### Step 4: Red flags

- About to say "Development workflow activated" before finishing this guard
- Classifying a multi-module change as "direct technical instruction"
- Feeling "confident" about the approach without having considered alternatives
- Skipping this guard because the request "sounds simple"
- Running git diff, reading code files, or doing any analysis before completing this guard

**Default: invoke brainstorming.** The cost is near-zero (isolated subagent). The cost of building the wrong thing is high.

---

## Post-Brainstorming Handler

After brainstorming returns:

- **If brainstorming invoked core-dev (Proceed path):** Pre-Step C handles it.
- **If `USER CHOICE: PASS_THROUGH` or `BRAINSTORM_RESULT::PASS_THROUGH`:** Proceed to language detection. Announce: "Development workflow activated."
- **If brainstorming returned Standalone/Abandon:** STOP core-dev. Return control to user.
- **If unexpected format:** Present output and ask user (1. Proceed, 2. Adjust, 3. Stop).

---

## Workflow Mode Selection

After the brainstorming guard completes:

**LIGHTWEIGHT MODE** applies if ALL:
- Scope is 3 files or fewer
- Single obvious approach
- Fully reversible
- Brainstorming was NOT invoked

If lightweight, pass `LIGHTWEIGHT_MODE=true` as context when invoking the language skill.

---

## Step 1: Identify Project Language/Framework

Check in this order (first match wins):

1. `*.py`, `requirements*.txt`, `pyproject.toml`, `setup.py`, `Makefile` with Python targets -> **Python**
2. `*.java`, `pom.xml`, `build.gradle`, `*.kt` -> **Java**
3. `*.swift`, `Package.swift`, `*.xcodeproj` -> **Swift**
4. **Frontend detection** (check BEFORE generic TypeScript):
   - `next.config.*`, or `app/` directory with `layout.tsx`/`page.tsx` -> **Frontend (Next.js)**
   - `@raycast/api` in `package.json` deps -> **Frontend (Raycast)**
   - `vite.config.*` + (`react` in deps) -> **Frontend (Vite + framework)**
   - `*.tsx`/`*.jsx` + `react` in `package.json` deps -> **Frontend (React)**
5. `*.ts`, `tsconfig.json`, `package.json` with TypeScript deps (no frontend framework signals) -> **TypeScript**

**Note:** Any project with a frontend UI framework MUST use frontend-dev, NOT typescript-dev.

## Step 2: Invoke Language Skill (REQUIRED)

| Language/Framework | Skill to invoke |
|----------|----------------|
| Python | `development-skills:python-dev` |
| Java | `development-skills:java-dev` |
| Swift | `development-skills:swift-dev` |
| Frontend (any) | `development-skills:frontend-dev` |
| TypeScript (pure) | `development-skills:typescript-dev` |

**Do NOT write any code before invoking the language skill.** The language skill loads the mandatory workflow that governs ALL development work.

If the language skill is already in your context: defer to it. Do NOT re-invoke.
