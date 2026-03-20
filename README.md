# Development Skills

Unified development workflow plugin for Claude Code. Provides a mandatory 7-phase workflow (with lightweight mode for small tasks) for all coding tasks, with language-specific and framework-specific patterns for Python, Java, TypeScript, Swift, and frontend frameworks (React, Next.js, Raycast, Vite).

## Quick Start

The plugin activates automatically when Claude detects a development task. A SessionStart hook injects a lightweight context reminder at the beginning of every conversation. You can also invoke skills directly:

```
/python-dev          # Language-specific dev workflows
/java-dev
/typescript-dev
/frontend-dev
/swift-dev
/debugging           # Systematic root-cause debugging
/brainstorming       # Critical evaluation before implementation
/commit              # Conventional commit messages
/align-docs          # Align docs with current project state
/update-precommit    # Update pre-commit hooks to latest
/update-reqs         # Update requirements.in versions
/update-reqs-dev     # Update requirements-dev.in versions
/produce-feedback-dev-skills   # Generate feedback report from current conversation
/ingest-feedback-dev-skills    # Ingest feedback report and apply vetted changes
```

## Prerequisites

- **`skill-creator` plugin** — Required for creating and improving Claude Code skills. This is an official plugin from the Claude marketplace. It must be enabled in your `~/.claude/settings.json` under `enabledPlugins` as `"skill-creator@claude-plugins-official": true`. The project-level `.claude/settings.json` already declares this dependency.

## Skills

| Skill | Invocable | Description |
|-------|-----------|-------------|
| `core-dev` | auto | Thin workflow router (~75 lines): checks for in-progress plans, loads brainstorming guard from `routing-rules.md`, detects language, dispatches to correct skill. |
| `brainstorming` | `/brainstorming` | Requirements comprehension + critical evaluation: understands WHAT + WHY, proposes HOW, evaluates risks. Two modes: Full Analysis and Focused Evaluation. Standalone-capable. |
| `python-dev` | `/python-dev` | Python patterns (Pydantic, FastAPI, asyncpg) |
| `java-dev` | `/java-dev` | Java patterns (Records, Streams, Spring Boot) |
| `typescript-dev` | `/typescript-dev` | Pure TypeScript patterns (Zod, Express, Fastify) -- backend, CLI, libraries only |
| `frontend-dev` | `/frontend-dev` | Frontend framework patterns with auto-detection: React, Next.js, Raycast, Vite |
| `swift-dev` | `/swift-dev` | Swift patterns (SwiftUI, UIKit, Vapor, SPM) |
| `debugging` | `/debugging` | Systematic root-cause debugging: 4-phase methodology (investigate -> analyze -> hypothesize -> fix). Enhances Phase 1 for bug-fix tasks. |
| `chronicles` | auto | Project snapshots capturing the WHY behind changes -- full user context, decisions, discoveries, project state |
| `commit` | `/commit` | Conventional commits: analyzes staged changes and generates commit messages |
| `align-docs` | `/align-docs` | Align all relevant docs (CLAUDE.md, MEMORY.md, chronicles) with current project status and new discoveries |
| `update-precommit` | `/update-precommit` | Update `.pre-commit-config.yaml` hooks to latest versions from GitHub, preserving tag format |
| `update-reqs` | `/update-reqs` | Update `requirements.in` with latest PyPI versions, preserving version specifier patterns |
| `update-reqs-dev` | `/update-reqs-dev` | Update `requirements-dev.in` with latest PyPI versions, preserving version specifier patterns |

### Commands

| Command | Description |
|---------|-------------|
| `/produce-feedback-dev-skills` | Generate a factual chronicle of all plugin interactions in the current conversation. Writes to `docs/reports/`. |
| `/ingest-feedback-dev-skills` | Ingest a feedback report and critically evaluate each friction point against Core Pillars. Default verdict is SKIP — changes must earn their place. |

### Subagents

Custom subagents defined in `agents/`, spawned by skills during workflow phases:

| Agent | Model | Purpose |
|-------|-------|---------|
| `staff-reviewer` | opus | Two-stage code review: spec compliance (completeness) then code quality (simplification). Returns APPROVED, SPEC_ISSUES, or ISSUES with file:line references. |
| `implementer` | sonnet | All-task implementation with smart isolation (no worktree by default; worktree only for parallel orthogonal groups). Receives curated context (task list, plan summary, file paths). Test-first discipline, anti-poisoning verification, module refactoring discipline, verification honesty, writes artifact trail to plan file. |
| `test-verifier` | sonnet | Test/build/lint execution. Runs verification commands. Returns pass/fail summary with failure details. Verbose output stays in subagent context. |

