# Development skills

This repository is the source of the `development-skills` plugin for Claude Code and Codex CLI.

1. Challenge unsupported assumptions. Evidence validates a decision; agreement alone does not.
2. Use the smallest useful change. Every changed line must trace to the request.
3. Follow [`shared/development-loop.md`](shared/development-loop.md) for scope, authorization, checks, and completion.
4. Follow [`shared/writing.md`](shared/writing.md) for every natural-language artifact.
5. Follow [`shared/engineering.md`](shared/engineering.md) for code and design.
6. Test new behavior with a failing proof when practical. Keep refactor characterization proof green before and after.
7. Never suppress a failing check or weaken proof to claim success.
8. Preserve user work and inspect callers before removing or moving files.
9. Store durable reasons in chronicles and resumable execution state in plans.
10. Commit only when explicitly requested. Never add AI attribution or `Co-Authored-By` trailers.

- Skills and agents reference canonical files under `shared/`; they do not copy those contracts.
- One named subagent ships: `staff-reviewer`. Implementation and verification stay in the main context.
- The plugin is language-agnostic and ships no organization, language, framework, or product conventions.
- `pyproject.toml` exists for repository tools. The plugin is not a Python package.
- Use `uv` for Python commands.
- Hooks run on Claude Code and supported Codex versions. Document a manual fallback for a new hook.
- Personal machine facts stay in ignored `.claude/CLAUDE.md` or global Codex instructions.

Version files are `VERSION`, `pyproject.toml`, both plugin manifests, and `.claude-plugin/marketplace.json`.
Use Commitizen to update them together.
Use `--files-only` when a tag or automatic commit is not authorized.
Create or move a tag only after explicit confirmation.

| Rule | Scope | Topic |
|---|---|---|
| [`.agents/rules/skill-authoring.md`](.agents/rules/skill-authoring.md) | `skills/**`, `agents/**` | Skill and subagent structure. |
| [`.agents/rules/shared-canonical.md`](.agents/rules/shared-canonical.md) | `shared/**` | Canonical workflow files. |
| [`.agents/rules/plugin-packaging.md`](.agents/rules/plugin-packaging.md) | Manifests, catalogs, versions, changelog | Packaging and releases. |
| [`.agents/rules/formatting-hooks.md`](.agents/rules/formatting-hooks.md) | `hooks/**` | Formatting and hook behavior. |
