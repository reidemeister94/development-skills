# Codex Tool Mapping — development-skills

development-skills SKILL.md bodies use Claude Code tool names. On Codex, use the equivalents below.

## Tool Name Mapping

| Skill references | Codex equivalent |
|------------------|------------------|
| `Task` tool (dispatch subagent) | `spawn_agent` (see [Named agent dispatch](#named-agent-dispatch)) |
| Multiple `Task` calls (parallel) | Multiple `spawn_agent` calls |
| `Task` returns result | `wait` |
| `Task` completes automatically | `close_agent` to free slot |
| `Agent` tool (alternative name) | Same as `Task` — use `spawn_agent` |
| `TodoWrite` (task tracking) | `update_plan` |
| `TaskCreate` / `TaskUpdate` / `TaskList` | `update_plan` (Codex consolidates task management in a single tool) |
| `Skill` tool (invoke a skill) | Skills load natively on description match — just follow their instructions |
| `Read`, `Write`, `Edit`, `Glob`, `Grep` | Use Codex native file tools (`read_file`, `write_file`, etc.) |
| `Bash` | Use Codex native shell tool |
| `EnterPlanMode` | Not supported — Codex has no explicit plan mode; produce a textual plan and ask the user to confirm before executing |
| `AskUserQuestion` | Ask in plain prose (Codex has no dedicated elicitation tool) |

## Required Codex Config

Subagent dispatch requires enabling multi-agent mode. Add to `~/.codex/config.toml`:

```toml
[features]
multi_agent = true
```

This unlocks `spawn_agent`, `send_input`, `resume_agent`, `wait_agent`, `close_agent`. Without this flag, skills that require subagents (e.g. `core-dev`, `brainstorming`, `roast-my-code`) will not work end-to-end on Codex.

## Named Agent Dispatch

Claude Code skills reference named subagent types:

- `development-skills:implementer` (executes task lists, writes code, runs tests)
- `development-skills:staff-reviewer` (two-stage code review: spec compliance → code quality)
- `development-skills:test-verifier` (runs tests/build/lint, reports pass/fail)

Codex does NOT have a named subagent registry. `spawn_agent` creates generic workers. When a skill says "dispatch `development-skills:X` subagent":

1. Read the agent's prompt file: `plugins/development-skills/agents/<X>.md`
2. Copy the full body (everything after the YAML frontmatter)
3. Wrap it using the XML template below
4. Spawn a `worker` agent with the wrapped content as `message`

### Wrapping Template

```
Your task is to perform the following. Follow the instructions below exactly.

<agent-instructions>
[paste the body of agents/<X>.md here, with placeholders like {TASK}, {BASE_SHA}, {WHAT_WAS_IMPLEMENTED} already filled in]
</agent-instructions>

Execute this now. Output ONLY the structured response following the format specified in the instructions above.
```

### Dispatch Equivalents

| Skill instruction (Claude Code) | Codex equivalent |
|---------------------------------|------------------|
| `Task(subagent_type="development-skills:implementer", prompt=...)` | Read `agents/implementer.md`, wrap, `spawn_agent(agent_type="worker", message=<wrapped>)` |
| `Task(subagent_type="development-skills:staff-reviewer", prompt=...)` | Read `agents/staff-reviewer.md`, wrap, `spawn_agent(agent_type="worker", message=<wrapped>)` |
| `Task(subagent_type="development-skills:test-verifier", prompt=...)` | Read `agents/test-verifier.md`, wrap, `spawn_agent(agent_type="worker", message=<wrapped>)` |
| `Task(subagent_type="general-purpose", prompt=...)` | `spawn_agent(agent_type="worker", message=<prompt>)` — no file lookup needed |
| `Task(subagent_type="Explore", prompt=...)` | `spawn_agent(agent_type="explorer", message=<prompt>)` |

### Framing Guidelines

- Use **task-delegation framing** ("Your task is...") rather than persona framing ("You are..."). Codex treats the `message` parameter as user-level input, not a system prompt.
- Wrap instructions in `<agent-instructions>` XML tags — the model gives tagged blocks authoritative weight.
- End with an explicit execution directive so the worker executes rather than summarizes.

## When This Workaround Can Be Removed

When Codex's `RawPluginManifest` schema gains an `agents` field, this plugin can ship a symlink pattern that exposes named subagents to Codex natively. Until then, the read-wrap-spawn procedure is the portable equivalent.

## Hooks

development-skills ships two hooks (SessionStart context-inject, PostToolUse auto-format). Neither runs on Codex.

- **SessionStart equivalent:** `using-development-skills` skill (this skill) serves as the bootstrap context on Codex. Its description triggers on every conversation start.
- **PostToolUse auto-format equivalent:** run formatters manually after edits. See the project root `.codex/INSTALL.md` for per-language commands (`ruff format`, `biome format`, `google-java-format`, `swift-format`).
