"""Parse AI agent session transcripts + aggregate run artifacts into unified metrics.

Supported agents:
  - claude   : Claude Code stream-json (newline-delimited)
  - codex    : OpenAI Codex `exec --json` (newline-delimited)
  - opencode : stub (session.jsonl captured, parser not yet implemented)

Modes:
  1. Single-transcript parse:
       python parse_transcript.py --agent claude --session session.jsonl > metrics.json

  2. Full run-dir aggregation (produced by run_trial.py):
       python parse_transcript.py --agent claude --run-dir eval-results/<task>/claude/run-1-<ts>/ \\
           --output metrics.json --render-report report.md

  3. Cross-agent comparison (multiple run dirs):
       python parse_transcript.py --aggregate \\
           eval-results/<task>/claude/run-1-* \\
           eval-results/<task>/codex/run-1-*  \\
           --output comparison.json --render-report comparison.md

The core is task-agnostic: it does not know about "plants", "VP logs", or any project-specific
convention. It aggregates whatever JSON structure the task's measure_cmd produces and computes
deltas variant-by-variant when both baseline and post use the `{"variants": {...}}` convention.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

# ---------------------------------------------------------------------------
# Generic helpers
# ---------------------------------------------------------------------------


def _iter_jsonl(path: Path) -> Iterable[dict]:
    """Yield JSON objects from a newline-delimited JSON file. Tolerate blank/non-JSON lines."""
    if not path.exists():
        return
    with path.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue


def _ext_of(path: str | None) -> str:
    if not path:
        return "<unknown>"
    suffix = Path(path).suffix
    return suffix.lower() if suffix else "<no-ext>"


def _detect_harness_duplications(tool_calls: list[dict], basenames: set[str]) -> list[dict]:
    """Find agent tool calls whose shell command contains a harness basename.

    These are protocol violations: the harness owns `gate_cmd` and `measure_cmd`
    execution (baseline / post / gate phases). If the agent runs them from inside
    its own session, the trial's wall time inflates and the comparison axis across
    agents becomes noisy.

    `tool_calls` shape:
      - Claude: `{"name": str, "input": {...}, "id": str}` — Bash command lives in
        `input.command`; file-edit tools have no shell command.
      - Codex: `{"name": str, "command": str}` — `command` is always the raw shell
        string (or JSON-serialized for structured tools).

    Returns `[{"tool_call_index", "matched", "command"}]` in order.
    """
    if not basenames:
        return []
    matches: list[dict] = []
    for idx, tc in enumerate(tool_calls):
        cmd = tc.get("command")
        if not cmd:
            inp = tc.get("input") or {}
            cmd = inp.get("command") if isinstance(inp, dict) else None
        if not isinstance(cmd, str):
            continue
        for bn in basenames:
            if bn and bn in cmd:
                matches.append({"tool_call_index": idx, "matched": bn, "command": cmd})
                break
    return matches


# ---------------------------------------------------------------------------
# Claude Code stream-json parser
# ---------------------------------------------------------------------------


def parse_claude_session(path: Path, harness_basenames: set[str] | None = None) -> dict:
    events = list(_iter_jsonl(path))
    if not events:
        return {"agent": "claude", "error": f"no events in {path}", "raw_event_count": 0}

    # Cumulative token tallies. Claude Opus 4.6+ splits cache_creation into 5m/1h TTL buckets
    # (different per-token prices: 5m = 1.25× input, 1h = 2.0× input).
    input_tokens = 0
    output_tokens = 0
    cache_read_tokens = 0
    cache_creation_tokens = 0
    cache_creation_5m = 0
    cache_creation_1h = 0

    # Thinking tokens: Claude stream-json exposes thinking blocks in message.content with
    # type="thinking". There is no separate token count — the thinking content is charged as
    # output tokens. We count chars + blocks as a proxy signal for "how much thinking happened".
    thinking_blocks = 0
    thinking_chars = 0

    tool_calls: list[dict] = []
    tool_use_per_assistant: list[int] = []  # parallel-call histogram

    result_block: dict | None = None
    init_block: dict | None = None
    model: str | None = None
    n_assistant = 0
    n_user = 0

    for ev in events:
        et = ev.get("type")
        if et == "system" and ev.get("subtype") == "init":
            init_block = ev
        elif et == "assistant":
            n_assistant += 1
            msg = ev.get("message", {}) or {}
            model = model or msg.get("model")
            usage = msg.get("usage", {}) or {}
            input_tokens += int(usage.get("input_tokens") or 0)
            output_tokens += int(usage.get("output_tokens") or 0)
            cache_read_tokens += int(usage.get("cache_read_input_tokens") or 0)
            cache_creation_tokens += int(usage.get("cache_creation_input_tokens") or 0)
            cache_creation_nested = usage.get("cache_creation") or {}
            cache_creation_5m += int(cache_creation_nested.get("ephemeral_5m_input_tokens") or 0)
            cache_creation_1h += int(cache_creation_nested.get("ephemeral_1h_input_tokens") or 0)

            content = msg.get("content") or []
            tool_uses_in_msg = 0
            for block in content:
                if not isinstance(block, dict):
                    continue
                btype = block.get("type")
                if btype == "tool_use":
                    tool_uses_in_msg += 1
                    tool_calls.append(
                        {
                            "name": block.get("name"),
                            "input": block.get("input"),
                            "id": block.get("id"),
                        }
                    )
                elif btype == "thinking":
                    thinking_blocks += 1
                    thinking_chars += len(block.get("thinking") or "")
            if tool_uses_in_msg > 0:
                tool_use_per_assistant.append(tool_uses_in_msg)
        elif et == "user":
            n_user += 1
        elif et == "result":
            result_block = ev

    # Cost & duration from final result event (Claude self-reports these).
    cost_usd = None
    duration_ms = None
    num_turns = None
    if result_block:
        cost_usd = result_block.get("total_cost_usd") or result_block.get("cost_usd")
        duration_ms = result_block.get("duration_ms")
        num_turns = result_block.get("num_turns")
        final_usage = result_block.get("usage") or {}
        # Fall back to final tally if per-assistant accumulation yielded zero.
        if input_tokens == 0 and final_usage.get("input_tokens"):
            input_tokens = int(final_usage["input_tokens"])
        if output_tokens == 0 and final_usage.get("output_tokens"):
            output_tokens = int(final_usage["output_tokens"])

    # Trajectory + tool-usage derived metrics.
    by_tool = Counter(tc["name"] or "<unknown>" for tc in tool_calls)
    trajectory = _claude_trajectory(tool_calls)
    harness_duplications = _detect_harness_duplications(tool_calls, harness_basenames or set())
    parallel_distribution = Counter(tool_use_per_assistant)
    avg_parallel = (
        sum(tool_use_per_assistant) / len(tool_use_per_assistant) if tool_use_per_assistant else 0.0
    )

    return {
        "agent": "claude",
        "model": model,
        "session_id": (init_block or {}).get("session_id") if init_block else None,
        "raw_event_count": len(events),
        "tokens": {
            "input": input_tokens,
            "output": output_tokens,
            "cache_read": cache_read_tokens,
            "cache_creation": cache_creation_tokens,
            "cache_creation_5m_ttl": cache_creation_5m,
            "cache_creation_1h_ttl": cache_creation_1h,
            "total": input_tokens + output_tokens + cache_read_tokens + cache_creation_tokens,
        },
        "thinking": {
            "blocks": thinking_blocks,
            "chars": thinking_chars,
            # Rough proxy: ~4 chars/token for English prose. Not billed separately from output_tokens
            # but useful as a signal of deliberation volume.
            "approx_tokens": thinking_chars // 4,
        },
        "cost_usd": cost_usd,
        "duration_ms_self_reported": duration_ms,
        "num_turns": num_turns,
        "messages": {"assistant": n_assistant, "user": n_user},
        "tool_calls": {
            "total": len(tool_calls),
            "by_tool": dict(by_tool),
            "parallel_distribution": {str(k): v for k, v in parallel_distribution.items()},
            "avg_parallel_calls_per_message": round(avg_parallel, 3),
        },
        "skills_used": trajectory["skills_used"],
        "subagents_used": trajectory["subagents_used"],
        "trajectory": {
            "files_read_total": trajectory["files_read_total"],
            "files_read_unique": trajectory["files_read_unique"],
            "files_read_by_extension": trajectory["files_read_by_extension"],
            "files_read_before_first_edit": trajectory["files_read_before_first_edit"],
            "n_edits": trajectory["n_edits"],
            "n_subagents": trajectory["n_subagents_total"],
            "gate_invocations": trajectory["gate_invocations"],
            "harness_duplications": harness_duplications,
            "harness_duplications_count": len(harness_duplications),
        },
    }


def _claude_trajectory(tool_calls: list[dict]) -> dict:
    edit_tools = {"Edit", "Write", "MultiEdit", "NotebookEdit"}
    read_paths_ordered: list[str] = []
    read_paths_unique: set[str] = set()
    first_edit_idx: int | None = None
    n_edits = 0
    skills_used: Counter[str] = Counter()
    subagents_used: Counter[str] = Counter()
    gate_invocations = 0

    gate_re = re.compile(r"\b(pytest|npm test|go test|cargo test|pre-commit|make test)\b")

    for idx, tc in enumerate(tool_calls):
        name = tc.get("name")
        inp = tc.get("input") or {}

        if name == "Read":
            p = inp.get("file_path") or inp.get("path")
            if p:
                read_paths_ordered.append(p)
                read_paths_unique.add(p)

        if name in edit_tools:
            n_edits += 1
            if first_edit_idx is None:
                first_edit_idx = idx

        if name == "Skill":
            skill_name = inp.get("skill") or "<unknown>"
            skills_used[skill_name] += 1

        if name in ("Agent", "Task"):
            sub = inp.get("subagent_type") or "<default>"
            subagents_used[sub] += 1

        if name == "Bash":
            cmd = inp.get("command") or ""
            if gate_re.search(cmd):
                gate_invocations += 1

    # files_read_before_first_edit: count of unique files read before the first edit event.
    files_before_edit = 0
    if first_edit_idx is None:
        files_before_edit = len(read_paths_unique)
    else:
        seen: set[str] = set()
        for tc in tool_calls[:first_edit_idx]:
            if tc.get("name") == "Read":
                p = (tc.get("input") or {}).get("file_path") or (tc.get("input") or {}).get("path")
                if p:
                    seen.add(p)
        files_before_edit = len(seen)

    by_ext = Counter(_ext_of(p) for p in read_paths_ordered)

    return {
        "files_read_total": len(read_paths_ordered),
        "files_read_unique": len(read_paths_unique),
        "files_read_by_extension": dict(by_ext),
        "files_read_before_first_edit": files_before_edit,
        "n_edits": n_edits,
        "skills_used": dict(skills_used),
        "subagents_used": dict(subagents_used),
        "n_subagents_total": sum(subagents_used.values()),
        "gate_invocations": gate_invocations,
    }


# ---------------------------------------------------------------------------
# Codex `exec --json` parser
# ---------------------------------------------------------------------------


def parse_codex_session(path: Path, harness_basenames: set[str] | None = None) -> dict:
    """Parse a Codex `exec --json` session transcript.

    Handles TWO schemas (auto-detected per event):
      - NEW (2025-09+): `thread.started`, `turn.completed` with cumulative `usage`,
        `item.started` / `item.completed` with nested `item.type` (command_execution,
        agent_message, agent_reasoning, file_change, web_search, mcp_tool_call, plan_update).
        See https://developers.openai.com/codex/noninteractive and
        https://github.com/openai/codex/blob/main/docs/exec.md
      - OLD: top-level `session_configured`, `token_count`, `agent_message`,
        `agent_reasoning`, `exec_command_begin`, `tool_call`, `function_call`, `shell_call`,
        `web_search`, optionally nested under `payload` or `msg`.

    Token accounting: the `turn.completed.usage` field is CUMULATIVE across a session (see
    openai/codex#17539), so we take the LAST observed value as the total — summing would
    double-count. Old schema falls back to the final `token_count` info block.
    """
    events = list(_iter_jsonl(path))
    if not events:
        return {"agent": "codex", "error": f"no events in {path}", "raw_event_count": 0}

    # Tokens — either from new-schema turn.completed.usage (last one = cumulative total)
    # or from old-schema token_count info block.
    last_turn_usage: dict | None = None
    last_token_count: dict | None = None

    tool_calls: list[dict] = []
    n_agent_messages = 0
    n_user_messages = 0
    n_reasoning = 0
    reasoning_chars = 0
    web_searches = 0
    errors: list[str] = []
    model: str | None = None
    session_id: str | None = None
    thread_id: str | None = None
    # Track item.started so we can match item.completed events that only carry `item_id`.
    started_items: dict[str, dict] = {}

    for ev in events:
        et = ev.get("type") if isinstance(ev, dict) else None
        if not et:
            continue

        # ---- NEW SCHEMA (dotted types) ----
        if et == "thread.started":
            thread_id = ev.get("thread_id") or thread_id
            model = model or ev.get("model")
            continue
        if et == "turn.completed":
            usage = ev.get("usage")
            if isinstance(usage, dict):
                last_turn_usage = usage
            continue
        if et == "turn.failed":
            errors.append(str(ev.get("error") or ev.get("message") or "turn.failed"))
            continue
        if et == "error":
            errors.append(str(ev.get("message") or ev.get("error") or "error"))
            continue
        if et in ("item.started", "item.completed"):
            # Only count items on `item.completed` to avoid double-counting. For `item.started`
            # we just remember the payload so late `completed` events that lack details can
            # look it up by id.
            item = ev.get("item") or {}
            if et == "item.started":
                iid = item.get("id")
                if iid:
                    started_items[iid] = item
                continue
            # item.completed
            if not item:
                iid = ev.get("item_id")
                if iid and iid in started_items:
                    item = started_items[iid]
            it_type = item.get("type")
            if it_type == "agent_message":
                n_agent_messages += 1
            elif it_type in ("agent_reasoning", "reasoning"):
                n_reasoning += 1
                reasoning_chars += len(item.get("text") or item.get("reasoning") or "")
            elif it_type == "command_execution":
                cmd = item.get("command")
                tool_calls.append(
                    {
                        "name": _classify_codex_cmd_string(
                            cmd if isinstance(cmd, str) else json.dumps(cmd, default=str)
                        ),
                        "command": cmd if isinstance(cmd, str) else json.dumps(cmd, default=str),
                    }
                )
            elif it_type == "file_change":
                tool_calls.append(
                    {
                        "name": "Edit",
                        "command": json.dumps(
                            item.get("changes") or item.get("path") or "", default=str
                        ),
                    }
                )
            elif it_type == "web_search":
                web_searches += 1
                tool_calls.append({"name": "WebSearch", "command": item.get("query") or None})
            elif it_type == "mcp_tool_call":
                tool_calls.append(
                    {
                        "name": f"MCP:{item.get('server') or '?'}:{item.get('name') or item.get('tool') or '?'}",
                        "command": json.dumps(item.get("arguments") or {}, default=str),
                    }
                )
            elif it_type == "plan_update":
                # Not a tool call and not a message — just track as a trajectory signal.
                pass
            continue

        # ---- OLD SCHEMA (flat/wrapped types) ----
        # Codex used to wrap payloads under 'msg' or 'payload'; accept both for backward compat.
        payload = ev.get("payload") or ev.get("msg") or ev
        ptype = payload.get("type") if isinstance(payload, dict) else None
        if not ptype:
            continue

        if ptype == "session_configured":
            model = model or payload.get("model")
            session_id = session_id or payload.get("session_id") or ev.get("session_id")
        elif ptype == "token_count":
            info = payload.get("info") or payload
            last_token_count = info
        elif ptype == "agent_message":
            n_agent_messages += 1
        elif ptype == "agent_reasoning":
            n_reasoning += 1
            reasoning_chars += len((payload.get("text") or payload.get("reasoning") or ""))
        elif ptype == "user_message":
            n_user_messages += 1
        elif ptype in ("exec_command_begin", "tool_call", "function_call", "shell_call"):
            cmd = (
                payload.get("command")
                or (payload.get("call") or {}).get("command")
                or payload.get("name")
            )
            tool_calls.append(
                {
                    "name": _classify_codex_tool(payload),
                    "command": cmd if isinstance(cmd, str) else json.dumps(cmd, default=str),
                }
            )
        elif ptype == "web_search":
            web_searches += 1
            tool_calls.append({"name": "WebSearch", "command": None})

    tokens_summary = {
        "input": 0,
        "output": 0,
        "cache_read": 0,
        "cache_creation": 0,
        "reasoning": 0,
        "total": 0,
    }
    # Prefer new-schema cumulative usage when available.
    if last_turn_usage:
        tokens_summary["input"] = int(last_turn_usage.get("input_tokens") or 0)
        tokens_summary["cache_read"] = int(last_turn_usage.get("cached_input_tokens") or 0)
        tokens_summary["output"] = int(last_turn_usage.get("output_tokens") or 0)
        tokens_summary["reasoning"] = int(
            last_turn_usage.get("reasoning_output_tokens")
            or last_turn_usage.get("reasoning_tokens")
            or 0
        )
        tokens_summary["total"] = sum(
            tokens_summary[k] for k in ("input", "output", "cache_read", "reasoning")
        )
    elif last_token_count:
        tokens_summary["input"] = int(
            last_token_count.get("input_tokens") or last_token_count.get("total_input_tokens") or 0
        )
        tokens_summary["cache_read"] = int(
            last_token_count.get("cached_input_tokens")
            or last_token_count.get("cache_read_tokens")
            or 0
        )
        tokens_summary["output"] = int(
            last_token_count.get("output_tokens")
            or last_token_count.get("total_output_tokens")
            or 0
        )
        tokens_summary["reasoning"] = int(
            last_token_count.get("reasoning_tokens")
            or last_token_count.get("reasoning_output_tokens")
            or 0
        )
        tokens_summary["total"] = int(
            last_token_count.get("total_tokens")
            or sum(
                tokens_summary[k]
                for k in ("input", "output", "cache_read", "cache_creation", "reasoning")
            )
        )

    by_tool = Counter(tc["name"] or "<unknown>" for tc in tool_calls)
    trajectory = _codex_trajectory(tool_calls)
    harness_duplications = _detect_harness_duplications(tool_calls, harness_basenames or set())
    trajectory["harness_duplications"] = harness_duplications
    trajectory["harness_duplications_count"] = len(harness_duplications)

    return {
        "agent": "codex",
        "model": model,
        "session_id": session_id or thread_id,
        "thread_id": thread_id,
        "raw_event_count": len(events),
        "tokens": tokens_summary,
        "thinking": {
            "blocks": n_reasoning,
            "chars": reasoning_chars,
            "approx_tokens": tokens_summary["reasoning"] or (reasoning_chars // 4),
        },
        "cost_usd": None,  # Codex stream does not report cost; estimated downstream from pricing.
        "duration_ms_self_reported": None,
        "num_turns": None,
        "messages": {
            "assistant": n_agent_messages,
            "user": n_user_messages,
            "reasoning": n_reasoning,
        },
        "tool_calls": {
            "total": len(tool_calls),
            "by_tool": dict(by_tool),
            "web_searches": web_searches,
        },
        "errors": errors,
        "skills_used": {},
        "subagents_used": {},
        "trajectory": trajectory,
    }


def _classify_codex_cmd_string(cmd: str) -> str:
    """Classify a command string into a coarse tool category (mirrors Claude tools)."""
    if not cmd:
        return "Bash"
    s = cmd.strip()
    if s.startswith(("apply_patch", "patch")) or " apply_patch" in s:
        return "Edit"
    if s.startswith(("cat ", "head ", "tail ", "less ")) or "sed -n" in s:
        return "Read"
    if s.startswith(("rg ", "grep ")) or " | grep " in s:
        return "Grep"
    if s.startswith(("ls", "find ")) or "fd " in s:
        return "Glob"
    return "Bash"


def _classify_codex_tool(payload: dict) -> str:
    """Heuristic mapping of Codex tool-call payload to a coarse tool category (mirrors Claude tools)."""
    if payload.get("type") == "web_search":
        return "WebSearch"
    cmd = payload.get("command")
    if isinstance(cmd, list):
        cmd_str = " ".join(str(c) for c in cmd)
    elif isinstance(cmd, str):
        cmd_str = cmd
    else:
        cmd_str = ""
    if not cmd_str:
        return payload.get("name") or "<unknown>"
    if cmd_str.startswith(("apply_patch", "patch")) or " apply_patch" in cmd_str:
        return "Edit"
    if cmd_str.startswith(("cat ", "head ", "tail ", "less ")) or "sed -n" in cmd_str:
        return "Read"
    if cmd_str.startswith(("rg ", "grep ")) or " | grep " in cmd_str:
        return "Grep"
    if cmd_str.startswith(("ls", "find ")) or "fd " in cmd_str:
        return "Glob"
    return "Bash"


def _codex_trajectory(tool_calls: list[dict]) -> dict:
    read_paths_ordered: list[str] = []
    read_paths_unique: set[str] = set()
    first_edit_idx: int | None = None
    n_edits = 0
    gate_invocations = 0
    gate_re = re.compile(r"\b(pytest|npm test|go test|cargo test|pre-commit|make test)\b")

    for idx, tc in enumerate(tool_calls):
        name = tc.get("name")
        cmd = tc.get("command") or ""
        if name == "Read":
            # Crude path extraction from `cat X`, `sed -n ... X`.
            for t in reversed(cmd.split()):
                if "/" in t or t.endswith(
                    (".py", ".md", ".sh", ".yaml", ".json", ".toml", ".js", ".ts", ".go")
                ):
                    read_paths_ordered.append(t)
                    read_paths_unique.add(t)
                    break
        if name == "Edit":
            n_edits += 1
            if first_edit_idx is None:
                first_edit_idx = idx
        if gate_re.search(cmd):
            gate_invocations += 1

    files_before_edit = 0
    if first_edit_idx is None:
        files_before_edit = len(read_paths_unique)
    else:
        seen: set[str] = set()
        for tc in tool_calls[:first_edit_idx]:
            if tc.get("name") == "Read":
                for t in reversed((tc.get("command") or "").split()):
                    if "/" in t or t.endswith(
                        (".py", ".md", ".sh", ".yaml", ".json", ".toml", ".js", ".ts", ".go")
                    ):
                        seen.add(t)
                        break
        files_before_edit = len(seen)

    return {
        "files_read_total": len(read_paths_ordered),
        "files_read_unique": len(read_paths_unique),
        "files_read_by_extension": dict(Counter(_ext_of(p) for p in read_paths_ordered)),
        "files_read_before_first_edit": files_before_edit,
        "n_edits": n_edits,
        "n_subagents": 0,  # Codex has no sub-agent primitive
        "gate_invocations": gate_invocations,
    }


# ---------------------------------------------------------------------------
# OpenCode parser — STUB
# ---------------------------------------------------------------------------


def parse_opencode_stub(path: Path, harness_basenames: set[str] | None = None) -> dict:
    """Placeholder for OpenCode. Counts raw events so the transcript is preserved and
    at-least-one signal is exposed. See references/extending-agents.md for how to
    replace this with a proper parser once the OpenCode event schema is stable.
    """
    events = list(_iter_jsonl(path))
    return {
        "agent": "opencode",
        "error": "opencode parser not yet implemented — session.jsonl captured for manual analysis",
        "raw_event_count": len(events),
        "tokens": {"input": 0, "output": 0, "cache_read": 0, "cache_creation": 0, "total": 0},
        "tool_calls": {"total": 0, "by_tool": {}},
        "skills_used": {},
        "subagents_used": {},
        "trajectory": {},
    }


PARSERS = {
    "claude": parse_claude_session,
    "codex": parse_codex_session,
    "opencode": parse_opencode_stub,
}


# ---------------------------------------------------------------------------
# Pricing & cost estimation
# ---------------------------------------------------------------------------


def load_pricing(path: Path | None = None) -> dict:
    """Load pricing.json from the given path or the script's sibling file."""
    path = path or (Path(__file__).parent / "pricing.json")
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text())
        return data.get("models", {}) or {}
    except (json.JSONDecodeError, OSError):
        return {}


