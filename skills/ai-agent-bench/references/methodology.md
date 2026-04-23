# Measurement discipline — read before claiming a speedup

These principles apply to any perf benchmark.

---

## 1. Bimodality on macOS `multiprocessing.Pool`

On macOS, Python's spawn-based `Pool` exhibits **bimodal** wall-time distributions: samples split
into a fast cluster (~7–8s) and a slow cluster (~11–12s). Typical CV: 15–25%.

**Consequence**: naive median at small N is misleading. A 3-sample median drawn from a
bimodal distribution can land anywhere.

**Discipline**:
- Primary metric = **fast-cluster min** (minimum across all samples). Robust against bimodality
  by construction.
- Secondary metric = **fast-cluster median** (median of samples below the bimodal split). Only
  report if ≥4 samples are in the fast cluster.
- CPU median is more stable than wall median and is the sanity check: real speedups drop wall
  AND CPU coherently.

The auto-report emits `noise_warning: true` when `stddev/median > 10%`. If you see it, treat the
wall numbers as directional only.

---

## 2. Stddev as % of median

**Threshold**: if `stddev / median > 10%`, the measurement is noise-dominated. Any claimed delta
below 15% is fragile. Either increase N or state "no observable speedup".

Rule of thumb for minimum samples:

| Stddev% of median | Min N to detect |
|---|---|
| < 5% | 3 trusts a 3% delta |
| 5–10% | 15 trusts a 10% delta |
| 10–20% | 15 trusts a 15% delta |
| > 20% | N=15 still fragile; use CPU median as primary |

---

## 3. cProfile distorts Python-heavy code

If you rewrite pandas-heavy code to Python dicts, cProfile's per-call overhead often exceeds the
actual work. The "optimized" version shows slower ABSOLUTE times under cProfile, even though
real wall time is faster.

**Rule**: never use cProfile absolute times for before/after comparisons in Python-heavy paths.
Trust `measure_cmd` wall/CPU + step timers (in-process, nanosecond scale).

---

## 4. Scope precision — say exactly what you measured

Claims like "the function is 12% faster" are meaningless without:
- Which function? (full path)
- Which N? (3? 15?)
- Which metric? (min? median? fast-cluster min?)
- Which tool? (wall bench? cProfile? pyinstrument?)

The report template captures all of this automatically. Manual prose claims must match.

---

## 5. Sequential variants, never parallel

If your bench spawns workers for each variant (plant, dataset, etc.), do NOT run variants in
parallel. They compete for CPU and distort each other's numbers. `measure_cmd` should run
variants sequentially (subprocess per variant works well for clean state).

---

## 6. Fast path must be bit-identical to general path

If the optimization introduces a "fast path" (e.g. single-row branch), the output must be
bit-identical to the general path — structurally (same columns/keys) AND numerically. A fast
path that produces different values even by floating-point epsilon is a regression, not an
optimization.

Catch this in the gate (assertion equality on outputs) or in an e2e test with a golden fixture.
Don't rely on downstream tests to notice a phantom stock difference.

---

## 7. Single-sample real-workload wall is fine — as a sanity check

Fixture benches are deterministic and reproducible. Real-workload benches (production data,
real DB) are not — you typically get one sample per branch per day. That's ok for a sanity
check: if fixture bench says -50% but real workload shows +20%, something's wrong with the
fixture fidelity.

---

## 8. Team/subscription plans and cost visibility

Cost numbers from Claude API/Codex API billing don't directly apply to Max/Team/ChatGPT Plus
subscriptions — those are quota-based, not per-token. The cost numbers in the report are
**API-equivalent references** for cross-agent comparison. The real constraint on a plan is
quota consumption, which is not directly observable via CLI.

Use the cost estimate to compare agents on a level playing field (what would the raw API cost),
not to predict your actual bill.

---

## 9. A trial with a failed gate is NOT a valid result

The harness records the gate exit code and preserves artifacts even if the gate fails — but the
trial is unsuccessful. Do not report speedup numbers from a trial with a failed gate: the code
is broken. If the gate passes but marginally (flaky test re-run, one assertion tweak), flag it
in the manual-review section of the report.

---

## 10. Two orthogonal axes — agent sessions vs measurement repetitions

Two distinct sources of noise; distinct knobs.

### Axis 1 — measurement repetitions (inside a single trial)

`measure_cmd` is invoked N times for baseline and N times for post within one trial.
Per-process bimodality on macOS (section 1) means each invocation is a fresh sample; internal
`--runs 15` inside a single process does NOT replace external repetitions. Default **3**. Set
to **1** only if the measurement is deterministic (bit-reproducible output across invocations).

Configured via the TOML field `measure_repetitions` or CLI flag `--measure-reps`. Cheap —
each invocation is 5-10 min of CPU and zero agent tokens. The primary metric (fast-cluster
min) is computed over all samples across all reps and is robust by construction.

### Axis 2 — agent sessions (across trials)

Each trial runs the AI agent once. N>1 trials re-run the full agent session from scratch on
the same prompt and start commit, measuring how consistently the agent produces a working
solution. Default **1**. Only increase when you explicitly want an agent-consistency signal
— typical use cases: research evals, prompt tuning, "should I trust this agent on similar
tasks?". Expensive: each session is ~$10-30 and 30-120 min.

The harness runs one agent session per invocation by design. For N sessions, re-invoke the
skill or run the manual shell loop below:

```bash
# Three sessions per agent (agent consistency check). Each invocation internally does
# measure_repetitions passes of baseline + post — tune that in .ai-agent-bench.toml.
for i in 1 2 3; do
  python run_trial.py --agent claude --run $i --config .ai-agent-bench.toml
done
for i in 1 2 3; do
  python run_trial.py --agent codex --run $i --config .ai-agent-bench.toml
done
python parse_transcript.py --aggregate eval-results/<task>/*/run-*/ \
    --output comparison.json --render-report comparison.md
```

### Which axis when

| Goal | Agent sessions | Measurement reps |
|---|---|---|
| Perf refactor of a function | **1** | **3** (or 5+ if bench is noisy) |
| Deterministic correctness task (formatting, refactor-only) | **1** | **1** |
| Compare agent consistency on a single task | **3+** | 3 (same within each session) |
| Prompt-tuning research | **3+** | 1 (speed over noise) |

Don't over-spend on axis 1 — it multiplies cost linearly in agent tokens. Over-spending on
axis 2 is cheap and usually the right move for any perf task.
