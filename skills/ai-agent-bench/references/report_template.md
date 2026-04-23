# Agent trial report

- **Agent:** {{agent}}
- **Model:** {{session.model}}
- **Run dir:** `{{run_dir}}`
- **Branch preserved:** `{{branch_name}}`
- **Start commit:** `{{start_commit}}`

---

## Tier 1 — Gate & task outcome

| | |
|---|---|
| Gate passed | {{gate.passed}} |
| Gate exit code | {{gate.exit_code}} |
| Gate log | `{{gate.log_path}}` |
| Diff files changed | {{diff.files_changed}} |
| Insertions / deletions | +{{diff.insertions}} / -{{diff.deletions}} |

### Speedup (per variant)

{{speedup}}

---

## Tier 2 — Cost & velocity

| | |
|---|---|
| Cost USD (self-reported) | {{session.cost_usd}} |
| Cost USD (estimated) | {{session.cost_usd_estimated}} |
| Input tokens | {{session.tokens.input}} |
| Output tokens | {{session.tokens.output}} |
| Cache read tokens | {{session.tokens.cache_read}} |
| Cache creation tokens | {{session.tokens.cache_creation}} |
| — of which 5m TTL | {{session.tokens.cache_creation_5m_ttl}} |
| — of which 1h TTL | {{session.tokens.cache_creation_1h_ttl}} |
| Total tokens | {{session.tokens.total}} |
| Thinking blocks | {{session.thinking.blocks}} |
| Thinking chars | {{session.thinking.chars}} |
| Thinking approx tokens | {{session.thinking.approx_tokens}} |
| External wall time (s) | {{session_wall_seconds_external}} |
| Self-reported duration ms | {{session.duration_ms_self_reported}} |
| Num turns | {{session.num_turns}} |
| Assistant messages | {{session.messages.assistant}} |

### Tool usage

- **Total calls:** {{session.tool_calls.total}}
- **Avg parallel calls per message:** {{session.tool_calls.avg_parallel_calls_per_message}}
- **By tool:**

```
{{session.tool_calls.by_tool}}
```

- **Parallel distribution (calls-per-message):**

```
{{session.tool_calls.parallel_distribution}}
```

### Skills invoked

```
{{session.skills_used}}
```

### Sub-agents invoked

```
{{session.subagents_used}}
```

---

## Tier 3 — Methodology & trajectory

| | |
|---|---|
| Files read (total) | {{session.trajectory.files_read_total}} |
| Files read (unique) | {{session.trajectory.files_read_unique}} |
| Files read before first edit | {{session.trajectory.files_read_before_first_edit}} |
| Edits | {{session.trajectory.n_edits}} |
| Sub-agents (total) | {{session.trajectory.n_subagents}} |
| Gate invocations (from bash) | {{session.trajectory.gate_invocations}} |

### Files read by extension

```
{{session.trajectory.files_read_by_extension}}
```

### Commits made by agent

```
{{commits_made}}
```

> The agent is instructed not to commit. The snapshot commit on the eval branch is added by the
> harness AFTER the agent exits — it is NOT counted here. This list should be empty in normal runs.

---

## Manual review (fill in by hand)

The automated metrics above cover cost, velocity, and trajectory. The questions below cannot be
scored automatically — a human reviewer must inspect the diff on `{{branch_name}}`.

### Hard-constraint compliance

- [ ] All constraints listed in the prompt are preserved (list each; check or flag deviation).

### Prompt adherence

- [ ] The diff addresses the stated goal and nothing else.
- [ ] No out-of-scope refactoring.
- [ ] No fabricated constraints or invented requirements.

### Code quality (1–5 scale each)

| Dimension | Score | Notes |
|---|---|---|
| Simplicity | | |
| Readability | | |
| Correctness | | |
| Test quality | | |
| Comments (WHY not WHAT) | | |

### Behavioral risks

- [ ] Performance claim backed by post.json (not just prose).
- [ ] Noise warning? `{{speedup}}` — check `noise_warning` per variant.
- [ ] Gate preflight passed on HEAD before trial.

### Final verdict

- **Accept (merge):** ___
- **Accept with changes:** ___
- **Reject:** ___
- **Notes:**