def estimate_cost_usd(model: str | None, tokens: dict, pricing: dict) -> float | None:
    """TTL-aware cost estimate. Prefers 5m/1h cache creation breakdown when present."""
    if not model or not pricing:
        return None
    p = pricing.get(model)
    if p is None:
        for k, v in pricing.items():
            if model.startswith(k):
                p = v
                break
    if p is None:
        return None

    cc_5m = tokens.get("cache_creation_5m_ttl", 0)
    cc_1h = tokens.get("cache_creation_1h_ttl", 0)
    cc_fallback = tokens.get("cache_creation", 0) - cc_5m - cc_1h  # uncategorized share

    return (
        tokens.get("input", 0) * p["input"]
        + tokens.get("output", 0) * p["output"]
        + tokens.get("cache_read", 0) * p["cache_read"]
        + cc_5m * p["cache_creation_5m"]
        + cc_1h * p["cache_creation_1h"]
        + max(cc_fallback, 0) * p["cache_creation_5m"]
    ) / 1_000_000


# ---------------------------------------------------------------------------
# Run-directory aggregator
# ---------------------------------------------------------------------------


def _extract_variant_stats(payload: Any, variant: str) -> dict | None:
    """Given a measure_cmd output payload, extract the per-variant stats block.

    Supports:
      - `{"variants": {"<name>": {...}}}` — canonical multi-variant
      - flat `{"wall_s": {...}, "cpu_s": {...}, ...}` with optional `variant`/`name` field
    """
    if not isinstance(payload, dict) or "error" in payload:
        return None
    variants = payload.get("variants")
    if isinstance(variants, dict):
        return variants.get(variant)
    if payload.get("variant") == variant or payload.get("name") == variant:
        return payload
    return None


