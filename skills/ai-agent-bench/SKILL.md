---
name: ai-agent-bench
description: "Use when the user wants to benchmark or compare AI agents (Claude Code, Codex, OpenCode) on a refactoring, perf, or code-change task in the current repo. Use when user says compare agents, benchmark Claude vs Codex, agent eval, measure agent, AI agent comparison, agent trial, /ai-agent-bench."
user-invocable: true
allowed-tools: Glob, Grep, Read, Bash, Edit, Write, Skill
---

<!--
User interaction convention (aligned with `shared/workflow.md`): all questions use plain text
— display numbered options, STOP, wait. Do NOT use AskUserQuestion (it does not exist on Codex
and auto-resolves in skill contexts on Claude Code).
-->


# AI Agent Bench — Guided Comparative Benchmarking

**Announce:** "Using the ai-agent-bench skill. Preparing a comparative benchmark trial."

This skill turns a real development task in the current repo into a reproducible comparison
between AI agents. The central question it answers: *given a precise prompt and verification
tools, which agent does the task best, at what cost, in what time?*

The skill is split into two phases. **Phase A (Verification design)** is the critical one:
without validated gate and measurement commands, no comparison is meaningful. **Phase B (Run
configuration)** collects the remaining params and launches trials.

---

## Anomaly logging (MANDATORY, cross-cutting)

Every run appends a live anomaly log at `<repo-root>/AI_AGENT_BENCH_ANOMALIES.md`. This is
not optional and it is not end-of-run — write entries **as things happen**, so the user has
a forensic trail even if the session terminates mid-trial.

**What counts as an anomaly**: anything that happens that should not have happened —
errors, unexpected state, things not handled correctly, protocol violations by the agent
under test, harness failures, observability gaps. See `references/anomaly_log.md` for the
full trigger-event list and the per-entry format (timestamp, step, symptom, evidence,
chain of thought, impact, disposition).

**When to write**:
- Create the file if missing (first anomaly of the first run seeds it with the top-level
  header from the reference).
- Append a new `## Active Run` block when a new trial starts.
- Append a new `### <ISO timestamp> — <short title>` entry immediately when a trigger
  event fires.
- Never overwrite. Historical runs stay in the file for comparison.

**Mandatory fields per entry**: ISO timestamp with timezone, step (which phase of this
skill), severity (`info` / `medium` / `high`), symptom (what was observed), evidence
(exact commands, log excerpts, file paths with line numbers, exit codes), **chain of
thought** (what you expected vs what you observed vs what the gap implies for the trial's
validity — this is the field that distinguishes a log from a triage record), impact, and
disposition.

**Scope of sources to capture**: the skill orchestrator (this wizard), the trial harness
(`run_trial.py`), the agent being benchmarked (Claude Code / Codex / OpenCode — their
`session.jsonl` contents, stderr, error events, patch failures, reconnect notices), and
any external dependency called during baseline / post / gate phases.

The log is listed in the `.gitignore` block proposed in Step 2 — it is operational, not
source-of-truth.

---

## Step 0 — Preflight

1. Verify we're in a git repository:
   ```bash
   git rev-parse --show-toplevel
   ```
   If it fails, stop with a clear error: "run this skill from inside a git repo".

2. Capture state:
   ```bash
   REPO=$(git rev-parse --show-toplevel)
   BRANCH=$(git branch --show-current)
   HEAD_SHA=$(git rev-parse HEAD)
   ```

3. Check for persisted config. If `${REPO}/.ai-agent-bench.toml` exists, read it — every
   question below should be pre-filled from it. Tell the user explicitly: "Found existing config
   at `.ai-agent-bench.toml` — I'll confirm each field rather than re-asking from scratch."

---

## Step 1 — Phase A: Verification design (MANDATORY)

**Outcome required before Phase B**: a validated `gate_cmd` (and optionally a `measure_cmd`),
both dry-run on HEAD and exit code 0.

### 1.A.0 — Recon the repo

Before asking anything, the AI does its homework. Never assume a directory layout — verify what
actually exists.

1. Glob common test/bench/toolchain markers:
   ```
   **/tests/**, **/test/**, **/__tests__/**, **/spec/**
   **/bench*, **/benchmark*, **/perf*
   pyproject.toml, package.json, go.mod, Cargo.toml, pom.xml, build.gradle, Makefile, Justfile
   ```

