# Development Skills

Unified development workflow plugin for Claude Code. Provides a mandatory 7-phase workflow (with lightweight mode for small tasks), language-specific patterns for Python, Java, TypeScript, Swift, and frontend frameworks (React, Next.js, Raycast, Vite).

## Quick Start

The plugin activates automatically on development tasks. A SessionStart hook injects context at conversation start. Direct invocation:

```
/python-dev          /java-dev            /typescript-dev
/frontend-dev        /swift-dev           /debugging
/brainstorming       /commit              /align-docs
/create-test         /distill             /update-precommit
/update-reqs         /update-reqs-dev     /eval-regression
/produce-feedback-dev-skills   /ingest-feedback-dev-skills
```

## Prerequisites

- **`skill-creator` plugin** — Required. Enable in `~/.claude/settings.json` under `enabledPlugins` as `"skill-creator@claude-plugins-official": true`.

## Skills

| Skill | Invocable | Description |
|-------|-----------|-------------|
| `core-dev` | auto | Thin workflow router: checks in-progress plans, loads brainstorming guard, detects language, dispatches to skill. |
| `brainstorming` | `/brainstorming` | Requirements comprehension + critical evaluation. Two modes: Full Analysis and Focused Evaluation. Standalone-capable. |
| `python-dev` | `/python-dev` | Python patterns (Pydantic, FastAPI, asyncpg) |
| `java-dev` | `/java-dev` | Java patterns (Records, Streams, Spring Boot) |
| `typescript-dev` | `/typescript-dev` | Pure TypeScript patterns (Zod, Express, Fastify) — backend/CLI/libraries only |
| `frontend-dev` | `/frontend-dev` | Frontend patterns with auto-detection: React, Next.js, Raycast, Vite |
| `swift-dev` | `/swift-dev` | Swift patterns (SwiftUI, UIKit, Vapor, SPM) |
| `debugging` | `/debugging` | Systematic root-cause debugging: investigate -> analyze -> hypothesize -> fix |
| `chronicles` | auto | Project snapshots capturing the WHY behind changes |
| `commit` | `/commit` | Conventional commits from staged changes |
| `align-docs` | `/align-docs` | Align docs with current project state |
| `distill` | `/distill` | Semantic text compression via information theory. Measures entropy via gzip. See [theory doc](skills/distill/references/distill-theory.md). |
| `update-precommit` | `/update-precommit` | Update `.pre-commit-config.yaml` hooks to latest versions |
| `update-reqs` | `/update-reqs` | Update `requirements.in` with latest PyPI versions |
| `update-reqs-dev` | `/update-reqs-dev` | Update `requirements-dev.in` with latest PyPI versions |
| `create-test` | `/create-test` | Intelligent test design: explores untested code, generates boundary/property/invariant/golden-fixture tests. Two modes: explorer (codebase audit) and targeted (specific file). |
| `eval-regression` | `/eval-regression` | Pre-commit regression testing. Compares current vs committed version using skill-creator evals. |

### Commands

| Command | Description |
|---------|-------------|
| `/produce-feedback-dev-skills` | Generate factual chronicle of all plugin interactions. Writes to `docs/reports/`. |
| `/ingest-feedback-dev-skills` | Ingest feedback report, critically evaluate each friction point. Default verdict: SKIP. |

### Subagents

| Agent | Model | Purpose |
|-------|-------|---------|
| `staff-reviewer` | opus | Two-stage code review: spec compliance then quality. Returns APPROVED, SPEC_ISSUES, or ISSUES with file:line refs. |
| `implementer` | sonnet | All-task implementation with smart isolation. Test-first discipline, anti-poisoning verification, verification honesty. |
| `test-verifier` | sonnet | Runs verification commands. Returns pass/fail summary with failure details. |

Model tier: **Opus** for judgment (review, research, analysis). **Sonnet** for implementation (following well-specified plans). **Explore** for codebase exploration (Haiku).

### Frontend Framework Support

`frontend-dev` auto-detects from config files and `package.json`:

| Framework | Pattern Files Loaded |
|-----------|---------------------|
| Next.js | `react.md` + `nextjs.md` |
| React + Vite | `react.md` + `vite.md` |
| Raycast | `react.md` + `raycast.md` |
| React (standalone) | `react.md` |

### Hooks

| Hook | Trigger | Purpose |
|------|---------|---------|
| `SessionStart` | startup, clear, compact | Injects lightweight plugin context |
| `PostToolUse` | Edit, Write | Auto-formats edited file per language |

**Auto-format per language:**