def _variant_names(payload: Any) -> list[str]:
    """List the variants present in a measure_cmd output payload."""
    if not isinstance(payload, dict) or "error" in payload:
        return []
    variants = payload.get("variants")
    if isinstance(variants, dict):
        return list(variants.keys())
    if "wall_s" in payload or "cpu_s" in payload:
        return [payload.get("variant") or payload.get("name") or "default"]
    return []


def _compute_variant_speedup(baseline: dict, post: dict) -> dict:
    """Compute before/after deltas for a single variant.

    Expected shape per side:
      {"wall_s": {"median":..,"min":..,"mean":..,"stddev":..}, "cpu_s": {...}, "n_runs": N}

    Reports fast-cluster min as the primary metric (robust against macOS Pool bimodality —
    see references/methodology.md) plus median, mean, CPU median, and stddev-as-%-of-median
    as a noise indicator.
    """
    b_wall = baseline.get("wall_s") or {}
    p_wall = post.get("wall_s") or {}
    b_cpu = baseline.get("cpu_s") or {}
    p_cpu = post.get("cpu_s") or {}

    def delta(b: Any, p: Any) -> dict:
        if not isinstance(b, (int, float)) or not isinstance(p, (int, float)):
            return {"baseline": b, "post": p, "delta": None, "pct_reduction": None}
        d = p - b
        return {
            "baseline": b,
            "post": p,
            "delta": d,
            "pct_reduction": (-d / b * 100) if b else None,
        }

    b_stddev_pct = (
        b_wall["stddev"] / b_wall["median"] * 100
        if isinstance(b_wall.get("stddev"), (int, float))
        and isinstance(b_wall.get("median"), (int, float))
        and b_wall.get("median")
        else None
    )
    noise_warning = bool(b_stddev_pct and b_stddev_pct > 10.0)

    return {
        "n_runs_baseline": baseline.get("n_runs"),
        "n_runs_post": post.get("n_runs"),
        "wall_min": delta(b_wall.get("min"), p_wall.get("min")),
        "wall_median": delta(b_wall.get("median"), p_wall.get("median")),
        "wall_mean": delta(b_wall.get("mean"), p_wall.get("mean")),
        "cpu_median": delta(b_cpu.get("median"), p_cpu.get("median")),
        "stddev_pct_of_median": {
            "baseline": b_stddev_pct,
            "post": (
                p_wall["stddev"] / p_wall["median"] * 100
                if isinstance(p_wall.get("stddev"), (int, float))
                and isinstance(p_wall.get("median"), (int, float))
                and p_wall.get("median")
                else None
            ),
        },
        "noise_warning": noise_warning,
    }


