# Development Skills

**A structured development workflow that makes Claude Code produce staff-engineer-quality code.**

Without structure, Claude Code skips verification, doesn't plan, writes before thinking, and never reviews its own work. This plugin fixes that by enforcing a 7-phase workflow with specialized subagents — a brainstorming analyst, an implementer with TDD discipline, a test verifier, and a staff-engineer code reviewer — that run in isolated contexts so your main conversation stays clean.

Built from months of real production development with Claude Code across Python, Java, TypeScript, Swift, and frontend projects. Every rule in this plugin exists because we hit the failure mode it prevents.

---

## What You Get

**Before this plugin:** You ask Claude to implement a feature. It starts coding immediately, misses edge cases, skips tests, and declares "done" without verification. You find bugs in review.

**After this plugin:**

1. **Brainstorming guard** evaluates every request — challenges flawed premises, identifies when multiple approaches exist, prevents building the wrong thing
2. **Research phase** explores the codebase and web in an isolated subagent (zero token cost to your main context)
3. **Plan** is written, persisted to disk, and requires your explicit approval before any code is written
4. **Chronicle** captures the WHY behind changes — months later you'll know why code exists, not just what it does
5. **Implementation** runs in a single subagent with TDD discipline (RED/GREEN/REFACTOR), anti-hallucination checks, and progress tracking on disk
6. **Verification** delegates to a test-runner subagent — pass/fail evidence, not "it should work"
7. **Staff review** — a separate Opus-powered subagent performs two-stage code review: spec compliance first, then quality with simplification as the primary mandate

Every phase is a gate. The workflow cannot skip phases, cannot claim completion without evidence, and persists all state to disk so it survives context compaction.

---

## Quick Start

### Install the plugin

```bash
claude install-plugin github:reidemeister94/development-skills
```

### Add to your project's CLAUDE.md

```markdown
ALWAYS invoke the "development-skills" plugin for ALL work on this project -- including analysis, investigation, diff review, error debugging, approach evaluation, brainstorming, development, bug fixing, new features, and any code-related work.
```

### That's it

Give Claude a development task. The plugin activates automatically via `core-dev` and routes to the correct language skill and workflow mode.

---

## Skills

| Skill | Trigger | What it does |
|-------|---------|-------------|
| **core-dev** | Any coding task | Thin router: brainstorming guard, language detection, workflow mode selection |
| **brainstorming** | `/brainstorming` | Critical evaluation of approaches. Runs in isolated subagent. Outputs: researched plan + approach options |
| **python-dev** | `/python-dev` | Python workflow (Pydantic, FastAPI, asyncpg, pytest, ruff) |
| **java-dev** | `/java-dev` | Java workflow (Records, Streams, Spring Boot, Maven/Gradle) |
| **typescript-dev** | `/typescript-dev` | TypeScript workflow (Zod, Express, Fastify, vitest/jest) -- backend/CLI only |
| **frontend-dev** | `/frontend-dev` | Frontend workflow with auto-detection: React, Next.js, Raycast, Vite |
| **swift-dev** | `/swift-dev` | Swift workflow (SwiftUI, UIKit, Vapor, SPM, XCTest) |
| **debugging** | `/debugging` | Systematic 4-phase root-cause methodology. No fixes without investigation first |
| **chronicles** | Auto | Project snapshots capturing WHY -- full user context, decisions, discoveries |
| **commit** | `/commit` | Conventional commits from staged changes |
| **align-docs** | `/align-docs` | Align all project docs with current disk state |
| **update-precommit** | `/update-precommit` | Update `.pre-commit-config.yaml` hooks to latest GitHub versions |
| **update-reqs** | `/update-reqs` | Update `requirements.in` to latest PyPI versions |
| **update-reqs-dev** | `/update-reqs-dev` | Update `requirements-dev.in` to latest PyPI versions |

### Subagents

These run in isolated contexts — their token usage doesn't bloat your main conversation:

| Agent | Model | Purpose |
|-------|-------|---------|
| **staff-reviewer** | Opus | Two-stage code review: spec compliance then quality. Primary mandate: simplification. Returns APPROVED or ISSUES with `file:line` references. |
| **implementer** | Opus | Receives all tasks + plan context. TDD discipline, anti-hallucination verification, writes progress to disk after each task. |
| **test-verifier** | Sonnet | Runs build/test/lint commands. Returns structured pass/fail summary. Verbose output stays in its context, not yours. |

---

## How It Works

### The Brainstorming Guard

Every request passes through a 4-question evaluation before any code is written:

1. **Scope** — Will this change affect more than 3 files?
2. **Reversibility** — Can this be fully undone in under 1 hour?
3. **Approaches** — Is there only one obvious way to implement this?
4. **Motivation** — Does the request state WHY?

If the task is large, hard to reverse, has multiple valid approaches, or involves a technical decision → brainstorming is invoked in an isolated subagent. The subagent researches the web, explores the codebase, proposes approaches, scores complexity, and writes a plan to disk.

The guard also includes a **first-principles challenge**: before evaluating scope, it checks whether the developer is solving the right problem. If the request has contradictions, targets a symptom instead of root cause, or introduces unnecessary complexity — the model stops and says so.

**The default is to invoke brainstorming.** The burden of proof is on skipping, not on activating.

### Progressive Disclosure Architecture

The plugin minimizes context overhead through two layers:

- **L1 (always loaded):** `workflow.md` — phase sequence, gate rules, anti-rationalization tables, red flags (~70 lines)
- **L2 (on-demand):** `phases/phase-N-*.md` — detailed phase instructions loaded just-in-time when entering each phase (~300 words each)

Language skills provide only their specific configuration (verification commands, implementation rules, patterns file). The shared workflow handles everything else. No duplication.

### Workflow State Persistence

Three layers ensure quality gates survive "clear context and proceed":

1. **WORKFLOW STATE block** in the plan file (written at TOP of plan)
2. **Plan file on disk** at `docs/plans/` with Status and remaining phases
3. **Pre-Step C** in core-dev checks for in-progress plans FIRST and resumes from the correct phase

If context is compacted mid-workflow, the plan file on disk contains everything needed to recover: current phase, research file path, chronicle path, task checklist with progress, verification results, review audit log.

### Two Workflow Modes

**Full Mode** (default) — All 7 phases with subagents, plan files, chronicles, and staff review. For non-trivial tasks.

**Lightweight Mode** — For genuinely small tasks (3 files or fewer, single approach, fully reversible). Collapses phases: inline research, inline plan confirmation, direct implementation, inline verification, quick self-review. Exits to full mode if complexity is discovered.

---

## The 7-Phase Workflow

| Phase | Name | What happens | Gate |
|-------|------|-------------|------|
| 1 | **Research** | Explore codebase + web research in isolated subagent. Fill knowledge gaps only. | "RESEARCH COMPLETE" |
| 2 | **Plan** | EnterPlanMode. Write plan with WORKFLOW STATE. Persist to disk. | User approves plan |
| 3 | **Chronicle** | Capture WHY: user requirements, context, objectives, affected areas | "CHRONICLE INITIATED" |
| 4 | **Implement** | Single implementer subagent with all tasks. TDD cycles. Progress tracked on disk. | "SOLUTION COMPLETE" |
| 5 | **Verify** | test-verifier subagent runs build/test/lint. Results persisted to plan file. | "VERIFICATION COMPLETE" + evidence |
| 6 | **Staff Review** | Two-stage: spec compliance then code quality. Iterate until APPROVED. | "STAFF REVIEW: APPROVED" |
| 7 | **Finalize** | Finalize chronicle, update CLAUDE.md, align all docs | "WORKFLOW COMPLETE" |

**You cannot skip phases.** Each gate leads directly to the next. The model is instructed to stop and self-check if it catches itself rationalizing a skip.

---

## Anti-Rationalization

The plugin includes tables that catch common failure modes:

| Model's thought | Reality |
|---|---|
| "This is simple enough to skip planning" | Simple-looking changes cause the hardest bugs. Follow the workflow. |
| "The user said exactly what to do" | Knowing WHAT does not mean only one HOW. Multiple approaches = invoke brainstorming. |
| "I can review my own code instead of spawning the reviewer" | Self-review is part of the implementer's protocol. Staff review is independent evaluation — not redundant. |
| "I already know this codebase well" | Familiarity with the codebase does not mean knowing the best approach for THIS specific change. |
| "The developer seems confident, so the request is probably sound" | Confidence does not equal correctness. Evaluate the reasoning, not the tone. |

These tables appear in `core-dev`, `workflow.md`, each language skill, and the staff reviewer — reinforcing the behavior at every decision point.

---

## Chronicles

Chronicles capture the WHY behind changes at a higher level than code or plan docs:

```
Code + Git = WHAT changed (low-level diffs, line-by-line)
Plan docs  = HOW it was implemented (tasks, approaches, file-level changes)
Chronicles = WHY it happened, WHAT the user communicated, PROJECT STATE
```