2. Read project-level docs if they exist — look for sections named "Testing", "Benchmarks",
   "Verification", "CI", "Checks", "Pre-commit":
   - `CLAUDE.md`, `AGENTS.md`, `README.md`
   - `CONTRIBUTING.md`, `DEVELOPMENT.md`
   - `docs/**/*testing*.md`, `docs/**/*verification*.md`

3. Read CI configuration if present — the commands run in CI are usually the canonical gate:
   - `.github/workflows/*.yml`, `.github/workflows/*.yaml`
   - `bitbucket-pipelines.yml`
   - `.gitlab-ci.yml`
   - `.circleci/config.yml`
   - `Jenkinsfile`, `azure-pipelines.yml`

4. Glob for bespoke orchestrators (only if they exist — do NOT invent):
   `scripts/*.sh`, `tools/*.sh`, `Makefile`, `Justfile`, `tasks/*.yml` — check if any target
   obviously composes multiple test suites (names like `check`, `ci`, `verify`, `regression`,
   `all-tests`).

5. Build a concrete proposal grounded in what you actually read:
   - pytest visible in `pyproject.toml` → propose `pytest -q` as gate
   - `package.json` with `test` script → propose `npm test`
   - If a CI workflow file exists, extract the exact commands it runs for PRs / merges (the job
     names are usually `test`, `lint`, `check`, `ci`) and propose those literally — don't
     paraphrase, don't simplify
   - No bespoke orchestrator found → propose composing from primitives that are actually
     configured (check `pyproject.toml` / `package.json` scripts / `Makefile` targets)
   - For measure_cmd: only propose a bench file whose path you verified with Glob

Present the recon findings to the user in plain text — it's a briefing, not a choice. State
explicitly what you DID and DID NOT find; never paper over a missing file. Then ask for
confirmations in plain text (numbered options), seeded from what actually exists in the repo.

### 1.A.1 — Correctness gate (REQUIRED)

Read `references/gate_examples.md` before proposing a default.

Ask the user (plain text, numbered options, STOP and wait for reply):

> **Gate cmd** — which command verifies the code did not regress? (Exit 0 = pass.) I'll run
> this on HEAD first to confirm it works.
>   1. `<candidate 1 based on recon>`  *(Recommended)*
>   2. `<candidate 2>`
>   3. `<candidate 3>`
>   4. Other — type the command.

**Validate before continuing** (critical step):
```bash
cd $REPO && <gate_cmd>
```
If exit code != 0:
1. Show the user the tail of the output.
2. Explain: "the gate cannot be used as a baseline if it fails on HEAD. Fix the code or choose
   a different gate."
3. STOP. Do not proceed until the gate passes on HEAD.

If the user insists on skipping the gate:
1. Ask in plain text: "Skipping the gate is dangerous — please type a one-line written
   justification. The trial will be marked 'unverified' in the final report."
2. Record the reply in the config as `no_gate_justification = "<text>"`.

### 1.A.1b — Test sufficiency (HARD BLOCK)

ultrathink

A passing gate is not a sufficient gate. Before Phase B, establish that the test suite
locks down the behaviors the task will touch. If it doesn't, delegate to `create-test`
and re-verify — no shortcuts.

**Two-tier check** — read `references/sufficiency_check.md` for the full procedure:

- **Tier 1** — mechanical signals computed from 1.A.0 recon. `NO_TESTS_IN_GATE` and
  `NO_TEST_FILES` are hard stops with NO override. `MISSING_MODULE_COVERAGE` and
  `WEAK_ASSERTIONS` allow override. `FEW_TEST_FILES` is warning-only.
- **Tier 2** — critical analysis grounded on the task prompt: parse
  `change_surface` / `must_preserve` / `new_behavior` / `boundary_cases`, read the
  tests covering those modules, answer five binary questions with file:line evidence,
  emit verdict `SUFFICIENT` / `PARTIAL` / `INSUFFICIENT`. Runs always (unless Tier 1
  hard-stopped with no override).

If verdict is not `SUFFICIENT`: invoke `development-skills:create-test` via Skill tool
with `goal = <prompt body> + <gap list>`. After `create-test` returns, re-run the gate
on HEAD and loop Tier 1 + Tier 2 until `SUFFICIENT`.

Override (only where allowed) requires the exact sentence documented in
`references/sufficiency_check.md`, stored as `no_sufficiency_justification` in the
TOML and surfaced in the report as `unverified-sufficiency`.

### 1.A.2 — Perf measurement (OPTIONAL but recommended)

Read `references/measure_examples.md` before proposing defaults.

Ask the user (plain text, numbered options, STOP and wait):