Model tier philosophy: right-size for the task.
- **Opus**: Judgment-heavy work -- code review, research, analysis, critical evaluation
- **Sonnet**: Implementation and mechanical tasks -- following well-specified plans, running tests, collecting output
- **Explore (built-in)**: Codebase exploration (runs on Haiku for speed)

**Why Sonnet for implementation?** When the plan is well-specified (Phase 2 ensures this), implementation is primarily instruction-following, not reasoning about architecture. Sonnet handles this well at lower cost and faster speed. Opus is reserved for tasks requiring deep judgment.

### Frontend Framework Support

The `frontend-dev` skill auto-detects your framework from config files and `package.json` dependencies, then loads the appropriate pattern files:

| Framework | Pattern Files Loaded |
|-----------|---------------------|
| Next.js | `react.md` + `nextjs.md` |
| React + Vite | `react.md` + `vite.md` |
| Raycast | `react.md` + `raycast.md` |
| React (standalone) | `react.md` |

### Hooks

| Hook | Trigger | Purpose |
|------|---------|---------|
| `SessionStart` | startup, clear, compact | Injects lightweight plugin context reminder |
| `PostToolUse` | Edit, Write | Auto-formats the edited file using the best formatter per language |

**Auto-format — best-in-class formatters per language:**

| Language | Primary | Fallback | Why primary |
|----------|---------|----------|-------------|
| Python | ruff | — | 30x faster than Black, used by Django/FastAPI/pandas |
| JS/TS | biome | prettier | 7-100x faster than Prettier, Rust-based linter+formatter |
| Java | google-java-format | — | Standard standalone CLI formatter |
| Kotlin | ktfmt | ktlint | 40% faster than ktlint, adopted by Square/Block |
| Swift | swift-format | swiftformat | Official Apple toolchain (Xcode 16+) |
| CSS/JSON/GraphQL | biome | prettier | Same binary as JS/TS, native support |
| HTML/YAML/Vue | prettier | — | Biome YAML/HTML support still maturing |

## Architecture

### Shared Workflow Layer -- Progressive Disclosure

The 7-phase workflow uses a **progressive disclosure** architecture to minimize context overhead:

- **`shared/workflow.md`** -- Always loaded. Contains phase sequence, gate rules, Iron Rule (no claims without evidence), compaction guide. This is the L1 (always-loaded) layer.
- **`shared/phases/phase-N-*.md`** (~300 words avg) -- Loaded just-in-time when entering each phase. Contains detailed phase instructions. This is the L2 (on-demand) layer.
- **`skills/core-dev/routing-rules.md`** -- Loaded on-demand by core-dev for the brainstorming guard. Keeps core-dev SKILL.md thin (~75 lines).
- **`skills/brainstorming/templates/`** -- Research and plan file templates loaded on-demand by the analysis agent.

Each language skill provides only its language-specific configuration (verification commands, implementation rules, quality checklist items). This eliminates duplication and ensures all languages follow the same process.

### Subagent-Orchestrated Workflow

The main agent acts as a **thin orchestrator** -- it holds the plan and completion status while delegating vertical execution to specialized subagents:

- **Brainstorming:** The orchestrator spawns a **Task agent** for all heavy analysis (research, web search, code reading, critical evaluation). The agent's tokens stay completely isolated from the main conversation. Only the plan file on disk and a concise summary return to main context.
- **Phase 1 (Research):** Opus subagent for codebase exploration + web searches when gaps exist
- **Phase 2 (Plan):** Writes WORKFLOW STATE block for context recovery
- **Phase 4 (Implementation):** Task dependency analysis determines execution strategy: **single agent** (default, no worktree) when tasks share files, or **N parallel agents** (each in worktree) when tasks form orthogonal groups with zero file overlap. Curated context packages, test-first discipline, anti-poisoning verification, module refactoring discipline, verification honesty. Observation masking: verbose outputs go to plan file on disk, only compact summaries return to conversation.
- **Phase 5 (Verification):** `test-verifier` runs commands, returns summary. Full results persisted to plan file.
- **Phase 6 (Staff Review):** `staff-reviewer` reads plan file (artifact trail + verification results) and patterns.md, performs two-stage review
- **Phase 7 (Finalize):** Chronicle finalization, doc alignment, and **integration options** (merge locally, create PR, keep branch, or discard)

### Workflow Modes

**Full Mode (default):** All 7 phases with subagents, plan files, chronicles, and staff review. Implementation uses smart isolation: single agent in the working directory (default) or parallel agents in worktrees for orthogonal task groups. Used for non-trivial tasks.

