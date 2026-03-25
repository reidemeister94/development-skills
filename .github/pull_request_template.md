## Summary

<!-- What does this PR change and why? -->

## Regression Benchmark

<!-- REQUIRED: Paste the benchmark.md output from /eval-regression below -->
<!-- PRs without a passing regression benchmark will not be reviewed -->

<details>
<summary>benchmark.md</summary>

```
PASTE BENCHMARK HERE
```

</details>

**Pass rate:** <!-- e.g., 27/27 evals, 89/89 assertions -->
**Verdict:** <!-- SAFE TO COMMIT or REGRESSIONS FOUND -->

## New Evals

<!-- If you added/modified skills or routing, list the new evals you added -->

- [ ] No new behavior introduced (no new evals needed)
- [ ] New evals added to `evals/evals.json` for: <!-- describe -->

## Checklist

- [ ] Ran `/eval-regression` — zero regressions
- [ ] `benchmark.md` included above
- [ ] New evals added for any new/modified behavior
- [ ] One concern per PR
- [ ] Tested locally with `claude --plugin-dir ./development-skills`