> **Measure cmd** — what should be measured before vs after the agent's work? (Prints JSON to
> stdout.)
>   1. Use existing bench found at `<path>`
>   2. Use hyperfine wrapper on a command
>   3. No perf measurement (gate-only)
>   4. Other — type the command.

**Validate before continuing** (if non-skip):
```bash
cd $REPO && <measure_cmd>  # ideally with reduced --runs for a quick sanity check
```
Check: exit 0, stdout is parseable JSON, at least one numeric field is present. If parsing
fails, show the user the output and ask to adjust.

If the user picks "no perf", skip this silently — the trial is still valid with gate-only.

### 1.A.3 — Summary before Phase B

Print a summary block to the user:
```
Verification plan:
  [GATE]        <cmd>    → validated ✓ (exit 0)
  [SUFFICIENCY] <verdict>    → Tier 2 answers Q1..Q5
  [PERF]        <cmd>    → validated ✓ (emits {wall_s, ...})
```
Ask once: "Confirm to proceed to Phase B? (Yes / edit a field)". Honor edits in place.

---

## Step 1 — Phase B: Run configuration

Each step is a plain-text question: display numbered options, STOP, wait for the reply.

1. **Start commit** — ask:
   > Which commit should the trial start from?
   >   1. current HEAD (`<short-sha>`)  *(Recommended)*
   >   2. parent commit HEAD~1 (`<short-sha>`)
   >   3. Other — type a SHA or ref.

   If the user has uncommitted changes (`git status --porcelain` non-empty), STOP first:
   "commit or stash your changes — the trial runs from a specific commit and stray changes
   would pollute it."

2. **Prompt file** — Glob `**/*.md` in the repo (excluding README, CLAUDE.md, CHANGELOG) and
   ask:
   > Which file contains the task prompt?
   >   1. `<candidate 1>`
   >   2. `<candidate 2>`
   >   3. `<candidate 3>`
   >   4. I'll provide a different path.
   >   5. Help me draft it now.

   If "draft now": ask separately for (a) goal (one paragraph) and (b) hard constraints
   (zero-regression, scope limits, anything invalidable). No separate "out-of-scope"
   section — it is a subset of hard constraints. Write the draft to a path the user
   approves (default: `prompts/<task-name>.md`), show it, iterate until confirmed.
   **Do not write silently.**

   Keep the prompt minimal. Operational details — which commands are harness-owned,
   which fast commands the agent may run — belong in the TOML (`measure_cmd`,
   `gate_cmd`, `agent_test_commands`). The harness will auto-inject them into
   `prompt_resolved.md` at trial time. Do not repeat them here.

   **2.b — Prompt hygiene (MANDATORY)** — see `references/prompt_hygiene.md` for the
   full grep patterns and user options. In summary: after the prompt is selected or
   drafted, grep it for references to harness-owned tools (`measure_cmd` / `gate_cmd`
   basenames), profiling knobs (`PROFILE`, `STEP_TIMER`, `hyperfine`, `cProfile`, etc.),
   and rerun-the-full-harness phrases. If any match fires, STOP and offer the user
   edit / rewrite / override paths. Override requires the exact sentence from
   `references/prompt_hygiene.md`, stored as `prompt_hygiene_override` in the TOML.

   Rationale: the agent correctly follows the prompt — so a prompt that tells it to
   re-run `measure_cmd` causes a protocol violation that is a prompt-design bug, not a
   model-discipline bug. Catch it here, before launching trials.

3. **Agent(s)** — ask:
   > Which agents to benchmark? (Reply with a list, e.g. "1 and 2".)
   >   1. claude  *(Recommended)*
   >   2. codex
   >   3. opencode (parser stub — session captured but metrics partial)

4. **Agent sessions per agent** (default `1`) — ask in plain text:
   > How many agent sessions do you want to run? Each session is a full run of the task
   > from scratch — the agent rewrites the code every time (typical cost: $10-30 + 30-120
   > min per session).
   >   1. `1` — single session *(Recommended for perf / refactor tasks)*
   >   2. `2` — A/B comparison of the same AI on the same prompt
   >   3. `3+` — agent consistency check (costly, research / tuning use case)

   If the reply is >1, warn: "N agent sessions multiplies cost and time. It only measures
   variance in the agent's output (consistency). To beat measurement noise, use
   `measure_repetitions` (next question) instead — that axis is cheap."
   Require confirmation before proceeding.

