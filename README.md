<p align="center">
  <img src="docs/images/social-preview.svg" alt="development-skills" width="100%"/>
</p>

<p align="center">
  <a href="https://github.com/reidemeister94/development-skills/releases"><img src="https://img.shields.io/github/v/release/reidemeister94/development-skills?style=flat-square&color=blue" alt="Release"/></a>
  <a href="LICENSE"><img src="https://img.shields.io/github/license/reidemeister94/development-skills?style=flat-square" alt="License"/></a>
  <a href="https://github.com/reidemeister94/development-skills/stargazers"><img src="https://img.shields.io/github/stars/reidemeister94/development-skills?style=flat-square&color=yellow" alt="Stars"/></a>
  <a href="https://github.com/reidemeister94/development-skills/issues"><img src="https://img.shields.io/github/issues/reidemeister94/development-skills?style=flat-square" alt="Issues"/></a>
  <img src="https://img.shields.io/badge/Claude_Code-plugin-7c3aed?style=flat-square&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJ3aGl0ZSI+PGNpcmNsZSBjeD0iMTIiIGN5PSIxMiIgcj0iMTAiLz48L3N2Zz4=" alt="Claude Code"/>
</p>

<p align="center">
  <b>A Claude Code plugin that turns your AI agent into a disciplined software engineer.</b>
</p>

<p align="center">
  <a href="#installation">Installation</a> &middot;
  <a href="#how-it-works">How It Works</a> &middot;
  <a href="#19-skills-5-languages">19 Skills</a> &middot;
  <a href="#design-philosophy">Philosophy</a> &middot;
  <a href="https://medium.com/@silvio.pavanetto/how-i-taught-agents-to-follow-a-process-not-just-write-code-b135b6573c54">Blog Post</a>
</p>

---

## Installation

In Claude Code, register the marketplace first:

```bash
/plugin marketplace add reidemeister94/development-skills
```

Then install the plugin:

```bash
/plugin install development-skills@development-skills
```

The plugin activates automatically on any coding task. No configuration needed.

### Verify Installation

Start a new session and give Claude a development task. The plugin should activate automatically — you'll see it follow a structured workflow (research, plan, implement, verify, review) instead of jumping straight to code.

You can also invoke skills directly:

```
/brainstorming    — Evaluate approaches before committing to one
/debugging        — Systematic root-cause analysis
/create-test      — Design tests that find bugs, not just exist
/distill          — Compress verbose text while preserving facts
/commit           — Conventional commit from staged changes
```

### Updating

```bash
/plugin update development-skills@development-skills
```

### Optional: Regression Testing