def aggregate_run_dir(agent: str, run_dir: Path, pricing: dict) -> dict:
    """Aggregate all artifacts in a run_trial.py output directory into a single metrics dict."""
    out: dict[str, Any] = {"agent": agent, "run_dir": str(run_dir)}

    # Harness command basenames — used by the parser to detect duplication events
    # (agent re-running gate_cmd / measure_cmd inside its own session).
    harness_basenames: set[str] = set()
    hc_path = run_dir / "harness_commands.json"
    if hc_path.exists():
        try:
            hc = json.loads(hc_path.read_text())
            harness_basenames = set(hc.get("gate_basenames") or []) | set(
                hc.get("measure_basenames") or []
            )
            out["harness_commands"] = hc
        except (json.JSONDecodeError, OSError):
            pass

    # Session transcript
    session_path = run_dir / "session.jsonl"
    parser = PARSERS.get(agent)
    if parser is None:
        out["session"] = {"error": f"unknown agent: {agent}"}
    elif not session_path.exists():
        out["session"] = {"error": "session.jsonl missing"}
    else:
        out["session"] = parser(session_path, harness_basenames)

    # Cost estimate if not self-reported.
    session = out["session"]
    if isinstance(session, dict) and session.get("tokens") and not session.get("cost_usd"):
        session["cost_usd_estimated"] = estimate_cost_usd(
            session.get("model"), session["tokens"], pricing
        )

    # External session wall time (captured by run_trial.py from /usr/bin/time or a wrapper)
    sw = run_dir / "session_wall_seconds.txt"
    if sw.exists():
        try:
            out["session_wall_seconds_external"] = int(sw.read_text().strip() or 0)
        except ValueError:
            pass

    # Baseline / post measurement JSON (literal output of task's measure_cmd).
    for label in ("baseline", "post"):
        p = run_dir / f"{label}.json"
        if p.exists():
            try:
                out[label] = json.loads(p.read_text())
            except json.JSONDecodeError as e:
                out[label] = {"error": f"could not parse {label}.json: {e}"}

    # Per-variant speedup derived metrics.
    baseline_variants = _variant_names(out.get("baseline"))
    post_variants = _variant_names(out.get("post"))
    common = [v for v in baseline_variants if v in post_variants]
    if common:
        out["speedup"] = {}
        for v in common:
            b = _extract_variant_stats(out.get("baseline"), v)
            p = _extract_variant_stats(out.get("post"), v)
            if b is None or p is None:
                continue
            try:
                out["speedup"][v] = _compute_variant_speedup(b, p)
            except (KeyError, TypeError, ZeroDivisionError) as e:
                out["speedup"][v] = {"error": str(e)}

    # Gate result
    rc = run_dir / "gate_exit_code.txt"
    if rc.exists():
        try:
            code = int(rc.read_text().strip())
            out["gate"] = {
                "exit_code": code,
                "passed": code == 0,
                "log_path": str(run_dir / "gate.log"),
            }
        except ValueError:
            out["gate"] = {"error": "invalid exit code"}

    # Gate preflight (the gate executed on HEAD before the trial started)
    preflight = run_dir / "gate_preflight_exit_code.txt"
    if preflight.exists():
        try:
            out["gate_preflight"] = {"exit_code": int(preflight.read_text().strip())}
        except ValueError:
            pass

    # Diff stats
    ds = run_dir / "diff_stat.txt"
    if ds.exists():
        text = ds.read_text()
        last = text.strip().splitlines()[-1] if text.strip() else ""
        m = re.search(
            r"(\d+) files? changed(?:,\s*(\d+) insertions?\(\+\))?(?:,\s*(\d+) deletions?\(-\))?",
            last,
        )
        if m:
            out["diff"] = {
                "files_changed": int(m.group(1)),
                "insertions": int(m.group(2) or 0),
                "deletions": int(m.group(3) or 0),
                "stat_text": text,
            }
        else:
            out["diff"] = {"stat_text": text}

    # Commits made by the agent (should be 0 — the agent is instructed not to commit; the
    # snapshot commit is added by run_trial.py after agent exit, not here).
    commits = run_dir / "commits.txt"
    if commits.exists():
        out["commits_made"] = [ln for ln in commits.read_text().splitlines() if ln.strip()]

    # Branch name for the persisted worktree (lets the user check out the agent's work)
    bn = run_dir / "branch_name.txt"
    if bn.exists():
        out["branch_name"] = bn.read_text().strip()

    # Start commit (for downstream diff commands)
    sc = run_dir / "start_commit.txt"
    if sc.exists():
        out["start_commit"] = sc.read_text().strip()

    return out


