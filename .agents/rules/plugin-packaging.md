---
paths:
  - ".claude-plugin/**"
  - ".codex-plugin/**"
  - ".agents/plugins/**"
  - "evals/**"
  - "VERSION"
  - "CHANGELOG.md"
  - "pyproject.toml"
---

# Plugin packaging, versioning, and distribution

Files in this scope control how the plugin is installed, listed, and version-tracked across Claude Code and Codex CLI. Both CLIs install via the same marketplace flow — no manual symlink or clone fallback.

## Version — single source of truth

Five locations carry the plugin version. `cz bump` (invoked via `make bump-version-{minor,major,patch}`) keeps them in sync atomically — never bump manually.

| Location | Role |
|----------|------|
| `pyproject.toml` `[tool.commitizen] version` | Source of truth that `cz` reads on bump. |
| `VERSION` | Mirror, consumed by the Makefile (`VERSION=v$(cat VERSION)`). |
| `.claude-plugin/plugin.json` `"version"` | Claude Code plugin manifest. |
| `.codex-plugin/plugin.json` `"version"` | Codex plugin manifest. |
| `.claude-plugin/marketplace.json` plugins[0] `"version"` | Claude Code marketplace catalog. |

`tag_format = "$version"` means `cz bump` creates an annotated git tag matching the new version (e.g., `0.6.0`, not `v0.6.0`). `cz` then commits the bump with message `bump: version <old> → <new>` and updates `CHANGELOG.md`.

Sanity check before any version-related commit:

```bash
grep -E '"version"' .claude-plugin/plugin.json .codex-plugin/plugin.json .claude-plugin/marketplace.json
cat VERSION
grep -A1 '\[tool.commitizen\]' pyproject.toml | grep version
```

All five values must match exactly. If they diverge, the divergence is the bug — first audit `pyproject.toml`'s `version_files` list (every location above must appear, with the `:version` selector where applicable), then re-bump or align by hand.

## Manifests — dual, parallel structure

| File | Purpose |
|------|---------|
| `.claude-plugin/plugin.json` | Claude Code plugin manifest. Minimal: `name`, `description`, `version`. |
| `.codex-plugin/plugin.json` | Codex plugin manifest. Same `name`/`version`/`description` + richer `interface{}` block (`displayName`, `shortDescription`, `longDescription`, `developerName`, `category`, `capabilities[]`, `defaultPrompt`, `brandColor`) for Codex's `/plugins` UI. |

Both required for marketplace install on the respective CLI. Edit them together; never let descriptions drift.

## Marketplace catalogs — dual

| File | Purpose |
|------|---------|
| `.claude-plugin/marketplace.json` | Catalog for `/plugin marketplace add reidemeister94/development-skills` (Claude Code). Owner schema. |
| `.agents/plugins/marketplace.json` | Catalog for `codex plugin marketplace add reidemeister94/development-skills` (Codex). Source-object schema. |

Edits to plugin name, description, or version propagate to users on next install — keep wording aligned with `README.md` and the manifests above.

## Installation — marketplace only

The README documents the canonical install for both CLIs. Do not add a symlink-based or clone-based fallback path. Codex 0.128+ supports the same marketplace flow as Claude Code; the only difference is that Codex install is interactive (`/plugins` in-app) rather than a CLI one-liner.

Two Codex facts that drift if forgotten:

- Codex 0.128+ ships the multi-agent engine by default. There is no `MultiAgentV2 = true` boolean to flip — `spawn_agent` / `wait_agent` / `close_agent` are available out of the box. The earlier `[features] multi_agent = true` (0.124–0.127) flag is deprecated.
- Native plugin hooks require `[features] plugin_hooks = true` in `~/.codex/config.toml`. Without it, auto-format hooks do not fire on Codex; users must run formatters manually (table in `AGENTS.md`).

If either fact changes upstream, update `skills/using-development-skills/references/codex-tools.md` AND `README.md` AND any skill that references hook behavior.

## Cross-platform reference — single source of truth

Skill bodies use Claude Code tool names as canonical. Cross-platform translations (Codex `spawn_agent` ↔ Claude Code `Task`, `AskUserQuestion` fallback, named-agent dispatch recipe, hooks, marketplace) live ONLY in `skills/using-development-skills/references/codex-tools.md`. Do NOT add inline "on Claude Code do X / on Codex do Y" branching in any other skill body — point at `codex-tools.md` instead. Exception: `align-docs` is the dual-platform bridge skill by design.

## Changelog

`CHANGELOG.md` follows Keep a Changelog-ish format. One entry per release. Group by `BREAKING / Feat / Fix / Evals / Removed`. The unreleased section accumulates until the version bump.

## Evals

`evals/evals.json` defines the regression suite that `/eval-regression` runs. Skill behavior changes that move pass/fail outcomes MUST update the eval expectations in the same change — never let the eval file lag behind the skill it tests.

## Python tooling

`pyproject.toml` exists for the plugin's internal scripts (eval runners, lint helpers), NOT as a user-facing Python package. Do not advertise PyPI distribution. The plugin's surface stays markdown-first.
