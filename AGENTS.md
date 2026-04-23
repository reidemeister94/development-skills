# Development Skills

Full-stack development workflow plugin covering Python, Java, TypeScript, Swift, and frontend projects.

## Supported Agents

| Platform | Installation | Status |
|----------|--------------|--------|
| Claude Code | Marketplace (`.claude-plugin/`) | Full support (skills + subagents + hooks) |
| Codex CLI | Symlink discovery (see `.codex/INSTALL.md`) | Skills + named-agent dispatch via workaround (see `skills/using-development-skills/references/codex-tools.md`); hooks not supported |

Codex users MUST set `[features] multi_agent = true` in `~/.codex/config.toml` for subagent-dispatching skills (`core-dev`, `brainstorming`, `roast-my-code`, `create-test`, `distill`, `eval-regression`).

## Skills (cross-tool)

| Skill | Trigger |
|-------|---------|
| `using-development-skills` | Auto-activates at conversation start — read first to understand components and per-platform invocation |
| `core-dev` | Auto-activates on any coding task (implementing, fixing, refactoring, reviewing) |
| `python-dev` | Python, FastAPI, Pydantic, pytest, pandas, SQLAlchemy |
| `java-dev` | Java, Spring Boot, Maven, Gradle, JPA, Hibernate |
| `typescript-dev` | TypeScript, Node.js, Express, Fastify, Zod, vitest, jest |
| `swift-dev` | Swift, SwiftUI, UIKit, Vapor, SPM, XCTest |
| `frontend-dev` | React, Next.js, Raycast extensions, Vite projects |
| `debugging` | Fixing bugs, investigating errors, diagnosing failures |
| `create-test` | Writing tests, auditing coverage, finding untested code |
| `commit` | Creating commits with conventional commit messages |
| `brainstorming` | Multiple approaches exist, costly to reverse |
| `best-practices` | Deep research on any engineering topic |
| `distill` | Reducing noise in markdown/text files |
| `roast-my-code` | Honest code quality critique and AI-readiness audit |
| `resolve-merge` | Resolving git merge conflicts |
| `align-docs` | Aligning documentation with current state |
| `update-precommit` | Updating pre-commit hooks to latest versions |
| `update-reqs` | Updating requirements.in with latest PyPI versions |
| `update-reqs-dev` | Updating requirements-dev.in with latest versions |
| `eval-regression` | Running regression tests on skills |
| `chronicles` | Capturing development context and decisions |
| `ai-agent-bench` | Benchmarking AI agents (Claude Code vs Codex vs others) on repo tasks |
| `claude-to-codex` | Converting a project's agent context to be compatible with both Claude Code and Codex CLI |

## User-Invocable Skills (cross-tool, ex-commands)

`disable-model-invocation: true` — won't auto-fire; invoke explicitly via Claude Code `/name` or Codex `skill` tool:

| Skill | Purpose |
|-------|---------|
| `context-transfer` | Produce a structured session handoff document for a new chat |
| `ingest-feedback` | Ingest a development-skills feedback report and apply FIX verdicts |
| `produce-feedback` | Produce a factual chronicle of plugin interactions in the current conversation |

## Subagents (Claude Code native; Codex via workaround)

| Agent | Purpose |
|-------|---------|
| `implementer` | Executes task lists, writes code, runs tests |
| `staff-reviewer` | Two-stage code review: spec compliance → code quality |
| `test-verifier` | Runs tests/build/lint, reports pass/fail |

On Codex: read `agents/<name>.md`, wrap per `skills/using-development-skills/references/codex-tools.md`, pass to `spawn_agent(agent_type="worker", message=<wrapped>)`.

## Hooks (Claude Code only)

- `SessionStart` — injects plugin context reminder. On Codex, the `using-development-skills` skill serves the same purpose (auto-activates on any conversation start).
- `PostToolUse` — auto-formats files after `Edit`/`Write`. On Codex, run formatters manually (see table below).

## Workflow

The plugin follows a structured workflow: brainstorm → plan → implement → verify → review.
Implementation runs in parallel for independent tasks. A staff-level code review checks every change.

## IMPORTANT: Auto-Format After Edits

Claude Code auto-runs these via hook. Codex users MUST run manually after each edit:

| Language | Formatter | Command |
|----------|-----------|---------|
| Python | ruff | `ruff format <file> && ruff check <file> --fix` |
| JS/TS | biome (preferred) or prettier | `biome format --write <file>` |
| Java | google-java-format | `google-java-format --replace <file>` |
| Kotlin | ktfmt | `ktfmt <file>` |
| Swift | swift-format | `swift-format format --in-place <file>` |
| CSS/JSON/GraphQL | biome | `biome format --write <file>` |
| HTML/YAML | prettier | `prettier --write <file>` |

## Iron Rule

Be objective and critical — never agreeable. Challenge assumptions, flag risks, push back on bad ideas. Honest direct feedback prevents costly mistakes.
