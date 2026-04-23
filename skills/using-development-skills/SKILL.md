---
name: using-development-skills
description: Use when starting any conversation - establishes how the development-skills plugin works and how to invoke its components on each platform (Claude Code, Codex). Read first; points to per-platform tool mapping and named-agent dispatch.
---

<SUBAGENT-STOP>
If you were dispatched as a subagent to execute a specific task, skip this skill.
</SUBAGENT-STOP>

# Using development-skills

This plugin ships specialized skills, three named subagents, and Claude-Code-only hooks. The invocation surface differs per platform; the content is identical.

## Iron Rule

Be objective and critical — never agreeable. Challenge assumptions, flag risks, push back on bad ideas. Honest direct feedback prevents costly mistakes. This rule is non-negotiable regardless of platform.

## Plugin Components

| Component | Location | Platforms |
|-----------|----------|-----------|
| 21 skills (core-dev, python-dev, java-dev, typescript-dev, swift-dev, frontend-dev, debugging, create-test, commit, brainstorming, best-practices, distill, roast-my-code, resolve-merge, align-docs, update-precommit, update-reqs, update-reqs-dev, eval-regression, chronicles, ai-agent-bench) | `skills/<name>/SKILL.md` | Claude Code + Codex (agentskills.io standard) |
| 3 user-invocable skills (ex-commands): `context-transfer`, `ingest-feedback`, `produce-feedback` | `skills/<name>/SKILL.md` (`disable-model-invocation: true`) | Claude Code `/name` + Codex `skill` tool |
| 3 named subagents: `implementer`, `staff-reviewer`, `test-verifier` | `agents/*.md` | Claude Code native; Codex via `spawn_agent` workaround (see below) |
| SessionStart context-inject hook | `hooks/hooks.json` | Claude Code only — Codex substitutes this skill |
| PostToolUse auto-format hook (Python/JS/TS/Java/Swift) | `hooks/hooks.json` | Claude Code only — Codex runs formatters manually (see `.codex/INSTALL.md`) |

## How to Invoke

### On Claude Code

- Skills auto-activate when their `description` matches the user's task, or via `/skill-name` / `Skill` tool.
- Subagents dispatched via `Task` / `Agent` tool with `subagent_type: "development-skills:<name>"`.
- Hooks fire automatically.

### On Codex

- Skills auto-discovered from `~/.agents/skills/development-skills/` (symlink set during install — see `.codex/INSTALL.md`).
- Skills load as metadata (~100 tok each) at session start; full body loads when description matches.
- Subagents dispatched manually: read `agents/<name>.md`, wrap in XML, pass to `spawn_agent`. Requires `[features] multi_agent = true` in `~/.codex/config.toml`. Full procedure in `references/codex-tools.md`.
- No hooks. Manual formatter invocation after edits.

## Platform Adaptation

Skills in this plugin use Claude Code tool names as canonical references (`Task`, `TodoWrite`, `Skill`, `Read`, `Write`, `Edit`, `Bash`). When operating on Codex, consult `references/codex-tools.md` for equivalents and the named-agent dispatch pattern.

Do NOT read skill files with the `Read` tool. Use the platform's native skill-invocation mechanism:
- Claude Code: `Skill` tool
- Codex: skills load natively on description match; follow body instructions directly

## Skill Priority

1. **Process skills first** (`brainstorming`, `debugging`) — these determine HOW to approach the task.
2. **Implementation skills second** (`core-dev`, `python-dev`, `typescript-dev`, etc.) — these guide execution.

"Let's build X" → `brainstorming` first, then `core-dev`.
"Fix this bug" → `debugging` first, then domain-specific skill.

## Red Flags (STOP — you're rationalizing)

| Thought | Reality |
|---------|---------|
| "This is just a simple question" | Questions are tasks. Check for skills. |
| "I need more context first" | Skill check comes BEFORE clarifying questions. |
| "Let me explore the codebase first" | Skills tell you HOW to explore. Check first. |
| "This doesn't need a formal skill" | If a skill exists, use it. |
| "I'll just do this one thing first" | Check BEFORE doing anything. |
| "I know what that means" | Knowing the concept ≠ using the skill. Invoke it. |