# ---------------------------------------------------------------------------
# Cross-agent comparison
# ---------------------------------------------------------------------------


def build_comparison(run_metrics: list[dict]) -> dict:
    """Side-by-side aggregation of multiple per-run metrics dicts."""
    trials = []
    for m in run_metrics:
        sess = m.get("session") or {}
        trial = {
            "agent": m.get("agent"),
            "run_dir": m.get("run_dir"),
            "branch_name": m.get("branch_name"),
            "model": sess.get("model"),
            "cost_usd": sess.get("cost_usd") or sess.get("cost_usd_estimated"),
            "tokens_total": (sess.get("tokens") or {}).get("total"),
            "thinking_approx_tokens": (sess.get("thinking") or {}).get("approx_tokens"),
            "num_turns": sess.get("num_turns"),
            "session_wall_s": m.get("session_wall_seconds_external"),
            "duration_ms_self": sess.get("duration_ms_self_reported"),
            "tool_calls_total": (sess.get("tool_calls") or {}).get("total"),
            "n_subagents": (sess.get("trajectory") or {}).get("n_subagents"),
            "skills_used": sess.get("skills_used") or {},
            "subagents_used": sess.get("subagents_used") or {},
            "files_read_total": (sess.get("trajectory") or {}).get("files_read_total"),
            "files_read_unique": (sess.get("trajectory") or {}).get("files_read_unique"),
            "files_read_before_first_edit": (sess.get("trajectory") or {}).get(
                "files_read_before_first_edit"
            ),
            "n_edits": (sess.get("trajectory") or {}).get("n_edits"),
            "harness_duplications_count": (sess.get("trajectory") or {}).get(
                "harness_duplications_count", 0
            )
            or 0,
            "harness_duplications": (sess.get("trajectory") or {}).get("harness_duplications")
            or [],
            "gate_passed": (m.get("gate") or {}).get("passed"),
            "diff_files_changed": (m.get("diff") or {}).get("files_changed"),
            "speedup_summary": _summarize_speedup(m.get("speedup") or {}),
        }
        trials.append(trial)
    return {"trials": trials, "n_trials": len(trials)}