Months later, a developer or model can read a chronicle and understand the full context of what happened at that moment in the project. Chronicles are stored in `docs/chronicles/` with timestamps.

---

## Project Directives

On first activation, the plugin injects **universal project directives** into your project's `CLAUDE.md`. These establish documentation-as-first-class-output habits:

- Document as you go (patterns, gotchas, data shapes)
- Remove ambiguity for your future self
- Use the right document for the right purpose (CLAUDE.md vs MEMORY.md vs plans vs chronicles)
- Keep CLAUDE.md a cheat sheet, not a novel

The injection is one-time — the plugin detects the heading and skips if already present.

---

## Language Support

Each language skill provides:
- **Verification commands** for Phase 5 (build, test, lint)
- **Implementation rules** for Phase 4 (model structure, complexity patterns, compatibility)
- **Patterns file** (`patterns.md`) with team-standard code examples and anti-patterns
- **Quality checklist** items specific to the language
- **Anti-rationalization entries** specific to common mistakes in that language

The patterns files are designed to be customized for your team's standards.

| Language | Skill | Patterns |
|----------|-------|----------|
| Python | `python-dev` | Pydantic, FastAPI, asyncpg, DI via lifespan, pytest |
| Java | `java-dev` | Records, Streams, Spring Boot, constructor injection |
| TypeScript | `typescript-dev` | Zod, strict mode, ESM, Result types |
| Swift | `swift-dev` | SwiftUI, async/await, actors, Codable, SPM |
| Frontend | `frontend-dev` | Auto-detects: React, Next.js, Raycast, Vite |

---

## Architecture

```
.claude-plugin/plugin.json              # Plugin metadata + version
skills/
├── core-dev/SKILL.md                   # Workflow router (brainstorming guard, language detection)
├── brainstorming/                      # Critical evaluation + analysis subagent
│   ├── SKILL.md                        # Orchestrator (delegates to analysis agent)
│   ├── analysis-agent.md               # Isolated analysis engine
│   ├── critical-analysis.md            # Complexity scoring + evaluation framework
│   └── templates/                      # Plan and research file templates
├── python-dev/                         # Python skill + patterns
├── java-dev/                           # Java skill + patterns
├── typescript-dev/                     # TypeScript skill + patterns
├── swift-dev/                          # Swift skill + patterns
├── frontend-dev/                       # Frontend skill + framework patterns
│   ├── patterns/                       # react.md, nextjs.md, typescript.md
│   └── environments/                   # raycast.md, vite.md
├── debugging/SKILL.md                  # Systematic root-cause methodology
├── chronicles/SKILL.md                 # Project snapshot creation
├── commit/SKILL.md                     # Conventional commits
├── align-docs/SKILL.md                 # Documentation alignment
├── update-precommit/SKILL.md           # Pre-commit hook updater
├── update-reqs/SKILL.md               # requirements.in updater
└── update-reqs-dev/SKILL.md           # requirements-dev.in updater
agents/
├── implementer.md                      # Implementation specialist (Opus)
├── staff-reviewer.md                   # Code review specialist (Opus)
└── test-verifier.md                    # Test/build execution (Sonnet)
shared/
├── workflow.md                         # Mandatory 7-phase workflow (L1 - always loaded)
├── phases/                             # Phase instructions (L2 - loaded on demand)
│   ├── phase-1-research.md
│   ├── phase-2-plan.md
│   ├── phase-3-chronicle.md
│   ├── phase-4-implement.md
│   ├── phase-5-verify.md
│   ├── phase-6-review.md
│   ├── phase-7-finalize.md
│   ├── lightweight-mode.md
│   └── compaction-guide.md
├── agents/research-agent.md            # Research agent template
└── references/
    ├── workflow-reference.md            # Skills vs agents lookup, anti-rationalization
    └── project-directives.md            # Universal project directives template
hooks/
├── hooks.json                          # Auto ruff-format on Edit/Write
└── ruff-format                         # Ruff format hook script
scripts/
└── find-plan.sh                        # Plan file helper (active/next)
```

---

## Contributing

Contributions welcome. The key constraint: **every change must align with the 6 behavior principles** (see `CLAUDE.md`). If a change would make the model more accommodating, weaken critical evaluation, or reduce planning rigor — it doesn't belong here.

To test changes, use the eval suite:
1. Snapshot the current plugin state
2. Apply your changes
3. Run all 20 evals against both versions
4. Compare — no regressions allowed on passing assertions

## License

MIT