5. **Measure repetitions** (default `3`) — ask in plain text. Skip this question if
   `measure_cmd` is not configured:
   > How many times should `measure_cmd` be invoked per session (baseline + post, each)?
   > More repetitions = more stable measurement against noise / macOS bimodality.
   >   1. `3` — robust default for non-deterministic perf benchmarks
   >   2. `1` — deterministic tests (bit-reproducible output)
   >   3. `N` (other) — typically 5-15 for very noisy benches

   If reply is <3 AND measure_cmd is configured, confirm: "measure_repetitions=<N> is
   only safe if the measurement is deterministic (output reproducible across
   invocations). Confirm?"

   Persist as `measure_repetitions` in TOML.

6. **Run ID label** (default `1` if no existing trials, else next integer) — free text or
   accept default.

7. **Pre-hooks** (optional) — ask:
   > Does the target setup need any fixture/env files copied into the worktree? E.g.
   > `cp -r <repo>/tests/fixtures/. tests/fixtures/`.
   >   1. No.
   >   2. Yes — paste the commands.

8. **Agent-allowed fast commands** (optional) — ask:
   > Which fast commands is the implementer agent allowed to run inside its session
   > for self-correction? Unit tests, cheap benchmarks, lint, type-check — never the
   > full `measure_cmd` or `gate_cmd` (those are orchestrator-owned).
   >   1. None — agent falls back to the generic "unit tests / lint / type-check"
   >      categories listed in the auto-injected HARNESS PROTOCOL block.
   >   2. Provide list — one command per line.

   Persist in TOML as `agent_test_commands`. `run_trial.py` appends these to
   `prompt_resolved.md` under "You MAY run" so the agent sees them as safe, alongside
   the reminder that `measure_cmd` and `gate_cmd` are orchestrator-owned. Recommended
   for any repo whose fast dev tool is script-specific (e.g. a single benchmark script
   with a `--runs 3` flag, or a narrow pytest subset).

---

## Step 2 — Persist config

Write `${REPO}/.ai-agent-bench.toml` with all the answers. Schema in
`references/task_config_schema.md`. Format:

```toml
name = "<kebab-case-task-name>"
description = "<one-liner>"
start_commit = "<SHA>"
prompt_file = "<relative path to prompt.md>"

pre_hooks = [<shell commands>]
measure_cmd = "<shell command>"
measure_repetitions = 3            # how many times to invoke measure_cmd for baseline + post
gate_cmd = "<shell command>"
agent_test_commands = [<fast commands the agent may run during iteration>]
```

Note: `measure_repetitions` defaults to 3 when omitted. Set to 1 for deterministic
measurements (e.g. bit-reproducible output). Agent sessions are NOT a TOML field —
one invocation of the skill = one session. Re-invoke the skill to add more sessions.

Ask the user: "Add `.ai-agent-bench.toml`, `eval-results/`, `.worktree-eval-*/`, and `AI_AGENT_BENCH_ANOMALIES.md` to `.gitignore`? (Recommended)"
If yes, append the block:
```
# ai-agent-bench
eval-results/
.ai-agent-bench.toml
.worktree-eval-*/
AI_AGENT_BENCH_ANOMALIES.md
```
unless already ignored.

---

## Step 3 — Preflight CLI and resources

For each agent in the selected list:
- `claude`: `which claude` must succeed.
- `codex`: `which codex` must succeed.
- `opencode`: `which opencode` must succeed; warn the user that the parser is a stub.

Also:
- `python --version` must report ≥ 3.11.
- `git worktree list` must not already contain a `.worktree-eval-*` stale entry; if present,
  clean it up with `git worktree prune`.

If any check fails, stop with actionable install instructions.

---

## Step 4 — Launch trials sequentially

For each `(agent, run_id)` combination **in sequence** (never in parallel — they compete for
CPU during measurement):

```bash
python "${CLAUDE_PLUGIN_ROOT}/skills/ai-agent-bench/scripts/run_trial.py" \
    --repo "$REPO" \
    --config "$REPO/.ai-agent-bench.toml" \
    --agent "$AGENT" \
    --run "$RUN_ID"
```

`${CLAUDE_PLUGIN_ROOT}` is an env var set by Claude Code when a plugin is loaded. If it's not
available (e.g. running under Codex), resolve the skill directory from `${0}` or use the
absolute path found via Glob on `**/skills/ai-agent-bench/scripts/run_trial.py`.

**Monitoring** — see `references/monitoring.md` for the full policy. In short:

