# `.ai-agent-bench.toml` schema

The wizard (`/ai-agent-bench`) writes this file at the root of the target repo after collecting
answers. It is read by `run_trial.py` on every trial. The file is idempotent — safe to hand-edit
between trials.

## Fields

| Key | Required | Type | Purpose |
|---|---|---|---|
| `name` | yes | string | Task label. Used as the top-level dir in `eval-results/<name>/...`. Kebab-case recommended. |
| `start_commit` | yes | string | SHA, branch, or ref. Resolved to a SHA by the harness. The agent works from this commit. |
| `prompt_file` | yes | string | Path (relative to repo or absolute) to a markdown file containing the task prompt. `{{START_COMMIT}}` placeholder is expanded. |
| `measure_cmd` | no | string | Shell command that prints benchmark JSON to stdout. Run in the worktree. Placeholders: `{repo}`, `{worktree}`, `{run_dir}`. Omit if the task has no perf dimension. |
| `gate_cmd` | no | string | Shell command whose exit code gates correctness. Preflight-validated on HEAD before the trial starts. Placeholders as above. |
| `pre_hooks` | no | array[string] | Shell commands executed in the worktree after creation, before baseline. Use for copying gitignored fixtures or env files. |
| `agent_test_commands` | no | array[string] | Fast commands the implementer agent may run during iteration (unit tests, cheap benches, lint). The harness appends them to `prompt_resolved.md` under "You MAY run" so the agent knows what is safe. Never put `measure_cmd` or `gate_cmd` here — those are orchestrator-owned. |
| `description` | no | string | Free-text. Not consumed programmatically — just documentation. |
| `no_gate_justification` | no | string | Written justification when the user skips the correctness gate. Surfaced in the report. Set by the wizard only. |
| `no_sufficiency_justification` | no | string | Full-sentence justification when the user overrides the Test sufficiency check (step `1.A.1b`). Only allowed for weaker signals (`MISSING_MODULE_COVERAGE`, `WEAK_ASSERTIONS`, Tier 2 `INSUFFICIENT`/`PARTIAL`). Never set for `NO_TESTS_IN_GATE` or `NO_TEST_FILES` — those are hard-stop with no override. Surfaces in the report as `unverified-sufficiency`. |
| `prompt_hygiene_override` | no | string | Full-sentence justification when the user overrides the Prompt hygiene check (Phase B step 2.b). Set when the prompt contains iterative-measurement or profiling instructions contrary to the harness protocol. Surfaces in the report as `prompt-hygiene-override`. |

## Recommended `measure_cmd` output convention

Multi-variant (e.g. one variant per dataset, region, config profile):

```json
{
  "variants": {
    "small_dataset": {
      "wall_s":  {"median": 7.8, "min": 7.1, "mean": 8.0, "stddev": 0.6, "p95": 8.9},
      "cpu_s":   {"median": 6.9, "min": 6.2, "mean": 7.0, "stddev": 0.5},
      "n_runs":  15
    },
    "large_dataset": { "wall_s": {...}, "cpu_s": {...}, "n_runs": 15 }
  }
}
```

Single-variant (flat, no `variants` key):

```json
{
  "wall_s": {"median": 7.8, "min": 7.1, "mean": 8.0, "stddev": 0.6},
  "cpu_s":  {"median": 6.9, ...},
  "n_runs": 15,
  "variant": "default"
}
```

The parser computes per-variant deltas automatically. Any field that's not numeric is passed
through untouched — so you can include arbitrary extra fields for your own post-hoc analysis.

## Example — Python performance task with gitignored fixtures

```toml
name = "hot-path-speedup"
start_commit = "HEAD"
prompt_file = "prompts/hot-path.md"
description = "Reduce wall time of the critical path"

# The worktree is created at start_commit, but gitignored fixture files aren't part of that
# commit — copy them in from the source repo before measurement.
pre_hooks = [
  "mkdir -p tests/fixtures",
  "cp -r {repo}/tests/fixtures/. tests/fixtures/",
  "mkdir -p .env.d && cp {repo}/.env.d/*.env .env.d/ 2>/dev/null || true",
]

measure_cmd = "python scripts/bench.py --runs 15 --warmup 2"

gate_cmd = "pytest -q && pytest -m integration -q"

# Fast commands the agent may run inside its session for self-correction. Never
# list `measure_cmd` or `gate_cmd` here — those are orchestrator-owned and the
# harness will flag duplicate runs in the final report.
agent_test_commands = [
  "pytest tests/unit -q",
  "python scripts/quick_bench.py --runs 3",
]
```

## Example — Node.js refactor task

```toml
name = "api-handler-refactor"
start_commit = "HEAD"
prompt_file = "prompts/handler-refactor.md"

measure_cmd = "hyperfine --export-json - --runs 15 --warmup 2 'npm run bench:handler'"

gate_cmd = "npm test && npm run typecheck"
```

## Example — Go optimization task

```toml
name = "query-planner-opt"
start_commit = "HEAD"
prompt_file = "prompts/planner-opt.md"

measure_cmd = "go test -bench=BenchmarkPlanner -benchmem -count=5 -run=^$ ./planner/... -json"

gate_cmd = "go test ./... -race"
```

## Example — doc-only task (gate-only, no perf)

```toml
name = "api-docs-cleanup"
start_commit = "HEAD"
prompt_file = "prompts/docs-cleanup.md"

# no measure_cmd — skipped automatically
gate_cmd = "markdownlint '**/*.md' && mkdocs build --strict"
```