**Lightweight Mode:** For genuinely small tasks (3 files or fewer, single approach, fully reversible, no brainstorming). Collapses phases: inline research, inline plan confirmation, no chronicle, direct implementation (no worktree), inline verification, no staff review. Exits to full mode if complexity is discovered.

### Workflow State Persistence

Three layers ensure quality gates survive "clear context and proceed":

1. **WORKFLOW STATE block** in the plan content (written at TOP of plan)
2. **Plan file on disk** at `docs/plans/` with Status and remaining phases
3. **Step 1 in core-dev** checks for in-progress plans FIRST (before the brainstorming guard) and resumes from correct phase

### Observation Masking

Tool outputs consume 80%+ of tokens in typical agent trajectories. The plugin uses **observation masking** to keep verbose outputs off the main conversation:

- Implementer writes `## Implementation Log` to plan file on disk, returns only a compact summary
- Test-verifier's verbose output stays in its subagent context; only pass/fail summary returns
- Staff-reviewer reads plan file directly from disk instead of receiving paraphrased summaries
- Full details are always available on disk for investigation when needed

### Relationship to Native `/simplify`

Claude Code has a built-in `/simplify` skill that spawns 3 parallel review agents. The plugin's staff-reviewer adds value beyond `/simplify`:
- **Spec compliance check** (Stage 1) — did implementation match the plan?
- **Plan-file awareness** — reads artifact trail, verification results, and clarifications from disk
- **Team standards enforcement** — reviews against language-specific patterns.md

For lightweight mode, consider using native `/simplify` instead of the full staff-reviewer.

### Automatic Routing

When you give Claude a development task, `core-dev` activates and evaluates:

1. **Scope** -- Will this change affect more than 3 files?
2. **Reversibility** -- Can this be fully undone in under 1 hour?
3. **Approaches** -- Is there only one obvious way to implement this?
4. **Motivation** -- Does the request state WHY?

If the task is large, hard to reverse, has multiple valid approaches, or involves a technical decision, `brainstorming` is invoked first. Otherwise, the task goes directly to the language-specific skill (in lightweight or full mode based on scope).

### Mandatory 7-Phase Workflow

Defined in `shared/workflow.md`. Every language skill references and follows this sequence -- each phase is a gate:

| Phase | Name | Description |
|-------|------|-------------|
| 1 | **Research** | Explore codebase + inline web research |
| 2 | **Plan** | Use EnterPlanMode with WORKFLOW STATE, persist to disk |
| 3 | **Chronicle** | Invoke `chronicles` to document context, user requirements, and objectives |
| 4 | **Implement** | Smart isolation: single agent (default) or N parallel agents for orthogonal task groups. Test-first discipline. |
| 5 | **Verify** | Delegate to `test-verifier` subagent |
| 6 | **Staff Review** | Two-stage: spec compliance then code quality |
| 7 | **Finalize** | Chronicle, docs, and integration (merge/PR/keep/discard) |

### Brainstorming

Activated for non-trivial tasks and technical decisions. Two modes:

All analysis runs in an **isolated Task agent** -- tokens stay completely separate from the main conversation. The orchestrator in the main context only handles: finding the agent prompt, spawning the agent, displaying results, and routing based on user choice. After analysis, the user chooses: **Proceed** (starts dev workflow), **Adjust** (modify approach), **Standalone** (analysis only), or **Abandon**.

**Full Analysis** (business requirements, new features):
1. Comprehends WHAT the user wants and WHY
2. Challenges the problem framing with first-principles thinking (is this the right problem?)
3. Identifies gaps and assumptions
4. Asks clarifying questions (zero-ambiguity policy)
5. Performs inline web research (isolated in forked context)
6. Proposes 1-2 approaches
7. Critically evaluates using the analysis framework
8. Presents final approach for user approval
9. Writes implementation plan to `docs/plans/` if proceeding

**Focused Evaluation** (specific technical decisions):
1. Restates the decision
2. Performs inline web research
3. Scores complexity and applies critical analysis
4. Delivers verdict with options

Verdicts: **PROCEED**, **PROCEED WITH CHANGES**, **RECONSIDER**, or **STOP**.

### Chronicles

Project snapshots that capture the WHY behind changes -- full user requirements, business context, decisions made, discoveries, and project state before/after. Stored in `docs/chronicles/` with timestamps. Chronicles sit above code and plan docs in the abstraction hierarchy: code shows WHAT changed, plans show HOW, chronicles capture WHY and the full context of what happened. Not created for trivial single-line fixes.