The [`skill-creator`](https://github.com/anthropics/claude-plugins-official) plugin is required for running regression tests (`/eval-regression`):

```bash
/plugin install skill-creator@claude-plugins-official
```

---

<p align="center">
  <img src="docs/images/terminal-demo.svg" alt="development-skills in action" width="100%"/>
</p>

## Why This Exists

AI agents are fast but undisciplined. [67% of developers](https://addyo.substack.com/p/the-80-problem-in-agentic-coding) spend *more* time debugging AI-generated code, which contains [1.7x more major issues](https://www.elektormagazine.com/articles/2026-an-ai-odyssey-vibe-coding-hangover) and 2.74x more security vulnerabilities. Agents [delete unit tests](https://newsletter.pragmaticengineer.com/p/tdd-ai-agents-and-coding-with-kent) to make them pass. They generate code at 140-200 lines/min while humans comprehend at 20-40 — creating [cognitive debt](https://margaretstorey.com/blog/2026/02/09/cognitive-debt/).

**development-skills makes the good-day workflow the only workflow** — research before planning, plan before coding, test before shipping, review before merging. Every time, without reminding.

> *As Anthropic's [2026 Agentic Coding Trends Report](https://resources.anthropic.com/hubfs/2026%20Agentic%20Coding%20Trends%20Report.pdf) concluded: success comes from treating agentic development as a "workflow design problem, not a tool adoption problem."*

<p align="center">
  <img src="docs/images/before-after.svg" alt="Without vs With development-skills" width="100%"/>
</p>

---

## How It Works

When you give Claude Code a development task with this plugin installed, it doesn't just start writing code. Instead, it follows a mandatory gated workflow:

<p align="center">
  <img src="docs/images/workflow-phases.svg" alt="7-Phase Development Workflow" width="100%"/>
</p>

Each phase is a **gate** — the agent cannot proceed until the gate conditions are met. No skipping. No combining. No "this is trivial, I'll just code it."

### The 7 Phases

| # | Phase | What Happens | Gate |
|---|-------|-------------|------|
| 1 | **Research** | Explore the codebase and gather context | "RESEARCH COMPLETE" |
| 2 | **Plan** | Write a plan to disk, enter plan mode | User approves the plan |
| 3 | **Chronicle** | Document the WHY — business context, requirements, decisions | "CHRONICLE INITIATED" |
| 4 | **Implement** | TDD cycles with dedicated implementer subagent | "SOLUTION COMPLETE" |
| 5 | **Verify** | Dedicated test-verifier runs the full test suite | Evidence of passing |
| 6 | **Staff Review** | Two-stage code review: spec compliance, then quality | "APPROVED" |
| 7 | **Finalize** | Update docs, chronicle, integration options | "WORKFLOW COMPLETE" |

**Small tasks get a fast track.** If a change touches 3 files or fewer with a single obvious approach, the plugin collapses into lightweight mode — same quality checks, no ceremony.

---

## Key Features

<p align="center">
  <img src="docs/images/subagent-architecture.svg" alt="Subagent Orchestration" width="100%"/>
</p>

**Brainstorming Guard** — Before coding, evaluates scope, reversibility, and approach clarity. If anything is ambiguous, spawns an isolated analysis agent. The default is to analyze; burden of proof is on *skipping*. Anti-rationalization tables counter the model's tendency to justify shortcuts. Without this guard, the agent skips analysis [~40% of the time](https://medium.com/@silvio.pavanetto/how-i-taught-agents-to-follow-a-process-not-just-write-code-b135b6573c54) on tasks that need it.

**Subagent Architecture** — Three specialized agents: Staff Reviewer (Opus, two-stage code review), Implementer (Sonnet, TDD execution), Test Verifier (Sonnet, structured pass/fail). Mirrors Anthropic's [effective sub-agent patterns](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents). Giving agents a way to verify their own work [improves quality 2-3x](https://venturebeat.com/technology/the-creator-of-claude-code-just-revealed-his-workflow-and-developers-are).

**Observation Masking** — Verbose tool output (80%+ of context tokens) stays on disk. Implementation logs, test output, and review criteria live in files — your main conversation stays clean for [decision-making](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents).

**Filesystem Persistence** — Plans, chronicles, and workflow state survive context compaction. The agent resumes from any phase, even after a full context clear. Projects with persistent memory show [40% fewer errors and 55% faster completion](https://resources.anthropic.com/hubfs/2026%20Agentic%20Coding%20Trends%20Report.pdf).

**Smart Parallel Implementation** — For 4+ independent tasks, analyzes file-touch maps and spawns parallel agents in git worktrees — but only when proven safe via dependency analysis. Naive parallelization [produced 100% unusable code](https://medium.com/@silvio.pavanetto/how-i-taught-agents-to-follow-a-process-not-just-write-code-b135b6573c54); single-agent is the safe default.

**Chronicles** — The missing documentation layer. Code says WHAT, plans say HOW, chronicles capture **WHY**. Business context, decisions, and failed approaches — timestamped and browseable.

---

## 19 Skills, 5 Languages

### Development Skills

| Skill | Trigger | What It Does |
|-------|---------|-------------|
| `core-dev` | Auto (any coding task) | Workflow router — detects language, enforces brainstorming guard, dispatches |
| `brainstorming` | `/brainstorming` | Critical evaluation with isolated analysis agent. Two modes: full analysis, focused evaluation |
| `python-dev` | `/python-dev` | Python patterns — Pydantic, FastAPI, asyncpg, pytest |
| `java-dev` | `/java-dev` | Java patterns — Records, Streams, Spring Boot, JPA |
| `typescript-dev` | `/typescript-dev` | TypeScript patterns — Zod, Express, Fastify, vitest (backend/CLI only) |
| `frontend-dev` | `/frontend-dev` | Auto-detects React, Next.js, Raycast, Vite. Loads framework-specific patterns |
| `swift-dev` | `/swift-dev` | Swift patterns — SwiftUI, UIKit, Vapor, SPM |
| `debugging` | `/debugging` | Systematic root-cause debugging: investigate, analyze, hypothesize, fix |

### Specialized Skills

| Skill | Trigger | What It Does |
|-------|---------|-------------|
| `create-test` | `/create-test` | Risk-scored test design. Explorer mode audits your codebase for dangerous untested code; targeted mode generates boundary, property-based, and invariant tests with strong assertions |
| `distill` | `/distill` | Hybrid semantic text compression: deterministic regex pre-processing + LLM compression + deterministic post-verification. Multilingual noise removal (EN/IT/FR/ES/DE). Measures entropy via gzip |
| `commit` | `/commit` | Conventional commits from staged changes |
| `chronicles` | Auto | Project snapshots capturing the WHY behind changes |
| `align-docs` | `/align-docs` | Align documentation with current project state |
| `eval-regression` | `/eval-regression` | Pre-commit regression testing — compares current version against last committed version |
| `update-precommit` | `/update-precommit` | Update `.pre-commit-config.yaml` hooks to latest versions |
| `update-reqs` | `/update-reqs` | Update `requirements.in` with latest PyPI versions |
| `update-reqs-dev` | `/update-reqs-dev` | Update `requirements-dev.in` with latest PyPI versions |
| `resolve-merge` | `/resolve-merge` | Systematic merge conflict resolution with numbered docs renumbering support |
| `best-practices` | `/best-practices <topic>` | Deep web research from authoritative sources (engineering blogs, official docs, books, GitHub projects >5k stars). Produces structured state-of-the-art report with trade-offs, decision frameworks, anti-patterns, and cited sources |

### Auto-Format on Save

A `PostToolUse` hook automatically formats files when Claude edits them:

| Language | Formatter | Fallback |
|----------|-----------|----------|
| Python | ruff (30x faster than Black) | — |
| JS/TS/CSS/JSON | biome (Rust-based, 7-100x faster) | prettier |
| Java | google-java-format | — |
| Kotlin | ktfmt | ktlint |
| Swift | swift-format | swiftformat |
| HTML/YAML | prettier | — |

---

## Design Philosophy

**Iron Rules** — enforced at every phase, not suggested:

1. No positive claims without fresh verification evidence
2. Red/Green TDD — every implementation starts with a failing test ([Kent Beck agrees](https://newsletter.pragmaticengineer.com/p/tdd-ai-agents-and-coding-with-kent))
3. Comment the WHY, not the WHAT
4. No commits without explicit user request
5. Every gate must be explicitly passed

**Model Behavior** — maximum honesty (zero accommodation), always-on critical thinking, calibrated criticism (concrete and evidence-based), planning as 90% of the work, data-validated decisions, and persistent knowledge on disk.

---

## Architecture

```
skills/          19 skills (core-dev, 5 languages, brainstorming, debugging, testing, utilities)
agents/          3 subagents (implementer, staff-reviewer, test-verifier)
hooks/           Auto-format on Edit/Write (multi-language) + session context
shared/          Workflow engine with just-in-time phase loading
commands/        Feedback production/ingestion
```

Context is loaded progressively following Anthropic's [just-in-time pattern](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents): `workflow.md` always loaded (~120 lines), phase instructions loaded per-phase (~300 words each), language patterns loaded on-demand.

---

## Context Engineering

Implements patterns from Anthropic's [Context Engineering guide](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) and validated by [Manus](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus) across millions of production users:

<p align="center">
  <img src="docs/images/context-engineering.svg" alt="Context Engineering: Progressive Disclosure" width="100%"/>
</p>

- **Progressive disclosure** — phase instructions loaded just-in-time, not all at once
- **Observation masking** — verbose output on disk, condensed summaries in conversation
- **Filesystem as extended context** — plans, chronicles, workflow state, implementation logs
- **Clean subagent windows** — each agent gets only the context it needs
- **Anti-rationalization tables** — keep the model honest under pressure

> Built from 60,000+ lines of production Python — FastAPI backends, legacy databases, shared environments. Every feature exists because its absence caused a real problem.

---

## Further Reading

- [How I Taught Agents to Follow a Process, Not Just Write Code](https://medium.com/@silvio.pavanetto/how-i-taught-agents-to-follow-a-process-not-just-write-code-b135b6573c54) — the full story behind this plugin
- [Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — Anthropic's guide to the patterns we implement
- [Building Claude Code with Boris Cherny](https://newsletter.pragmaticengineer.com/p/building-claude-code-with-boris-cherny) — how the creator thinks about agent workflows
- [TDD, AI Agents and Coding with Kent Beck](https://newsletter.pragmaticengineer.com/p/tdd-ai-agents-and-coding-with-kent) — why testing matters more with AI
- [Agentic Engineering](https://addyosmani.com/blog/agentic-engineering/) — Addy Osmani on structured workflows
- [Context Engineering: Lessons from Manus](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus) — production-validated patterns

---

## Regression Testing

**30 evals, 98 assertions** across 11 behavioral dimensions — a test suite for agent behavior. Powered by Anthropic's [`skill-creator`](https://github.com/anthropics/claude-plugins-official) plugin.

```
/eval-regression
```

Covers: brainstorming guard (7), smart isolation (6), anti-rationalization (4), performance review (3), workflow phases (3), implementer discipline (2), language detection, chronicle quality, turn boundaries, project directives, and AskUserQuestion avoidance. Each eval snapshots the committed version as baseline, runs the modified version, and produces a clear verdict: **SAFE TO COMMIT** or **REGRESSIONS FOUND**.

---

## Contributing

Contributions welcome — especially new language skills (Rust, Go, Kotlin, Ruby, C#). See [CONTRIBUTING.md](CONTRIBUTING.md).

**Golden rule:** no PR without a passing `/eval-regression` benchmark. Zero regressions = merge. Open an issue first to discuss.

## License

MIT

---

<p align="center">
  <b>If this plugin makes your AI agent more disciplined, consider giving it a star.</b><br/>
  <sub>It helps others discover the project and motivates continued development.</sub>
</p>

<p align="center">
  <a href="https://github.com/reidemeister94/development-skills/stargazers"><img src="https://img.shields.io/github/stars/reidemeister94/development-skills?style=social" alt="Star on GitHub"/></a>
</p>

<p align="center">
  <a href="https://medium.com/@silvio.pavanetto/how-i-taught-agents-to-follow-a-process-not-just-write-code-b135b6573c54">Read the full story</a> &middot; <a href="https://github.com/reidemeister94/development-skills/issues">Report an issue</a> &middot; <a href="CONTRIBUTING.md">Contribute</a>
</p>
