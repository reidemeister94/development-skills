# Test sufficiency check — full procedure

This is the full procedure invoked from `SKILL.md` step `1.A.1b`. A gate that exits 0 on
HEAD is not the same as a gate that catches regressions introduced by the task. Before
launching trials, establish that the test suite locks down the behaviors the task will
touch. If it doesn't, delegate to `create-test` to plug the gaps.

The check is two-tier: Tier 1 is a mechanical filter that triggers on obvious failure
modes; Tier 2 is critical analysis of the task prompt against the actual test content.
Tier 2 runs always (unless Tier 1 hard-stopped with no override).

---

## Tier 1 — Mechanical signals

Compute from the recon already done in `1.A.0`. Do not ask the user — these are
observations, not choices.

| Signal | Trigger | Severity |
|---|---|---|
| `NO_TESTS_IN_GATE` | `gate_cmd` string contains only lint/typecheck tokens (`ruff`, `mypy`, `eslint`, `tsc`, `black`, `markdownlint`, `pre-commit`) and no test runner (`pytest`, `npm test`, `vitest`, `jest`, `mocha`, `go test`, `mvn test`, `gradle test`, `./gradlew test`, `cargo test`, `swift test`) | **Hard stop, NO override** |
| `NO_TEST_FILES` | Recon found zero files under `**/tests/**`, `**/test/**`, `**/__tests__/**`, `**/spec/**`, `src/test/**` | **Hard stop, NO override** |
| `MISSING_MODULE_COVERAGE` | Modules/symbols named in `prompt_file` have no corresponding test file (path does not contain the module name) | Hard stop, override allowed |
| `WEAK_ASSERTIONS` | Grep of test files finds >3 instances of `assert True`, sole-assertion `assertNotNull(...)`, sole-assertion `assert x is not None`, `@pytest.mark.skip`, `@Disabled`, `it.skip`, `test.skip`, `xit(`, `xdescribe(` | Hard stop, override allowed |
| `FEW_TEST_FILES` | <5 test files and task touches a non-trivial change surface | Warning only (does not block if Tier 2 passes) |

### Tier 1 dispositions

- `NO_TESTS_IN_GATE` or `NO_TEST_FILES` triggers: print which signals fired (with
  evidence) and offer ONLY two paths:
  1. **Invoke `create-test`** — see the handoff section below.
  2. **Fix manually** — commit real tests, then re-invoke `/ai-agent-bench`.

  Do NOT offer an override for these two. The skill refuses.

- `MISSING_MODULE_COVERAGE` or `WEAK_ASSERTIONS` triggers: proceed to Tier 2 and include
  the signal in the Tier 2 summary. Override is allowed (see below).

- `FEW_TEST_FILES` alone: proceed to Tier 2 and show the warning; Tier 2 decides.

---

## Tier 2 — Critical analysis

Follow this structure — low degrees of freedom, do not paraphrase.

### Step 2.1 — Parse the task prompt

Read `prompt_file` and extract FOUR lists in plain text. Store them internally; you will
cite them back when answering the questions in step 2.3.

- `change_surface` — modules / files / functions the task will modify
- `must_preserve` — contracts, invariants, output shapes, perf floors that must NOT break
- `new_behavior` — behavior the task must add or guarantee
- `boundary_cases` — explicit or implicit edge cases (empty input, thresholds, null,
  overflow, concurrency, error paths)

### Step 2.2 — Read the relevant tests

Glob test directories for file names matching `change_surface` modules. Open the 3–5
most relevant test files. Read the assertions — do NOT stop at names. If `change_surface`
is broad, sample at least one test file per module.

### Step 2.3 — Answer five binary questions with file:line evidence

For each `NO`, cite the gap concretely (which `must_preserve` item, which file has no
corresponding test, etc.):

- Q1. Is every `must_preserve` item locked down by at least one strong assertion?
- Q2. Does `new_behavior` have a test exercising it (or, if greenfield, is creating one
  the explicit task)?
- Q3. Are assertions specific (exact values, shapes, invariants) rather than only
  nullability / truthiness / type?
- Q4. Does every `boundary_case` have N-1 / N / N+1 coverage (or strategy-appropriate
  equivalent — property-based, fuzz, state-transition)?
- Q5. If `must_preserve` includes a perf floor, does `measure_cmd` cover it numerically?

### Step 2.4 — Verdict

One of:

- `SUFFICIENT` — all five `YES` (or `N/A` with justification for Q5). Print 2–3 line
  rationale. Proceed to `1.A.2`.
- `PARTIAL` — 1–2 `NO`s on non-critical paths (typically Q3 or Q4). List each gap
  concretely. Offer delegation to `create-test` OR one-line override.
- `INSUFFICIENT` — ≥2 `NO`s, or any `NO` on Q1/Q2 (must_preserve or new_behavior
  uncovered). List each gap concretely. Strongly prefer delegation to `create-test`;
  override requires full-sentence justification.

Print the verdict and the answers to the user in plain text before offering paths
forward.

---

## Handoff to `create-test`

When the user chooses "invoke create-test" (or when you recommend it and they confirm):

Invoke `development-skills:create-test` via Skill tool with `goal` set to:

```
<full body of prompt_file>

SUFFICIENCY GAPS from ai-agent-bench Phase A:
- <Tier 1 signals that triggered, with evidence>
- <Tier 2 NO answers with file:line evidence>
```

`create-test` Mode A takes this as a natural-language goal and focuses its analysis on
closing exactly these gaps. When `create-test` returns (tests written, run, and verified):

1. Re-run `gate_cmd` on HEAD and confirm exit 0. If it now fails (new tests reveal a
   pre-existing bug), STOP and surface it — the user fixes the bug before trials.
2. Re-run Tier 1 + Tier 2 from scratch. Loop until `SUFFICIENT`, or user explicit override.

---

## Override (only where allowed)

If override is permitted for the triggered signals and the user chooses it:

Ask the user to type the exact sentence (plain text, STOP and wait):

> "I accept that the trial results will be scientifically invalid because the tests are insufficient: <reason>"

Record in `.ai-agent-bench.toml` as `no_sufficiency_justification = "<full sentence>"`.
Surface it in the final report as `unverified-sufficiency`. Do not accept shorter input.

Override is NEVER permitted for `NO_TESTS_IN_GATE` or `NO_TEST_FILES`. The skill refuses
those two signals outright — no exceptions.
