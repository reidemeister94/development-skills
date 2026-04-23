# `AI_AGENT_BENCH_ANOMALIES.md` — format spec

This document defines how the wizard (and any orchestrator invoking the skill) writes the
live anomaly log during a trial. The log captures anything that happens that **should not
have happened** or that weakens the scientific validity of the run.

## File location and lifecycle

- **Path**: `<repo-root>/AI_AGENT_BENCH_ANOMALIES.md` (NOT inside `eval-results/` — it must
  be visible at the project root so the user sees it immediately).
- **Creation**: if missing, create it with the top-level header (see below) on the first
  anomaly of the first run.
- **Append-only**: never overwrite. Every new run appends a new `## Active Run` block;
  every new anomaly during a run appends an `### <ISO timestamp> — <short title>` entry
  under that run's `## Event Log` section.
- **Gitignore**: listed in the `.gitignore` block the wizard proposes in Step 2. The log is
  operational, not source-of-truth — keep it out of version control.

## Top-level structure

```markdown
# AI Agent Bench Anomalies

Anything unexpected, unhandled, or operationally relevant during `/ai-agent-bench` runs.

## Logging Policy

- Scope: ai-agent-bench wizard + trial harness + live monitoring + agent execution
  (Claude Code / Codex / OpenCode).
- Format: factual event log. Timestamps, commands, symptoms, evidence, impact,
  disposition.
- Reasoning policy: include concise chain-of-thought (why you expected X, why the
  observation is anomalous, what it affects). Not private deliberation — operational
  reasoning that helps the user triage.

## Active Run

- Agent: <claude|codex|opencode>
- Run ID: <label>
- Start commit: <SHA>
- Start commit summary: <first line of git log>
- Run dir: <path relative to repo>
- Worktree branch: <eval-...-...>
- Prompt file: <path>
- Wizard version: <plugin version> (from `.claude-plugin/plugin.json`)

## Event Log

### <ISO timestamp with timezone> — <Short title>

- Step: <which phase / wizard step>
- Severity: <info|medium|high>
- Symptom: <one-paragraph description of what was observed>
- Evidence:
  - <exact command or path>
  - <log excerpt, exit code, stderr tail>
- Chain of thought:
  - <what you expected>
  - <what you observed>
  - <why these two differ>
  - <what it implies for the trial's validity>
- Impact: <blocks the run | weakens metrics | observability only | resolved>
- Disposition: <auto-resolved | waiting for user | aborted | logged and continuing>

### <next anomaly...>
```

Entries are in chronological order. When a new run starts, append a **new** `## Active
Run` block (do not edit the previous one) — historical runs remain visible for comparison.

## Trigger events (when to write an entry)

The wizard/harness MUST append a new entry when any of these occurs. This list is
authoritative — do not rely on judgment alone:

### Wizard / preflight phase

- `git status --porcelain` non-empty on launch
- Gate preflight fails on HEAD (exit != 0)
- Tier 1 sufficiency signal triggers hard stop (`NO_TESTS_IN_GATE` or `NO_TEST_FILES`)
- Tier 2 sufficiency verdict `INSUFFICIENT`
- Prompt hygiene grep matches (2.b)
- `measure_cmd` validation fails or stdout is not JSON
- Agent CLI missing from PATH
- `git worktree list` finds a stale `.worktree-eval-*` the user did not remove manually

### Trial execution (within `run_trial.py`)

- Pre-hook command fails (exit != 0)
- Baseline measurement exits non-zero OR emits empty `baseline.json`
- Agent session exits non-zero
- Post measurement exits non-zero OR emits empty `post.json`
- Gate post-trial fails (exit != 0)
- `status.txt` stops advancing for > 10 min while phase is still `agent:running`
- `session.jsonl` size stops growing for > 10 min during `agent:running`
- Codex `{"type":"error","message":"Reconnecting..."}` appears in `session.jsonl`
- `apply_patch verification failed` in Codex stderr
- Wall time crosses 150 min (warn) or 240 min (recommend terminate)

### Agent-side behaviors detected from `session.jsonl`

