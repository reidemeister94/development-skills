# development-skills

A Claude Code plugin that turns your AI agent into a disciplined software engineer.

<a href="https://github.com/reidemeister94/development-skills/releases"><img src="https://img.shields.io/github/v/release/reidemeister94/development-skills?style=flat-square&color=blue" alt="Release"/></a>
<a href="LICENSE"><img src="https://img.shields.io/github/license/reidemeister94/development-skills?style=flat-square" alt="License"/></a>
<a href="https://github.com/reidemeister94/development-skills/stargazers"><img src="https://img.shields.io/github/stars/reidemeister94/development-skills?style=flat-square&color=yellow" alt="Stars"/></a>

---

## Installation

```bash
/plugin marketplace add reidemeister94/development-skills
/plugin install development-skills@development-skills
```

Activates automatically on any coding task. No configuration needed.

---

<img src="docs/images/terminal-demo.svg" alt="development-skills in action" width="640"/>

## What It Does

AI agents are fast but undisciplined — [67% of developers](https://addyo.substack.com/p/the-80-problem-in-agentic-coding) spend *more* time debugging AI-generated code than writing it. This plugin enforces a mandatory gated workflow: research before planning, plan before coding, test before shipping, review before merging. Every time.

<img src="docs/images/workflow-phases.svg" alt="7-Phase Development Workflow" width="640"/>

Three subagents handle specialized work: an **Implementer** (TDD cycles), a **Test Verifier** (structured pass/fail), and a **Staff Reviewer** (two-stage code review). The orchestrator delegates but never implements directly.

<img src="docs/images/subagent-architecture.svg" alt="Subagent Architecture" width="640"/>

Small tasks (3 files or fewer, single obvious approach) get a fast track — same quality checks, no ceremony.

---

## 19 Skills

**Workflow** — `core-dev` (auto-activates), `brainstorming`, `debugging`, `chronicles`

**Languages** — `python-dev`, `java-dev`, `typescript-dev`, `frontend-dev`, `swift-dev`

**Testing** — `create-test`, `roast-my-code` (`--fix`), `eval-regression`

**Utilities** — `commit`, `distill`, `align-docs`, `resolve-merge`, `update-precommit`, `update-reqs`, `update-reqs-dev`, `best-practices`

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