- Heartbeat: read the last line of `${run_dir}/status.txt` every 3–5 min during
  `agent:running`. Do NOT infer phase from file existence — shell redirection creates
  empty output files the instant a phase starts.
- Timeouts: nominal 60–150 min per trial. Warn at 150 min wall time; recommend
  terminating at 240 min if `status.txt` is still `agent:running`.
- Stall detection: `session.jsonl` not growing for >10 min while `agent:running` is a
  probable stall. Codex `{"type":"error","message":"Reconnecting..."}` combined with
  flat byte growth for >10 min means the session is likely stuck.

Log overrun, stall, and reconnect events to `AI_AGENT_BENCH_ANOMALIES.md` per the
anomaly-logging policy.

After each trial: print the run dir, the branch name + `git checkout` command, and the
`gate_exit_code.txt` result prominently. If the gate failed, ask: *"Trial <agent> run
<id> gate FAILED. Continue with remaining trials or stop?"*

---

## Step 5 — Aggregate and show

Once all trials complete, run the cross-agent aggregator:

```bash
python "${CLAUDE_PLUGIN_ROOT}/skills/ai-agent-bench/scripts/parse_transcript.py" \
    --aggregate "$REPO/eval-results/<task>/*/run-*/" \
    --output "$REPO/eval-results/<task>/comparison.json" \
    --render-report "$REPO/eval-results/<task>/comparison.md"
```

Then print the output layout, the top-line summary extracted from `comparison.json` (who
passed the gate, lowest cost USD, biggest speedup if perf measured), and the manual-review
reminder. See `references/aggregation.md` for the exact text template.

---

## Step 6 — Next steps

Offer the user:

- **Add more agent sessions (consistency check)**: "Re-run the skill — config is persisted, I'll
  only ask for `run N / agent`. Each invocation adds one session per selected agent."
- **Reduce measurement noise**: increase `measure_repetitions` in `.ai-agent-bench.toml` and
  re-run the skill. This is cheap (no extra agent session) and is the right knob for perf
  stability.
- **Change the prompt and rerun on the same commit**: edit `prompts/<task>.md` and re-invoke.
- **Adopt an agent's work**: `git checkout eval-<agent>-run<id>-<ts>`; cherry-pick / rebase /
  merge the bits you like.
- **Clean up**: `git branch -D eval-*` once analysis is done; `rm -rf eval-results/<old-task>/`.

---

## Rules

- **Idempotent**: re-invoking `/ai-agent-bench` never loses work. Persisted TOML and the
  `eval-results/` tree carry forward every previous answer and every previous run. If a
  TOML field is already set, confirm it — don't re-ask.
- **Never commit to the user's branch**: the agent works inside a worktree on
  `eval-<agent>-run<id>-<ts>`. The snapshot commit is added by `run_trial.py` using
  `user=agent-eval`. The worktree directory is removed at trial end; the branch and
  all artifacts under `eval-results/` are preserved.
- **Gate + sufficiency are mandatory**: the skill refuses to launch without a validated
  `gate_cmd` AND a `SUFFICIENT` verdict (or explicit override where allowed). See
  `references/sufficiency_check.md`.
- **Sequential trials only**: do not parallelize. CPU contention distorts timing.
- **Prompt edits don't propagate retroactively**: if the user edits the prompt between
  trials, re-invoke the skill — only new trials see the update.

---

## Files in this skill

- `scripts/run_trial.py` — single-trial orchestrator (worktree + baseline + agent + post + gate + parse)
- `scripts/parse_transcript.py` — per-agent transcript parsers + cross-agent aggregator
- `scripts/pricing.json` — USD/M tokens per model (update to keep cost estimates accurate)
- `references/anomaly_log.md` — `AI_AGENT_BENCH_ANOMALIES.md` format spec + triggers
- `references/sufficiency_check.md` — Tier 1 + Tier 2 test sufficiency procedure
- `references/prompt_hygiene.md` — prompt-hygiene grep patterns + user options
- `references/monitoring.md` — heartbeat / overrun / stream-disconnect policy
- `references/aggregation.md` — Step 5 output template + top-line extraction
- `references/report_template.md` — per-trial report template
- `references/task_config_schema.md` — `.ai-agent-bench.toml` schema with examples
- `references/measure_examples.md` — language-specific `measure_cmd` recipes
- `references/gate_examples.md` — common `gate_cmd` recipes
- `references/methodology.md` — measurement discipline (bimodality, fast-cluster min, N≥3 trials)
- `references/extending-agents.md` — how to plug in a new agent (OpenCode, Aider, etc.)
