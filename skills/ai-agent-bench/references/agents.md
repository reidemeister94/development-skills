# Extending the skill to a new agent

Fully supported: `claude` (Claude Code), `codex` (OpenAI Codex). `opencode` is a stub. Adding an agent is four touch-points.

## 1. Transcript parser in `scripts/parse_transcript.py`

`def parse_<agent>(path: Path) -> dict` returning the same shape as `parse_claude_session`:

```python
{
    "agent", "model", "session_id", "raw_event_count",
    "tokens": {"input", "output", "cache_read", "cache_creation", ..., "total"},
    "thinking": {"blocks", "chars", "approx_tokens"},
    "cost_usd", "duration_ms_self_reported", "num_turns",
    "messages": {"assistant", "user", ...},
    "tool_calls": {"total", "by_tool", "parallel_distribution", "avg_parallel_calls_per_message"},
    "skills_used", "subagents_used",
    "trajectory": {"files_read_total", "files_read_unique", "files_read_by_extension",
                   "files_read_before_first_edit", "n_edits", "n_subagents", "gate_invocations"},
}
```

Leave unpopulated fields at `0` / `{}` / `None`; the report renders them as `-`.

## 2. Register in `PARSERS`

```python
PARSERS = {"claude": parse_claude_session, "codex": parse_codex_session, "opencode": parse_opencode_stub}
```

## 3. CLI invocation in `scripts/run_trial.py`

Add a branch to `build_agent_command()` returning the argv list. The command must:
- emit newline-delimited JSON events to stdout (for the parser)
- run with the worktree as CWD or via an agent-native flag (`--cd`, `--add-dir`)
- run non-interactively without approval prompts (Claude `--dangerously-skip-permissions`; Codex `exec` subcommand)

## 4. Pricing in `scripts/pricing.json`

USD per 1M tokens. Set `cache_creation_1h` to `0` when the provider has no TTL split:

```json
{ "models": { "<model-id>": { "input": 0, "output": 0, "cache_read": 0, "cache_creation_5m": 0, "cache_creation_1h": 0 } } }
```

`estimate_cost_usd` matches exact key first, then prefix (`model.startswith(k)`) — registering a family root like `"gpt-5"` covers its variants.
