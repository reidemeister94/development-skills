# development-skills — In-Depth Guide

Everything the README doesn't cover. How things work under the hood, why they're built this way, and how to get the most out of each part.

---

## The 7-Phase Workflow

When you give Claude a development task, the plugin enforces a mandatory gated workflow. Each phase must be explicitly passed before the next begins.

| # | Phase | What Happens | Gate |
|---|-------|-------------|------|
| 0 | **Brainstorming Guard** | Evaluates scope, reversibility, approach clarity. Triggers analysis if ambiguous | Automatic |
| 1 | **Research** | Explore the codebase and gather context | "RESEARCH COMPLETE" |
| 2 | **Plan** | Write a plan to disk, enter plan mode | User approves the plan |
| 3 | **Chronicle** | Document the WHY — business context, requirements, decisions | "CHRONICLE INITIATED" |
| 4 | **Implement** | TDD cycles with dedicated implementer subagent | "SOLUTION COMPLETE" |
| 5 | **Verify** | Dedicated test-verifier runs the full test suite | Evidence of passing |
| 6 | **Staff Review** | Two-stage code review: spec compliance, then quality | "APPROVED" |
| 7 | **Finalize** | Update docs, chronicle, integration options | "WORKFLOW COMPLETE" |

**Lightweight mode:** Tasks touching 3 files or fewer with a single obvious approach skip ceremony but keep quality checks.

---

## Key Features

### Brainstorming Guard

Before coding, evaluates scope, reversibility, and approach clarity. If anything is ambiguous, spawns an isolated analysis agent. The default is to analyze; burden of proof is on *skipping*.

Anti-rationalization tables counter the model's tendency to justify shortcuts. Without this guard, the agent skips analysis [~40% of the time](https://medium.com/@silvio.pavanetto/how-i-taught-agents-to-follow-a-process-not-just-write-code-b135b6573c54) on tasks that need it.

### Subagent Architecture

Three specialized agents:

- **Staff Reviewer** (Opus) — Two-stage code review: spec compliance first, then code quality
- **Implementer** (Sonnet) — TDD execution with anti-poisoning verification
- **Test Verifier** (Sonnet) — Structured pass/fail report, distinguishes real tests from lint-only

Mirrors Anthropic's [effective sub-agent patterns](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents). Giving agents a way to verify their own work [improves quality 2-3x](https://venturebeat.com/technology/the-creator-of-claude-code-just-revealed-his-workflow-and-developers-are).

### Observation Masking

Verbose tool output (80%+ of context tokens) stays on disk. Implementation logs, test output, and review criteria live in files — your main conversation stays clean for [decision-making](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents).

### Filesystem Persistence

