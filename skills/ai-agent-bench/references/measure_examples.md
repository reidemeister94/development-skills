# `measure_cmd` recipes

The `measure_cmd` prints JSON to stdout that `parse_transcript.py` treats as opaque. What
matters is that the SAME command runs before and after the agent session, and that it produces
numerically comparable output.

The parser understands the convention `{"variants": {"<name>": {"wall_s": {median, min, mean, stddev, p95}, "cpu_s": {...}, "n_runs": N}}}` — matching that lets the auto-speedup table populate in the report.
Any other JSON structure is stored verbatim; deltas will not be auto-computed but the raw data is
preserved for manual analysis.

---

## Python

### Wall + CPU via `perf_counter_ns` / `psutil`

```python
# scripts/bench_generic.py
import argparse, json, psutil, statistics, subprocess, sys, time

def run_one(target_cmd):
    proc = psutil.Process()
    cpu_start = proc.cpu_times()
    t0 = time.perf_counter_ns()
    subprocess.run(target_cmd, check=True, shell=True)
    wall_s = (time.perf_counter_ns() - t0) / 1e9
    cpu_end = proc.cpu_times()
    cpu_s = (cpu_end.user - cpu_start.user) + (cpu_end.system - cpu_start.system)
    return wall_s, cpu_s

def stats(samples):
    return {
        "median": statistics.median(samples),
        "min": min(samples),
        "mean": statistics.mean(samples),
        "stddev": statistics.pstdev(samples) if len(samples) > 1 else 0.0,
        "p95": sorted(samples)[int(0.95 * len(samples))] if samples else 0.0,
    }

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--runs", type=int, default=10)
    p.add_argument("--warmup", type=int, default=2)
    p.add_argument("--cmd", required=True, help="shell command to time")
    args = p.parse_args()
    for _ in range(args.warmup):
        run_one(args.cmd)
    walls, cpus = [], []
    for _ in range(args.runs):
        w, c = run_one(args.cmd)
        walls.append(w); cpus.append(c)
    json.dump({"wall_s": stats(walls), "cpu_s": stats(cpus), "n_runs": args.runs}, sys.stdout, indent=2)
```

Usage in TOML:

```toml
measure_cmd = "python scripts/bench_generic.py --runs 15 --warmup 2 --cmd 'python -m mymodule'"
```

### Multi-variant (e.g. per-plant, per-dataset)

Subprocess-per-variant pattern (isolation from module-level caches):

```python
for variant in variants:
    env = {**os.environ, "PLANT": variant}
    ... run_one ...
# Emit {"variants": {v: stats_v}} at the end.
```

### `pyperf` (microbenchmarks only)

```bash
python -m pyperf timeit --rigorous --json-append bench.json 'import mymod; mymod.f()'
# Post-process bench.json into the {wall_s:{median,...}} shape.
```

---

## Node.js / TypeScript

### `hyperfine` (any shell command)

```bash
hyperfine --export-json - --runs 15 --warmup 2 'npm run bench:handler'
```

Wrap in a jq filter to reshape to the canonical format if desired:

```toml
measure_cmd = """\
hyperfine --export-json - --runs 15 --warmup 2 'npm run bench' | \
jq '{wall_s: {median: .results[0].median, min: .results[0].min, mean: .results[0].mean, \
stddev: .results[0].stddev}, n_runs: .results[0].times | length}'\
"""
```

### `benchmark.js` or `tinybench`

Run your bench harness with JSON output, pipe through jq.

---

## Go

### `go test -bench`

```bash
go test -bench=BenchmarkXxx -benchmem -count=5 -run=^$ ./pkg/... -json
```

Convert Go's ns/op stream to the canonical format:

```bash
go test -bench=BenchmarkXxx -count=15 -run=^$ ./... | \
awk '/^Benchmark/ {print $3}' | \
python -c "
import sys, json, statistics
ns = [int(x) for x in sys.stdin if x.strip()]
s_vals = [n/1e9 for n in ns]
print(json.dumps({'wall_s': {'median': statistics.median(s_vals), 'min': min(s_vals), 'mean': statistics.mean(s_vals), 'stddev': statistics.pstdev(s_vals)}, 'n_runs': len(s_vals)}))
"
```

---

## Java

### JMH with JSON output

```bash
./gradlew jmh
# JMH writes build/reports/jmh/results.json — reshape via jq to the canonical format.
```

---

## Any language — `hyperfine` as universal tool

If the command to time is deterministic and you don't need per-step breakdowns:

```toml
measure_cmd = "hyperfine --export-json - --runs 15 --warmup 2 'make my-bench-target'"
```

---

## Measurement hygiene (READ THIS)

- **Sequential, not parallel** for multi-variant: if your bench spawns workers, run one variant at
  a time to avoid CPU contention distorting results.
- **Warmup matters**: first run often includes JIT/cold-cache costs. Use warmup >= 2.
- **macOS Pool bimodality**: wall times on Python `multiprocessing.Pool` often cluster bimodally
  (fast cluster + slow cluster). Fast-cluster min is more robust than naive median. See
  `methodology.md` for the discipline.
- **Stddev as % of median**: if >10%, your measurement is noise-dominated. Either increase `runs`
  or acknowledge that small deltas (<15%) cannot be distinguished from noise.
- **CPU time is a sanity check**: if wall time drops but CPU time doesn't, you probably just got
  lucky with scheduling. Real speedups show coherent wall + CPU reductions.
