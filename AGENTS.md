# Development Skills

Full-stack development workflow plugin covering Python, Java, TypeScript, Swift, and frontend projects.

For the canonical skills + subagents + hooks listing, see `README.md`.

## Supported Agents

| Platform | Installation | Status |
|----------|--------------|--------|
| Claude Code | Marketplace (`.claude-plugin/`) | Full support (skills + subagents + hooks + commands) |
| Codex CLI | Symlink discovery (see `.codex/INSTALL.md`) | Skills + named-agent dispatch via workaround (see `skills/using-development-skills/references/codex-tools.md`); hooks not supported |

Codex users MUST set `[features] multi_agent = true` in `~/.codex/config.toml` for subagent-dispatching skills (`brainstorming`, `roast-my-code`, `create-test`, `distill`, `eval-regression` — anything that spawns a research subagent or the `staff-reviewer` agent).

## Workflow

4 phases: Research+Plan → Chronicle → Implement+Verify → Review+Finalize. Implementation runs in the main thread. A staff-level code review checks every change via the `staff-reviewer` agent.

See `shared/workflow.md` for the canonical sequence and `shared/iron-rules.md` for the rules that apply across phases.

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

## Iron Rules

See `shared/iron-rules.md` — 8 Core Pillars (from the project's `AGENTS.md`) + 3 workflow process rules. Every phase and every skill references it. Do not duplicate.