| Language | Primary | Fallback | Why |
|----------|---------|----------|-----|
| Python | ruff | — | 30x faster than Black |
| JS/TS | biome | prettier | 7-100x faster, Rust-based |
| Java | google-java-format | — | Standard CLI formatter |
| Kotlin | ktfmt | ktlint | 40% faster |
| Swift | swift-format | swiftformat | Official Apple toolchain |
| CSS/JSON/GraphQL | biome | prettier | Same binary as JS/TS |
| HTML/YAML/Vue | prettier | — | Biome support still maturing |

## Architecture

### Progressive Disclosure

- **`shared/workflow.md`** — Always loaded. Phase sequence, gate rules, Iron Rules, compaction guide.
- **`shared/phases/phase-N-*.md`** (~300 words avg) — Loaded just-in-time per phase.
- **`skills/core-dev/routing-rules.md`** — Loaded on-demand for brainstorming guard.
- **`skills/brainstorming/templates/`** — Research and plan templates loaded on-demand.

Each language skill provides only language-specific config (verification commands, implementation rules, quality checklist). No duplication.

### Subagent-Orchestrated Workflow

The main agent is a **thin orchestrator** — holds the plan and completion status, delegates to subagents:

- **Brainstorming:** Task agent for analysis (research, web search, code reading, evaluation). Tokens isolated from main context. Only plan file + summary return.
- **Phase 1 (Research):** Opus subagent for exploration + web searches
- **Phase 2 (Plan):** Writes WORKFLOW STATE block for context recovery
- **Phase 4 (Implementation):** Task dependency analysis determines strategy: **single agent** (default, no worktree) for shared files, or **N parallel agents** (worktrees) for orthogonal groups. Observation masking: verbose output to plan file, compact summaries to conversation.
- **Phase 5 (Verification):** `test-verifier` runs commands, returns summary
- **Phase 6 (Staff Review):** `staff-reviewer` reads plan file + patterns.md, two-stage review
- **Phase 7 (Finalize):** Chronicle, doc alignment, integration options (merge/PR/keep/discard)

### Workflow Modes

**Full Mode (default):** All 7 phases with subagents, plan files, chronicles, staff review. Smart isolation for implementation.

**Lightweight Mode:** For small tasks (3 files or fewer, single approach, fully reversible, no brainstorming). Collapses phases: inline research/plan/verify, no chronicle, no subagents. Exits to full mode if complexity discovered.

### Workflow State Persistence

Three layers ensure gates survive context clearing:
1. **WORKFLOW STATE block** at top of plan file
2. **Plan file on disk** at `docs/plans/` with status and remaining phases
3. **Step 1 in core-dev** checks for in-progress plans first

### Observation Masking

Tool outputs consume 80%+ of tokens. The plugin keeps verbose outputs off the main conversation:
- Implementer writes `## Implementation Log` to plan file, returns compact summary
- Test-verifier's verbose output stays in subagent context
- Staff-reviewer reads plan file directly from disk
- Full details always available on disk

### Relationship to Native `/simplify`

The staff-reviewer adds beyond `/simplify`: spec compliance check, plan-file awareness, team standards enforcement. For lightweight mode, consider native `/simplify` instead.

### Automatic Routing

`core-dev` evaluates: **Scope** (>3 files?), **Reversibility** (<1 hour to undo?), **Approaches** (single obvious way?), **Motivation** (WHY stated?). Large, irreversible, multi-approach, or unmotivated tasks invoke brainstorming first.

### Mandatory 7-Phase Workflow

| Phase | Name | Description |
|-------|------|-------------|
| 1 | **Research** | Explore codebase + inline web research |
| 2 | **Plan** | EnterPlanMode with WORKFLOW STATE, persist to disk |
| 3 | **Chronicle** | Document context, requirements, objectives |
| 4 | **Implement** | Smart isolation: single or parallel agents. Test-first. |
| 5 | **Verify** | Delegate to `test-verifier` |
| 6 | **Staff Review** | Spec compliance then code quality |
| 7 | **Finalize** | Chronicle, docs, integration |

### Brainstorming

Two modes, all analysis in an **isolated Task agent**:

**Full Analysis** (business requirements, new features): Comprehend WHAT+WHY → challenge framing → identify gaps → clarify → research → propose 1-2 approaches → evaluate → plan to disk. Verdicts: PROCEED, PROCEED WITH CHANGES, RECONSIDER, STOP.

**Focused Evaluation** (technical decisions): Restate → research → score complexity → evaluate → verdict.

After analysis, user chooses: Proceed, Adjust, Standalone, or Abandon.

### Chronicles

Project snapshots capturing WHY changes happened — user requirements, business context, decisions, discoveries, project state. Code = WHAT, Plans = HOW, Chronicles = WHY. Not created for trivial fixes.
