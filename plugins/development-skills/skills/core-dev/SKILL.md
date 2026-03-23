---
name: core-dev
description: "Use when any coding, development, analysis, debugging, or code-related task is detected. Triggers on: implementing features, fixing bugs, refactoring code, reviewing diffs, investigating errors, evaluating approaches, or making architecture decisions."
user-invocable: false
allowed-tools: Glob, Read, Bash, Task, Skill, EnterPlanMode, Edit, Write
---

# Development Workflow Director

**DEFAULT ACTION: Invoke brainstorming.** The burden of proof is on SKIPPING brainstorming, not on activating it.

---

## Step 1: Check for In-Progress Workflow (FIRST)

Check `docs/plans/` for an active plan: `Grep("Status: In Progress", path="docs/plans/", glob="*.md")`. If `docs/plans/` doesn't exist, skip — no active plan.

- **`ACTIVE_PLAN:`** -- in-progress workflow exists. **Skip the brainstorming guard entirely.**
  1. Read the plan file to recover full context (WORKFLOW STATE, Research path, Chronicle path)
  2. **Brainstorming-created plans** (has "Brainstorming Summary" section): Start from Phase 1 (lightweight -- reads existing research, fills gaps only)
  3. **Non-brainstorming plans** at Phase 2 with user saying proceed: Treat as plan approval, advance to Phase 3
  4. Announce: "Resuming workflow from Phase [N] based on `[filename]`."
  5. **Skip language detection** -- the plan already specifies the language
  6. **STILL invoke the language skill** -- REQUIRED for workflow instructions
- **`NO_ACTIVE_PLAN`** -- proceed to Step 2.

---

## Step 2: Brainstorming Guard

**STOP.** Before announcing yourself, before identifying the language, before doing anything: complete this guard.

Read `routing-rules.md` in this skill's directory (use Glob to find `**/core-dev/routing-rules.md`). Follow ALL instructions there. Return here after the guard completes.

---

## Step 3: Post-Brainstorming Handler

After brainstorming returns:

- **If brainstorming invoked core-dev (Proceed path):** Step 1 handles it via active plan detection.
- **If `USER CHOICE: PASS_THROUGH` or `BRAINSTORM_RESULT::PASS_THROUGH`:** Proceed to Step 4. Announce: "Development workflow activated."
- **If brainstorming returned Standalone/Abandon:** STOP core-dev. Return control to user.
- **If unexpected format:** Present output and ask user (1. Proceed, 2. Adjust, 3. Stop).

---

## Step 4: Workflow Mode Selection

**LIGHTWEIGHT MODE** applies if ALL:
- Scope is 3 files or fewer
- Single obvious approach
- Fully reversible
- Brainstorming was NOT invoked

If lightweight, pass `LIGHTWEIGHT_MODE=true` as context when invoking the language skill.

---

## Step 5: Identify Project Language/Framework

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

## Step 6: Invoke Language Skill (REQUIRED)

| Language/Framework | Skill to invoke |
|----------|----------------|
| Python | `development-skills:python-dev` |
| Java | `development-skills:java-dev` |
| Swift | `development-skills:swift-dev` |
| Frontend (any) | `development-skills:frontend-dev` |
| TypeScript (pure) | `development-skills:typescript-dev` |

**Do NOT write any code before invoking the language skill.** The language skill loads the mandatory workflow that governs ALL development work.

If the language skill is already in your context: defer to it. Do NOT re-invoke.
