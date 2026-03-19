# ⚙️ Development Skills

[![GitHub stars](https://img.shields.io/github/stars/reidemeister94/development-skills?style=flat-square)](https://github.com/reidemeister94/development-skills/stargazers)
[![GitHub license](https://img.shields.io/github/license/reidemeister94/development-skills?style=flat-square)](https://github.com/reidemeister94/development-skills/blob/main/LICENSE)
[![Version](https://img.shields.io/badge/version-0.0.1-blue?style=flat-square)](https://github.com/reidemeister94/development-skills/releases)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-plugin-blueviolet?style=flat-square)](https://docs.anthropic.com/en/docs/claude-code)

**A structured development workflow that makes Claude Code produce staff-engineer-quality code.**

Without structure, Claude Code skips verification, doesn't plan, writes before thinking, and never reviews its own work. This plugin enforces a 7-phase workflow with specialized subagents — brainstorming analyst, TDD implementer, test verifier, and staff-engineer reviewer — running in isolated contexts so your main conversation stays clean.

Built from months of real production work, grounded in the [official Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code) and distilled knowledge from projects like [superpowers](https://github.com/obra/superpowers), [claude-code-tips](https://github.com/ykdojo/claude-code-tips), and [Agent-Skills-for-Context-Engineering](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering). Every rule exists because we hit the failure mode it prevents.

## 📦 Quick Start

```bash
claude install-plugin github:reidemeister94/development-skills
```

Give Claude a task — the plugin activates automatically.

---

## 🎯 Core Pillars

These aren't aspirational — they're enforced at every decision point in the workflow.

**🧠 Critical thinking is always on.** The model evaluates every request for flaws, contradictions, wrong assumptions, and symptom-vs-root-cause confusion. If something doesn't add up, it stops and says so — even if the developer sounds confident. Confidence ≠ correctness.

**✨ Maximize simplicity, minimize complexity.** All else being equal, simpler is better. A small improvement that adds ugly complexity is not worth it. Removing something and getting equal or better results is a simplification win. The staff reviewer's primary mandate is simplification.

**📐 All signal, zero noise.** Code, docs, logs, comments — everything must earn its place. Comments explain WHY, not WHAT. Don't comment self-evident code. Don't add features nobody asked for. Don't over-engineer for hypothetical futures.

**💾 Offload everything to disk.** Context windows are ephemeral — compaction erases discoveries. The plugin continuously persists knowledge to structured markdown files so nothing is lost:
- **Plans** (`docs/plans/`) — task checklist, implementation log, verification results, review audit trail. The single persistent document for a workflow.
- **Chronicles** (`docs/chronicles/`) — project snapshots capturing WHY changes happened, what the user communicated, decisions made, discoveries. Months later, a developer or model reads a chronicle and understands the full context.
- **CLAUDE.md** — project-wide knowledge promoted from discoveries. A cheat sheet, not a novel.

**🔬 Maximize final code quality.** The refactoring objective at every phase: make the project clear, descriptive, efficient, performant, reliable, robust, and maintainable. TDD discipline (RED → GREEN → REFACTOR), anti-hallucination verification, and independent staff review ensure the output meets production standards.

**⚡ Efficient context usage.** Progressive disclosure loads only what's needed. Subagents run in isolated contexts — their token usage doesn't bloat your conversation. Research, implementation, testing, and review each happen in separate token budgets.

---

## 🔄 The 7-Phase Workflow

Every task goes through gated phases. No skipping, no shortcuts.

| # | Phase | Gate |
|---|-------|------|
| 1 | **Research** — codebase + web research in isolated subagent | `RESEARCH COMPLETE` |
| 2 | **Plan** — persisted to disk, requires your approval | User approves |
| 3 | **Chronicle** — captures the WHY behind changes | `CHRONICLE INITIATED` |
| 4 | **Implement** — single subagent, TDD cycles, progress on disk | `SOLUTION COMPLETE` |
| 5 | **Verify** — test/build/lint via subagent, evidence required | `VERIFICATION COMPLETE` |
| 6 | **Staff Review** — spec compliance + code quality, iterate until approved | `STAFF REVIEW: APPROVED` |
| 7 | **Finalize** — chronicle, docs alignment, CLAUDE.md updates | `WORKFLOW COMPLETE` |

**Lightweight mode** kicks in for small tasks (≤3 files, single approach, reversible) — same gates, less ceremony.

---

## 🧠 Brainstorming Guard

Before any code is written, every request is evaluated:

- **Scope** — More than 3 files?
- **Reversibility** — Undoable in under 1 hour?
- **Approaches** — Only one obvious way?
- **Motivation** — Does the request state WHY?

If the task is large, hard to reverse, or has multiple valid approaches → brainstorming runs in an isolated subagent: web research, codebase exploration, approach scoring, plan written to disk.

Includes a **first-principles challenge** — if the developer is solving the wrong problem, the model stops and says so.

**Default: invoke brainstorming.** The burden of proof is on skipping.

---

## 🤖 Subagents

Token-isolated — their work doesn't bloat your conversation:

| Agent | Model | Job |
|-------|-------|-----|
| **implementer** | Opus | All tasks in one session. TDD discipline, anti-hallucination checks, progress on disk. |
| **staff-reviewer** | Opus | Two-stage review: spec compliance → code quality. Primary mandate: simplification. |
| **test-verifier** | Sonnet | Runs build/test/lint. Returns pass/fail summary. Verbose output stays in its context. |

---

## 🛡️ Anti-Rationalization

Tables at every decision point catch the model rationalizing shortcuts:

| Model thinks... | Reality |
|---|---|
| *"Simple enough to skip planning"* | Simple-looking changes cause the hardest bugs. |
| *"The user said exactly what to do"* | Knowing WHAT ≠ only one HOW. |
| *"I can review my own code"* | Self-review ≠ independent evaluation. |
| *"The developer seems confident"* | Confidence ≠ correctness. Evaluate reasoning, not tone. |

---

## 🗣️ Skills

| Skill | Trigger | Description |
|-------|---------|-------------|
| **core-dev** | Auto | Workflow router: brainstorming guard, language detection, mode selection |
| **brainstorming** | `/brainstorming` | Critical evaluation in isolated subagent → researched plan + options |
| **python-dev** | `/python-dev` | Pydantic, FastAPI, asyncpg, pytest, ruff |
| **java-dev** | `/java-dev` | Records, Streams, Spring Boot, Maven/Gradle |
| **typescript-dev** | `/typescript-dev` | Zod, Express, Fastify, vitest/jest (backend/CLI) |
| **frontend-dev** | `/frontend-dev` | Auto-detects: React, Next.js, Raycast, Vite |
| **swift-dev** | `/swift-dev` | SwiftUI, UIKit, Vapor, SPM, XCTest |
| **debugging** | `/debugging` | Systematic 4-phase root-cause methodology |
| **chronicles** | Auto | Project snapshots capturing WHY behind changes |
| **commit** | `/commit` | Conventional commits from staged changes |
| **align-docs** | `/align-docs` | Sync all docs with current disk state |
| **update-precommit** | `/update-precommit` | Update pre-commit hooks to latest versions |
| **update-reqs** | `/update-reqs` | Update `requirements.in` to latest PyPI versions |
| **update-reqs-dev** | `/update-reqs-dev` | Update `requirements-dev.in` to latest PyPI versions |

---

## 🌐 Language Support

Each language skill provides verification commands, implementation rules, a `patterns.md` with code examples and anti-patterns, and a quality checklist. The patterns files are designed to be customized for your team.

| Language | Skill | Patterns |
|----------|-------|----------|
| 🐍 Python | `python-dev` | Pydantic, FastAPI, asyncpg, DI via lifespan, pytest |
| ☕ Java | `java-dev` | Records, Streams, Spring Boot, constructor injection |
| 🔷 TypeScript | `typescript-dev` | Zod, strict mode, ESM, Result types |
| 🍎 Swift | `swift-dev` | SwiftUI, async/await, actors, Codable, SPM |
| 🖥️ Frontend | `frontend-dev` | Auto-detects: React, Next.js, Raycast, Vite |

---

## 🏗️ How It Works

**Progressive disclosure** — minimal context overhead:
- **L1 (always loaded):** `workflow.md` — phase sequence, gates, anti-rationalization (~70 lines)
- **L2 (on-demand):** `phases/phase-N-*.md` — detailed instructions loaded just-in-time (~300 words each)

**State persistence** — survives context compaction:
- WORKFLOW STATE block at top of plan file
- Plan file on disk with status + remaining phases
- Auto-resume: `core-dev` checks for in-progress plans first

**Three layers of knowledge:**
```
Code + Git  = WHAT changed
Plan docs   = HOW it was implemented
Chronicles  = WHY it happened + full project context
```

---

## 📁 Architecture

```
.claude-plugin/plugin.json        # Plugin metadata
skills/                           # 14 skills
  core-dev/                       #   Workflow router + brainstorming guard
  brainstorming/                  #   Critical evaluation + analysis subagent
  python-dev/ java-dev/           #   Language-specific workflows
  typescript-dev/ swift-dev/      #   + patterns.md files
  frontend-dev/                   #   Auto-detects React, Next.js, Raycast, Vite
  debugging/ chronicles/          #   Root-cause debugging, project snapshots
  commit/ align-docs/             #   Conventional commits, docs sync
  update-precommit/               #   Dependency updaters
  update-reqs/ update-reqs-dev/
agents/                           # 3 subagents
  implementer.md                  #   Opus — TDD implementation
  staff-reviewer.md               #   Opus — two-stage code review
  test-verifier.md                #   Sonnet — build/test/lint runner
shared/                           # Workflow engine
  workflow.md                     #   L1: always-loaded workflow rules
  phases/                         #   L2: on-demand phase instructions
  references/                     #   Anti-rationalization, project directives
hooks/                            # Auto ruff-format on Edit/Write
scripts/                          # Plan file helper
```

---

## 🤝 Contributing

Contributions welcome. The key constraint: **every change must align with the [6 behavior principles](CLAUDE.md)**. If a change would make the model more accommodating, weaken critical evaluation, or reduce planning rigor — it doesn't belong here.

## 📄 License

MIT
