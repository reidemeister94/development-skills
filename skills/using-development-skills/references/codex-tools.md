# Codex Tool Mapping — development-skills

development-skills SKILL.md bodies use Claude Code tool names as canonical references. On Codex, use the equivalents below.

## Tool Name Mapping

| Claude Code | Codex equivalent |
|------------------|------------------|
| `Task` tool (dispatch subagent) | `spawn_agent` |
| Multiple `Task` calls (parallel) | Multiple `spawn_agent` calls |
| `Task` returns result | `wait` |
| `Task` completes automatically | `close_agent` to free slot |
| `TaskCreate` / `TaskUpdate` / `TaskList` | `update_plan` (Codex consolidates task management) |
| `Skill` tool | Skills load natively on description match — follow body instructions |
| `Read`, `Write`, `Edit`, `Glob`, `Grep` | Codex native file tools (`read_file`, `write_file`, etc.) |
| `Bash` | Codex native shell tool |
| `AskUserQuestion` | Numbered list with explicit STOP marker (see below) |

## Required Codex Config

Subagent dispatch needs multi-agent mode. Add to `~/.codex/config.toml`:

```toml
[features]
multi_agent = true
```

Required for the `staff-reviewer` agent and any research subagent spawn (brainstorming web research, Phase 1 gap-fill).

## AskUserQuestion Fallback

When a skill needs structured user input, use a numbered list with an explicit STOP marker:

```
1. [option A] (Recommended)
2. [option B]
3. Other (describe)

Reply with the number or free text. STOP. Wait.
```

End your turn. Wait for the user's reply.

## Named-Agent Dispatch

development-skills ships one named subagent: `staff-reviewer`. Codex has no named subagent registry; `spawn_agent` creates generic workers. To dispatch:

1. Read `agents/staff-reviewer.md`.
2. Copy the body (everything after the YAML frontmatter).
3. Wrap using the template below.
4. Spawn a `worker` with the wrapped content as `message`.

### Wrapping template

```
Your task is to perform the following. Follow the instructions below exactly.

<agent-instructions>
[paste body of agents/staff-reviewer.md, with placeholders like {TASK}, {GIT_DIFF}, {PLAN_FILE_PATH} already filled in]
</agent-instructions>

Execute this now. Output ONLY the structured response following the format specified in the instructions above.
```

### Dispatch equivalents

| Claude Code | Codex |
|---|---|
| `Task(subagent_type="development-skills:staff-reviewer", prompt=...)` | Read `agents/staff-reviewer.md`, wrap, `spawn_agent(agent_type="worker", message=<wrapped>)` |
| `Task(subagent_type="general-purpose", prompt=...)` | `spawn_agent(agent_type="worker", message=<prompt>)` |
| `Task(subagent_type="Explore", prompt=...)` | `spawn_agent(agent_type="explorer", message=<prompt>)` |

### Framing

- Task-delegation framing ("Your task is...") rather than persona framing ("You are..."). Codex treats `message` as user-level input.
- Wrap instructions in `<agent-instructions>` XML — the model treats tagged blocks as authoritative.
- End with an explicit execution directive.

## Hooks

development-skills ships two Claude Code hooks. Neither runs on Codex.

- **SessionStart context-inject:** the `using-development-skills` skill itself bootstraps via description-match on every conversation start.
- **PostToolUse auto-format:** run formatters manually after edits. See project-root `.codex/INSTALL.md` for per-language commands.