- Agent re-runs `measure_cmd` or any of its constituent tool names (harness duplication)
- Agent invokes profiling knobs (`STEP_TIMER`, `PROFILE`, `hyperfine`, `cProfile`)
- Agent runs `./scripts/full_regression.sh` or similar gate wrapper itself
- Agent creates git commits in the worktree (the snapshot commit is harness-owned;
  any other commit is a protocol violation)

### Parser / metrics phase

- `parse_transcript.py` output has `raw_event_count > 0` but `tokens.total == 0` (parser
  schema mismatch)
- `tool_calls.total == 0` despite observed `session.jsonl` tool activity
- `speedup` block reports `noise_warning: true` (stddev > 10% of median)
- Gate log contains severity=`ERROR` lines but exit code is 0 (silent failure — domain
  errors not surfaced by the gate)

### External-dependency or regression gate failures

- HTTP `5xx` from any downstream service called during baseline/post/gate
- Flaky test on retry
- AWS / credential rotation during the trial

## Per-entry rules

- **Timestamps**: always ISO 8601 with timezone offset (`2026-04-22T14:30:00+02:00` or
  `2026-04-22T12:30:00Z`). Local time without offset is ambiguous — do not use it.
- **Evidence**: paste exact excerpts. Never paraphrase error messages. Include line
  numbers when citing a log file (`baseline.stderr.log:44-58`). Redact secrets.
- **Chain of thought**: mandatory. Three lines minimum: what you expected, what you
  observed, what the gap implies. This is the field that distinguishes a log line from
  a triage record.
- **Severity**:
  - `info` — observed but does not affect validity (e.g., slow phase within nominal
    bounds, operator-side shell quoting glitch)
  - `medium` — weakens interpretation but run can continue (e.g., domain `ERROR` lines
    during measurement, Tier 2 `PARTIAL` with override)
  - `high` — invalidates the trial or requires user decision (e.g., gate hard-fail,
    agent duplication of harness work, >240min runtime)

## Example entry

```markdown
### 2026-04-22T14:12:33+02:00 — Agent re-ran measure_cmd inside session

- Step: agent:running (trial `codex` run 2)
- Severity: high
- Symptom: `session.jsonl` contains a `command_execution` item_completed for
  `python scripts/bench.py --runs 5 --warmup 1`. This duplicates the harness's own
  `measure_cmd`, adding ~4 min of wall time and producing ad-hoc numbers the report
  cannot reconcile with baseline/post.
- Evidence:
  - `eval-results/.../codex/run-2-20260422_140000/session.jsonl:147`
  - Tool: `command_execution`, status `completed`, wall ~230s.
  - Prompt file line 42: `"Use the same harness tool for iterative comparisons:
    scripts/bench.py"` — the prompt itself encouraged this.
- Chain of thought:
  - Expected: the agent edits code, runs only its own validation (unit tests,
    type-checks). The harness owns measurement.
  - Observed: the agent treated the prompt instruction literally and invoked the
    measurement script directly.
  - Gap implies: the prompt hygiene check in Phase B step 2.b should have caught this
    before launch. It did not fire because `bench.py` basename was not in the grep set
    for this config. The matched prompt line did NOT contain `measure_cmd` literally.
- Impact: trial wall time inflated; measurement interpretation now requires filtering
  out agent-side runs from the authoritative post phase. Does not invalidate the final
  `post.json` (harness re-runs cleanly after agent exits), but reduces trust in the
  agent-discipline axis of the comparison report.
- Disposition: logged; waiting for user to decide whether to (a) accept the trial as
  `unverified-prompt-hygiene`, (b) abort and tighten the prompt, (c) rerun.
```

## What NOT to log here

- Successful phase transitions — `status.txt` already records these.
- Routine informational output (per-run progress, warmup notices).
- Claude/Codex reasoning that the agent self-corrected from without human-visible impact.
- Anything already surfaced by the final `report.md` or `comparison.md` — those are the
  summary artifacts. This log is for **surprises**, not statistics.

If you're unsure whether an event is anomaly-worthy, log it. Over-logging is cheap;
under-logging loses forensic context.
