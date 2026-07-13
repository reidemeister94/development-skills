---
name: ai-agent-bench
description: "Compare Claude Code and Codex on the same real code-change task with isolated worktrees, identical gates, transcripts, time, and cost."
user-invocable: true
allowed-tools: Glob, Grep, Read, Bash, Edit, Write
---

# AI agent bench

Benchmark agents only when the task, starting commit, and outcome check are identical. The harness keeps each result branch and removes its temporary worktree.

Create `<repo>/.agent-bench.toml`:

```toml
prompt = "prompts/task.md"
start_branch = "main"              # or start_commit
agents = ["claude", "codex"]
outer_check = "./scripts/full_check.sh"
inner_check = "pytest tests/integration/test_x.py -q"
```

`outer_check` is both the before/after gate and wall-time measure; it must exercise the real outcome. `inner_check` is the fast command agents use while working.

Require a clean repository, available CLIs, and a passing `outer_check` before trials. Confirm the agents and next run ID, then run each agent **sequentially** so concurrent load cannot corrupt timing:

```bash
python <skill>/scripts/run_trial.py --repo "$REPO" --config "$REPO/.agent-bench.toml" --agent "$AGENT" --run "$RUN_ID"
```

Results live under `eval-results/<task>/<agent>/run-<id>-<timestamp>/`. Unexpected harness or agent behavior is appended to `ai-agent-bench-anomalies.md`; details are in [anomalies.md](references/anomalies.md).

Aggregate completed runs with `scripts/parse_transcript.py --aggregate <run-dirs> --output comparison.json --render-report comparison.md`. Report gate results, branches, time delta, tokens, and cost; never rank a failed trial as faster.

For plugin behavior rather than a real code task, use the Pydantic runner documented by `eval-regression` and `scripts/fresh_context_eval.py`.

Never commit on the user's branch. A repeated run creates a new timestamped result and preserves prior evidence.
