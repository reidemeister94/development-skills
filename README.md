# development-skills

A plugin for Claude Code and Codex CLI that turns your AI agent into a disciplined software engineer.

<a href="https://github.com/reidemeister94/development-skills/releases"><img src="https://img.shields.io/github/v/release/reidemeister94/development-skills?style=flat-square&color=blue" alt="Release"/></a>
<a href="LICENSE"><img src="https://img.shields.io/github/license/reidemeister94/development-skills?style=flat-square" alt="License"/></a>
<a href="https://github.com/reidemeister94/development-skills/stargazers"><img src="https://img.shields.io/github/stars/reidemeister94/development-skills?style=flat-square&color=yellow" alt="Stars"/></a>

---

## Installation

### Claude Code

```bash
/plugin marketplace add reidemeister94/development-skills
/plugin install development-skills@development-skills
```

Activates automatically on any coding task. No configuration needed.

### Codex CLI

```bash
git clone https://github.com/reidemeister94/development-skills.git ~/.codex/development-skills
mkdir -p ~/.agents/skills
ln -s ~/.codex/development-skills/skills ~/.agents/skills/development-skills
```

Add to `~/.codex/config.toml`:

```toml
[features]
multi_agent = true
```

Required for subagent-dispatching skills. See [`.codex/INSTALL.md`](.codex/INSTALL.md) for full details, and [`AGENTS.md`](AGENTS.md) for the portable per-agent instructions both platforms read.

---

<img src="docs/images/terminal-demo.svg" alt="development-skills in action" width="640"/>

## What It Does

AI agents are fast but undisciplined — [67% of developers](https://addyo.substack.com/p/the-80-problem-in-agentic-coding) spend *more* time debugging AI-generated code than writing it. This plugin enforces a mandatory gated workflow: research before planning, plan before coding, test before shipping, review before merging. Every time.

<img src="docs/images/workflow-phases.svg" alt="7-Phase Development Workflow" width="640"/>

Three subagents handle specialized work: an **Implementer** (TDD cycles), a **Test Verifier** (structured pass/fail), and a **Staff Reviewer** (two-stage code review). The orchestrator delegates but never implements directly.

<img src="docs/images/subagent-architecture.svg" alt="Subagent Architecture" width="640"/>

Small tasks (3 files or fewer, single obvious approach) get a fast track — same quality checks, no ceremony.

---

## Plans and Chronicles

Every task produces persistent artifacts on disk, numbered incrementally like SQL migrations (`0001`, `0002`, ...). Context windows get compacted. These files don't.

**Plan files** (`docs/plans/0042__2026-03-15__implementation_plan__auth-refactor.md`) are the single source of truth for a task. They accumulate across phases: research notes, implementation checklist, verification results, review log. Subagents read from and write to the same plan file. When the context window clears, the agent picks up where it left off by reading the plan.

**Chronicles** (`docs/chronicles/0042__2026-03-15__auth-refactor.md`) capture what code and plans don't — **WHY**. The user's original request, the business context behind it, rejected alternatives, discoveries made during implementation. Without chronicles, a conversation with Claude disappears when the session ends. With chronicles, the reasoning survives: why cursor-based pagination instead of offset, why the auth middleware was rewritten, why a simpler approach was rejected.

```
Code + Git    →  WHAT changed    (diffs)
Plan files    →  HOW it was built (steps, checklist, verification)
Chronicles    →  WHY it happened  (intent, context, decisions)
```

Full details on templates and lifecycle in the **[in-depth guide](docs/GUIDE.md)**.

---

## 26 Skills

**Workflow** — `core-dev` (auto-activates), `brainstorming`, `debugging`, `chronicles`, `using-development-skills`

**Languages** — `python-dev`, `java-dev`, `typescript-dev`, `frontend-dev`, `swift-dev`

**Testing** — `create-test`, `roast-my-code` (`--fix`), `eval-regression`, `ai-agent-bench`

**Utilities** — `commit`, `distill`, `align-docs`, `resolve-merge`, `update-precommit`, `update-reqs`, `update-reqs-dev`, `best-practices`, `claude-to-codex`

**User-invocable (ex-commands)** — `context-transfer`, `produce-feedback`, `ingest-feedback`

Auto-format on save via hooks: ruff (Python), biome (JS/TS), google-java-format, swift-format, prettier.

Full details in the **[in-depth guide](docs/GUIDE.md)**.

---

## Acknowledgments

Draws inspiration from [superpowers](https://github.com/obra/superpowers) by Jesse Vincent — spec-first brainstorming, subagent-per-task dispatch with two-stage review, bite-sized TDD plans, and git worktree isolation.

Where development-skills diverges: **language-specific engineering patterns** (5 languages with framework-level guidance), **context engineering** (observation masking, progressive phase loading), and a **chronicles** layer for capturing WHY decisions were made.

---

## Further Reading

- [How I Taught Agents to Follow a Process, Not Just Write Code](https://medium.com/@silvio.pavanetto/how-i-taught-agents-to-follow-a-process-not-just-write-code-b135b6573c54) — the full story
- [Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — the patterns we implement
- [TDD, AI Agents and Coding with Kent Beck](https://newsletter.pragmaticengineer.com/p/tdd-ai-agents-and-coding-with-kent) — why testing matters more with AI

---

## Contributing

Contributions welcome — especially new language skills (Rust, Go, Kotlin, Ruby, C#). See [CONTRIBUTING.md](CONTRIBUTING.md).

No PR without a passing `/eval-regression`. Open an issue first.

## License

MIT
