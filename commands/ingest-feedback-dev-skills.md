Ingest a development-skills feedback report. Challenge every suggestion against the project's Core Pillars before accepting anything. Report path: $ARGUMENTS

## Ground Rule: The Report Is Input, Not Truth

The feedback report describes what happened. It does NOT prescribe what should change. Most friction points are model behavior, edge cases, or things the plugin already handles. **The default verdict is SKIP.** A change must EARN its place by proving it makes the plugin simpler, clearer, or more reliable — without adding complexity.

Before ANY verdict, apply the project's Core Pillars (from CLAUDE.md):
1. **Maximize simplicity, minimize complexity.** A small improvement that adds ugly complexity is not worth it.
2. **All signal, zero noise.** Everything must earn its place. If it doesn't add value, remove it.

**If a proposed fix adds words/rules/exceptions to the plugin but the improvement is marginal → SKIP.**

---

## Step 1: Read the Report

Read the full report. Extract friction points (Section 3), proposed evals (Section 4), and the chain-of-thought (Section 2) for context.

## Step 2: Read Current Plugin State

Read every plugin file referenced in the friction points. Understand the current instruction, why it exists, and what the report says went wrong.

## Step 3: Gather Best Practices (targeted)

Research these sources ONLY for content directly relevant to the friction points:
- Official Claude Code docs: https://code.claude.com/docs/en/overview
- https://github.com/obra/superpowers — hooks, agents, skills
- https://github.com/ykdojo/claude-code-tips — community tips
- https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering — skill design patterns

Skip everything unrelated. Do not pad research for completeness.

## Step 4: Critical Evaluation — Friction Points

For EACH friction point, write a verdict in `docs/reports/ingest-YYYY-MM-DD.md`.

### Verdict Definitions

| Verdict | Meaning | Burden of proof |
|---------|---------|-----------------|
| **FIX** | Plugin instruction is clearly wrong, misleading, or causes repeated waste. The fix is a net simplification or a correction. | HIGH — must prove the change reduces complexity or fixes a clear error. "It could be better" is not enough. |
| **SKIP** | Edge case, model behavior, already handled, or fix adds more complexity than it removes. | LOW — this is the default. |
| **INVESTIGATE** | Not enough information. State what's missing. | — |

### Mandatory Rejection Filters (apply BEFORE writing any verdict)

For each friction point, answer these questions. If ANY answer is YES → **SKIP**.

1. **Is this model behavior, not a plugin instruction problem?** The model ignored a clear, bolded instruction → SKIP. Adding more emphasis or rewording won't change model behavior.
2. **Does the proposed fix add a new rule, exception, mode, or instruction?** If yes: does the plugin CURRENTLY cause this friction REPEATEDLY across different tasks, or was it a one-time event? One-time → SKIP.
3. **Does the fix make the plugin longer/more complex?** Apply the simplicity pillar: is the improvement worth the added complexity? If marginal → SKIP.
4. **Is the friction point already covered by existing instructions that the model didn't follow?** If yes → SKIP. The problem is compliance, not coverage.
5. **Would removing or shortening an instruction fix this better than adding one?** If yes, that's the only acceptable FIX direction.

### Verdict Table Format

| # | Friction Point | Verdict | Rejection filter hit? | Reasoning |
|---|---------------|---------|----------------------|-----------|

## Step 5: Critical Evaluation — Proposed Evals

For EACH proposed eval in Section 4:

| Verdict | Meaning |
|---------|---------|
| **ADD** | Tests a real, reproducible scenario tied to a FIX verdict. |
| **SKIP** | Tied to a SKIP verdict, duplicates an existing eval, or tests model behavior. |
| **MERGE** | Should be combined with an existing eval. State which one. |

**Rule: An eval can only be ADD if its corresponding friction point is FIX.** If the friction point was SKIP, the eval is SKIP too — don't add tests for problems you're not fixing.

Cross-reference with `plugins/development-skills/evals/evals.json` to avoid duplicates.

| # | Eval Name | Verdict | Linked Friction | Reasoning |
|---|-----------|---------|----------------|-----------|

## Step 6: Apply Changes

**Only for FIX verdicts.** Surgical edits only:
- Prefer removing or shortening instructions over adding new ones
- If a fix adds words, it must remove at least as many words elsewhere (net-zero or net-negative complexity)
- For ADD evals: append to `evals.json` with next sequential ID

Do NOT touch files unrelated to verdicts. Do NOT refactor surrounding code.

## Step 7: Validate

- Verify `evals.json` is valid JSON (if modified)
- Run `pre-commit run` on staged files (if any `.py` files touched, also `ruff format .` + `ruff check . --fix`)

## Step 8: Summary

Tell the user:
- How many friction points: FIX / SKIP / INVESTIGATE
- Which specific files were changed and why
- How many evals added/merged/skipped
- Ingest report location

**Expected ratio: most friction points should be SKIP.** If more than 30% are FIX, re-examine whether you're being critical enough.
