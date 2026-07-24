---
paths:
  - "hooks/**"
---

# Auto-format hooks

`hooks/` contains Claude Code lifecycle hooks. The session-start hook injects context; the edit hooks auto-run formatters on every `Edit` / `Write`. On Codex these only fire when the user opts in via `[features] plugin_hooks = true` in `~/.codex/config.toml` (0.128+).

## Formatter command table (canonical)

| Language | Formatter | Command |
|----------|-----------|---------|
| Python | ruff | `ruff format <file> && ruff check <file> --fix` |
| JS/TS | biome (preferred) or prettier | `biome format --write <file>` |
| Java | google-java-format | `google-java-format --replace <file>` |
| Kotlin | ktfmt | `ktfmt <file>` |
| Swift | swift-format | `swift-format format --in-place <file>` |
| CSS / JSON / GraphQL | biome | `biome format --write <file>` |
| HTML / YAML | prettier | `prettier --write <file>` |

Changes to this table must propagate to:

- The hook scripts under `hooks/` that invoke these formatters.
- The user-facing README's "Auto-format on edit" line.
- Any skill or doc that documents formatter expectations.

If the table moves out of sync with the hook implementations, the hooks ARE the source of truth — update the table to match.

## Hook authoring conventions

- Hooks are shell scripts (or Python where shell is too limited).
- Exit codes are load-bearing — a non-zero exit fails the tool call. Format errors should `exit 0` after printing a warning unless a hard failure is intended.
- Session-start hooks should be idempotent and fast (< 200ms) — they run on every conversation start.
- Hooks must NOT block on network calls. If a hook needs network, gate behind an env var and document it.

## Codex parity

Every Claude Code hook that ships with the plugin should have a documented manual equivalent for Codex users who haven't enabled `plugin_hooks`. Test changes on both sides — Codex `plugin_hooks = true` is still relatively new (0.128+) and edge cases differ.