def _summarize_speedup(speedup: dict) -> dict:
    """Collapse per-variant speedup into a single top-line for cross-trial comparison."""
    out = {}
    for variant, s in speedup.items():
        if not isinstance(s, dict) or "error" in s:
            continue
        out[variant] = {
            "wall_min_pct": (s.get("wall_min") or {}).get("pct_reduction"),
            "wall_median_pct": (s.get("wall_median") or {}).get("pct_reduction"),
            "noise_warning": s.get("noise_warning"),
        }
    return out


# ---------------------------------------------------------------------------
# Markdown rendering
# ---------------------------------------------------------------------------


def render_template(template_path: Path, metrics: dict) -> str:
    """Substitute `{{dotted.key.path}}` placeholders with lookups from `metrics`."""
    text = template_path.read_text()

    def lookup(dotted: str) -> str:
        parts = dotted.split(".")
        cur: Any = metrics
        for p in parts:
            if isinstance(cur, dict) and p in cur:
                cur = cur[p]
            else:
                return f"<MISSING:{dotted}>"
        if isinstance(cur, float):
            return f"{cur:.4f}"
        if isinstance(cur, (list, dict)):
            return json.dumps(cur, indent=2, default=str)
        return str(cur)

    return re.sub(r"\{\{([^}]+)\}\}", lambda m: lookup(m.group(1).strip()), text)


