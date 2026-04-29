# Installing development-skills for Codex

## Quick Setup

```bash
# Clone the plugin
git clone https://github.com/reidemeister94/development-skills.git ~/.codex/development-skills

# Symlink skills
mkdir -p ~/.agents/skills
ln -s ~/.codex/development-skills/skills ~/.agents/skills/development-skills
```

## Required Codex Config

Edit `~/.codex/config.toml` and add:

```toml
[features]
multi_agent = true
```

Required for subagent-dispatching skills (`core-dev`, `brainstorming`, `roast-my-code`, `create-test`, `distill`, `eval-regression`). Unlocks `spawn_agent`, `wait`, `close_agent`. Without it, those skills fail mid-execution.

Restart Codex.

## Read This First

`skills/using-development-skills/SKILL.md` — components overview and per-platform invocation.
`skills/using-development-skills/references/codex-tools.md` — tool mapping + named-agent dispatch pattern.

## Available Skills

**Auto-invoking:** `using-development-skills`, `core-dev`, `python-dev`, `java-dev`, `typescript-dev`, `swift-dev`, `frontend-dev`, `debugging`, `create-test`, `commit`, `brainstorming`, `best-practices`, `distill`, `roast-my-code`, `resolve-merge`, `align-docs`, `update-precommit`, `update-reqs`, `update-reqs-dev`, `eval-regression`, `chronicles`, `ai-agent-bench`.

**User-invocable only** (`disable-model-invocation: true` — call via `skill` tool or its name): `context-transfer`, `ingest-feedback`, `produce-feedback`.

## Subagents (workaround on Codex)

Claude Code has native named subagents (`development-skills:implementer`, `staff-reviewer`, `test-verifier`). Codex does not — skills dispatch them via the read-wrap-spawn pattern in `skills/using-development-skills/references/codex-tools.md`.

## Hooks Not Supported

- **SessionStart context inject:** replaced by `using-development-skills` skill (auto-activates on any conversation start).
- **PostToolUse auto-format:** run formatters manually after edits:
  - **Python:** `ruff format <file> && ruff check <file> --fix`
  - **JS/TS:** `biome format --write <file>` (or `prettier --write <file>`)
  - **Java:** `google-java-format --replace <file>`
  - **Swift:** `swift-format format --in-place <file>`