Plans, chronicles, and workflow state survive context compaction. The agent resumes from any phase, even after a full context clear. Projects with persistent memory show [40% fewer errors and 55% faster completion](https://resources.anthropic.com/hubfs/2026%20Agentic%20Coding%20Trends%20Report.pdf).

### Smart Parallel Implementation

For 4+ independent tasks, analyzes file-touch maps and spawns parallel agents in git worktrees — but only when proven safe via dependency analysis. Naive parallelization [produced 100% unusable code](https://medium.com/@silvio.pavanetto/how-i-taught-agents-to-follow-a-process-not-just-write-code-b135b6573c54); single-agent is the safe default.

---

## Plans and Chronicles

Every task produces persistent artifacts on disk, numbered incrementally like SQL migrations.

### Numbering

Both plans and chronicles use a shared 4-digit zero-padded counter (`0001`, `0002`, ...) that increments per task. The plugin finds the highest existing number and adds 1. A task that gets both a plan and a chronicle shares the same prefix:

```
docs/plans/0042__research.md
docs/plans/0042__2026-03-15__implementation_plan__auth-refactor.md
docs/chronicles/0042__2026-03-15__auth-refactor.md
```

If merging branches creates duplicate numbers, the `resolve-merge` skill renumbers automatically.

### Plan Files

The single source of truth for a task. Created in Phase 2, updated through Phase 7. Sections accumulate:

| Phase | What gets added |
|-------|----------------|
| 1 | Research notes, codebase analysis |
| 2 | Implementation steps, task checklist |
| 3 | Chronicle reference |
| 4 | Implementation log, file-touch map, task completion |
| 5 | Verification results (test output) |
| 6 | Review log (feedback + fixes) |
| 7 | Status: Completed |

Subagents read from and write to the same plan file. When context compaction clears the conversation, the agent resumes by reading the plan — no progress is lost.

Each plan also has a companion **research file** (`NNNN__research.md`) written during brainstorming: web research with sources, codebase analysis, rejected alternatives with reasoning, and reusable code patterns found.

### Chronicles

Chronicles capture what code and plans don't — **WHY**.

A conversation with Claude disappears when the session ends. The prompts you gave, the business context behind a request, the trade-offs you discussed — gone. Chronicles preserve this:

- **User requirements** — the original request, complete, not summarized
- **Business context** — why this change matters, who asked for it, what constraint drives it
- **Decisions and rejected alternatives** — what was considered and why it was discarded
- **Discoveries** — unexpected findings during implementation, gotchas, patterns
- **Project state transitions** — before and after

**When a chronicle is created:**
- New feature or architectural change
- Complex bug fix with non-obvious root cause
- Breaking change or multi-file refactoring
- Significant business logic or research

**When it's NOT needed** (all must apply): single-line fix, no new patterns, self-evident from diff, no business context.

**Chronicle template:**

```markdown
# [Brief Title]

> Chronicle: 0042__2026-03-15__auth-refactor.md
> Status: Draft | In Progress | Completed

## User Requirements (Complete)
[FULL user communication — preserve ALL signal]

## Context
[Background, project state, technical context]

## Objective (The WHY)
[Business context, user needs, problems being solved]

## Affected Areas
| Area | Files/Modules | Impact |
|------|---------------|--------|

## Discoveries & Insights
- **[Date]**: [Discovery or insight added during implementation]
```

The chronicle is created in Phase 3, updated during Phase 4 (implementer appends discoveries), and finalized in Phase 7 (status set to Completed, "after" state filled in).

---

## Context Engineering

Implements patterns from Anthropic's [Context Engineering guide](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) and validated by [Manus](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus) across millions of production users:

- **Progressive disclosure** — phase instructions loaded just-in-time, not all at once
- **Observation masking** — verbose output on disk, condensed summaries in conversation
- **Filesystem as extended context** — plans, chronicles, workflow state, implementation logs
- **Clean subagent windows** — each agent gets only the context it needs
- **Anti-rationalization tables** — keep the model honest under pressure

Context is loaded progressively following Anthropic's [just-in-time pattern](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents): `workflow.md` always loaded (~120 lines), phase instructions loaded per-phase (~300 words each), language patterns loaded on-demand.

---

## Design Philosophy

**Iron Rules** — enforced at every phase, not suggested:

1. No positive claims without fresh verification evidence
2. Red/Green TDD — every implementation starts with a failing test
3. Comment the WHY, not the WHAT
4. No commits without explicit user request
5. Every gate must be explicitly passed

**Model Behavior** — maximum honesty (zero accommodation), always-on critical thinking, calibrated criticism (concrete and evidence-based), planning as 90% of the work, data-validated decisions, and persistent knowledge on disk.

---

## Architecture

```
skills/          25 skills (core-dev, 5 languages, brainstorming, debugging, testing, utilities, user-invocable)
agents/          3 subagents (implementer, staff-reviewer, test-verifier)
hooks/           Auto-format on Edit/Write (multi-language) + session context
shared/          Workflow engine with just-in-time phase loading
```

---

## Auto-Format on Save

A `PostToolUse` hook automatically formats files when Claude edits them:

| Language | Formatter | Fallback |
|----------|-----------|----------|
| Python | ruff | — |
| JS/TS/CSS/JSON | biome | prettier |
| Java | google-java-format | — |
| Kotlin | ktfmt | ktlint |
| Swift | swift-format | swiftformat |
| HTML/YAML | prettier | — |

---

## All Skills Reference

### Development

| Skill | Trigger | What It Does |
|-------|---------|-------------|
| `core-dev` | Auto | Workflow router — detects language, enforces brainstorming guard, dispatches |
| `brainstorming` | `/brainstorming` | Critical evaluation with isolated analysis agent |
| `python-dev` | `/python-dev` | Python patterns — Pydantic, FastAPI, asyncpg, pytest |
| `java-dev` | `/java-dev` | Java patterns — Records, Streams, Spring Boot, JPA |
| `typescript-dev` | `/typescript-dev` | TypeScript patterns — Zod, Express, Fastify, vitest |
| `frontend-dev` | `/frontend-dev` | Auto-detects React, Next.js, Raycast, Vite |
| `swift-dev` | `/swift-dev` | Swift patterns — SwiftUI, UIKit, Vapor, SPM |
| `debugging` | `/debugging` | Systematic root-cause debugging |

### Testing & Quality

| Skill | Trigger | What It Does |
|-------|---------|-------------|
| `create-test` | `/create-test` | Risk-scored test design with explorer and targeted modes |
| `roast-my-code` | `/roast-my-code` | Brutally honest code critique + AI-readiness audit (`--fix` to auto-fix) |
| `eval-regression` | `/eval-regression` | Pre-commit regression testing (30 evals, 98 assertions) |

### Utilities

| Skill | Trigger | What It Does |
|-------|---------|-------------|
| `commit` | `/commit` | Conventional commits from staged changes |
| `distill` | `/distill` | Semantic text compression with multilingual noise removal |
| `chronicles` | Auto | Project snapshots capturing the WHY behind changes |
| `align-docs` | `/align-docs` | Align documentation with current project state |
| `resolve-merge` | `/resolve-merge` | Systematic merge conflict resolution |
| `update-precommit` | `/update-precommit` | Update pre-commit hooks to latest versions |
| `update-reqs` | `/update-reqs` | Update requirements.in with latest PyPI versions |
| `update-reqs-dev` | `/update-reqs-dev` | Update requirements-dev.in with latest PyPI versions |
| `best-practices` | `/best-practices <topic>` | Deep web research producing structured state-of-the-art report |

---

## Regression Testing

**30 evals, 98 assertions** across 11 behavioral dimensions — a test suite for agent behavior. Powered by Anthropic's [`skill-creator`](https://github.com/anthropics/claude-plugins-official) plugin.

```
/eval-regression
```

Covers: brainstorming guard (7), smart isolation (6), anti-rationalization (4), performance review (3), workflow phases (3), implementer discipline (2), language detection, chronicle quality, turn boundaries, project directives, and AskUserQuestion avoidance.

Each eval snapshots the committed version as baseline, runs the modified version, and produces a verdict: **SAFE TO COMMIT** or **REGRESSIONS FOUND**.

Requires the `skill-creator` plugin:

```bash
/plugin install skill-creator@claude-plugins-official
```

---

## Further Reading

- [How I Taught Agents to Follow a Process, Not Just Write Code](https://medium.com/@silvio.pavanetto/how-i-taught-agents-to-follow-a-process-not-just-write-code-b135b6573c54) — the full story behind this plugin
- [Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — Anthropic's guide to the patterns we implement
- [Building Claude Code with Boris Cherny](https://newsletter.pragmaticengineer.com/p/building-claude-code-with-boris-cherny) — how the creator thinks about agent workflows
- [TDD, AI Agents and Coding with Kent Beck](https://newsletter.pragmaticengineer.com/p/tdd-ai-agents-and-coding-with-kent) — why testing matters more with AI
- [Agentic Engineering](https://addyosmani.com/blog/agentic-engineering/) — Addy Osmani on structured workflows
- [Context Engineering: Lessons from Manus](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus) — production-validated patterns