def render_comparison(comparison: dict) -> str:
    """Render a cross-agent comparison as a concise markdown table."""
    trials = comparison.get("trials", [])
    if not trials:
        return "# Comparison\n\nNo trials to compare.\n"

    lines = ["# Cross-agent comparison\n"]
    lines.append(f"**Trials:** {len(trials)}\n")
    lines.append("## Summary\n")
    header = "| Agent | Model | Gate | Cost USD | Tokens | Thinking | Turns | Wall s | Tools | Sub-agents | Skills | Edits | Files changed | Branch |"
    sep = "|" + "|".join(["---"] * 14) + "|"
    lines.append(header)
    lines.append(sep)
    for t in trials:
        gate = "✓" if t.get("gate_passed") else ("✗" if t.get("gate_passed") is False else "?")
        cost = f"${t['cost_usd']:.2f}" if isinstance(t.get("cost_usd"), (int, float)) else "-"
        tokens = f"{t['tokens_total']:,}" if isinstance(t.get("tokens_total"), int) else "-"
        think = (
            f"{t['thinking_approx_tokens']:,}"
            if isinstance(t.get("thinking_approx_tokens"), int)
            else "-"
        )
        turns = t.get("num_turns") or "-"
        wall = t.get("session_wall_s") or "-"
        tools = t.get("tool_calls_total") or "-"
        subs = t.get("n_subagents") or 0
        skills = len(t.get("skills_used") or {})
        edits = t.get("n_edits") or 0
        changed = t.get("diff_files_changed") or 0
        branch = t.get("branch_name") or "-"
        lines.append(
            f"| {t.get('agent')} | {t.get('model') or '-'} | {gate} | {cost} | {tokens} | {think} | {turns} | {wall} | {tools} | {subs} | {skills} | {edits} | {changed} | `{branch}` |"
        )

    # Speedup table, variant-by-variant
    all_variants: set[str] = set()
    for t in trials:
        all_variants.update((t.get("speedup_summary") or {}).keys())
    if all_variants:
        lines.append("\n## Speedup (per variant, % reduction vs baseline)\n")
        lines.append(
            "| Agent | " + " | ".join(f"{v} wall_min" for v in sorted(all_variants)) + " |"
        )
        lines.append("|" + "|".join(["---"] * (len(all_variants) + 1)) + "|")
        for t in trials:
            ss = t.get("speedup_summary") or {}
            cells = []
            for v in sorted(all_variants):
                val = (ss.get(v) or {}).get("wall_min_pct")
                cells.append(f"{val:.1f}%" if isinstance(val, (int, float)) else "-")
            lines.append(f"| {t.get('agent')} | " + " | ".join(cells) + " |")

    # Agent discipline — harness-protocol violations detected in session.jsonl
    any_dup = any((t.get("harness_duplications_count") or 0) > 0 for t in trials)
    if any_dup:
        lines.append("\n## Agent discipline — harness duplications\n")
        lines.append(
            "Tool-call invocations where the agent ran a command whose basename matches "
            "the harness-owned `gate_cmd` / `measure_cmd`. Non-zero counts indicate "
            "protocol violations that inflate wall time and contaminate measurement.\n"
        )
        lines.append("| Agent | Duplications | Matched basenames |")
        lines.append("|---|---|---|")
        for t in trials:
            n = t.get("harness_duplications_count") or 0
            dups = t.get("harness_duplications") or []
            matched = sorted({d.get("matched") for d in dups if d.get("matched")})
            matched_str = ", ".join(f"`{m}`" for m in matched) if matched else "-"
            marker = "✓" if n == 0 else f"✗ × {n}"
            lines.append(f"| {t.get('agent')} | {marker} | {matched_str} |")

    lines.append("\n## Per-trial details\n")
    for t in trials:
        lines.append(f"### {t.get('agent')} — `{t.get('run_dir')}`")
        lines.append("")
        if t.get("skills_used"):
            lines.append(f"- **Skills used:** {json.dumps(t['skills_used'], ensure_ascii=False)}")
        if t.get("subagents_used"):
            lines.append(f"- **Sub-agents:** {json.dumps(t['subagents_used'], ensure_ascii=False)}")
        lines.append(
            f"- **Files read:** total={t.get('files_read_total') or 0}, unique={t.get('files_read_unique') or 0}, before-first-edit={t.get('files_read_before_first_edit') or 0}"
        )
        dup_count = t.get("harness_duplications_count") or 0
        if dup_count:
            dups = t.get("harness_duplications") or []
            sample = dups[:3]
            lines.append(
                f"- **Harness duplications:** {dup_count} — first {len(sample)}: "
                + "; ".join(
                    f"idx {d.get('tool_call_index')} matched `{d.get('matched')}`" for d in sample
                )
            )
        lines.append("")

    lines.append(
        "\n> **Manual review still required**: hard-constraint compliance, code quality, "
        "and adherence to prompt. See each per-trial `report.md`.\n"
    )
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--agent", choices=["claude", "codex", "opencode"])
    parser.add_argument("--session", type=Path, help="path to session.jsonl (transcript-only mode)")
    parser.add_argument(
        "--run-dir", type=Path, help="aggregate all artifacts in a run_trial.py output directory"
    )
    parser.add_argument(
        "--aggregate",
        nargs="+",
        type=Path,
        help="cross-agent mode: multiple run dirs to build a comparison report",
    )
    parser.add_argument("--output", type=Path, help="write metrics JSON here (default: stdout)")
    parser.add_argument(
        "--render-report", type=Path, help="render a markdown report from a template to this path"
    )
    parser.add_argument(
        "--template",
        type=Path,
        default=Path(__file__).parent.parent / "references" / "report_template.md",
        help="path to the markdown template (used with --run-dir)",
    )
    parser.add_argument(
        "--pricing",
        type=Path,
        default=Path(__file__).parent / "pricing.json",
        help="path to pricing.json",
    )
    args = parser.parse_args()

    pricing = load_pricing(args.pricing)

    if args.aggregate:
        # Cross-agent comparison mode.
        run_metrics = []
        for run_dir in args.aggregate:
            # Prefer the pre-existing metrics.json if available (faster, matches what the user
            # sees in the per-trial report); otherwise re-aggregate from artifacts.
            mjson = run_dir / "metrics.json"
            if mjson.exists():
                try:
                    run_metrics.append(json.loads(mjson.read_text()))
                    continue
                except json.JSONDecodeError:
                    pass
            # Infer agent from path — the run_dir layout is .../<agent>/run-<id>-<ts>.
            inferred_agent = run_dir.parent.name if run_dir.parent.name in PARSERS else "claude"
            run_metrics.append(aggregate_run_dir(inferred_agent, run_dir, pricing))

        comparison = build_comparison(run_metrics)
        payload = json.dumps(comparison, indent=2, default=str)

        if args.output:
            args.output.write_text(payload + "\n")
            print(f"wrote {args.output}", file=sys.stderr)
        else:
            print(payload)

        if args.render_report:
            args.render_report.write_text(render_comparison(comparison))
            print(f"wrote {args.render_report}", file=sys.stderr)
        return 0

    # Single-run aggregation / single-transcript parse.
    if not args.agent:
        parser.error("provide --agent (required unless using --aggregate)")

    if args.run_dir:
        metrics = aggregate_run_dir(args.agent, args.run_dir, pricing)
    elif args.session:
        fn = PARSERS[args.agent]
        session = fn(args.session)
        if session.get("tokens") and not session.get("cost_usd"):
            session["cost_usd_estimated"] = estimate_cost_usd(
                session.get("model"), session["tokens"], pricing
            )
        metrics = {"agent": args.agent, "session": session}
    else:
        parser.error("provide --session or --run-dir (or --aggregate)")

    payload = json.dumps(metrics, indent=2, default=str)
    if args.output:
        args.output.write_text(payload + "\n")
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        print(payload)

    if args.render_report:
        template = args.template
        if not template.exists():
            print(f"WARN: template not found at {template}", file=sys.stderr)
        else:
            rendered = render_template(template, metrics)
            args.render_report.write_text(rendered)
            print(f"wrote {args.render_report}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
